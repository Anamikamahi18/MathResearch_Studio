"""Confidence estimator for evaluating RAG retrieval quality, context coverage, and answer completeness."""

from __future__ import annotations

from src.rag.prompt_builder.models import PromptResponse


class ConfidenceEstimator:
    """Estimates answer confidence based on retrieval quality, context coverage, and answer completeness."""

    def estimate_confidence(
        self,
        prompt_response: PromptResponse,
        raw_answer: str,
        warnings: list[str] | None = None,
    ) -> tuple[float, dict[str, float]]:
        """Compute heuristic confidence score (0.0 - 1.0) and metric breakdown.

        Args:
            prompt_response: PromptResponse containing selected context chunks and coverage score.
            raw_answer: Post-processed answer string.
            warnings: List of validation warning strings.

        Returns:
            Tuple of (overall_confidence_score, metric_breakdown_dict).
        """
        # 1. Retrieval Quality Score (average final_score of included chunks)
        included = prompt_response.included_chunks
        if included:
            retrieval_quality = sum(c.final_score for c in included) / len(included)
        else:
            retrieval_quality = 0.0

        # 2. Context Coverage Score
        context_coverage = prompt_response.context_coverage

        # 3. Answer Completeness Score
        word_count = len(raw_answer.split()) if raw_answer else 0
        if word_count == 0:
            completeness = 0.0
        elif word_count < 15:
            completeness = 0.5
        elif word_count < 50:
            completeness = 0.8
        else:
            completeness = 1.0

        # 4. Weighted combination
        base_confidence = (0.50 * retrieval_quality) + (0.30 * context_coverage) + (0.20 * completeness)

        # 5. Warning penalties
        penalty = 0.15 * len(warnings) if warnings else 0.0
        final_confidence = max(0.0, min(1.0, base_confidence - penalty))

        breakdown = {
            "retrieval_quality": round(retrieval_quality, 4),
            "context_coverage": round(context_coverage, 4),
            "answer_completeness": round(completeness, 4),
            "warning_penalty": round(penalty, 4),
            "final_confidence": round(final_confidence, 4),
        }

        return round(final_confidence, 4), breakdown
