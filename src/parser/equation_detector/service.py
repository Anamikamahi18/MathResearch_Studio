"""Heuristic equation extraction from page text."""

from __future__ import annotations

import re
from typing import Any

from ..helpers import clean_line

EQUATION_SIGNAL = re.compile(
    r"(=|\\int|\\sum|\\prod|\\forall|\\exists|\\leq|\\geq|\^|_)"
)


def _is_equation_line(line: str) -> bool:
    if not line:
        return False
    if len(line) > 240:
        return False
    if EQUATION_SIGNAL.search(line):
        alpha = sum(char.isalpha() for char in line)
        symbols = sum(
            not char.isalnum() and not char.isspace()
            for char in line
        )
        return symbols >= 3 and alpha <= max(35, len(line) // 2)
    return False


def detect_equations(
    pages: list[dict[str, Any]], sections: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Detect candidate equation lines and attach lightweight provenance."""
    section_lookup: dict[int, str] = {}
    for section in sections:
        for page_num in range(section["page_start"], section["page_end"] + 1):
            section_lookup.setdefault(page_num, section["section_id"])

    equations: list[dict[str, Any]] = []
    counter = 1
    for page in pages:
        page_num = page["page"]
        for line in (page.get("text") or "").splitlines():
            normalized = clean_line(line)
            if not _is_equation_line(normalized):
                continue

            equations.append(
                {
                    "equation_id": f"eq_{counter:03d}",
                    "label": None,
                    "text_repr": normalized,
                    "latex_repr": None,
                    "section_id": section_lookup.get(page_num, "s1"),
                    "page": page_num,
                    "confidence": 0.55,
                }
            )
            counter += 1

    return equations
