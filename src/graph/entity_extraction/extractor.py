"""Modular mathematical entity extraction engine."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Sequence

from .models import EntityType, ExtractedEntity

logger = logging.getLogger(__name__)

# Regex for extracting LaTeX commands and mathematical symbols
SYMBOL_PATTERN = re.compile(
    r"\\[a-zA-Z]+|\$[^\$]+\$|\\\(.*?\\\)|\\\[.*?\\\]", re.DOTALL
)

# Regex for extracting in-text citations and reference markers
CITATION_PATTERN = re.compile(
    r"\[\d+(?:[,\-]\s*\d+)*\]|(?:\b[A-Z][a-zA-Z\.\'\-]+\s+(?:et\s+al\.\s+)?\(\d{4}\))|\(\s*[A-Z][a-zA-Z\.\'\-]+\s+(?:et\s+al\.\s*)?,\s*\d{4}\s*\)",
    re.IGNORECASE,
)

# Regex patterns for statement extraction from narrative text
ENTITY_PATTERNS: dict[str, re.Pattern[str]] = {
    "definitions": re.compile(
        r"^\s*(Definition|Def\.)\s*(\d+[\w\.]*)?\s*[:.\-]?\s*(.*)$",
        re.IGNORECASE,
    ),
    "theorems": re.compile(
        r"^\s*(Theorem|Thm\.)\s*(\d+[\w\.]*)?\s*[:.\-]?\s*(.*)$",
        re.IGNORECASE,
    ),
    "lemmas": re.compile(
        r"^\s*(Lemma|Lem\.)\s*(\d+[\w\.]*)?\s*[:.\-]?\s*(.*)$",
        re.IGNORECASE,
    ),
    "corollaries": re.compile(
        r"^\s*(Corollary|Cor\.)\s*(\d+[\w\.]*)?\s*[:.\-]?\s*(.*)$",
        re.IGNORECASE,
    ),
    "proofs": re.compile(
        r"^\s*(Proof|Pf\.)\s*[:.\-]?\s*(.*)$",
        re.IGNORECASE,
    ),
    "examples": re.compile(
        r"^\s*(Example|Ex\.)\s*(\d+[\w\.]*)?\s*[:.\-]?\s*(.*)$",
        re.IGNORECASE,
    ),
    "remarks": re.compile(
        r"^\s*(Remark|Rmk\.)\s*(\d+[\w\.]*)?\s*[:.\-]?\s*(.*)$",
        re.IGNORECASE,
    ),
}


class EntityExtractor:
    """Extracts structured mathematical entities from parsed paper documents."""

    def __init__(self) -> None:
        """Initialize EntityExtractor instance."""
        pass

    def extract_symbols(self, text: str) -> list[str]:
        """Extract unique mathematical symbols and LaTeX expressions from text.

        Args:
            text: Input mathematical statement string.

        Returns:
            Deduplicated list of extracted math symbols or LaTeX expressions.
        """
        if not text:
            return []
        matches = SYMBOL_PATTERN.findall(text)
        seen: set[str] = set()
        result: list[str] = []
        for m in matches:
            clean = m.strip()
            if clean and clean not in seen:
                seen.add(clean)
                result.append(clean)
        return result

    def extract_references(self, text: str) -> list[str]:
        """Extract in-text citation keys and reference markers from text.

        Args:
            text: Input mathematical statement string.

        Returns:
            Deduplicated list of citation markers.
        """
        if not text:
            return []
        matches = CITATION_PATTERN.findall(text)
        seen: set[str] = set()
        result: list[str] = []
        for m in matches:
            clean = m.strip()
            if clean and clean not in seen:
                seen.add(clean)
                result.append(clean)
        return result

    def extract_from_document(
        self, document: dict[str, Any]
    ) -> list[ExtractedEntity]:
        """Extract all structured mathematical entities from a parsed document dict.

        Reuses pre-extracted Day 2 parser entities whenever available and scans sections
        for additional examples, remarks, or statements.

        Args:
            document: Parsed document dictionary adhering to Schema v1.0.

        Returns:
            List of structured ExtractedEntity instances.
        """
        if not isinstance(document, dict):
            raise TypeError(f"Expected document dictionary, got {type(document)}")

        paper_id = document.get("paper_id") or "unknown_paper"
        source_paper = (
            document.get("title")
            or document.get("source_file", {}).get("file_name")
            or paper_id
        )

        entities: list[ExtractedEntity] = []
        extracted_texts: set[str] = set()

        # Build fast section lookup map
        section_map: dict[str, dict[str, Any]] = {}
        for sec in document.get("sections") or []:
            if isinstance(sec, dict) and sec.get("section_id"):
                section_map[sec["section_id"]] = sec

        # Map entity category keys to EntityType
        category_type_map = [
            ("definitions", EntityType.DEFINITION, "def"),
            ("theorems", EntityType.THEOREM, "thm"),
            ("lemmas", EntityType.LEMMA, "lem"),
            ("corollaries", EntityType.COROLLARY, "cor"),
            ("proofs", EntityType.PROOF, "prf"),
            ("examples", EntityType.EXAMPLE, "ex"),
            ("remarks", EntityType.REMARK, "rmk"),
        ]

        entity_counters: dict[str, int] = {cat: 1 for cat, _, _ in category_type_map}

        # 1. Reuse existing pre-extracted parser entities
        for cat_key, e_type, prefix in category_type_map[:5]:  # Pre-extracted in Day 2
            parser_entities = document.get(cat_key) or []
            for item in parser_entities:
                if not isinstance(item, dict):
                    continue

                text = (item.get("text") or "").strip()
                if not text:
                    continue

                extracted_texts.add(text)

                raw_label = str(item.get("label") or "").strip()
                if not raw_label:
                    label = f"{e_type.value.capitalize()} {entity_counters[cat_key]}"
                elif not raw_label.lower().startswith(e_type.value.lower()):
                    label = f"{e_type.value.capitalize()} {raw_label}"
                else:
                    label = raw_label

                entity_counters[cat_key] += 1

                sec_id = item.get("section_id") or ""
                sec = section_map.get(sec_id, {})
                sec_title = sec.get("heading") or ""

                page_start = int(
                    item.get("page_start")
                    or item.get("page")
                    or sec.get("page_start")
                    or 1
                )
                page_end = int(
                    item.get("page_end")
                    or item.get("page")
                    or sec.get("page_end")
                    or page_start
                )

                raw_id = (
                    item.get(f"{prefix}_id")
                    or item.get(f"{e_type.value}_id")
                    or item.get("entity_id")
                    or f"{prefix}_{entity_counters[cat_key]:03d}"
                )
                entity_id = f"{paper_id}_{e_type.value}_{raw_id}"

                symbols = self.extract_symbols(text)
                references = self.extract_references(text)

                entities.append(
                    ExtractedEntity(
                        entity_id=entity_id,
                        entity_type=e_type,
                        title=str(label),
                        text=text,
                        source_paper=source_paper,
                        section_id=sec_id,
                        section_title=sec_title,
                        page_start=page_start,
                        page_end=page_end,
                        symbols=symbols,
                        references=references,
                        dependencies=[],
                    )
                )

        # 2. Scan section narrative text for additional examples, remarks, or statements
        sections = document.get("sections") or []
        for sec in sections:
            if not isinstance(sec, dict):
                continue

            sec_id = sec.get("section_id") or ""
            sec_title = sec.get("heading") or ""
            sec_page_start = int(sec.get("page_start") or 1)
            sec_page_end = int(sec.get("page_end") or sec_page_start)
            lines = (sec.get("text") or "").splitlines()

            for line in lines:
                clean_line = line.strip()
                if not clean_line or clean_line in extracted_texts:
                    continue

                for cat_key, e_type, prefix in category_type_map:
                    pattern = ENTITY_PATTERNS[cat_key]
                    match = pattern.match(clean_line)
                    if match:
                        extracted_texts.add(clean_line)

                        groups = match.groups()
                        if len(groups) >= 3:
                            num_label = groups[1]
                            title = (
                                f"{groups[0]} {num_label}".strip()
                                if num_label
                                else groups[0]
                            )
                            text_body = groups[2] or clean_line
                        elif len(groups) == 2:
                            title = groups[0]
                            text_body = groups[1] or clean_line
                        else:
                            title = e_type.value.capitalize()
                            text_body = clean_line

                        idx_num = entity_counters[cat_key]
                        entity_counters[cat_key] += 1
                        entity_id = f"{paper_id}_{e_type.value}_{prefix}_{idx_num:03d}"

                        symbols = self.extract_symbols(text_body)
                        references = self.extract_references(text_body)

                        entities.append(
                            ExtractedEntity(
                                entity_id=entity_id,
                                entity_type=e_type,
                                title=title,
                                text=text_body,
                                source_paper=source_paper,
                                section_id=sec_id,
                                section_title=sec_title,
                                page_start=sec_page_start,
                                page_end=sec_page_end,
                                symbols=symbols,
                                references=references,
                                dependencies=[],
                            )
                        )
                        break

        logger.info(
            "Extracted %d entity/entities from paper '%s'",
            len(entities),
            paper_id,
        )
        return entities

    def extract_from_file(self, file_path: str | Path) -> list[ExtractedEntity]:
        """Load a parsed document JSON file and extract mathematical entities.

        Args:
            file_path: Path to parsed document JSON file.

        Returns:
            List of ExtractedEntity objects.
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Parsed JSON file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            document = json.load(f)

        return self.extract_from_document(document)
