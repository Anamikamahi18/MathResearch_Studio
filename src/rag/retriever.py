"""Semantic retrieval layer for mathematical document search."""

from __future__ import annotations

import logging
from typing import Any

from src.embeddings.provider import EmbeddingProvider
from src.rag.vector_store import FAISSVectorStore

logger = logging.getLogger(__name__)


class SemanticRetriever:
    """Converts natural language queries into embeddings and retrieves ranked document chunks."""

    def __init__(
        self,
        provider: EmbeddingProvider,
        vector_store: FAISSVectorStore,
    ) -> None:
        """Initialize retriever with an embedding provider and vector store.

        Args:
            provider: Active EmbeddingProvider instance.
            vector_store: Active FAISSVectorStore instance.
        """
        if not isinstance(provider, EmbeddingProvider):
            raise TypeError(f"Expected EmbeddingProvider, got {type(provider)}")
        if not isinstance(vector_store, FAISSVectorStore):
            raise TypeError(f"Expected FAISSVectorStore, got {type(vector_store)}")

        self.provider = provider
        self.vector_store = vector_store

    def retrieve(
        self, query: str, top_k: int = 5
    ) -> list[dict[str, Any]]:
        """Retrieve top_k relevant document chunks for a natural language query.

        Args:
            query: Natural language search query string.
            top_k: Maximum number of relevant chunks to return (default: 5).

        Returns:
            List of search result dictionaries formatted with chunk details, similarity score,
            retrieved chunk text, and complete metadata fields.
        """
        if not isinstance(query, str) or not query.strip():
            logger.warning("Empty or invalid search query provided")
            return []
        if top_k <= 0:
            raise ValueError("top_k must be a positive integer")

        clean_query = query.strip()
        logger.info(
            "Processing semantic search query: '%s' (top_k=%d)",
            clean_query,
            top_k,
        )

        try:
            query_vector = self.provider.embed_text(clean_query)
        except Exception as exc:
            logger.error(
                "Failed to generate query embedding for '%s': %s",
                clean_query,
                exc,
            )
            raise RuntimeError(f"Query embedding generation failed: {exc}") from exc

        try:
            raw_results = self.vector_store.search(query_vector, top_k=top_k)
        except Exception as exc:
            logger.error("FAISS vector search failed: %s", exc)
            raise RuntimeError(f"Vector search failed: {exc}") from exc

        formatted_results: list[dict[str, Any]] = []
        for res in raw_results:
            metadata = res.get("metadata") or {}
            formatted_results.append(
                {
                    "chunk_id": res.get("chunk_id", ""),
                    "score": float(res.get("score", 0.0)),
                    "text": res.get("text", ""),
                    "paper_id": metadata.get("paper_id", ""),
                    "paper_title": metadata.get("paper_title", ""),
                    "authors": metadata.get("authors", []),
                    "section_id": metadata.get("section_id", ""),
                    "section_title": metadata.get("section_title", ""),
                    "section_type": metadata.get("section_type", "other"),
                    "page_start": int(metadata.get("page_start", 1)),
                    "page_end": int(metadata.get("page_end", 1)),
                    "entity_type": metadata.get("entity_type"),
                }
            )

        logger.info(
            "Retrieved %d chunk(s) for query '%s'. Top score: %.4f",
            len(formatted_results),
            clean_query,
            formatted_results[0]["score"] if formatted_results else 0.0,
        )
        return formatted_results
