"""Strategy interface and implementations for query understanding."""

from __future__ import annotations

from abc import ABC, abstractmethod
import logging
from typing import Any

from src.rag.query_processing.entity_extractor import MathematicalEntityExtractor
from src.rag.query_processing.intent_detector import IntentDetector
from src.rag.query_processing.models import QueryAnalysis, QueryIntent
from src.rag.query_processing.normalizer import QueryNormalizer
from src.rag.query_processing.operation_detector import OperationDetector
from src.rag.query_processing.symbol_extractor import MathematicalSymbolExtractor

logger = logging.getLogger(__name__)


class BaseQueryStrategy(ABC):
    """Abstract Base Class for query processing strategies.

    Allows downstream code to use RuleBasedQueryStrategy, LLMQueryStrategy,
    or hybrid strategies interchangeably without API changes.
    """

    @abstractmethod
    def process(self, query: str) -> QueryAnalysis:
        """Process a raw user query string into a structured QueryAnalysis object.

        Args:
            query: Raw natural language or mathematical user question.

        Returns:
            Structured QueryAnalysis instance.
        """
        pass


class RuleBasedQueryStrategy(BaseQueryStrategy):
    """Rule-based query understanding strategy utilizing deterministic regex and heuristics."""

    def __init__(
        self,
        normalizer: QueryNormalizer | None = None,
        entity_extractor: MathematicalEntityExtractor | None = None,
        symbol_extractor: MathematicalSymbolExtractor | None = None,
        operation_detector: OperationDetector | None = None,
        intent_detector: IntentDetector | None = None,
    ) -> None:
        """Initialize RuleBasedQueryStrategy with component dependencies."""
        self.normalizer = normalizer or QueryNormalizer()
        self.entity_extractor = entity_extractor or MathematicalEntityExtractor()
        self.symbol_extractor = symbol_extractor or MathematicalSymbolExtractor()
        self.operation_detector = operation_detector or OperationDetector()
        self.intent_detector = intent_detector or IntentDetector()

    def process(self, query: str) -> QueryAnalysis:
        """Process a user query using rule-based normalization, extraction, and detection.

        Args:
            query: User query string.

        Returns:
            QueryAnalysis result object.

        Raises:
            TypeError: If query is not a string.
        """
        if not isinstance(query, str):
            raise TypeError(f"Expected query to be a string, got {type(query).__name__}")

        raw_query = query
        normalized_query = self.normalizer.normalize(raw_query)

        if not normalized_query:
            return QueryAnalysis(
                original_query=raw_query,
                normalized_query="",
                intent=QueryIntent.UNKNOWN,
                operations=[],
                referenced_entities=[],
                symbols=[],
                confidence=0.0,
                confidence_type="rule_based",
            )

        # 1. Extract Entities (supports multi-entity extraction & proof decomposition)
        entities = self.entity_extractor.extract(normalized_query)

        # 2. Extract Symbols
        symbols = self.symbol_extractor.extract(normalized_query)

        # 3. Detect Operations
        operations = self.operation_detector.detect(normalized_query)

        # 4. Detect Intent & Confidence
        intent, confidence = self.intent_detector.detect(
            normalized_query,
            entities=entities,
            operations=operations,
            symbols=symbols,
        )

        analysis = QueryAnalysis(
            original_query=raw_query,
            normalized_query=normalized_query,
            intent=intent,
            operations=operations,
            referenced_entities=entities,
            symbols=symbols,
            language="en",
            metadata={
                "strategy": "RuleBasedQueryStrategy",
                "entity_count": len(entities),
                "symbol_count": len(symbols),
                "operation_count": len(operations),
            },
            confidence=confidence,
            confidence_type="rule_based",
        )

        logger.debug(
            "Processed query '%s' -> Intent: %s, Confidence: %.2f (Type: %s)",
            normalized_query,
            intent.value if isinstance(intent, QueryIntent) else intent,
            confidence,
            analysis.confidence_type,
        )
        return analysis


class LLMQueryStrategy(BaseQueryStrategy):
    """Placeholder strategy for future LLM-based query understanding.

    Conforms to BaseQueryStrategy so downstream RAG layers can switch to LLM-driven
    intent/entity extraction without structural code changes.
    """

    def __init__(self, llm_client: Any = None, fallback_strategy: BaseQueryStrategy | None = None) -> None:
        """Initialize LLM query strategy with optional client and fallback strategy."""
        self.llm_client = llm_client
        self.fallback_strategy = fallback_strategy or RuleBasedQueryStrategy()

    def process(self, query: str) -> QueryAnalysis:
        """Process query using LLM structured extraction, falling back to rule-based if needed.

        Args:
            query: User query string.

        Returns:
            QueryAnalysis result object with confidence_type="llm".
        """
        logger.info("Executing LLMQueryStrategy (falling back to rule-based processing)...")
        # In future implementations, call LLM structured output endpoint here
        analysis = self.fallback_strategy.process(query)
        analysis.metadata["strategy"] = "LLMQueryStrategy(Fallback)"
        analysis.confidence_type = "llm"
        return analysis
