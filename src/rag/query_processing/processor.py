"""High-level query processor service for the mathematical RAG pipeline."""

from __future__ import annotations

import logging
from typing import Sequence

from src.rag.query_processing.models import QueryAnalysis
from src.rag.query_processing.strategies import BaseQueryStrategy, RuleBasedQueryStrategy

logger = logging.getLogger(__name__)


class QueryProcessor:
    """Reusable query processing layer for mathematical research questions."""

    def __init__(self, strategy: BaseQueryStrategy | None = None) -> None:
        """Initialize QueryProcessor with a query understanding strategy.

        Args:
            strategy: Optional query understanding strategy instance (defaults to RuleBasedQueryStrategy).
        """
        self.strategy = strategy or RuleBasedQueryStrategy()
        logger.info("Initialized QueryProcessor using strategy '%s'", type(self.strategy).__name__)

    def set_strategy(self, strategy: BaseQueryStrategy) -> None:
        """Change the active query understanding strategy dynamically.

        Args:
            strategy: New BaseQueryStrategy instance.

        Raises:
            TypeError: If strategy does not inherit from BaseQueryStrategy.
        """
        if not isinstance(strategy, BaseQueryStrategy):
            raise TypeError(f"Expected BaseQueryStrategy, got {type(strategy).__name__}")
        self.strategy = strategy
        logger.info("Updated QueryProcessor strategy to '%s'", type(self.strategy).__name__)

    def process(self, query: str) -> QueryAnalysis:
        """Process a single natural language or mathematical research query.

        Args:
            query: User input query string.

        Returns:
            Structured QueryAnalysis containing normalized query, intent, entities, symbols, and operations.

        Raises:
            TypeError: If query is not a string.
        """
        if not isinstance(query, str):
            logger.error("Invalid query type provided: %s", type(query))
            raise TypeError(f"Expected query to be a string, got {type(query).__name__}")

        logger.info("Processing query: '%s'", query)
        analysis = self.strategy.process(query)
        logger.info(
            "Query analysis complete. Intent: '%s', Entities: %d, Symbols: %d, Confidence: %.2f",
            analysis.intent,
            len(analysis.referenced_entities),
            len(analysis.symbols),
            analysis.confidence,
        )
        return analysis

    def batch_process(self, queries: Sequence[str]) -> list[QueryAnalysis]:
        """Process a batch of user queries sequentially.

        Args:
            queries: Sequence of raw query strings.

        Returns:
            List of QueryAnalysis objects corresponding to each input query.

        Raises:
            TypeError: If queries is not a valid sequence or contains non-string items.
        """
        if not isinstance(queries, (list, tuple)):
            raise TypeError(f"Expected queries to be a list or tuple, got {type(queries).__name__}")

        results: list[QueryAnalysis] = []
        for i, q in enumerate(queries):
            logger.debug("Processing batch item %d/%d", i + 1, len(queries))
            results.append(self.process(q))
        return results
