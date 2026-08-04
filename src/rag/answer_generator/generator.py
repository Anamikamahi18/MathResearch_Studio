"""AnswerGenerator service implementation for creating structured research responses."""

from __future__ import annotations

import logging
from typing import Any

from src.rag.answer_generator.base import BaseAnswerGenerator
from src.rag.answer_generator.confidence import ConfidenceEstimator
from src.rag.answer_generator.formatter import AnswerFormatter
from src.rag.answer_generator.models import (
    AnswerMetadata,
    AnswerRequest,
    AnswerResponse,
)
from src.rag.answer_generator.postprocessor import AnswerPostProcessor
from src.rag.answer_generator.validator import AnswerValidator
from src.rag.llm.base import BaseLLMAdapter
from src.rag.llm.factory import LLMAdapterFactory
from src.rag.llm.models import LLMRequest, LLMResponse
from src.rag.prompt_builder.models import PromptResponse

logger = logging.getLogger(__name__)


class AnswerGenerator(BaseAnswerGenerator):
    """Main orchestrator service converting LLM text into validated, confidence-scored research responses."""

    def __init__(

        self,
        llm_adapter: BaseLLMAdapter | None = None,
        postprocessor: AnswerPostProcessor | None = None,
        validator: AnswerValidator | None = None,
        confidence_estimator: ConfidenceEstimator | None = None,
        formatter: AnswerFormatter | None = None,
    ) -> None:
        """Initialize AnswerGenerator with sub-components.

        Args:
            llm_adapter: Optional BaseLLMAdapter instance (defaults to MockLLMAdapter via factory).
            postprocessor: Optional AnswerPostProcessor instance.
            validator: Optional AnswerValidator instance.
            confidence_estimator: Optional ConfidenceEstimator instance.
            formatter: Optional AnswerFormatter instance.
        """
        self.llm_adapter = llm_adapter or LLMAdapterFactory.get_adapter(provider_name="mock")
        self.postprocessor = postprocessor or AnswerPostProcessor()
        self.validator = validator or AnswerValidator()
        self.confidence_estimator = confidence_estimator or ConfidenceEstimator()
        self.formatter = formatter or AnswerFormatter()
        logger.info("Initialized AnswerGenerator service successfully with adapter '%s'", type(self.llm_adapter).__name__)

    def generate_answer(self, request: AnswerRequest | PromptResponse) -> AnswerResponse:
        """Transform a PromptResponse or AnswerRequest into a structured AnswerResponse.

        Args:
            request: AnswerRequest or PromptResponse artifact.

        Returns:
            AnswerResponse container with structured sections, metadata, and warnings.

        Raises:
            TypeError: If request is not an instance of AnswerRequest or PromptResponse.
        """
        if isinstance(request, PromptResponse):
            answer_request = AnswerRequest(prompt_response=request)
        elif isinstance(request, AnswerRequest):
            answer_request = request
        else:
            raise TypeError(f"Expected AnswerRequest or PromptResponse, got {type(request).__name__}")

        prompt_resp = answer_request.prompt_response
        adapter = answer_request.llm_adapter or self.llm_adapter

        # 1. Create LLMRequest
        llm_req = LLMRequest.from_prompt_response(
            prompt_response=prompt_resp,
            provider=getattr(adapter, "provider_name", "mock"),
            model=getattr(adapter, "model_name", "mock-math-v1"),
            temperature=answer_request.temperature,
            max_tokens=answer_request.max_tokens,
        )

        # 2. Call LLM Adapter
        llm_resp: LLMResponse = adapter.generate(llm_req)

        # 3. Post-process raw text
        cleaned_text = self.postprocessor.clean_and_normalize(llm_resp.raw_text)

        # 4. Validate output text
        warnings = self.validator.validate(
            text=cleaned_text,
            context_chunks_count=len(prompt_resp.included_chunks),
        )

        # 5. Estimate confidence score
        confidence_score, confidence_breakdown = self.confidence_estimator.estimate_confidence(
            prompt_response=prompt_resp,
            raw_answer=cleaned_text,
            warnings=warnings,
        )

        # 6. Format 5 structured research sections
        query_text = prompt_resp.metadata.query_text if prompt_resp.metadata else "Research Question"
        formatted_markdown, sections, limitations = self.formatter.format_answer(
            raw_text=cleaned_text,
            query_text=query_text,
            included_chunks=prompt_resp.included_chunks,
        )

        direct_answer_text = cleaned_text.split("\n\n")[0] if cleaned_text else ""

        # 7. Construct AnswerMetadata
        metadata = AnswerMetadata(
            query_text=query_text,
            intent=prompt_resp.metadata.intent if prompt_resp.metadata else "general_question",
            provider=llm_resp.metadata.provider,
            model=llm_resp.metadata.model,
            latency_ms=llm_resp.metadata.latency_ms,
            prompt_tokens=llm_resp.metadata.prompt_tokens,
            completion_tokens=llm_resp.metadata.completion_tokens,
            total_tokens=llm_resp.metadata.total_tokens,
            context_coverage=prompt_resp.context_coverage,
            confidence_score=confidence_score,
            warnings=warnings,
            limitations=limitations,
            extra_info={
                "confidence_breakdown": confidence_breakdown,
                "finish_reason": llm_resp.metadata.finish_reason,
            },
        )

        logger.info(
            "AnswerGenerator generated response for query '%s' (Confidence: %.2f, %d sections, %d warnings)",
            query_text,
            confidence_score,
            len(sections),
            len(warnings),
        )

        return AnswerResponse(
            question=query_text,
            direct_answer=direct_answer_text,
            formatted_answer=formatted_markdown,
            sections=sections,
            metadata=metadata,
            warnings=warnings,
            limitations=limitations,
        )
