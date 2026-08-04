"""Token manager for estimating prompt lengths and enforcing context token budgets."""

from __future__ import annotations

import math
from typing import Sequence

from src.rag.retrieval.models import RetrievalResult


class TokenManager:
    """Estimates token counts and manages token budgets without truncating equations."""

    def __init__(self, chars_per_token: float = 4.0) -> None:
        """Initialize TokenManager.

        Args:
            chars_per_token: Average characters per token ratio (default: 4.0).
        """
        self.chars_per_token = max(1.0, chars_per_token)

    def estimate_tokens(self, text: str) -> int:
        """Estimate token length of a given text string.

        Args:
            text: Input string.

        Returns:
            Estimated integer token count.
        """
        if not text:
            return 0
        # Combine character length heuristic with word count heuristic for accuracy
        char_tokens = len(text) / self.chars_per_token
        word_tokens = len(text.split()) * 1.3
        return max(1, int(math.ceil((char_tokens + word_tokens) / 2.0)))

    def estimate_chunk_tokens(self, chunk: RetrievalResult) -> int:
        """Estimate total token length of a retrieved chunk including section headers.

        Args:
            chunk: RetrievalResult item.

        Returns:
            Estimated token count.
        """
        header_text = (
            f"Paper: {chunk.paper_title or chunk.paper_id} | "
            f"Section: {chunk.section_title or chunk.section_type} | "
            f"Chunk ID: {chunk.chunk_id} | Final Score: {chunk.final_score:.4f}\n"
        )
        return self.estimate_tokens(header_text) + self.estimate_tokens(chunk.text)

    def filter_chunks_by_token_limit(
        self, chunks: Sequence[RetrievalResult], max_tokens: int
    ) -> tuple[list[RetrievalResult], list[RetrievalResult], int]:
        """Select top-ranked chunks fitting within max_tokens without equation truncation.

        Args:
            chunks: Sequence of candidate RetrievalResult items sorted by rank/score.
            max_tokens: Target context token budget.

        Returns:
            Tuple of (included_chunks, excluded_chunks, total_used_tokens).
        """
        included: list[RetrievalResult] = []
        excluded: list[RetrievalResult] = []
        used_tokens = 0

        for chunk in chunks:
            chunk_tokens = self.estimate_chunk_tokens(chunk)
            if used_tokens + chunk_tokens <= max_tokens:
                included.append(chunk)
                used_tokens += chunk_tokens
            else:
                excluded.append(chunk)

        return included, excluded, used_tokens
