"""PromptBuilder service implementation for constructing grounded LLM prompts."""

from __future__ import annotations

import logging
from typing import Sequence

from src.rag.prompt_builder.base import BasePromptBuilder
from src.rag.prompt_builder.context_selector import ContextSelector
from src.rag.prompt_builder.formatter import PromptFormatter
from src.rag.prompt_builder.models import (
    PromptMetadata,
    PromptRequest,
    PromptResponse,
)
from src.rag.prompt_builder.templates import TemplateRegistry
from src.rag.prompt_builder.token_manager import TokenManager
from src.rag.query_processing.models import QueryAnalysis, QueryIntent
from src.rag.retrieval.models import RetrievalResponse, RetrievalResult

logger = logging.getLogger(__name__)


class PromptBuilder(BasePromptBuilder):
    """Main prompt builder orchestrator transforming retrieval context into grounded LLM prompts."""

    def __init__(
        self,
        context_selector: ContextSelector | None = None,
        token_manager: TokenManager | None = None,
        template_registry: TemplateRegistry | None = None,
        formatter: PromptFormatter | None = None,
    ) -> None:
        """Initialize PromptBuilder with sub-components.

        Args:
            context_selector: Optional ContextSelector instance.
            token_manager: Optional TokenManager instance.
            template_registry: Optional TemplateRegistry instance.
            formatter: Optional PromptFormatter class/instance.
        """
        self.token_manager = token_manager or TokenManager()
        self.context_selector = context_selector or ContextSelector(token_manager=self.token_manager)
        self.template_registry = template_registry or TemplateRegistry()
        self.formatter = formatter or PromptFormatter()
        logger.info("Initialized PromptBuilder service successfully")

    def _resolve_intent_template(self, intent: str | QueryIntent, request_template: str) -> str:
        """Determine appropriate template name based on query intent if default is requested."""
        if request_template != "default":
            return request_template

        intent_str = intent.value if isinstance(intent, QueryIntent) else str(intent).lower()
        if intent_str in ("definition", "notation"):
            return "definition"
        if intent_str in ("theorem", "proof", "lemma"):
            return "theorem_proof"
        if intent_str in ("dependency", "comparison"):
            return "dependency"
        if intent_str == "summary":
            return "summary"
        return "default"

    def build_prompt(self, request: PromptRequest) -> PromptResponse:
        """Construct a grounded LLM prompt response from a prompt request.

        Args:
            request: PromptRequest container holding query, retrieval candidates, and token limits.

        Returns:
            PromptResponse containing assembled system prompt, user prompt, full prompt, token estimates, and metadata.

        Raises:
            TypeError: If request is of invalid type.
            ValueError: If max_prompt_tokens <= 0.
        """
        if not isinstance(request, PromptRequest):
            raise TypeError(f"Expected PromptRequest, got {type(request).__name__}")
        if request.max_prompt_tokens <= 0:
            raise ValueError("max_prompt_tokens must be positive")

        # 1. Unpack query text and QueryAnalysis metadata
        if isinstance(request.query, QueryAnalysis):
            query_analysis = request.query
            query_text = query_analysis.original_query
            intent_val = query_analysis.intent
        else:
            query_text = str(request.query)
            query_analysis = None
            intent_val = "general_question"

        # 2. Unpack candidate retrieval results
        if isinstance(request.retrieval_response, RetrievalResponse):
            candidates: Sequence[RetrievalResult] = request.retrieval_response.results
            if not query_analysis and request.retrieval_response.query_analysis:
                qa = request.retrieval_response.query_analysis
                if isinstance(qa, QueryAnalysis):
                    query_analysis = qa
                    intent_val = qa.intent
        elif isinstance(request.retrieval_response, (list, tuple)):
            candidates = request.retrieval_response
        else:
            candidates = []

        # 3. Resolve template
        template_name = self._resolve_intent_template(intent_val, request.template_name)
        template = self.template_registry.get_template(template_name)

        # 4. Perform context selection and token budget filtering
        context = self.context_selector.select_context(
            query_text=query_text,
            candidates=candidates,
            max_context_tokens=request.max_context_tokens,
        )

        # 5. Format section-based prompts
        system_prompt, user_prompt, full_prompt = self.formatter.format_full_prompt(
            query_text=query_text,
            context=context,
            template=template,
        )

        # 6. Calculate token estimates
        system_tokens = self.token_manager.estimate_tokens(system_prompt)
        context_tokens = context.total_context_tokens
        user_tokens = self.token_manager.estimate_tokens(user_prompt)
        total_tokens = self.token_manager.estimate_tokens(full_prompt)

        intent_str = intent_val.value if isinstance(intent_val, QueryIntent) else str(intent_val)

        # 7. Construct metadata
        metadata = PromptMetadata(
            query_text=query_text,
            intent=intent_str,
            included_chunk_ids=[c.chunk_id for c in context.included_chunks],
            excluded_chunk_ids=[c.chunk_id for c in context.excluded_chunks],
            estimated_system_tokens=system_tokens,
            estimated_context_tokens=context_tokens,
            estimated_user_tokens=user_tokens,
            estimated_total_tokens=total_tokens,
            context_coverage=context.coverage_score,
            prompt_version=template.version,
            template_name=template.template_name,
        )

        logger.info(
            "PromptBuilder generated prompt for query '%s' (%d tokens, %d included chunks, %d excluded chunks)",
            query_text,
            total_tokens,
            len(context.included_chunks),
            len(context.excluded_chunks),
        )

        return PromptResponse(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            full_prompt=full_prompt,
            estimated_tokens=total_tokens,
            included_chunks=context.included_chunks,
            excluded_chunks=context.excluded_chunks,
            context_coverage=context.coverage_score,
            prompt_version=template.version,
            metadata=metadata,
        )
