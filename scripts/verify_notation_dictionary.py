#!/usr/bin/env python3
"""Verification script for Day 6 Step 6: Notation Dictionary UI."""

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
from src.application.graph_service import GraphService
from src.ui.pages.notation import classify_notation_category, extract_all_notation_items

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def create_mock_parsed_paper() -> dict:
    """Create mock parsed document dict with notation symbols for testing dictionary verification."""
    return {
        "paper_id": "paper_quantum_004",
        "metadata": {
            "title": "Quantum Mechanics and Hilbert Spaces",
            "authors": ["P. Dirac"],
            "year": 1930,
            "source": "Oxford University Press",
            "doi": "10.1000/dirac.1930",
            "keywords": ["Quantum Mechanics", "State Vector", "Operator"],
            "ingested_at": "2024-08-05T10:00:00Z",
        },
        "sections": [
            {
                "section_id": "s1",
                "heading": "1. State Vectors and Hilbert Space",
                "level": 1,
                "page_start": 1,
                "page_end": 4,
                "text": "Definition 1.1 (State Vector |psi>). A state vector |psi> is a unit element in a complex Hilbert space H representing a quantum state.",
                "section_type": "definition",
            },
        ],
        "equations": [],
        "references": [],
        "source_file": {
            "file_name": "quantum_mechanics.pdf",
            "file_path": "uploads/quantum_mechanics.pdf",
        },
        "math_entities": {
            "definitions": [{"id": "def_1.1", "title": "Definition 1.1 (State Vector |psi>)"}],
            "theorems": [],
            "lemmas": [],
            "corollaries": [],
            "proofs": [],
        },
    }


def main() -> None:
    """Run verification for Notation Dictionary page integrations and GraphService."""
    print("\n============================================================")
    print(" DAY 6 STEP 6: NOTATION DICTIONARY VERIFICATION")
    print("============================================================\n")

    doc_service = DocumentService(
        upload_dir="uploads",
        parsed_dir="exports/parser_outputs",
    )
    graph_service = GraphService(backend_graph_service=doc_service.graph_service)

    sample_doc = create_mock_parsed_paper()

    # 1. Ingest document into Knowledge Graph
    print("[1] Ingesting sample paper into ResearchGraph...")
    store_metrics = doc_service.store_paper(sample_doc)
    print(f"    Paper ID:           '{store_metrics['paper_id']}'")
    print(f"    Graph Node Count:   {store_metrics['graph_node_count']}")

    # 2. Build Notation Graph via GraphService
    print("\n[2] Building Notation Graph via GraphService...")
    notation_graph = graph_service.build_notation_graph()
    print(f"    Symbols Extracted:  {notation_graph['symbol_count']}")
    print(f"    Concepts Extracted: {notation_graph['concept_count']}")
    print(f"    Equations Count:    {notation_graph['equation_count']}")

    # 3. Test Symbol Classification
    print("\n[3] Testing Symbol Classification Helper...")
    c_fn = classify_notation_category({"label": "f(x)", "text": "Function mapping R to R"})
    assert c_fn == "Function"
    c_set = classify_notation_category({"label": "Hilbert Space H", "text": "Set of square integrable functions"})
    assert c_set == "Set"
    c_mat = classify_notation_category({"label": "Matrix M_ij", "text": "Square matrix of operators"})
    assert c_mat == "Matrix"
    print("    Classification verified for Function, Set, and Matrix categories")

    # 4. Extract Notation Items
    print("\n[4] Extracting Notation Dictionary Items...")
    all_nodes = graph_service.node_lookup()
    items = extract_all_notation_items(notation_graph, all_nodes)
    print(f"    Total Notation Items: {len(items)}")
    assert len(items) >= 1, "Expected at least 1 notation item"

    # 5. Test Node Lookup & Relationships
    print("\n[5] Testing Notation Node Lookup & Relationships...")
    first_item = items[0]
    node_id = first_item["node_id"]
    antecedents = graph_service.get_antecedents(node_id)
    consequents = graph_service.get_consequents(node_id)
    print(f"    Item '{node_id}': Antecedents={len(antecedents)}, Consequents={len(consequents)}")

    # 6. Test Graph Metrics
    print("\n[6] Testing Graph Metrics for Notation...")
    metrics = graph_service.get_graph_metrics()
    print(f"    Total Graph Nodes:  {metrics['total_nodes']}")
    print(f"    Total Graph Edges:  {metrics['total_edges']}")

    print("\n============================================================")
    print(" VERIFICATION COMPLETED SUCCESSFULLY FOR NOTATION DICTIONARY")
    print("============================================================\n")


if __name__ == "__main__":
    main()
