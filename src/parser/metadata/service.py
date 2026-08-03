"""Metadata extraction logic for scientific PDFs."""

from __future__ import annotations

import re
from typing import Any

from ..helpers import clean_line, non_empty_lines

DOI_PATTERN = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
YEAR_PATTERN = re.compile(r"\b(19|20)\d{2}\b")


def _split_authors(author_text: str) -> list[dict[str, Any]]:
    if not author_text:
        return []
    normalized = re.sub(r"\band\b", ",", author_text, flags=re.IGNORECASE)
    names = [
        clean_line(name) for name in normalized.split(",") if clean_line(name)
        ]
    return [
        {"name": name, "affiliation": None, "email": None} for name in names
        ]


def _heuristic_title(lines: list[str]) -> str:
    for line in lines[:12]:
        if len(line) < 20:
            continue
        if line.lower().startswith(("arxiv", "doi", "abstract")):
            continue
        return line
    return lines[0] if lines else ""


def _heuristic_authors(lines: list[str], title: str) -> list[dict[str, Any]]:
    if not lines:
        return []
    for line in lines[:15]:
        if line == title:
            continue
        if any(token in line.lower()
               for token in ["abstract", "arxiv", "doi"]):
            continue
        if 4 <= len(line) <= 200 and ("," in line or " and " in line.lower()):
            authors = _split_authors(line)
            if authors:
                return authors
    return []


def _extract_keywords(lines: list[str]) -> list[str]:
    for line in lines[:80]:
        if line.lower().startswith("keywords"):
            _, _, value = line.partition(":")
            candidates = [
                clean_line(item) for item in re.split(r"[,;]", value)
                ]
            return [item for item in candidates if item]
    return []


def extract_metadata(
    raw_metadata: dict[str, Any], first_page_text: str
) -> dict[str, Any]:
    """Extract title, authors, year, source, DOI and keywords."""
    lines = non_empty_lines(first_page_text)

    title = clean_line(str(raw_metadata.get("/Title", "")))
    if not title or title.lower() in {"untitled", "none"}:
        title = _heuristic_title(lines)

    authors = _split_authors(clean_line(str(raw_metadata.get("/Author", ""))))
    if not authors:
        authors = _heuristic_authors(lines, title)

    joined_preview = "\n".join(lines[:120])
    doi_match = DOI_PATTERN.search(joined_preview)
    doi = doi_match.group(0) if doi_match else None

    year = None
    creation_date = clean_line(str(raw_metadata.get("/CreationDate", "")))
    for candidate in [creation_date, joined_preview]:
        year_match = YEAR_PATTERN.search(candidate)
        if year_match:
            year = int(year_match.group(0))
            break

    source = clean_line(str(raw_metadata.get("/Producer", ""))) or None
    keywords = _extract_keywords(lines)

    return {
        "title": title,
        "authors": authors,
        "year": year,
        "source": source,
        "doi": doi,
        "keywords": keywords,
    }
