"""Retrieval performance statistics calculator."""

from __future__ import annotations

from collections import Counter
from typing import Sequence

from src.rag.query_processing.models import QueryAnalysis
from src.rag.retrieval.models import RetrievalResult, RetrievalStatistics


class RetrievalStatisticsCalculator:
    """Computes aggregated statistics over candidate results for a retrieval query."""

    @staticmethod
    def calculate(
        candidates: Sequence[RetrievalResult],
        query_analysis: QueryAnalysis | None = None,
        retrieval_time_ms: float = 0.0,
    ) -> RetrievalStatistics:
        """Compute RetrievalStatistics metrics across candidate retrieval results."""
        if not candidates:
            return RetrievalStatistics(retrieval_time_ms=retrieval_time_ms)

        num_candidates = len(candidates)
        semantic_scores = [c.semantic_score for c in candidates]
        final_scores = [c.final_score for c in candidates]

        avg_semantic = sum(semantic_scores) / num_candidates
        avg_final = sum(final_scores) / num_candidates
        highest = max(final_scores)
        lowest = min(final_scores)

        # Match rates
        entity_matches = sum(1 for c in candidates if c.entity_score > 0.0 or c.matched_entities)
        graph_matches = sum(1 for c in candidates if c.graph_score > 0.5)
        intent_matches = sum(1 for c in candidates if c.intent_score >= 0.80)

        entity_match_rate = entity_matches / num_candidates
        graph_match_rate = graph_matches / num_candidates
        intent_match_rate = intent_matches / num_candidates

        # Top entity types frequency
        entity_type_counter: Counter[str] = Counter()
        for c in candidates:
            if c.explanation and c.explanation.matched_entities:
                for ent in c.explanation.matched_entities:
                    # extract entity type if known (e.g. "Definition" from "Definition 2.1")
                    ent_type = ent.split()[0].lower() if ent.split() else "entity"
                    entity_type_counter[ent_type] += 1
            elif c.section_type and c.section_type != "other":
                entity_type_counter[c.section_type.lower()] += 1

        top_entity_types = [pair[0] for pair in entity_type_counter.most_common(3)]

        return RetrievalStatistics(
            number_of_candidates=num_candidates,
            average_semantic_score=round(avg_semantic, 4),
            average_final_score=round(avg_final, 4),
            highest_score=round(highest, 4),
            lowest_score=round(lowest, 4),
            entity_match_rate=round(entity_match_rate, 4),
            graph_match_rate=round(graph_match_rate, 4),
            intent_match_rate=round(intent_match_rate, 4),
            top_entity_types=top_entity_types,
            retrieval_time_ms=round(retrieval_time_ms, 2),
        )
