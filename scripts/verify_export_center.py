#!/usr/bin/env python3
"""Verification script for Day 6 Step 8: Export Center UI."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.application.document_service import DocumentService
from src.application.export_service import ExportService
from src.ui.pages.export import format_bytes_to_kb, get_mime_type

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def create_mock_parsed_paper() -> dict:
    """Create mock parsed document dict for testing export verification."""
    return {
        "paper_id": "paper_export_006",
        "metadata": {
            "title": "Lie Groups and Representation Theory",
            "authors": ["S. Lie", "H. Weyl"],
            "year": 1888,
            "source": "Leipzig Teubner",
            "doi": "10.1000/lie.1888",
            "keywords": ["Lie Algebra", "Representation Theory", "Compact Group"],
            "ingested_at": "2024-08-05T10:00:00Z",
        },
        "sections": [
            {
                "section_id": "s1",
                "heading": "1. Lie Algebras",
                "level": 1,
                "page_start": 1,
                "page_end": 6,
                "text": "Definition 1.1 (Lie Algebra). A Lie algebra g over a field F is a vector space with a bilinear bracket operation satisfying antisymmetry and Jacobi identity.",
                "section_type": "definition",
            },
        ],
        "equations": [],
        "references": [],
        "source_file": {
            "file_name": "lie_groups.pdf",
            "file_path": "uploads/lie_groups.pdf",
        },
        "math_entities": {
            "definitions": [{"id": "def_1.1", "title": "Definition 1.1 (Lie Algebra)"}],
            "theorems": [],
            "lemmas": [],
            "corollaries": [],
            "proofs": [],
        },
    }


def main() -> None:
    """Run verification for Export Center page integrations and ExportService."""
    print("\n============================================================")
    print(" DAY 6 STEP 8: EXPORT CENTER VERIFICATION")
    print("============================================================\n")

    doc_service = DocumentService(
        upload_dir="uploads",
        parsed_dir="exports/parser_outputs",
    )
    export_service = ExportService(export_dir="exports/test_runs")

    sample_doc = create_mock_parsed_paper()

    # 1. Ingest document into catalog
    print("[1] Ingesting sample paper into system catalog...")
    store_metrics = doc_service.store_paper(sample_doc)
    print(f"    Paper ID:           '{store_metrics['paper_id']}'")

    # 2. Test Markdown Export via ExportService.export_summaries()
    print("\n[2] Testing ExportService Markdown Export...")
    papers = doc_service.list_papers()
    md_file = export_service.export_summaries(documents_or_results=papers, format="markdown")
    print(f"    Exported File:      {md_file.name}")
    print(f"    File Size:          {format_bytes_to_kb(md_file.stat().st_size)}")
    assert md_file.exists(), "Expected Markdown export file to exist"
    assert md_file.stat().st_size > 0, "Expected Markdown export file to be non-empty"

    # 3. Test JSON Export via ExportService.export_to_json()
    print("\n[3] Testing ExportService JSON Export...")
    json_file = export_service.export_to_json(data=papers, output_path=export_service.export_dir / "paper_summaries.json")
    print(f"    Exported File:      {json_file.name}")
    print(f"    File Size:          {format_bytes_to_kb(json_file.stat().st_size)}")
    assert json_file.exists()

    # 4. Test CSV Export via ExportService.export_to_csv()
    print("\n[4] Testing ExportService CSV Export...")
    csv_file = export_service.export_to_csv(data=papers, output_path=export_service.export_dir / "paper_summaries.csv")
    print(f"    Exported File:      {csv_file.name}")
    print(f"    File Size:          {format_bytes_to_kb(csv_file.stat().st_size)}")
    assert csv_file.exists()

    # 5. Test MIME Helper and Size Formatter
    print("\n[5] Testing MIME Types and File Size Helpers...")
    assert get_mime_type("markdown") == "text/markdown"
    assert get_mime_type("json") == "application/json"
    assert get_mime_type("csv") == "text/csv"
    assert format_bytes_to_kb(500) == "500 B"
    assert format_bytes_to_kb(2048) == "2.0 KB"
    print("    MIME types and file size formatting helpers verified")

    print("\n============================================================")
    print(" VERIFICATION COMPLETED SUCCESSFULLY FOR EXPORT CENTER")
    print("============================================================\n")


if __name__ == "__main__":
    main()
