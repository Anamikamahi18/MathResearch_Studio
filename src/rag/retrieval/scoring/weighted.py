"""Weighted linear combination scoring engine implementation."""

from __future__ import annotations

from typing import Any

from config.retrieval_config import RetrievalConfig
from src.rag.retrieval.models import HybridScoringWeights
from src.rag.retrieval.scoring.base import BaseScoringEngine


class WeightedScoringEngine(BaseScoringEngine):
    """Concrete scoring engine computing weighted linear combination of retrieval signals."""

    def __init__(
        self, weights: HybridScoringWeights | RetrievalConfig | None = None
    ) -> None:
        """Initialize WeightedScoringEngine with scoring weights or configuration.

        Args:
            weights: Optional HybridScoringWeights or RetrievalConfig instance.
        """
        if isinstance(weights, RetrievalConfig):
            self.weights = weights.get_scoring_weights()
        elif isinstance(weights, HybridScoringWeights):
            self.weights = weights
        else:
            self.weights = HybridScoringWeights()

    def set_weights(self, weights: HybridScoringWeights | RetrievalConfig) -> None:
        """Update scoring weights dynamically.

        Args:
            weights: New HybridScoringWeights or RetrievalConfig instance.
        """
        if isinstance(weights, RetrievalConfig):
            self.weights = weights.get_scoring_weights()
        elif isinstance(weights, HybridScoringWeights):
            self.weights = weights
        else:
            raise TypeError(f"Expected HybridScoringWeights or RetrievalConfig, got {type(weights).__name__}")

    def compute_score(
        self,
        semantic_score: float,
        entity_score: float,
        intent_score: float,
        graph_score: float,
        boost_score: float,
        candidate_metadata: dict[str, Any] | None = None,
    ) -> float:
        """Compute final combined score using weighted linear combination.

        Formula:
            FinalScore = (
                semantic_weight * semantic_score
                + entity_weight * entity_score
                + intent_weight * intent_score
                + graph_weight * graph_score
                + boost_weight * boost_score
            )
        """
        final_score = (
            self.weights.semantic_weight * semantic_score
            + self.weights.entity_weight * entity_score
            + self.weights.intent_weight * intent_score
            + self.weights.graph_weight * graph_score
            + self.weights.boost_weight * boost_score
        )
        return round(final_score, 4)
