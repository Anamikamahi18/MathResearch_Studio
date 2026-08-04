"""Extraction engine for mathematical statement references in user queries."""

from __future__ import annotations

import logging
import re

from src.rag.query_processing.models import ReferencedEntity

logger = logging.getLogger(__name__)


class MathematicalEntityExtractor:
    """Extracts references to mathematical statements, theorems, definitions, and proofs."""

    # Roman numerals pattern (case-insensitive)
    _ROMAN = r"(?:[ivxlcdm]+)"
    # Numbering pattern: 2.1, 4, 3.2.1, etc.
    _NUMBER = r"(?:[0-9]+(?:\.[0-9]+)*)"
    # Letter identifier: A, B.1
    _LETTER = r"(?:[a-z](?:\.[0-9]+)?)"
    # Combined identifier pattern
    _ID_PAT = f"(?:{_NUMBER}|{_ROMAN}|{_LETTER})"

    _ENTITY_TYPES = (
        "definition",
        "theorem",
        "lemma",
        "corollary",
        "proof",
        "example",
        "remark",
        "proposition",
        "conjecture",
        "axiom",
    )

    def __init__(self) -> None:
        """Initialize mathematical entity extractor."""
        # Pattern for "Proof of <Entity_Type> <ID>"
        self._proof_of_pattern = re.compile(
            rf"\bproof\s+of\s+((?:{'|'.join(self._ENTITY_TYPES)})\s+{self._ID_PAT})\b",
            flags=re.IGNORECASE,
        )

        # Pattern for standalone numbered entities ("Definition 2.1", "Lemma 4", etc.)
        self._numbered_entity_pattern = re.compile(
            rf"\b({'|'.join(self._ENTITY_TYPES)})\s+({self._ID_PAT})\b",
            flags=re.IGNORECASE,
        )

        # Pattern for generic un-numbered entity mentions ("lemma", "definition", "theorem", etc.)
        self._generic_entity_pattern = re.compile(
            rf"\b({'|'.join(self._ENTITY_TYPES)})s?\b",
            flags=re.IGNORECASE,
        )

    def extract(self, query: str) -> list[ReferencedEntity]:
        """Extract all referenced mathematical entities from a query string.

        Args:
            query: Query string to analyze.

        Returns:
            List of ReferencedEntity objects ordered by position in query.
        """
        if not isinstance(query, str) or not query.strip():
            return []

        entities: list[ReferencedEntity] = []
        matched_spans: list[tuple[int, int]] = []
        seen_keys: set[tuple[str, str | None]] = set()

        def _is_span_covered(start: int, end: int) -> bool:
            return any(s <= start and end <= e for s, e in matched_spans)

        # 1. Check for "Proof of <TargetEntity>" patterns (Proof Decomposition)
        for match in self._proof_of_pattern.finditer(query):
            start, end = match.span()
            raw_text = match.group(0)
            target_str = match.group(1).strip()
            matched_spans.append((start, end))

            # Add Proof Entity (generic un-numbered proof)
            proof_key = ("proof", None)
            if proof_key not in seen_keys:
                seen_keys.add(proof_key)
                entities.append(
                    ReferencedEntity(
                        entity_type="proof",
                        identifier=None,
                        normalized_label="Proof",
                        raw_text=raw_text,
                    )
                )

            # Add Linked Target Entity (e.g. Theorem 4 with metadata={"linked_from": "proof"})
            words = target_str.split(maxsplit=1)
            if len(words) == 2:
                target_type = words[0].lower()
                target_id = words[1]

                # Format Roman numerals or standard ID
                if re.fullmatch(r"[ivxlcdm]+", target_id, flags=re.IGNORECASE):
                    ident_formatted = target_id.upper()
                else:
                    ident_formatted = target_id

                target_key = (target_type, ident_formatted.lower())
                if target_key not in seen_keys:
                    seen_keys.add(target_key)
                    entities.append(
                        ReferencedEntity(
                            entity_type=target_type,
                            identifier=ident_formatted,
                            normalized_label=f"{target_type.capitalize()} {ident_formatted}",
                            raw_text=target_str,
                            metadata={"linked_from": "proof"},
                        )
                    )

        # 2. Check for numbered entity matches (Definition 2.1, Lemma 4, Theorem III, etc.)
        for match in self._numbered_entity_pattern.finditer(query):
            start, end = match.span()
            if _is_span_covered(start, end):
                continue

            raw_text = match.group(0)
            ent_type = match.group(1).lower()
            identifier = match.group(2).strip()

            if re.fullmatch(r"[ivxlcdm]+", identifier, flags=re.IGNORECASE):
                original_id = match.group(2)
                ident_formatted = original_id if original_id.isupper() else identifier.upper()
            else:
                ident_formatted = identifier

            key = (ent_type, ident_formatted.lower())
            if key not in seen_keys:
                matched_spans.append((start, end))
                seen_keys.add(key)
                entities.append(
                    ReferencedEntity(
                        entity_type=ent_type,
                        identifier=ident_formatted,
                        normalized_label=f"{ent_type.capitalize()} {ident_formatted}",
                        raw_text=raw_text,
                    )
                )

        # 3. Check for generic un-numbered entity mentions ("lemma", "definition", "theorem", etc.)
        for match in self._generic_entity_pattern.finditer(query):
            start, end = match.span()
            if _is_span_covered(start, end):
                continue

            ent_type = match.group(1).lower()
            key = (ent_type, None)

            if key not in seen_keys:
                matched_spans.append((start, end))
                seen_keys.add(key)
                entities.append(
                    ReferencedEntity(
                        entity_type=ent_type,
                        identifier=None,
                        normalized_label=ent_type.capitalize(),
                        raw_text=match.group(0),
                    )
                )

        logger.debug("Extracted %d entity reference(s) from query", len(entities))
        return entities
