"""Data models for hybrid retrieval engine, explainability, and statistics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class HybridScoringWeights:
    """Configurable weights for hybrid retrieval re-ranking."""

    semantic_weight: float = 0.45
    entity_weight: float = 0.20
    intent_weight: float = 0.15
    graph_weight: float = 0.10
    boost_weight: float = 0.10

    def __post_init__(self) -> None:
        """Validate and normalize weights if needed."""
        total = (
            self.semantic_weight
            + self.entity_weight
            + self.intent_weight
            + self.graph_weight
            + self.boost_weight
        )
        if total <= 0:
            raise ValueError("Total sum of scoring weights must be positive")
        if abs(total - 1.0) > 1e-4:
            self.semantic_weight /= total
            self.entity_weight /= total
            self.intent_weight /= total
            self.graph_weight /= total
            self.boost_weight /= total


@dataclass
class RetrievalExplanation:
    """Detailed explanation component breakdown for a retrieved document chunk."""

    semantic_score: float = 0.0
    entity_score: float = 0.0
    intent_score: float = 0.0
    graph_score: float = 0.0
    boost_score: float = 0.0
    final_score: float = 0.0
    matched_entities: list[str] = field(default_factory=list)
    matched_symbols: list[str] = field(default_factory=list)
    matched_sections: list[str] = field(default_factory=list)
    graph_neighbors: list[str] = field(default_factory=list)
    boost_reason: str = ""
    ranking_reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert RetrievalExplanation to dictionary representation."""
        return {
            "semantic_score": self.semantic_score,
            "entity_score": self.entity_score,
            "intent_score": self.intent_score,
            "graph_score": self.graph_score,
            "boost_score": self.boost_score,
            "final_score": self.final_score,
            "matched_entities": self.matched_entities,
            "matched_symbols": self.matched_symbols,
            "matched_sections": self.matched_sections,
            "graph_neighbors": self.graph_neighbors,
            "boost_reason": self.boost_reason,
            "ranking_reason": self.ranking_reason,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RetrievalExplanation:
        """Create RetrievalExplanation from dictionary representation."""
        return cls(
            semantic_score=float(data.get("semantic_score", 0.0)),
            entity_score=float(data.get("entity_score", 0.0)),
            intent_score=float(data.get("intent_score", 0.0)),
            graph_score=float(data.get("graph_score", 0.0)),
            boost_score=float(data.get("boost_score", 0.0)),
            final_score=float(data.get("final_score", 0.0)),
            matched_entities=list(data.get("matched_entities") or []),
            matched_symbols=list(data.get("matched_symbols") or []),
            matched_sections=list(data.get("matched_sections") or []),
            graph_neighbors=list(data.get("graph_neighbors") or []),
            boost_reason=str(data.get("boost_reason", "")),
            ranking_reason=str(data.get("ranking_reason", "")),
        )


@dataclass
class RetrievalResult:
    """Structured result item returned by retrieval engine."""

    chunk_id: str
    text: str
    paper_id: str = ""
    paper_title: str = ""
    section_id: str = ""
    section_title: str = ""
    section_type: str = "other"
    page_start: int = 1
    page_end: int = 1
    semantic_score: float = 0.0
    entity_score: float = 0.0
    intent_score: float = 0.0
    graph_score: float = 0.0
    boost_score: float = 0.0
    final_score: float = 0.0
    matched_entities: list[str] = field(default_factory=list)
    rank: int = 1
    explanation: RetrievalExplanation | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert RetrievalResult to dictionary representation."""
        return {
            "chunk_id": self.chunk_id,
            "text": self.text,
            "paper_id": self.paper_id,
            "paper_title": self.paper_title,
            "section_id": self.section_id,
            "section_title": self.section_title,
            "section_type": self.section_type,
            "page_start": self.page_start,
            "page_end": self.page_end,
            "semantic_score": self.semantic_score,
            "entity_score": self.entity_score,
            "intent_score": self.intent_score,
            "graph_score": self.graph_score,
            "boost_score": self.boost_score,
            "final_score": self.final_score,
            "matched_entities": self.matched_entities,
            "rank": self.rank,
            "explanation": self.explanation.to_dict() if self.explanation else None,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RetrievalResult:
        """Create RetrievalResult from dictionary representation."""
        exp_data = data.get("explanation")
        explanation = RetrievalExplanation.from_dict(exp_data) if isinstance(exp_data, dict) else None

        return cls(
            chunk_id=str(data.get("chunk_id", "")),
            text=str(data.get("text", "")),
            paper_id=str(data.get("paper_id", "")),
            paper_title=str(data.get("paper_title", "")),
            section_id=str(data.get("section_id", "")),
            section_title=str(data.get("section_title", "")),
            section_type=str(data.get("section_type", "other")),
            page_start=int(data.get("page_start", 1)),
            page_end=int(data.get("page_end", 1)),
            semantic_score=float(data.get("semantic_score", 0.0)),
            entity_score=float(data.get("entity_score", 0.0)),
            intent_score=float(data.get("intent_score", 0.0)),
            graph_score=float(data.get("graph_score", 0.0)),
            boost_score=float(data.get("boost_score", 0.0)),
            final_score=float(data.get("final_score", 0.0)),
            matched_entities=list(data.get("matched_entities") or []),
            rank=int(data.get("rank", 1)),
            explanation=explanation,
            metadata=dict(data.get("metadata") or {}),
        )


@dataclass
class RetrievalStatistics:
    """Aggregated performance metrics and score statistics for a retrieval query."""

    number_of_candidates: int = 0
    average_semantic_score: float = 0.0
    average_final_score: float = 0.0
    highest_score: float = 0.0
    lowest_score: float = 0.0
    entity_match_rate: float = 0.0
    graph_match_rate: float = 0.0
    intent_match_rate: float = 0.0
    top_entity_types: list[str] = field(default_factory=list)
    retrieval_time_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert RetrievalStatistics to dictionary representation."""
        return {
            "number_of_candidates": self.number_of_candidates,
            "average_semantic_score": round(self.average_semantic_score, 4),
            "average_final_score": round(self.average_final_score, 4),
            "highest_score": round(self.highest_score, 4),
            "lowest_score": round(self.lowest_score, 4),
            "entity_match_rate": round(self.entity_match_rate, 4),
            "graph_match_rate": round(self.graph_match_rate, 4),
            "intent_match_rate": round(self.intent_match_rate, 4),
            "top_entity_types": self.top_entity_types,
            "retrieval_time_ms": round(self.retrieval_time_ms, 2),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RetrievalStatistics:
        """Create RetrievalStatistics from dictionary representation."""
        return cls(
            number_of_candidates=int(data.get("number_of_candidates", 0)),
            average_semantic_score=float(data.get("average_semantic_score", 0.0)),
            average_final_score=float(data.get("average_final_score", 0.0)),
            highest_score=float(data.get("highest_score", 0.0)),
            lowest_score=float(data.get("lowest_score", 0.0)),
            entity_match_rate=float(data.get("entity_match_rate", 0.0)),
            graph_match_rate=float(data.get("graph_match_rate", 0.0)),
            intent_match_rate=float(data.get("intent_match_rate", 0.0)),
            top_entity_types=list(data.get("top_entity_types") or []),
            retrieval_time_ms=float(data.get("retrieval_time_ms", 0.0)),
        )


@dataclass
class RetrievalResponse:
    """Complete retrieval response container including query analysis, candidate results, and statistics."""

    query_analysis: Any
    results: list[RetrievalResult] = field(default_factory=list)
    statistics: RetrievalStatistics = field(default_factory=RetrievalStatistics)

    def to_dict(self) -> dict[str, Any]:
        """Convert RetrievalResponse to dictionary representation."""
        analysis_dict = (
            self.query_analysis.to_dict()
            if hasattr(self.query_analysis, "to_dict")
            else str(self.query_analysis)
        )
        return {
            "query_analysis": analysis_dict,
            "results": [r.to_dict() for r in self.results],
            "statistics": self.statistics.to_dict(),
        }
