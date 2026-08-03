"""Section detection and baseline mathematical entity extraction."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from ..helpers import clean_line


@dataclass(frozen=True)
class HeadingRule:
    """Canonical rule for matching a section heading label."""

    section_type: str
    pattern: re.Pattern[str]
    confidence: float


NUMBERED_HEADING = re.compile(
    r"^(?P<num>\d+(?:\.\d+)*)[\).:-]?\s+(?P<title>[^\n]{1,160})$"
)
ROMAN_HEADING = re.compile(
    r"^(?P<num>[IVXLCDM]+)[\).:-]?\s+(?P<title>[^\n]{1,160})$",
    re.IGNORECASE,
)
LETTER_HEADING = re.compile(
    r"^(?P<num>[A-Z])[\).:-]\s+(?P<title>[^\n]{1,160})$"
    )

HEADING_RULES: tuple[HeadingRule, ...] = (
    HeadingRule("abstract", re.compile(r"^abstract$", re.IGNORECASE), 0.99),
    HeadingRule(
        "introduction",
        re.compile(r"^(introduction|overview)$", re.IGNORECASE),
        0.98,
    ),
    HeadingRule(
        "preliminaries",
        re.compile(
            r"^(preliminar(?:y|ies)|preparation|background|notation)$",
            re.IGNORECASE,
        ),
        0.95,
    ),
    HeadingRule(
        "definitions",
        re.compile(r"^(definitions?|basic definitions?)$", re.IGNORECASE),
        0.97,
    ),
    HeadingRule(
        "lemmas",
        re.compile(r"^(lemmas?|auxiliary lemmas?)$", re.IGNORECASE),
        0.97,
    ),
    HeadingRule(
        "theorems",
        re.compile(
            r"^(theorems?|main theorems?|main results?)$", re.IGNORECASE
            ),
        0.97,
    ),
    HeadingRule(
        "proofs",
        re.compile(
            r"^(proofs?|proof of .*|proofs of .* results?)$", re.IGNORECASE
            ),
        0.94,
    ),
    HeadingRule(
        "results",
        re.compile(
            r"^(results?|discussion|experiments?|findings?|analysis)$",
            re.IGNORECASE,
        ),
        0.94,
    ),
    HeadingRule(
        "conclusion",
        re.compile(
            r"^(conclusion|conclusions|concluding remarks?)$",
            re.IGNORECASE,
        ),
        0.98,
    ),
    HeadingRule(
        "references",
        re.compile(r"^(references|bibliography|works cited)$", re.IGNORECASE),
        0.99,
    ),
)


def _looks_like_heading(candidate: str) -> bool:
    """Lightweight checks to avoid classifying prose lines as headings."""
    if not candidate:
        return False
    if len(candidate) > 160:
        return False
    if candidate.count(" ") > 14:
        return False
    if ":" in candidate and not candidate.endswith(":"):
        return False
    if candidate.endswith("."):
        return False
    alpha_count = sum(1 for char in candidate if char.isalpha())
    if alpha_count < 3:
        return False
    return True


def _strip_number_prefix(line: str) -> tuple[str, int, bool]:
    """Strip common numeric prefixes and infer heading level."""
    numbered = NUMBERED_HEADING.match(line)
    if numbered:
        level = numbered.group("num").count(".") + 1
        return clean_line(numbered.group("title")), level, True

    roman = ROMAN_HEADING.match(line)
    if roman:
        return clean_line(roman.group("title")), 1, True

    lettered = LETTER_HEADING.match(line)
    if lettered:
        return clean_line(lettered.group("title")), 2, True

    return line, 1, False


def _classify_section_type(heading_text: str) -> tuple[str | None, float]:
    """Map heading text to canonical section type and confidence."""
    lowered = heading_text.lower().rstrip(":")
    for rule in HEADING_RULES:
        if rule.pattern.match(lowered):
            return rule.section_type, rule.confidence
    return None, 0.0


def _detect_heading(line: str) -> tuple[bool, int, str, str | None, float]:
    """Return heading signal with level, cleaned label, type and confidence."""
    candidate = clean_line(line)
    if not _looks_like_heading(candidate):
        return False, 1, "", None, 0.0

    normalized_heading, level, had_number_prefix = _strip_number_prefix(
        candidate
        )
    if not _looks_like_heading(normalized_heading):
        return False, 1, "", None, 0.0

    section_type, confidence = _classify_section_type(normalized_heading)
    if section_type is not None:
        return True, level, normalized_heading, section_type, confidence

    looks_title_case = normalized_heading == normalized_heading.title()
    mostly_upper = normalized_heading.isupper()
    if had_number_prefix and (looks_title_case or mostly_upper):
        return True, level, normalized_heading, "other", 0.62

    return False, 1, "", None, 0.0


def _assign_parent_section_id(
    level: int,
    section_id: str,
    active_stack: list[tuple[int, str]],
) -> str | None:
    """Track heading hierarchy using a level stack."""
    while active_stack and active_stack[-1][0] >= level:
        active_stack.pop()

    parent_section_id = active_stack[-1][1] if active_stack else None
    active_stack.append((level, section_id))
    return parent_section_id


def detect_sections(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Detect hierarchical sections from page text."""
    indexed_lines: list[dict[str, Any]] = []
    for page in pages:
        page_number = page.get("page", 0)
        for line in (page.get("text") or "").splitlines():
            indexed_lines.append(
                {"page": page_number, "line": clean_line(line)}
                )

    heading_positions: list[dict[str, Any]] = []
    for index, item in enumerate(indexed_lines):
        is_heading, level, heading, section_type, confidence = _detect_heading(
            item["line"]
        )
        if is_heading:
            heading_positions.append(
                {
                    "index": index,
                    "level": level,
                    "heading": heading,
                    "section_type": section_type,
                    "confidence": confidence,
                }
            )

    if not heading_positions:
        full_text = "\n".join(
            item["line"] for item in indexed_lines if item["line"]
            )
        return [
            {
                "section_id": "s1",
                "heading": "Document",
                "level": 1,
                "page_start": 1 if pages else 0,
                "page_end": pages[-1]["page"] if pages else 0,
                "text": full_text,
                "parent_section_id": None,
            }
        ]

    sections: list[dict[str, Any]] = []
    hierarchy_stack: list[tuple[int, str]] = []
    for i, heading_info in enumerate(heading_positions, start=1):
        start_index = heading_info["index"]
        level = heading_info["level"]
        if i < len(heading_positions):
            end_index = heading_positions[i]["index"]
        else:
            end_index = len(indexed_lines)

        heading_line = heading_info["heading"]
        span_lines = indexed_lines[start_index + 1: end_index]
        section_text = "\n".join(
            item["line"] for item in span_lines if item["line"]
            )
        page_start = indexed_lines[start_index]["page"]
        if end_index - 1 >= start_index:
            page_end = indexed_lines[end_index - 1]["page"]
        else:
            page_end = page_start

        section_id = f"s{i}"
        parent_section_id = _assign_parent_section_id(
            level=level,
            section_id=section_id,
            active_stack=hierarchy_stack,
        )

        sections.append(
            {
                "section_id": section_id,
                "heading": heading_line,
                "level": level,
                "page_start": page_start,
                "page_end": page_end,
                "text": section_text,
                "parent_section_id": parent_section_id,
                "section_type": heading_info["section_type"] or "other",
                "confidence": round(float(heading_info["confidence"]), 3),
            }
        )

    return sections


