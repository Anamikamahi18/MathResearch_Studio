"""Operation detection engine for mathematical query analysis."""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)


class OperationDetector:
    """Detects intent actions and requested operations in user queries."""

    def __init__(self) -> None:
        """Initialize operation detector with pattern mappings."""
        self._operation_patterns: list[tuple[str, list[re.Pattern[str]]]] = [
            (
                "define",
                [
                    re.compile(r"\b(?:define|definition|what\s+is|what\s+are|meaning\s+of)\b", re.IGNORECASE),
                ],
            ),
            (
                "prove",
                [
                    re.compile(r"\b(?:prove|proof|how\s+to\s+prove|demonstrate)\b", re.IGNORECASE),
                ],
            ),
            (
                "summarize",
                [
                    re.compile(r"\b(?:summarize|summary|overview|abstract|recap)\b", re.IGNORECASE),
                ],
            ),
            (
                "compare",
                [
                    re.compile(r"\b(?:compare|comparison|difference|contrast|versus|vs\.?)\b", re.IGNORECASE),
                ],
            ),
            (
                "explain",
                [
                    re.compile(r"\b(?:explain|explanation|describe|elaboration|clarify)\b", re.IGNORECASE),
                ],
            ),
            (
                "list",
                [
                    re.compile(r"\b(?:list|enumerate|show\s+all|list\s+all|get\s+all)\b", re.IGNORECASE),
                ],
            ),
            (
                "show",
                [
                    re.compile(r"\b(?:show|display|present|give)\b", re.IGNORECASE),
                ],
            ),
            (
                "find",
                [
                    re.compile(r"\b(?:find|locate|search|where|which|identify)\b", re.IGNORECASE),
                ],
            ),
            (
                "calculate",
                [
                    re.compile(r"\b(?:calculate|compute|evaluate|solve)\b", re.IGNORECASE),
                ],
            ),
            (
                "derive",
                [
                    re.compile(r"\b(?:derive|derivation|deduce)\b", re.IGNORECASE),
                ],
            ),
        ]

    def detect(self, query: str) -> list[str]:
        """Detect all operation verbs/actions requested in the query.

        Args:
            query: Normalized query string.

        Returns:
            List of unique requested operation identifiers.
        """
        if not isinstance(query, str) or not query.strip():
            return []

        operations: list[str] = []
        for op_name, patterns in self._operation_patterns:
            if any(pattern.search(query) for pattern in patterns):
                operations.append(op_name)

        logger.debug("Detected operations in query: %s", operations)
        return operations
