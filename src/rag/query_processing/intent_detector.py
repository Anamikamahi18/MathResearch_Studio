"""Intent detection engine for mathematical research queries."""

from __future__ import annotations

import logging
import re
from typing import Sequence

from src.rag.query_processing.models import QueryIntent, ReferencedEntity

logger = logging.getLogger(__name__)


class IntentDetector:
    """Detects primary query intent and calculates confidence scores."""

    def __init__(self) -> None:
        """Initialize intent detector patterns."""

    def detect(
        self,
        query: str,
        entities: Sequence[ReferencedEntity] | None = None,
        operations: Sequence[str] | None = None,
        symbols: Sequence[str] | None = None,
    ) -> tuple[QueryIntent, float]:
        """Detect the primary intent of a mathematical query.

        Args:
            query: Normalized query string.
            entities: Optional list of extracted ReferencedEntity objects.
            operations: Optional list of detected operation names.
            symbols: Optional list of extracted symbols.

        Returns:
            Tuple of (QueryIntent, confidence_score).
        """
        if not isinstance(query, str) or not query.strip():
            return QueryIntent.UNKNOWN, 0.0

        q_lower = query.lower()
        entities = entities or []
        operations = operations or []
        symbols = symbols or []

        # 1. Proof Intent ("Proof of Theorem 4", "How to prove Lemma 2?")
        if any(e.entity_type == "proof" for e in entities) or re.search(r"\b(?:proof\s+of|how\s+to\s+prove)\b", q_lower):
            return QueryIntent.PROOF, 0.95

        # 2. Dependency Intent ("Which lemma proves theorem 3?", "Which theorem depends on lemma 5?", "Which definition is used in theorem 2?")
        dependency_pattern = re.compile(
            r"\b(?:dependency|proves?|depends?\s+on|used\s+in|is\s+used\s+in|prerequisite|relies?\s+on|required\s+for)\b",
            re.IGNORECASE,
        )
        if dependency_pattern.search(q_lower):
            return QueryIntent.DEPENDENCY, 0.95

        # 3. Comparison Intent ("Compare theorem 2 and theorem 4", "Difference between...")
        if "compare" in operations or re.search(r"\b(?:compare|comparison|difference\s+between|versus|vs\.?)\b", q_lower):
            return QueryIntent.COMPARISON, 0.95

        # 4. Notation Intent ("Show notation for λ", "What does symbol ℝ mean?")
        if "notation" in q_lower or "symbol" in q_lower or (re.search(r"\b(?:show|what\s+is)\s+notation\b", q_lower)):
            return QueryIntent.NOTATION, 0.95

        # 5. Summary Intent ("Summarize this paper", "Overview of section 2")
        if "summarize" in operations or re.search(r"\b(?:summarize|summary\s+of|overview\s+of|recap)\b", q_lower):
            return QueryIntent.SUMMARY, 0.95

        # 6. Citation Intent ("Citation for Theorem 3", "Who proved this?")
        if re.search(r"\b(?:citation|cite|reference\s+for|who\s+proved|author)\b", q_lower):
            return QueryIntent.CITATION, 0.90

        # 7. Entity Type Specific Intents (Definition, Theorem, Lemma, Example, Remark)
        entity_types = [e.entity_type.lower() for e in entities]
        if "definition" in entity_types or re.search(r"\b(?:definition|what\s+is\s+definition|define)\b", q_lower):
            return QueryIntent.DEFINITION, 0.90

        if "theorem" in entity_types:
            return QueryIntent.THEOREM, 0.90

        if "lemma" in entity_types:
            return QueryIntent.LEMMA, 0.90

        if "example" in entity_types or re.search(r"\b(?:example|counterexample|instance)\b", q_lower):
            return QueryIntent.EXAMPLE, 0.90

        if "remark" in entity_types or re.search(r"\b(?:remark)\b", q_lower):
            return QueryIntent.REMARK, 0.90

        # 8. General Question Intent (when query contains question words or symbols)
        if "?" in query or re.search(r"\b(?:what|how|why|where|when|which|is|are|can|does)\b", q_lower) or symbols:
            return QueryIntent.GENERAL_QUESTION, 0.70

        # 9. Fallback
        return QueryIntent.GENERAL_QUESTION, 0.50
