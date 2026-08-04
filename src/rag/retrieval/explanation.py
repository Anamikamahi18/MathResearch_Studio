"""Rule-based ranking reason generator for retrieval explainability."""

from __future__ import annotations

from src.rag.query_processing.models import QueryAnalysis, QueryIntent
from src.rag.retrieval.models import HybridScoringWeights, RetrievalExplanation, RetrievalResult


class RankingReasonGenerator:
    """Generates human-readable ranking reasons based on multi-signal retrieval scores and metadata."""

    @staticmethod
    def generate_explanation(
        result: RetrievalResult,
        query_analysis: QueryAnalysis | None = None,
        weights: HybridScoringWeights | None = None,
        matched_symbols: list[str] | None = None,
        matched_sections: list[str] | None = None,
        graph_neighbors: list[str] | None = None,
        boost_reason: str = "",
    ) -> RetrievalExplanation:
        """Construct a detailed RetrievalExplanation instance with rule-based human readable ranking reasons."""
        matched_entities = result.matched_entities or []
        symbols = matched_symbols or []
        sections = matched_sections or []
        neighbors = graph_neighbors or []

        # Generate rule-based human-readable bullet points/statements
        reasons: list[str] = []

        # 1. Entity match rule
        if len(matched_entities) == 1:
            reasons.append(f"Matched {matched_entities[0]}")
        elif len(matched_entities) > 1:
            reasons.append(f"Multiple entity matches ({', '.join(matched_entities)})")

        # 2. Semantic similarity rule
        if result.semantic_score >= 0.85:
            reasons.append("High semantic similarity")
        elif result.semantic_score >= 0.70:
            reasons.append("Moderate semantic match")

        # 3. Intent match rule
        if result.intent_score >= 0.90:
            intent_name = (
                query_analysis.intent.value.lower()
                if query_analysis and isinstance(query_analysis.intent, QueryIntent)
                else (query_analysis.intent.lower() if query_analysis else result.section_type.lower())
            )
            if intent_name not in ("unknown", "general_question"):
                reasons.append(f"Strong {intent_name} intent match")

        # 4. Graph connection rule
        if result.graph_score >= 0.80:
            if neighbors:
                reasons.append(f"Graph neighbor of {neighbors[0]}")
            else:
                reasons.append("Graph topological match")

        # 5. Section/Citation boost rule
        if boost_reason:
            reasons.append(boost_reason)
        elif result.boost_score >= 0.90:
            reasons.append(f"{result.section_type.capitalize()} section boost")

        # Fallback if no specific high score rule triggered
        if not reasons:
            reasons.append(f"Retrieved candidate from section '{result.section_title or result.section_type}'")

        ranking_reason = " | ".join(reasons)

        return RetrievalExplanation(
            semantic_score=round(result.semantic_score, 4),
            entity_score=round(result.entity_score, 4),
            intent_score=round(result.intent_score, 4),
            graph_score=round(result.graph_score, 4),
            boost_score=round(result.boost_score, 4),
            final_score=round(result.final_score, 4),
            matched_entities=matched_entities,
            matched_symbols=symbols,
            matched_sections=sections,
            graph_neighbors=neighbors,
            boost_reason=boost_reason,
            ranking_reason=ranking_reason,
        )
