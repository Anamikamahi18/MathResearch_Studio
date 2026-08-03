"""JSON export helpers for schema-consistent parser outputs."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from ..models import default_output_schema

REQUIRED_TOP_LEVEL_KEYS: tuple[str, ...] = (
    "schema_version",
    "paper_id",
    "source_file",
    "title",
    "authors",
    "abstract",
    "keywords",
    "sections",
    "definitions",
    "theorems",
    "lemmas",
    "corollaries",
    "proofs",
    "references",
    "equations",
    "figures",
    "tables",
    "metadata",
)


def _as_string(value: Any, fallback: str = "") -> str:
    if value is None:
        return fallback
    return str(value)


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def _normalize_source_file(source_file: dict[str, Any]) -> dict[str, str]:
    return {
        "file_name": _as_string(source_file.get("file_name")),
        "file_path": _as_string(source_file.get("file_path")),
        "file_hash": _as_string(source_file.get("file_hash")),
        "ingested_at": _as_string(source_file.get("ingested_at")),
    }


def _normalize_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    normalized = {
        "parser_version": _as_string(metadata.get("parser_version"), "0.1.0"),
        "extraction_mode": _as_string(
            metadata.get("extraction_mode"), "text_pdf"
            ),
        "extraction_confidence": float(
            metadata.get("extraction_confidence", 0.0)
            ),
        "language": _as_string(metadata.get("language"), "en"),
        "page_count": int(metadata.get("page_count", 0) or 0),
        "ocr_used": bool(metadata.get("ocr_used", False)),
        "processing_time_ms": int(metadata.get("processing_time_ms", 0) or 0),
        "warnings": [_as_string(item) for item in _as_list(
            metadata.get("warnings")
            )],
    }

    for optional_key in (
        "source",
        "year",
        "doi",
        "diagnostics",
        "parse_state",
    ):
        if optional_key in metadata:
            normalized[optional_key] = metadata.get(optional_key)
    return normalized


def normalize_document_schema(document: dict[str, Any]) -> dict[str, Any]:
    """Return a schema-complete document with normalized field types."""
    base = default_output_schema()
    normalized = deepcopy(base)
    normalized.update({key: value for key, value in document.items()})

    normalized["schema_version"] = _as_string(
        normalized.get("schema_version"), "1.0"
        )
    normalized["paper_id"] = _as_string(normalized.get("paper_id"))
    normalized["title"] = _as_string(normalized.get("title"))
    normalized["abstract"] = _as_string(normalized.get("abstract"))
    normalized["keywords"] = [
        _as_string(item) for item in _as_list(normalized.get("keywords"))
    ]

    normalized["source_file"] = _normalize_source_file(
        dict(
            normalized.get("source_file") or {}
            )
    )
    normalized["metadata"] = _normalize_metadata(dict(
        normalized.get("metadata") or {}
        ))

    collection_keys = (
        "authors",
        "sections",
        "definitions",
        "theorems",
        "lemmas",
        "corollaries",
        "proofs",
        "references",
        "equations",
        "figures",
        "tables",
    )
    for key in collection_keys:
        normalized[key] = _as_list(normalized.get(key))

    return normalized


def validate_document_schema(document: dict[str, Any]) -> None:
    """Raise ValueError when required schema fields are missing or invalid."""
    missing = [key for key in REQUIRED_TOP_LEVEL_KEYS if key not in document]
    if missing:
        raise ValueError(f"Missing required schema keys: {missing}")

    if not document.get("paper_id"):
        raise ValueError("paper_id must be a non-empty string")

    if not isinstance(document.get("source_file"), dict):
        raise ValueError("source_file must be an object")

    if not isinstance(document.get("metadata"), dict):
        raise ValueError("metadata must be an object")


def build_parsed_document(
    *,
    paper_id: str,
    source_file: dict[str, Any],
    title: str,
    authors: list[dict[str, Any]] | None,
    abstract: str,
    keywords: list[str] | None,
    sections: list[dict[str, Any]] | None,
    entities: dict[str, list[dict[str, Any]]] | None,
    references: list[dict[str, Any]] | None,
    equations: list[dict[str, Any]] | None,
    metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build one schema-aligned parser output document.

    This is the canonical constructor for downstream NLP/RAG-safe documents.
    """
    entities = entities or {}
    document = {
        "paper_id": paper_id,
        "source_file": source_file,
        "title": title,
        "authors": authors or [],
        "abstract": abstract,
        "keywords": keywords or [],
        "sections": sections or [],
        "definitions": entities.get("definitions") or [],
        "theorems": entities.get("theorems") or [],
        "lemmas": entities.get("lemmas") or [],
        "corollaries": entities.get("corollaries") or [],
        "proofs": entities.get("proofs") or [],
        "references": references or [],
        "equations": equations or [],
        "metadata": metadata or {},
    }

    normalized = normalize_document_schema(document)
    validate_document_schema(normalized)
    return normalized


def write_json_output(document: dict[str, Any], output_dir: Path) -> Path:
    """Write one parsed document to an output JSON file.

    The document is normalized and validated before persistence.
    """
    normalized = normalize_document_schema(document)
    validate_document_schema(normalized)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{normalized['paper_id']}.json"
    output_path.write_text(
        json.dumps(normalized, indent=2, ensure_ascii=True),
        encoding="utf-8",
    )
    return output_path
