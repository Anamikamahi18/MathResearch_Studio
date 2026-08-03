"""Shared parser model helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    """Return a UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def default_output_schema() -> dict[str, Any]:
    """Return the baseline output schema with safe defaults."""
    return {
        "schema_version": "1.0",
        "paper_id": "",
        "source_file": {
            "file_name": "",
            "file_path": "",
            "file_hash": "",
            "ingested_at": "",
        },
        "title": "",
        "authors": [],
        "abstract": "",
        "keywords": [],
        "sections": [],
        "definitions": [],
        "theorems": [],
        "lemmas": [],
        "corollaries": [],
        "proofs": [],
        "references": [],
        "equations": [],
        "figures": [],
        "tables": [],
        "metadata": {
            "parser_version": "0.1.0",
            "extraction_mode": "text_pdf",
            "extraction_confidence": 0.0,
            "language": "en",
            "page_count": 0,
            "ocr_used": False,
            "processing_time_ms": 0,
            "warnings": [],
        },
    }
