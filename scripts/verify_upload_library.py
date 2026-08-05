#!/usr/bin/env python3
"""Verification script for Day 6 Step 2: PDF Upload and Document Library."""

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
from src.ui.pages.library import count_math_entity_type, filter_papers_by_keyword

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def create_mock_parsed_paper() -> dict:
    """Create mock parsed document dict for testing library verification."""
    return {
        "paper_id": "paper_topology_01",
        "metadata": {
            "title": "Introduction to Algebraic Topology",
            "authors": ["A. Hatcher"],
            "year": 2002,
            "source": "Cambridge University Press",
            "doi": "10.1000/top.2002",
            "keywords": ["Topology", "Fundamental Group", "Homology"],
            "ingested_at": "2024-08-05T10:00:00Z",
        },
        "sections": [
            {
                "section_id": "s1",
                "heading": "1. Fundamental Group",
                "level": 1,
                "page_start": 1,
                "page_end": 2,
                "text": "Definition 1.1 (Fundamental Group). The fundamental group pi_1(X, x_0) consists of homotopy classes of loops based at x_0.",
                "section_type": "definition",
            },
            {
                "section_id": "s2",
                "heading": "2. Main Theorem",
                "level": 1,
                "page_start": 3,
                "page_end": 4,
                "text": "Theorem 2.1 (Seifert-van Kampen Theorem). The fundamental group of a union of path-connected spaces is the free product of their fundamental groups with amalgamation.",
                "section_type": "theorem",
            },
        ],
        "equations": [],
        "references": [],
        "source_file": {
            "file_name": "hatcher_topology.pdf",
            "file_path": "uploads/hatcher_topology.pdf",
        },
        "math_entities": {
            "definitions": [{"id": "def_1.1", "title": "Definition 1.1 (Fundamental Group)"}],
            "theorems": [{"id": "thm_2.1", "title": "Theorem 2.1 (Seifert-van Kampen)"}],
            "lemmas": [],
            "corollaries": [],
            "proofs": [],
        },
    }


def main() -> None:
    """Run verification for PDF Upload and Document Library UI integrations."""
    print("\n============================================================")
    print(" DAY 6 STEP 2: PDF UPLOAD & DOCUMENT LIBRARY VERIFICATION")
    print("============================================================\n")

    doc_service = DocumentService(
        upload_dir="uploads",
        parsed_dir="exports/parser_outputs",
    )

    sample_doc = create_mock_parsed_paper()

    # 1. Test Storing Paper via DocumentService
    print("[1] Verifying DocumentService.store_paper()...")
    metrics = doc_service.store_paper(sample_doc)
    print(f"    Paper ID:           '{metrics['paper_id']}'")
    print(f"    Title:              '{metrics['title']}'")
    print(f"    Chunks Indexed:     {metrics['chunk_count']}")
    print(f"    Graph Nodes:        {metrics['graph_node_count']}")

    # 2. Test Listing Papers via DocumentService
    print("\n[2] Verifying DocumentService.list_papers()...")
    papers = doc_service.list_papers()
    print(f"    Library Count:      {len(papers)} paper(s)")
    assert len(papers) >= 1, "Expected at least 1 paper in library"

    # 3. Test Keyword Filtering Logic
    print("\n[3] Verifying Library Keyword Filtering...")
    match_title = filter_papers_by_keyword(papers, "Topology")
    print(f"    Keyword 'Topology':  Matched {len(match_title)} paper(s)")
    assert len(match_title) == 1, "Expected keyword 'Topology' to match 1 paper"

    match_author = filter_papers_by_keyword(papers, "Hatcher")
    print(f"    Keyword 'Hatcher':   Matched {len(match_author)} paper(s)")
    assert len(match_author) == 1, "Expected keyword 'Hatcher' to match 1 paper"

    match_none = filter_papers_by_keyword(papers, "Quantum")
    print(f"    Keyword 'Quantum':   Matched {len(match_none)} paper(s)")
    assert len(match_none) == 0, "Expected keyword 'Quantum' to match 0 papers"

    # 4. Test Entity Counting Helpers
    print("\n[4] Verifying Math Entity Extraction Helpers...")
    def_count = count_math_entity_type(papers[0], "definitions")
    thm_count = count_math_entity_type(papers[0], "theorems")
    lem_count = count_math_entity_type(papers[0], "lemmas")
    print(f"    Extracted Definitions: {def_count}")
    print(f"    Extracted Theorems:    {thm_count}")
    print(f"    Extracted Lemmas:      {lem_count}")
    assert def_count == 1
    assert thm_count == 1

    # 5. Test Refreshing Library
    print("\n[5] Verifying DocumentService.refresh_library()...")
    refreshed = doc_service.refresh_library()
    print(f"    Refreshed Catalog:  {len(refreshed)} paper(s)")

    print("\n============================================================")
    print(" VERIFICATION COMPLETED SUCCESSFULLY FOR UPLOAD & LIBRARY UI")
    print("============================================================\n")


if __name__ == "__main__":
    main()
