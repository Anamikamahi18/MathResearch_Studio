"""Reference extraction from detected bibliography sections."""

from __future__ import annotations

import re
from typing import Any

from ..helpers import clean_line

ENTRY_SPLIT_PATTERN = re.compile(r"\n\s*(?:\[(\d+)\]|(\d+)\.)\s+")
YEAR_PATTERN = re.compile(r"\b(19|20)\d{2}\b")
DOI_PATTERN = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
URL_PATTERN = re.compile(r"https?://\S+")


def _extract_reference_section(sections: list[dict[str, Any]]) -> str:
    for section in sections:
        heading = (section.get("heading") or "").lower()
        if "reference" in heading or "bibliograph" in heading:
            return section.get("text") or ""
    return ""


def _split_entries(reference_block: str) -> list[str]:
    block = reference_block.strip()
    if not block:
        return []

    if ENTRY_SPLIT_PATTERN.search(f"\n{block}"):
        raw_parts = ENTRY_SPLIT_PATTERN.split(f"\n{block}")
        entries = [
            clean_line(part)
            for part in raw_parts
            if part and not part.isdigit()
        ]
        return [entry for entry in entries if entry]

    chunks = [
        chunk.strip()
        for chunk in re.split(r"\n\s*\n", block)
        if chunk.strip()
    ]
    return [clean_line(chunk) for chunk in chunks if clean_line(chunk)]


def extract_references(sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Extract basic bibliography entries and optional structured fields."""
    reference_block = _extract_reference_section(sections)
    entries = _split_entries(reference_block)

    references: list[dict[str, Any]] = []
    for index, entry in enumerate(entries, start=1):
        year_match = YEAR_PATTERN.search(entry)
        doi_match = DOI_PATTERN.search(entry)
        url_match = URL_PATTERN.search(entry)

        year = int(year_match.group(0)) if year_match else None
        doi = doi_match.group(0) if doi_match else None
        url = url_match.group(0) if url_match else None

        title = None
        if "." in entry:
            parts = [
                clean_line(part)
                for part in entry.split(".")
                if clean_line(part)
            ]
            if len(parts) >= 2:
                title = parts[1]

        authors: list[str] = []
        if "." in entry:
            author_part = clean_line(entry.split(".", maxsplit=1)[0])
            author_part = re.sub(r"^\[\d+\]\s*", "", author_part)
            author_part = re.sub(r"^\d+\.\s*", "", author_part)
            for candidate in re.split(
                r",|\band\b", author_part, flags=re.IGNORECASE
            ):
                normalized = clean_line(candidate)
                if normalized:
                    authors.append(normalized)

        references.append(
            {
                "reference_id": f"ref_{index:03d}",
                "raw_text": entry,
                "title": title,
                "authors": authors,
                "year": year,
                "venue": None,
                "doi": doi,
                "url": url,
            }
        )

    return references
