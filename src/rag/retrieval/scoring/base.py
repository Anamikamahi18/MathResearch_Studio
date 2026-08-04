"""Abstract base class interface for retrieval candidate scoring engines."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseScoringEngine(ABC):
    """Abstract Base Class defining the interface for candidate scoring backends."""

    @abstractmethod
    def compute_score(
        self,
        semantic_score: float,
        entity_score: float,
        intent_score: float,
        graph_score: float,
        boost_score: float,
        candidate_metadata: dict[str, Any] | None = None,
    ) -> float:
        """Compute final combined score for a candidate chunk based on its signal sub-scores.

        Args:
            semantic_score: Cosine similarity embedding score (0.0 to 1.0).
            entity_score: Referenced mathematical entity match score (0.0 to 1.0).
            intent_score: Query intent to section type alignment score (0.0 to 1.0).
            graph_score: ResearchGraph topological relevance score (0.0 to 1.0).
            boost_score: Section statement and citation boost score (0.0 to 1.0).
            candidate_metadata: Optional dictionary of raw chunk metadata.

        Returns:
            Final combined scalar score (0.0 to 1.0).
        """
        pass
