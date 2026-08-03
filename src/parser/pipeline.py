"""Day 2 parser pipeline orchestrator.

Usage:
    python -m src.parser.pipeline tests/sample_papers \
        --output-dir exports/parser_outputs
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Any

from .equation_detector import detect_equations
from .helpers import stable_paper_id
from .json_export import build_parsed_document, write_json_output
from .metadata import extract_metadata
from .models import utc_now_iso
from .pdf_loader import load_pdf
from .reference_parser import extract_references
from .reliability import (
    WarningCode,
    clamp_references,
    compute_extraction_confidence,
    diagnostics_to_warning_strings,
    evaluate_quality_thresholds,
    make_diagnostic,
    resolve_parse_state,
)
from .section_detector import detect_sections, extract_math_entities


def _collect_pdf_paths(input_path: Path) -> list[Path]:
    if input_path.is_file() and input_path.suffix.lower() == ".pdf":
        return [input_path]
    if input_path.is_dir():
        return sorted(
            path for path in input_path.glob("*.pdf") if path.is_file()
            )
    return []


def _derive_abstract(
    sections: list[dict[str, Any]], pages: list[dict[str, Any]]
) -> str:
    for section in sections:
        heading = (section.get("heading") or "").lower()
        if "abstract" in heading:
            return (section.get("text") or "")[:4000]
    first_page_text = (pages[0].get("text") if pages else "") or ""
    return first_page_text[:2000]


def _fallback_document_section(
        pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build a safe fallback section when section detection fails."""
    full_text = "\n".join(
        (page.get("text") or "") for page in pages if page.get("text")
    )
    return [
        {
            "section_id": "s1",
            "heading": "Document",
            "level": 1,
            "page_start": 1 if pages else 0,
            "page_end": pages[-1].get("page", 0) if pages else 0,
            "text": full_text,
            "parent_section_id": None,
            "section_type": "other",
            "confidence": 0.2,
        }
    ]


