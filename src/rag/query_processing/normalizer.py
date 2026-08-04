"""Query normalization engine for mathematical queries."""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)


class QueryNormalizer:
    """Normalizes user query strings while preserving mathematical notation and entity numbers."""

    def __init__(self) -> None:
        """Initialize query normalizer."""
        pass

    def normalize(self, query: str) -> str:
        """Normalize whitespace, quotes, and punctuation in query string.

        Args:
            query: Raw query string.

        Returns:
            Normalized query string with preserved math and numbering.

        Raises:
            TypeError: If query is not a string.
        """
        if not isinstance(query, str):
            raise TypeError(f"Expected query to be a string, got {type(query).__name__}")

        if not query.strip():
            return ""

        text = query

        # 1. Normalize smart quotes / unicode quotes to standard ASCII
        text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')

        # 2. Collapse multiple whitespace characters (spaces, tabs, newlines) into single space
        text = re.sub(r"\s+", " ", text).strip()

        # 3. Normalize spacing around entity label and identifier (e.g. "Theorem   3.2" -> "Theorem 3.2")
        entity_patterns = [
            r"\b(definition|theorem|lemma|corollary|proof|example|remark|section|proposition|conjecture|axiom|table|figure)\s+([0-9]+(?:\.[0-9]+)*|[a-z]+|[ivxlcdm]+)\b"
        ]
        for pattern in entity_patterns:
            def _entity_replacer(match: re.Match[str]) -> str:
                kind, idx = match.group(1), match.group(2)
                return f"{kind} {idx}"
            text = re.sub(pattern, _entity_replacer, text, flags=re.IGNORECASE)

        # 4. Remove space before trailing punctuation like ?, !, ., ,, :, ;
        #    e.g. "Theorem 3.2 ?" -> "Theorem 3.2?"
        text = re.sub(r"\s+([?!.,:;])", r"\1", text)

        # 5. Ensure space after punctuation if followed by a letter (e.g. "Theorem 3.2?What" -> "Theorem 3.2? What")
        #    Careful not to break decimals like 3.2 or LaTeX commands like \lambda
        text = re.sub(r"([?!:])([A-Za-z])", r"\1 \2", text)

        # 6. Final trim
        normalized = text.strip()

        logger.debug("Normalized query: '%s' -> '%s'", query, normalized)
        return normalized
