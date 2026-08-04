"""Retrieval engine configuration settings."""

from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Any


@dataclass
class RetrievalConfig:
    """Centralized configuration settings for the hybrid retrieval engine."""

    semantic_weight: float = 0.45
    entity_weight: float = 0.20
    intent_weight: float = 0.15
    graph_weight: float = 0.10
    boost_weight: float = 0.10
    top_k: int = 5
    candidate_multiplier: int = 4

    def __post_init__(self) -> None:
        """Validate configuration values."""
        if self.top_k <= 0:
            raise ValueError("top_k must be a positive integer")
        if self.candidate_multiplier <= 0:
            raise ValueError("candidate_multiplier must be a positive integer")

    def get_scoring_weights(self) -> Any:
        """Construct and return a normalized HybridScoringWeights instance."""
        from src.rag.retrieval.models import HybridScoringWeights

        return HybridScoringWeights(
            semantic_weight=self.semantic_weight,
            entity_weight=self.entity_weight,
            intent_weight=self.intent_weight,
            graph_weight=self.graph_weight,
            boost_weight=self.boost_weight,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert RetrievalConfig to a dictionary."""
        return {
            "semantic_weight": self.semantic_weight,
            "entity_weight": self.entity_weight,
            "intent_weight": self.intent_weight,
            "graph_weight": self.graph_weight,
            "boost_weight": self.boost_weight,
            "top_k": self.top_k,
            "candidate_multiplier": self.candidate_multiplier,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RetrievalConfig:
        """Create a RetrievalConfig instance from a dictionary."""
        return cls(
            semantic_weight=float(data.get("semantic_weight", 0.45)),
            entity_weight=float(data.get("entity_weight", 0.20)),
            intent_weight=float(data.get("intent_weight", 0.15)),
            graph_weight=float(data.get("graph_weight", 0.10)),
            boost_weight=float(data.get("boost_weight", 0.10)),
            top_k=int(data.get("top_k", 5)),
            candidate_multiplier=int(data.get("candidate_multiplier", 4)),
        )

    @classmethod
    def from_env(cls) -> RetrievalConfig:
        """Create RetrievalConfig from environment variables if present."""
        return cls(
            semantic_weight=float(os.getenv("RETRIEVAL_SEMANTIC_WEIGHT", "0.45")),
            entity_weight=float(os.getenv("RETRIEVAL_ENTITY_WEIGHT", "0.20")),
            intent_weight=float(os.getenv("RETRIEVAL_INTENT_WEIGHT", "0.15")),
            graph_weight=float(os.getenv("RETRIEVAL_GRAPH_WEIGHT", "0.10")),
            boost_weight=float(os.getenv("RETRIEVAL_BOOST_WEIGHT", "0.10")),
            top_k=int(os.getenv("RETRIEVAL_TOP_K", "5")),
            candidate_multiplier=int(os.getenv("RETRIEVAL_CANDIDATE_MULTIPLIER", "4")),
        )


DEFAULT_RETRIEVAL_CONFIG = RetrievalConfig()
