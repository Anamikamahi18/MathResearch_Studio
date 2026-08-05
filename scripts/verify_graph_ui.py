#!/usr/bin/env python3
"""Verification script for Day 6 Step 5: Research Graph UI."""

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
from src.ui.pages.graph import generate_interactive_graph_html

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def create_mock_parsed_paper() -> dict:
    """Create mock parsed document dict with statements for testing graph verification."""
    return {
        "paper_id": "paper_algebra_003",
        "metadata": {
            "title": "Homological Algebra and Category Theory",
            "authors": ["S. Mac Lane"],
            "year": 1963,
            "source": "Springer-Verlag",
            "doi": "10.1000/maclane.1963",
            "keywords": ["Category Theory", "Functor", "Natural Transformation"],
            "ingested_at": "2024-08-05T10:00:00Z",
        },
        "sections": [
            {
                "section_id": "s1",
                "heading": "1. Categories and Functors",
                "level": 1,
                "page_start": 1,
                "page_end": 5,
                "text": "Definition 1.1 (Category). A category C consists of a collection of objects and a collection of morphisms satisfying identity and associativity laws.",
                "section_type": "definition",
            },
            {
                "section_id": "s2",
                "heading": "2. Yoneda Lemma",
                "level": 1,
                "page_start": 6,
                "page_end": 10,
                "text": "Lemma 2.1 (Yoneda Lemma). Let C be a locally small category and F: C -> Set a functor. Then Nat(C(A, -), F) is isomorphic to F(A).",
                "section_type": "lemma",
            },
        ],
        "equations": [],
        "references": [],
        "source_file": {
            "file_name": "homological_algebra.pdf",
            "file_path": "uploads/homological_algebra.pdf",
        },
        "math_entities": {
            "definitions": [{"id": "def_1.1", "title": "Definition 1.1 (Category)"}],
            "theorems": [],
            "lemmas": [{"id": "lem_2.1", "title": "Lemma 2.1 (Yoneda Lemma)"}],
            "corollaries": [],
            "proofs": [],
        },
    }


def main() -> None:
    """Run verification for Research Graph page integrations and GraphService."""
    print("\n============================================================")
    print(" DAY 6 STEP 5: RESEARCH GRAPH VERIFICATION")
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
    print(f"    Graph Nodes:        {store_metrics['graph_node_count']}")
    print(f"    Graph Edges:        {store_metrics['graph_edge_count']}")


    # 2. Build Dependency Graph
    print("\n[2] Building Dependency Graph via GraphService...")
    graph = graph_service.build_dependency_graph()
    print(f"    Nodes in Graph:     {len(graph.nodes)}")
    print(f"    Edges in Graph:     {len(graph.edges)}")
    assert len(graph.nodes) >= 1, "Expected at least 1 node in graph"

    # 3. Test Node Lookup
    print("\n[3] Testing Graph Node Lookup...")
    all_nodes = graph_service.node_lookup()
    print(f"    Total Nodes Lookup: {len(all_nodes)}")
    assert len(all_nodes) >= 1

    category_nodes = graph_service.node_lookup(query="Category")
    print(f"    Query 'Category':   Found {len(category_nodes)} node(s)")

    def_nodes = graph_service.node_lookup(node_type="definition")
    print(f"    Type 'definition':  Found {len(def_nodes)} node(s)")

    # 4. Test Antecedents & Consequents
    print("\n[4] Testing Node Antecedents & Consequents...")
    first_node_id = list(graph.nodes.keys())[0]
    antecedents = graph_service.get_antecedents(first_node_id)
    consequents = graph_service.get_consequents(first_node_id)
    print(f"    Node '{first_node_id}': Antecedents={len(antecedents)}, Consequents={len(consequents)}")

    # 5. Test Graph Metrics Calculation
    print("\n[5] Testing Graph Metrics Calculation...")
    metrics = graph_service.get_graph_metrics()
    print(f"    Total Nodes Metric: {metrics['total_nodes']}")
    print(f"    Total Edges Metric: {metrics['total_edges']}")
    print(f"    Graph Density:      {metrics['density']:.4f}")
    assert metrics['total_nodes'] == len(graph.nodes)

    # 6. Test HTML Canvas Generator
    print("\n[6] Testing Interactive HTML Canvas Generator...")
    html_code = generate_interactive_graph_html(
        nodes=all_nodes,
        edges=[e.to_dict() for e in graph.edges.values()],
        layout="Hierarchical (DAG)",
    )
    assert "<svg id=\"graph-svg\">" in html_code
    print("    HTML canvas generator output verified")

    print("\n============================================================")
    print(" VERIFICATION COMPLETED SUCCESSFULLY FOR RESEARCH GRAPH UI")
    print("============================================================\n")


if __name__ == "__main__":
    main()
