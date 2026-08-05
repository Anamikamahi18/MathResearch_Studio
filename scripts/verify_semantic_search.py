#!/usr/bin/env python3
"""Verification script for Day 6 Step 3: Semantic Search UI."""

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
from src.application.search_service import SearchService
from src.ui.pages.search import get_score_badge_style

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def create_mock_parsed_paper() -> dict:
    """Create mock parsed document dict for testing search verification."""
    return {
        "paper_id": "paper_functional_01",
        "metadata": {
            "title": "Functional Analysis and Operator Algebras",
            "authors": ["J. von Neumann"],
            "year": 1936,
            "source": "Annals of Mathematics",
            "doi": "10.1000/annals.1936",
            "keywords": ["Operator Algebras", "Hilbert Space", "Functional Analysis"],
            "ingested_at": "2024-08-05T10:00:00Z",
        },
        "sections": [
            {
                "section_id": "s1",
                "heading": "1. Operator Algebras",
                "level": 1,
                "page_start": 1,
                "page_end": 3,
                "text": "Definition 1.1 (Von Neumann Algebra). A von Neumann algebra M is a *-subalgebra of bounded operators on a Hilbert space H that is closed in the weak operator topology.",
                "section_type": "definition",
            },
            {
                "section_id": "s2",
                "heading": "2. Bicommutant Theorem",
                "level": 1,
                "page_start": 4,
                "page_end": 6,
                "text": "Theorem 2.1 (Von Neumann Bicommutant Theorem). Let M be a *-subalgebra containing the identity. Then M is a von Neumann algebra if and only if M equals its double commutant M''.",
                "section_type": "theorem",
            },
        ],
        "equations": [],
        "references": [],
        "source_file": {
            "file_name": "von_neumann_algebra.pdf",
            "file_path": "uploads/von_neumann_algebra.pdf",
        },
        "math_entities": {
            "definitions": [{"id": "def_1.1", "title": "Definition 1.1 (Von Neumann Algebra)"}],
            "theorems": [{"id": "thm_2.1", "title": "Theorem 2.1 (Bicommutant Theorem)"}],
            "lemmas": [],
            "corollaries": [],
            "proofs": [],
        },
    }


def main() -> None:
    """Run verification for Semantic Search page integrations and SearchService."""
    print("\n============================================================")
    print(" DAY 6 STEP 3: SEMANTIC VECTOR SEARCH VERIFICATION")
    print("============================================================\n")

    doc_service = DocumentService(
        upload_dir="uploads",
        parsed_dir="exports/parser_outputs",
    )
    search_service = SearchService(vector_store=doc_service.vector_store)

    sample_doc = create_mock_parsed_paper()

    # 1. Ingest document into vector store
    print("[1] Ingesting sample paper into FAISS vector store...")
    store_metrics = doc_service.store_paper(sample_doc)
    print(f"    Paper ID:           '{store_metrics['paper_id']}'")
    print(f"    Vector Chunks:      {store_metrics['chunk_count']}")

    # 2. Test Semantic Search Execution
    print("\n[2] Executing Semantic Vector Search...")
    query = "What is a Von Neumann Algebra?"
    results = search_service.semantic_search(query=query, top_k=5)
    print(f"    Query:              '{query}'")
    print(f"    Results Found:      {len(results)}")
    assert len(results) >= 1, "Expected at least 1 search hit"
    top_hit = results[0]
    print(f"    Top Match Score:    {top_hit['score']:.4f}")
    print(f"    Top Section:        '{top_hit.get('section_title', '')}'")

    # 3. Test Metadata Filtering (section_type and paper_id)
    print("\n[3] Verifying Search Metadata Filters...")
    filtered_defs = search_service.semantic_search(
        query=query,
        top_k=5,
        filters={"section_type": "definition"},
    )
    print(f"    Filter section_type='definition': Found {len(filtered_defs)} hit(s)")
    if filtered_defs:
        assert filtered_defs[0]["section_type"].lower() == "definition"

    filtered_paper = search_service.semantic_search(
        query=query,
        top_k=5,
        filters={"paper_id": "paper_functional_01"},
    )
    print(f"    Filter paper_id='paper_functional_01': Found {len(filtered_paper)} hit(s)")
    assert len(filtered_paper) >= 1

    # 4. Test Score Badge Styling Helper
    print("\n[4] Verifying Score Badge Styling...")
    bg, fg, label_high = get_score_badge_style(0.85)
    assert label_high == "High Match"
    bg, fg, label_mod = get_score_badge_style(0.55)
    assert label_mod == "Moderate Match"
    bg, fg, label_low = get_score_badge_style(0.35)
    assert label_low == "Low Match"
    print("    Score badge formatting helper verified for High, Moderate, and Low tiers")

    # 5. Test Search History Logging & Clearing
    print("\n[5] Verifying Search Query History...")
    history = search_service.get_history()
    print(f"    Search History Count: {len(history)} queries logged")
    assert len(history) >= 3, "Expected at least 3 queries in history"

    search_service.clear_history()
    cleared_history = search_service.get_history()
    print(f"    Cleared History Count: {len(cleared_history)}")
    assert len(cleared_history) == 0, "Expected history to be cleared"

    print("\n============================================================")
    print(" VERIFICATION COMPLETED SUCCESSFULLY FOR SEMANTIC SEARCH UI")
    print("============================================================\n")


if __name__ == "__main__":
    main()