ENTITY_PATTERNS = {
    "definitions": re.compile(
        r"^\s*(Definition)\s*(\d+[\w\.]*)?\s*[:.\-]?\s*(.*)$",
        re.IGNORECASE,
    ),
    "theorems": re.compile(
        r"^\s*(Theorem)\s*(\d+[\w\.]*)?\s*[:.\-]?\s*(.*)$",
        re.IGNORECASE,
    ),
    "lemmas": re.compile(
        r"^\s*(Lemma)\s*(\d+[\w\.]*)?\s*[:.\-]?\s*(.*)$",
        re.IGNORECASE,
    ),
    "corollaries": re.compile(
        r"^\s*(Corollary)\s*(\d+[\w\.]*)?\s*[:.\-]?\s*(.*)$",
        re.IGNORECASE,
    ),
    "proofs": re.compile(
        r"^\s*(Proof)\s*[:.\-]?\s*(.*)$",
        re.IGNORECASE,
    ),
}


def extract_math_entities(
    sections: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Extract candidate definition/theorem/lemma/corollary/proof blocks."""
    output: dict[str, list[dict[str, Any]]] = {
        "definitions": [],
        "theorems": [],
        "lemmas": [],
        "corollaries": [],
        "proofs": [],
    }
    counters = {key: 1 for key in output}

    for section in sections:
        lines = (section.get("text") or "").splitlines()
        for idx, line in enumerate(lines):
            clean = clean_line(line)
            if not clean:
                continue

            for entity_type, pattern in ENTITY_PATTERNS.items():
                match = pattern.match(clean)
                if not match:
                    continue

                entity_id_prefix = entity_type[:-1]
                entity_id = f"{entity_id_prefix}_{counters[entity_type]:03d}"
                counters[entity_type] += 1

                text_body = clean
                label = None
                if entity_type == "proofs":
                    text_body = match.group(2) or clean
                else:
                    label = match.group(2) or None
                    remainder = match.group(3) or ""
                    text_body = remainder or clean

                payload: dict[str, Any] = {
                    f"{entity_id_prefix}_id": entity_id,
                    "label": label,
                    "text": text_body,
                    "section_id": section["section_id"],
                    "page": section["page_start"],
                    "span": {"start": idx, "end": idx},
                    "confidence": 0.7,
                }

                if entity_type == "proofs":
                    payload = {
                        "proof_id": entity_id,
                        "related_to": {
                            "theorem_id": None,
                            "lemma_id": None,
                            "corollary_id": None,
                        },
                        "text": text_body,
                        "section_id": section["section_id"],
                        "page_start": section["page_start"],
                        "page_end": section["page_end"],
                        "confidence": 0.65,
                    }

                output[entity_type].append(payload)
                break

    return output
