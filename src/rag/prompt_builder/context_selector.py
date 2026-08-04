"""Context selector for selecting and deduplicating document chunks for LLM prompts."""

from __future__ import annotations

from typing import Sequence

from src.rag.prompt_builder.models import PromptContext
from src.rag.prompt_builder.token_manager import TokenManager
from src.rag.retrieval.models import RetrievalResult


class ContextSelector:
    """Selects, deduplicates, and ranks retrieved document chunks for prompt inclusion."""

    def __init__(self, token_manager: TokenManager | None = None) -> None:
        """Initialize ContextSelector with an optional TokenManager.

        Args:
            token_manager: Optional TokenManager instance.
        """
        self.token_manager = token_manager or TokenManager()

    def select_context(
        self,
        query_text: str,
        candidates: Sequence[RetrievalResult],
        max_context_tokens: int = 3000,
    ) -> PromptContext:
        """Select highest quality candidate chunks fitting within max_context_tokens budget.

        Args:
            query_text: User question string.
            candidates: Sequence of retrieved candidate RetrievalResult items.
            max_context_tokens: Maximum token budget allowed for retrieved context.

        Returns:
            PromptContext container with included and excluded chunks.
        """
        if not candidates:
            return PromptContext(
                query_text=query_text,
                included_chunks=[],
                excluded_chunks=[],
                total_context_tokens=0,
                coverage_score=0.0,
            )

        # 1. Deduplicate candidates by chunk_id or text
        seen_ids: set[str] = set()
        seen_texts: set[str] = set()
        deduped: list[RetrievalResult] = []

        for item in candidates:
            text_norm = item.text.strip().lower()
            if item.chunk_id in seen_ids or text_norm in seen_texts:
                continue
            seen_ids.add(item.chunk_id)
            seen_texts.add(text_norm)
            deduped.append(item)

        # 2. Sort by final_score descending, prioritizing entity and graph scores
        deduped.sort(
            key=lambda c: (c.final_score, c.entity_score, c.graph_score, c.intent_score),
            reverse=True,
        )

        # 3. Filter chunks within max_context_tokens budget
        included, excluded, total_tokens = self.token_manager.filter_chunks_by_token_limit(
            chunks=deduped,
            max_tokens=max_context_tokens,
        )

        coverage = len(included) / len(deduped) if deduped else 0.0

        return PromptContext(
            query_text=query_text,
            included_chunks=included,
            excluded_chunks=excluded,
            total_context_tokens=total_tokens,
            coverage_score=round(coverage, 4),
        )
