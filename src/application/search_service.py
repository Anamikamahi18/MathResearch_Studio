"""SearchService application service for semantic search, metadata filtering, and query history."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from src.embeddings.provider import EmbeddingProvider, SentenceTransformerEmbeddingProvider
from src.rag.retriever import SemanticRetriever
from src.rag.vector_store import FAISSVectorStore

logger = logging.getLogger(__name__)


class SearchService:
    """Application service orchestrating semantic search, filtering, and query history."""

    def __init__(
        self,
        vector_store: FAISSVectorStore | None = None,
        embedding_provider: EmbeddingProvider | None = None,
    ) -> None:
        """Initialize SearchService with vector store and embedding provider.

        Args:
            vector_store: Optional FAISSVectorStore instance.
            embedding_provider: Optional EmbeddingProvider instance.
        """
        self.vector_store = vector_store or FAISSVectorStore()
        self.embedding_provider = (
            embedding_provider or SentenceTransformerEmbeddingProvider()
        )
        self.retriever = SemanticRetriever(
            provider=self.embedding_provider,
            vector_store=self.vector_store,
        )
        self._history: list[dict[str, Any]] = []

    def semantic_search(
        self,
        query: str,
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Perform semantic vector search and apply metadata filters.

        Args:
            query: Natural language or mathematical search query.
            top_k: Number of candidate search results to retrieve before filtering.
            filters: Optional dictionary of metadata filtering criteria.

        Returns:
            List of filtered result dictionaries with score, chunk text, and metadata.
        """
        if not isinstance(query, str) or not query.strip():
            logger.warning("Empty search query provided to SearchService")
            return []

        # Retrieve raw semantic candidates from vector store
        raw_results = self.retriever.retrieve(query, top_k=top_k)

        # Apply metadata filters if specified
        filtered_results = (
            self.apply_filters(raw_results, filters) if filters else raw_results
        )

        top_score = (
            filtered_results[0].get("score", 0.0) if filtered_results else 0.0
        )

        # Record query history entry
        history_entry = {
            "query": query.strip(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "filters": filters or {},
            "raw_result_count": len(raw_results),
            "filtered_result_count": len(filtered_results),
            "top_score": float(top_score),
        }
        self._history.append(history_entry)

        logger.info(
            "Search query '%s' returned %d result(s) (top_score=%.4f)",
            query.strip(),
            len(filtered_results),
            top_score,
        )

        return filtered_results

    def apply_filters(
        self,
        results: list[dict[str, Any]],
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Filter a list of search result dictionaries according to criteria.

        Supported filter keys:
            - paper_id: Exact paper ID (str) or list of allowed paper IDs.
            - section_type: Exact section type (str) e.g. "definition", "theorem", "proof".
            - entity_type: Exact entity type (str) e.g. "theorem", "definition".
            - min_score: Minimum similarity score (float).
            - author: Substring match for author name (str).

        Args:
            results: List of search result dictionaries.
            filters: Dictionary of filter criteria.

        Returns:
            Filtered list of search result dictionaries.
        """
        if not filters:
            return results

        filtered: list[dict[str, Any]] = []
        target_paper_id = filters.get("paper_id")
        target_section_type = filters.get("section_type")
        target_entity_type = filters.get("entity_type")
        min_score = filters.get("min_score")
        target_author = filters.get("author")

        for res in results:
            # Paper ID filter
            if target_paper_id is not None:
                paper_id = res.get("paper_id", "")
                if isinstance(target_paper_id, list):
                    if paper_id not in target_paper_id:
                        continue
                elif paper_id != target_paper_id:
                    continue

            # Section type filter
            if target_section_type is not None:
                sec_type = res.get("section_type", "")
                if sec_type.lower() != str(target_section_type).lower():
                    continue

            # Entity type filter
            if target_entity_type is not None:
                ent_type = res.get("entity_type", "")
                if ent_type and str(ent_type).lower() != str(target_entity_type).lower():
                    continue

            # Minimum score filter
            if min_score is not None:
                if float(res.get("score", 0.0)) < float(min_score):
                    continue

            # Author filter
            if target_author is not None:
                authors = res.get("authors", [])
                match = any(
                    str(target_author).lower() in str(a).lower() for a in authors
                )
                if not match:
                    continue

            filtered.append(res)

        return filtered

    def get_history(self) -> list[dict[str, Any]]:
        """Return the list of past search query history records."""
        return list(self._history)

    def clear_history(self) -> None:
        """Clear all search query history."""
        self._history.clear()
