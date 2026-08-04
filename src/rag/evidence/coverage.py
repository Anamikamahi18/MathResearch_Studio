"""Coverage analyzer for evaluating evidence support ratio and unused chunks."""

from __future__ import annotations

from typing import Sequence

from src.rag.evidence.models import EvidenceSpan
from src.rag.retrieval.models import RetrievalResult


class CoverageAnalyzer:
    """Analyzes evidence coverage across answer sentences and tracks unused retrieved chunks."""

    def analyze_coverage(
        self,
        spans: Sequence[EvidenceSpan],
        chunks: Sequence[RetrievalResult],
    ) -> tuple[float, int, int, list[str], list[str]]:
        """Calculate context coverage metrics.

        Args:
            spans: Sequence of EvidenceSpan items.
            chunks: Sequence of candidate RetrievalResult items.

        Returns:
            Tuple of (coverage_score, supported_count, total_count, unsupported_sentences, unused_chunks).
        """
        total_count = len(spans)
        if total_count == 0:
            return 0.0, 0, 0, [], [c.chunk_id for c in chunks]

        supported_count = 0
        unsupported_sentences: list[str] = []
        used_chunk_ids: set[str] = set()

        for span in spans:
            if span.support_level in ("DIRECT", "PARTIAL"):
                supported_count += 1
            else:
                unsupported_sentences.append(span.sentence_text)

            used_chunk_ids.update(span.supported_by_chunks)

        coverage_score = round(supported_count / total_count, 4)
        unused_chunks = [c.chunk_id for c in chunks if c.chunk_id not in used_chunk_ids]

        return coverage_score, supported_count, total_count, unsupported_sentences, unused_chunks
