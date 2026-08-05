#!/usr/bin/env python3
"""Verification script for Day 6 Step 7: Statistics Dashboard UI."""

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

from src.application.dashboard_service import DashboardService
from src.application.document_service import DocumentService
from src.application.graph_service import GraphService

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def create_mock_parsed_paper() -> dict:
    """Create mock parsed document dict for testing dashboard statistics verification."""
    return {
        "paper_id": "paper_stats_005",
        "metadata": {
            "title": "Differential Geometry and Riemannian Manifolds",
            "authors": ["B. Riemann"],
            "year": 1854,
            "source": "Göttingen Abhandlungen",
            "doi": "10.1000/riemann.1854",
            "keywords": ["Riemannian Metric", "Curvature", "Manifold"],
            "ingested_at": "2024-08-05T10:00:00Z",
        },
        "sections": [
            {
                "section_id": "s1",
                "heading": "1. Riemannian Manifolds",
                "level": 1,
                "page_start": 1,
                "page_end": 8,
                "text": "Definition 1.1 (Riemannian Metric). A Riemannian metric g on a smooth manifold M is a smooth inner product tensor.",
                "section_type": "definition",
            },
            {
                "section_id": "s2",
                "heading": "2. Gauss-Bonnet Theorem",
                "level": 1,
                "page_start": 9,
                "page_end": 15,
                "text": "Theorem 2.1 (Gauss-Bonnet Theorem). For a compact 2D Riemannian manifold M, the integral of Gaussian curvature equals 2*pi*chi(M).",
                "section_type": "theorem",
            },
        ],
        "equations": [],
        "references": [],
        "source_file": {
            "file_name": "riemannian_geometry.pdf",
            "file_path": "uploads/riemannian_geometry.pdf",
        },
        "math_entities": {
            "definitions": [{"id": "def_1.1", "title": "Definition 1.1 (Riemannian Metric)"}],
            "theorems": [{"id": "thm_2.1", "title": "Theorem 2.1 (Gauss-Bonnet Theorem)"}],
            "lemmas": [],
            "corollaries": [],
            "proofs": [],
        },
    }


def main() -> None:
    """Run verification for Statistics Dashboard page integrations and DashboardService."""
    print("\n============================================================")
    print(" DAY 6 STEP 7: STATISTICS DASHBOARD VERIFICATION")
    print("============================================================\n")

    doc_service = DocumentService(
        upload_dir="uploads",
        parsed_dir="exports/parser_outputs",
    )
    graph_service = GraphService(backend_graph_service=doc_service.graph_service)
    dash_service = DashboardService(
        document_service=doc_service,
        graph_service=graph_service,
        vector_store=doc_service.vector_store,
    )

    sample_doc = create_mock_parsed_paper()

    # 1. Ingest document into library and Knowledge Graph
    print("[1] Ingesting sample paper into system catalog...")
    store_metrics = doc_service.store_paper(sample_doc)
    print(f"    Paper ID:           '{store_metrics['paper_id']}'")
    print(f"    Chunks Indexed:     {store_metrics['chunk_count']}")

    # 2. Test Dashboard Statistics Aggregation
    print("\n[2] Testing DashboardService.get_statistics()...")
    stats = dash_service.get_statistics()
    print(f"    Papers Count:       {stats['paper_count']}")
    print(f"    Definitions Count:  {stats['definition_count']}")
    print(f"    Theorems Count:     {stats['theorem_count']}")
    print(f"    Lemmas Count:       {stats['lemma_count']}")
    print(f"    Vector Chunks:      {stats['total_vector_chunks']}")
    print(f"    Graph Nodes:        {stats['graph_nodes']}")
    print(f"    Graph Edges:        {stats['graph_edges']}")
    print(f"    Graph Density:      {stats['graph_density']:.4f}")

    assert stats["paper_count"] >= 1, "Expected at least 1 paper in catalog"
    assert stats["total_vector_chunks"] >= 1, "Expected at least 1 vector chunk"

    # 3. Test Statement Entity Retrievals
    print("\n[3] Testing Entity Retrieval Helpers...")
    defs = dash_service.get_definitions()
    thms = dash_service.get_theorems()
    lemmas = dash_service.get_lemmas()
    print(f"    Retrieved Defs:     {len(defs)}")
    print(f"    Retrieved Thms:     {len(thms)}")
    print(f"    Retrieved Lemmas:   {len(lemmas)}")

    # 4. Test Graph Metrics Integration
    print("\n[4] Testing Graph Metrics Integration...")
    g_metrics = dash_service.get_graph_metrics()
    print(f"    Graph Total Nodes:  {g_metrics['total_nodes']}")
    print(f"    Graph Total Edges:  {g_metrics['total_edges']}")
    assert g_metrics["total_nodes"] == stats["graph_nodes"]

    print("\n============================================================")
    print(" VERIFICATION COMPLETED SUCCESSFULLY FOR STATISTICS DASHBOARD")
    print("============================================================\n")


if __name__ == "__main__":
    main()