def parse_pdf(file_path: Path, output_dir: Path) -> Path:
    """Parse one PDF file and write a schema-aligned JSON output."""
    started_at = time.perf_counter()
    diagnostics: list[dict[str, Any]] = []

    loaded = load_pdf(file_path)
    pages = loaded.get("pages") or []
    section_fallback_used = False

    try:
        sections = detect_sections(pages)
    except Exception as exc:
        section_fallback_used = True
        diagnostics.append(
            make_diagnostic(
                code=WarningCode.SECTION_DETECTOR_FAILED,
                stage="detect_sections",
                message="Section detection failed; fallback section used.",
                details={"error": str(exc)},
            )
        )
        sections = _fallback_document_section(pages)

    first_page_text = pages[0].get("text", "") if pages else ""
    try:
        metadata = extract_metadata(loaded["metadata_raw"], first_page_text)
    except Exception as exc:
        diagnostics.append(
            make_diagnostic(
                code=WarningCode.META_FIELD_CONFLICT,
                stage="metadata",
                message="Metadata extraction failed; defaults applied.",
                details={"error": str(exc)},
            )
        )
        metadata = {
            "title": "",
            "authors": [],
            "year": None,
            "source": None,
            "doi": None,
            "keywords": [],
        }

    try:
        references = extract_references(sections)
    except Exception as exc:
        diagnostics.append(
            make_diagnostic(
                code=WarningCode.REFERENCES_PARSE_UNSTABLE,
                stage="parse_references",
                message="Reference parsing failed; references set to empty.",
                details={"error": str(exc)},
            )
        )
        references = []
    raw_reference_count = len(references)
    references, _ = clamp_references(references)

    try:
        equations = detect_equations(pages, sections)
    except Exception as exc:
        diagnostics.append(
            make_diagnostic(
                code=WarningCode.EXTRACT_MALFORMED_TEXT,
                stage="extract_equations",
                message="Equation extraction failed; equations set to empty.",
                details={"error": str(exc)},
            )
        )
        equations = []

    try:
        entities = extract_math_entities(sections)
    except Exception as exc:
        diagnostics.append(
            make_diagnostic(
                code=WarningCode.ENTITY_EXTRACTOR_FAILED,
                stage="extract_entities",
                message="Math entity extraction failed; entity "
                "arrays set empty.",
                details={"error": str(exc)},
            )
        )
        entities = {
            "definitions": [],
            "theorems": [],
            "lemmas": [],
            "corollaries": [],
            "proofs": [],
        }

    paper_id = stable_paper_id(loaded["file_hash"])
    source_file = {
        "file_name": loaded["file_name"],
        "file_path": loaded["file_path"],
        "file_hash": loaded["file_hash"],
        "ingested_at": utc_now_iso(),
    }

    processing_time_ms = int((time.perf_counter() - started_at) * 1000)
    warnings: list[str] = []
    ocr_used = False
    extraction_mode = "text_pdf"
    if loaded["empty_pages"] > 0:
        diagnostics.append(
            make_diagnostic(
                code=WarningCode.EXTRACT_EMPTY_PAGE,
                stage="extract_text",
                message=(
                    f"{loaded['empty_pages']} page(s) had empty text; OCR "
                    "fallback recommended."
                ),
                details={"empty_pages": loaded["empty_pages"]},
            )
        )
        ocr_used = True
        extraction_mode = "hybrid"

    if not metadata.get("title"):
        diagnostics.append(
            make_diagnostic(
                code=WarningCode.META_TITLE_MISSING,
                stage="metadata",
                message="Title missing from metadata and heuristics.",
            )
        )

    if not metadata.get("authors"):
        diagnostics.append(
            make_diagnostic(
                code=WarningCode.META_AUTHORS_MISSING,
                stage="metadata",
                message="Author list missing from metadata and heuristics.",
            )
        )

    if not metadata.get("year"):
        diagnostics.append(
            make_diagnostic(
                code=WarningCode.META_YEAR_MISSING,
                stage="metadata",
                message="Publication year not detected.",
            )
        )

    if not metadata.get("doi"):
        diagnostics.append(
            make_diagnostic(
                code=WarningCode.META_DOI_MISSING,
                stage="metadata",
                message="DOI not detected.",
            )
        )

    token_count = len(
        " ".join((page.get("text") or "") for page in pages).split()
        )
    diagnostics.extend(
        evaluate_quality_thresholds(
            token_count=token_count,
            section_count=len(sections),
            reference_count=raw_reference_count,
        )
    )

    warnings = diagnostics_to_warning_strings(diagnostics)
    extraction_confidence = compute_extraction_confidence(
        page_count=loaded["page_count"],
        has_title=bool(metadata.get("title")),
        has_authors=bool(metadata.get("authors")),
        section_count=len(sections),
        diagnostics=diagnostics,
        section_detection_succeeded=not section_fallback_used,
    )
    parse_state = resolve_parse_state(
        diagnostics=diagnostics,
        extraction_confidence=extraction_confidence,
    )

    export_metadata = {
        "parser_version": "0.1.0",
        "extraction_mode": extraction_mode,
        "extraction_confidence": extraction_confidence,
        "language": "en",
        "page_count": loaded["page_count"],
        "ocr_used": ocr_used,
        "processing_time_ms": processing_time_ms,
        "warnings": warnings,
        "diagnostics": diagnostics,
        "parse_state": parse_state,
        "source": metadata.get("source"),
        "year": metadata.get("year"),
        "doi": metadata.get("doi"),
    }

    document = build_parsed_document(
        paper_id=paper_id,
        source_file=source_file,
        title=metadata.get("title") or loaded["file_name"],
        authors=metadata.get("authors") or [],
        abstract=_derive_abstract(sections, loaded["pages"]),
        keywords=metadata.get("keywords") or [],
        sections=sections,
        entities=entities,
        references=references,
        equations=equations,
        metadata=export_metadata,
    )

    return write_json_output(document, output_dir)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Parse mathematics PDFs into structured JSON outputs."
    )
    parser.add_argument(
        "input",
        help="PDF file path or directory containing PDFs",
    )
    parser.add_argument(
        "--output-dir",
        default="exports/parser_outputs",
        help="Directory for JSON outputs",
    )
    args = parser.parse_args(argv)

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    pdf_paths = _collect_pdf_paths(input_path)

    if not pdf_paths:
        print(f"No PDF files found at: {input_path}")
        return 1

    print(f"Discovered {len(pdf_paths)} PDF file(s).")
    for path in pdf_paths:
        try:
            output_path = parse_pdf(path, output_dir)
            print(f"Parsed: {path.name} -> {output_path}")
        except Exception as exc:  # pragma: no cover - CLI resilience
            print(f"Failed: {path.name} ({exc})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
