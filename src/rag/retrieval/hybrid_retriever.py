"""Hybrid, multi-signal retrieval engine implementation."""

from __future__ import annotations

import logging
from typing import Any, Sequence

from config.retrieval_config import RetrievalConfig
from src.embeddings.provider import EmbeddingProvider
from src.graph.service import GraphService
from src.rag.query_processing.models import QueryAnalysis, QueryIntent
from src.rag.retrieval.base import BaseRetriever
from src.rag.retrieval.explanation import RankingReasonGenerator
from src.rag.retrieval.models import HybridScoringWeights, RetrievalResult
from src.rag.retrieval.scoring.base import BaseScoringEngine
from src.rag.retrieval.scoring.weighted import WeightedScoringEngine
from src.rag.vector_store import FAISSVectorStore

logger = logging.getLogger(__name__)


class HybridRetriever(BaseRetriever):
    """Hybrid document retriever combining FAISS vector search, entity boosting, intent ranking, and graph relevance."""

    def __init__(
        self,
        provider: EmbeddingProvider,
        vector_store: FAISSVectorStore,
        graph_service: GraphService | None = None,
        weights: HybridScoringWeights | RetrievalConfig | None = None,
        scoring_engine: BaseScoringEngine | None = None,
        candidate_multiplier: int = 4,
    ) -> None:
        """Initialize HybridRetriever with dependencies, configuration, and scoring backend.

        Args:
            provider: Active EmbeddingProvider instance.
            vector_store: Active FAISSVectorStore instance.
            graph_service: Optional GraphService instance from Day 4.
            weights: Optional HybridScoringWeights or RetrievalConfig instance.
            scoring_engine: Optional BaseScoringEngine instance (defaults to WeightedScoringEngine).
            candidate_multiplier: Top-K multiplier for FAISS candidate generation (default: 4).

        Raises:
            TypeError: If provider or vector_store are of invalid types.
        """
        if not isinstance(provider, EmbeddingProvider):
            raise TypeError(f"Expected EmbeddingProvider, got {type(provider).__name__}")
        if not isinstance(vector_store, FAISSVectorStore):
            raise TypeError(f"Expected FAISSVectorStore, got {type(vector_store).__name__}")

        self.provider = provider
        self.vector_store = vector_store
        self.graph_service = graph_service or GraphService()

        if isinstance(weights, RetrievalConfig):
            self.weights = weights.get_scoring_weights()
            self.candidate_multiplier = weights.candidate_multiplier
        elif isinstance(weights, HybridScoringWeights):
            self.weights = weights
            self.candidate_multiplier = candidate_multiplier
        else:
            self.weights = HybridScoringWeights()
            self.candidate_multiplier = candidate_multiplier

        # Delegated candidate scoring engine abstraction
        if scoring_engine is not None:
            if not isinstance(scoring_engine, BaseScoringEngine):
                raise TypeError(f"Expected BaseScoringEngine, got {type(scoring_engine).__name__}")
            self.scoring_engine = scoring_engine
        else:
            self.scoring_engine = WeightedScoringEngine(weights=self.weights)

    def set_weights(self, weights: HybridScoringWeights | RetrievalConfig) -> None:
        """Update scoring weights dynamically on retriever and underlying scoring engine.

        Args:
            weights: New HybridScoringWeights or RetrievalConfig instance.
        """
        if isinstance(weights, RetrievalConfig):
            self.weights = weights.get_scoring_weights()
            self.candidate_multiplier = weights.candidate_multiplier
        elif isinstance(weights, HybridScoringWeights):
            self.weights = weights
        else:
            raise TypeError(f"Expected HybridScoringWeights or RetrievalConfig, got {type(weights).__name__}")

        if isinstance(self.scoring_engine, WeightedScoringEngine):
            self.scoring_engine.set_weights(self.weights)

    def set_scoring_engine(self, scoring_engine: BaseScoringEngine) -> None:
        """Replace the candidate scoring engine dynamically (e.g. for ColBERT, CrossEncoder, or LearningToRank).

        Args:
            scoring_engine: New BaseScoringEngine instance.
        """
        if not isinstance(scoring_engine, BaseScoringEngine):
            raise TypeError(f"Expected BaseScoringEngine, got {type(scoring_engine).__name__}")
        self.scoring_engine = scoring_engine

    def retrieve(
        self, query_analysis: QueryAnalysis, top_k: int = 5
    ) -> list[RetrievalResult]:
        """Retrieve and rank candidate document chunks for a processed query analysis.

        Args:
            query_analysis: Structured QueryAnalysis object from QueryProcessor.
            top_k: Target number of ranked results to return (default: 5).

        Returns:
            List of RetrievalResult objects sorted by final_score descending, each containing rank and explanation.

        Raises:
            TypeError: If query_analysis is not a QueryAnalysis instance.
            ValueError: If top_k <= 0.
        """
        if not isinstance(query_analysis, QueryAnalysis):
            raise TypeError(f"Expected QueryAnalysis, got {type(query_analysis).__name__}")
        if top_k <= 0:
            raise ValueError("top_k must be a positive integer")

        if self.vector_store.number_of_vectors() == 0:
            logger.warning("Retrieval called on an empty FAISS vector store")
            return []

        search_query = query_analysis.normalized_query or query_analysis.original_query
        if not search_query.strip():
            logger.warning("Empty query provided for retrieval")
            return []

        logger.info(
            "Executing hybrid retrieval for query '%s' (intent: %s, entities: %d, top_k: %d)",
            search_query,
            query_analysis.intent,
            len(query_analysis.referenced_entities),
            top_k,
        )

        # 1. Candidate Generation: Semantic Search via FAISS
        try:
            query_vector = self.provider.embed_text(search_query)
        except Exception as exc:
            logger.error("Failed to generate query embedding: %s", exc)
            raise RuntimeError(f"Query embedding failed: {exc}") from exc

        candidate_limit = min(top_k * self.candidate_multiplier, self.vector_store.number_of_vectors())
        raw_candidates = self.vector_store.search(query_vector, top_k=candidate_limit)

        if not raw_candidates:
            return []

        # 2. Multi-Signal Re-Ranking & Explanation Construction
        ranked_results: list[RetrievalResult] = []
        for res in raw_candidates:
            chunk_id = str(res.get("chunk_id", ""))
            text = str(res.get("text", ""))
            raw_meta = res.get("metadata") or {}

            paper_id = str(raw_meta.get("paper_id", ""))
            paper_title = str(raw_meta.get("paper_title", ""))
            section_id = str(raw_meta.get("section_id", ""))
            section_title = str(raw_meta.get("section_title", ""))
            section_type = str(raw_meta.get("section_type", "other"))
            page_start = int(raw_meta.get("page_start", 1))
            page_end = int(raw_meta.get("page_end", 1))

            # a. Semantic Score
            raw_score = float(res.get("score", 0.0))
            semantic_score = max(0.0, min(1.0, raw_score))

            # b. Entity Match Score
            matched_entities: list[str] = []
            entity_score = self._compute_entity_score(
                query_analysis, text, section_title, chunk_id, matched_entities
            )

            # c. Intent Match Score
            intent_score = self._compute_intent_score(query_analysis, section_type, section_title, text)

            # d. Graph Relevance Score & Graph Neighbors
            graph_neighbors: list[str] = []
            graph_score = self._compute_graph_score(query_analysis, chunk_id, paper_id, text, graph_neighbors)

            # e. Section / Citation Boost Score & Boost Reason
            boost_score, boost_reason = self._compute_boost_score(section_type, section_title, text, raw_meta)

            # f. Matched Symbols and Sections
            matched_symbols = [sym for sym in query_analysis.symbols if sym in text]
            matched_sections = [section_title] if section_title else [section_type]

            # g. Final Score Computation (Delegated to ScoringEngine abstraction)
            final_score = self.scoring_engine.compute_score(
                semantic_score=semantic_score,
                entity_score=entity_score,
                intent_score=intent_score,
                graph_score=graph_score,
                boost_score=boost_score,
                candidate_metadata=raw_meta,
            )

            result_item = RetrievalResult(
                chunk_id=chunk_id,
                text=text,
                paper_id=paper_id,
                paper_title=paper_title,
                section_id=section_id,
                section_title=section_title,
                section_type=section_type,
                page_start=page_start,
                page_end=page_end,
                semantic_score=round(semantic_score, 4),
                entity_score=round(entity_score, 4),
                intent_score=round(intent_score, 4),
                graph_score=round(graph_score, 4),
                boost_score=round(boost_score, 4),
                final_score=round(final_score, 4),
                matched_entities=matched_entities,
                metadata=raw_meta,
            )

            # Generate and attach explanation
            result_item.explanation = RankingReasonGenerator.generate_explanation(
                result=result_item,
                query_analysis=query_analysis,
                weights=self.weights,
                matched_symbols=matched_symbols,
                matched_sections=matched_sections,
                graph_neighbors=graph_neighbors,
                boost_reason=boost_reason,
            )

            ranked_results.append(result_item)

        # 3. Sort by final_score descending
        ranked_results.sort(key=lambda r: r.final_score, reverse=True)

        # 4. Assign rank integer (1..N) to all candidates
        for idx, item in enumerate(ranked_results, start=1):
            item.rank = idx
            if item.explanation:
                item.explanation.final_score = item.final_score

        final_candidates = ranked_results[:top_k]

        logger.info(
            "Hybrid retrieval returned %d result(s). Top chunk: %s (final_score: %.4f)",
            len(final_candidates),
            final_candidates[0].chunk_id if final_candidates else "None",
            final_candidates[0].final_score if final_candidates else 0.0,
        )
        return final_candidates

    def _compute_entity_score(
        self,
        query_analysis: QueryAnalysis,
        text: str,
        section_title: str,
        chunk_id: str,
        matched_entities: list[str],
    ) -> float:
        """Calculate entity matching score based on query referenced entities."""
        if not query_analysis.referenced_entities:
            return 0.2 if any(k in text.lower() for k in ("theorem", "definition", "lemma", "proof")) else 0.0

        content_lower = f"{text} {section_title} {chunk_id}".lower()
        matches_count = 0

        for entity in query_analysis.referenced_entities:
            label_lower = entity.normalized_label.lower()
            ent_type_lower = entity.entity_type.lower()
            ident_lower = entity.identifier.lower() if entity.identifier else None

            # Check full label match (e.g. "definition 2.1")
            if label_lower in content_lower:
                if entity.normalized_label not in matched_entities:
                    matched_entities.append(entity.normalized_label)
                matches_count += 1
            # Check identifier match if present (e.g. "2.1")
            elif ident_lower and ident_lower in content_lower and ent_type_lower in content_lower:
                if entity.normalized_label not in matched_entities:
                    matched_entities.append(entity.normalized_label)
                matches_count += 1
            # Check generic entity type match if no identifier
            elif not ident_lower and ent_type_lower in content_lower:
                if entity.normalized_label not in matched_entities:
                    matched_entities.append(entity.normalized_label)
                matches_count += 1

        total_refs = len(query_analysis.referenced_entities)
        return min(1.0, matches_count / max(1, total_refs))

    def _compute_intent_score(
        self,
        query_analysis: QueryAnalysis,
        section_type: str,
        section_title: str,
        text: str,
    ) -> float:
        """Calculate intent-aware alignment score."""
        intent = (
            query_analysis.intent.value
            if isinstance(query_analysis.intent, QueryIntent)
            else str(query_analysis.intent).lower()
        )
        sec_type_lower = section_type.lower()
        sec_title_lower = section_title.lower()
        text_lower = text.lower()

        if intent == "definition":
            if sec_type_lower == "definition" or "definition" in sec_title_lower or "definition" in text_lower:
                return 1.0
            return 0.3

        if intent == "theorem":
            if sec_type_lower == "theorem" or "theorem" in sec_title_lower or "theorem" in text_lower:
                return 1.0
            return 0.3

        if intent == "proof":
            if sec_type_lower == "proof" or "proof" in sec_title_lower or "proof" in text_lower:
                return 1.0
            return 0.3

        if intent == "lemma":
            if sec_type_lower == "lemma" or "lemma" in sec_title_lower or "lemma" in text_lower:
                return 1.0
            return 0.3

        if intent == "summary":
            if sec_type_lower in ("abstract", "introduction", "conclusion", "summary") or any(
                k in sec_title_lower for k in ("abstract", "intro", "conclusion", "summary")
            ):
                return 1.0
            return 0.4

        if intent in ("comparison", "dependency"):
            if any(k in text_lower for k in ("compare", "proves", "depends", "used in", "requires", "relationship")):
                return 1.0
            return 0.5

        if intent == "notation":
            if "notation" in sec_title_lower or "symbol" in sec_title_lower or any(s in text for s in query_analysis.symbols):
                return 1.0
            return 0.3

        return 0.5

    def _compute_graph_score(
        self,
        query_analysis: QueryAnalysis,
        chunk_id: str,
        paper_id: str,
        text: str,
        graph_neighbors: list[str],
    ) -> float:
        """Calculate graph-aware relevance score based on Day 4 ResearchGraph relationships."""
        if not self.graph_service or not self.graph_service.graph or not self.graph_service.graph.nodes:
            return 0.5

        # Check if chunk_id maps directly to a node
        node = self.graph_service.graph.get_node(chunk_id)
        if not node and paper_id:
            # Fallback search node by text overlap
            for g_node in self.graph_service.graph.nodes.values():
                if g_node.paper_id == paper_id and text in g_node.text:
                    node = g_node
                    break

        if not node:
            return 0.3

        # If query has referenced entities, check graph distance/connections
        if query_analysis.referenced_entities:
            ref_labels = [e.normalized_label.lower() for e in query_analysis.referenced_entities]
            ref_ids = [e.identifier.lower() for e in query_analysis.referenced_entities if e.identifier]

            # Direct match on node label or ID
            node_label = getattr(node, "label", getattr(node, "title", ""))
            if any(lbl in node_label.lower() for lbl in ref_labels) or any(
                ident in node.node_id.lower() for ident in ref_ids
            ):
                graph_neighbors.append(node_label or node.node_id)
                return 1.0

            # Check antecedents / consequents / proof chains in graph
            antecedents = self.graph_service.get_antecedents(node.node_id)
            for ant in antecedents:
                ant_label = str(ant.get("label") or ant.get("title") or "")
                if any(lbl in ant_label.lower() for lbl in ref_labels):
                    graph_neighbors.append(ant_label or ant.get("node_id", "antecedent"))
                    return 0.85

            consequents = self.graph_service.get_consequents(node.node_id)
            for con in consequents:
                con_label = str(con.get("label") or con.get("title") or "")
                if any(lbl in con_label.lower() for lbl in ref_labels):
                    graph_neighbors.append(con_label or con.get("node_id", "consequent"))
                    return 0.85

        return 0.5

    def _compute_boost_score(
        self,
        section_type: str,
        section_title: str,
        text: str,
        metadata: dict[str, Any],
    ) -> tuple[float, str]:
        """Calculate section structure and citation boost score and return boost reason."""
        sec_lower = section_type.lower()
        title_lower = section_title.lower()

        # Formal mathematical statement boost
        if sec_lower in ("definition", "theorem", "lemma", "corollary", "proposition", "proof"):
            return 1.0, f"{section_type.capitalize()} section boost"
        if any(k in title_lower for k in ("definition", "theorem", "lemma", "proof", "corollary")):
            return 0.9, "Section title statement boost"
        if metadata.get("citation_count", 0) > 0:
            return 0.8, "Citation count boost"

        return 0.4, "Standard section score"
