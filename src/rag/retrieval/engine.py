"""High-level RetrievalEngine service orchestrator with explainability and statistics."""

from __future__ import annotations

import logging
import time
from typing import Sequence

from src.rag.query_processing.models import QueryAnalysis
from src.rag.query_processing.processor import QueryProcessor
from src.rag.retrieval.base import BaseRetriever
from src.rag.retrieval.models import RetrievalResponse, RetrievalResult, RetrievalStatistics
from src.rag.retrieval.statistics import RetrievalStatisticsCalculator

logger = logging.getLogger(__name__)


class RetrievalEngine:
    """High-level retrieval service for the AI Research Assistant RAG pipeline."""

    def __init__(
        self,
        retriever: BaseRetriever,
        query_processor: QueryProcessor | None = None,
    ) -> None:
        """Initialize RetrievalEngine with a retriever backend and query processor.

        Args:
            retriever: Active BaseRetriever backend instance (e.g. HybridRetriever).
            query_processor: Optional QueryProcessor instance.

        Raises:
            TypeError: If retriever does not inherit from BaseRetriever.
        """
        if not isinstance(retriever, BaseRetriever):
            raise TypeError(f"Expected BaseRetriever, got {type(retriever).__name__}")

        self.retriever = retriever
        self.query_processor = query_processor or QueryProcessor()
        logger.info(
            "Initialized RetrievalEngine using retriever backend '%s'",
            type(self.retriever).__name__,
        )

    def set_retriever(self, retriever: BaseRetriever) -> None:
        """Change the active retriever backend dynamically.

        Args:
            retriever: New BaseRetriever instance.

        Raises:
            TypeError: If retriever is not a BaseRetriever instance.
        """
        if not isinstance(retriever, BaseRetriever):
            raise TypeError(f"Expected BaseRetriever, got {type(retriever).__name__}")
        self.retriever = retriever
        logger.info("Updated RetrievalEngine backend to '%s'", type(self.retriever).__name__)

    def retrieve(
        self, query: str | QueryAnalysis, top_k: int = 5
    ) -> list[RetrievalResult]:
        """Retrieve top_k ranked candidate document chunks for a query string or QueryAnalysis object.

        Args:
            query: Raw user input query string OR pre-processed QueryAnalysis object.
            top_k: Number of ranked results to return (default: 5).

        Returns:
            List of RetrievalResult objects sorted by final score descending.

        Raises:
            TypeError: If query is neither a string nor a QueryAnalysis.
            ValueError: If top_k <= 0.
        """
        response = self.retrieve_with_response(query=query, top_k=top_k)
        return response.results

    def retrieve_with_response(
        self, query: str | QueryAnalysis, top_k: int = 5
    ) -> RetrievalResponse:
        """Retrieve top_k ranked candidates and compute complete retrieval response & performance statistics.

        Args:
            query: Raw user input query string OR pre-processed QueryAnalysis object.
            top_k: Target number of ranked candidate results to return (default: 5).

        Returns:
            RetrievalResponse container containing query_analysis, results, and RetrievalStatistics.

        Raises:
            TypeError: If query is neither a string nor a QueryAnalysis.
            ValueError: If top_k <= 0.
        """
        if top_k <= 0:
            raise ValueError("top_k must be a positive integer")

        start_time = time.perf_counter()

        if isinstance(query, str):
            if not query.strip():
                logger.warning("Empty string query provided to RetrievalEngine")
                empty_analysis = QueryAnalysis(original_query="", normalized_query="")
                return RetrievalResponse(
                    query_analysis=empty_analysis,
                    results=[],
                    statistics=RetrievalStatistics(),
                )
            query_analysis = self.query_processor.process(query)
        elif isinstance(query, QueryAnalysis):
            query_analysis = query
        else:
            logger.error("Invalid query type provided: %s", type(query))
            raise TypeError(
                f"Expected str or QueryAnalysis, got {type(query).__name__}"
            )

        logger.info(
            "RetrievalEngine processing retrieval request for normalized query: '%s'",
            query_analysis.normalized_query,
        )

        results = self.retriever.retrieve(query_analysis=query_analysis, top_k=top_k)
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        stats = RetrievalStatisticsCalculator.calculate(
            candidates=results,
            query_analysis=query_analysis,
            retrieval_time_ms=elapsed_ms,
        )

        logger.info(
            "RetrievalEngine complete (%d candidates in %.2fms). Top final_score: %.4f",
            len(results),
            elapsed_ms,
            results[0].final_score if results else 0.0,
        )

        return RetrievalResponse(
            query_analysis=query_analysis,
            results=results,
            statistics=stats,
        )

    def batch_retrieve(
        self, queries: Sequence[str | QueryAnalysis], top_k: int = 5
    ) -> list[list[RetrievalResult]]:
        """Retrieve top_k results for a batch of input queries.

        Args:
            queries: Sequence of string queries or QueryAnalysis objects.
            top_k: Number of ranked results per query.

        Returns:
            List of RetrievalResult lists corresponding to each query.

        Raises:
            TypeError: If queries is not a valid list or tuple.
        """
        if not isinstance(queries, (list, tuple)):
            raise TypeError(f"Expected queries to be a list or tuple, got {type(queries).__name__}")

        batch_results: list[list[RetrievalResult]] = []
        for i, q in enumerate(queries):
            logger.debug("Processing retrieval batch item %d/%d", i + 1, len(queries))
            batch_results.append(self.retrieve(q, top_k=top_k))
        return batch_results
