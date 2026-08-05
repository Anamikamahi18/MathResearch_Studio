#!/usr/bin/env python3
"""Verification script for Day 6 Step 0: Application Service Layer."""

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

from src.application.chat_service import ChatService
from src.application.dashboard_service import DashboardService
from src.application.document_service import DocumentService
from src.application.export_service import ExportService
from src.application.graph_service import GraphService
from src.application.search_service import SearchService

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def create_sample_paper_document() -> dict:
    """Create a sample mathematical paper schema document for verification."""
    return {
        "paper_id": "paper_hilbert_01",
        "metadata": {
            "title": "Spectral Theory of Hilbert Space Operators",
            "authors": ["A. Hilbert", "B. Banach"],
            "year": 2024,
            "source": "Journal of Functional Analysis",
            "doi": "10.1000/jfa.2024.01",
            "keywords": ["Hilbert space", "Spectral theory", "Compact operators"],
            "ingested_at": "2024-08-05T10:00:00Z",
        },
        "sections": [
            {
                "section_id": "s1",
                "heading": "1. Introduction and Basic Definitions",
                "level": 1,
                "page_start": 1,
                "page_end": 2,
                "text": "Definition 1.1 (Hilbert Space). A Hilbert space H is a complete inner product space over the complex field C. An operator T on H is compact if the image of the unit ball is relatively compact in H.",
                "section_type": "definition",
            },
            {
                "section_id": "s2",
                "heading": "2. Main Spectral Theorem",
                "level": 1,
                "page_start": 3,
                "page_end": 5,
                "text": "Theorem 2.1 (Spectral Decomposition Theorem). Let T be a self-adjoint compact operator on a Hilbert space H. Then there exists an orthonormal basis of H consisting of eigenvectors of T. Lemma 2.2 (Bounded Eigenvalues). All eigenvalues of T are real and bounded.",
                "section_type": "theorem",
            },
            {
                "section_id": "s3",
                "heading": "3. Proof of Theorem 2.1",
                "level": 1,
                "page_start": 6,
                "page_end": 8,
                "text": "Proof of Theorem 2.1. By Lemma 2.2, we construct an orthonormal sequence of eigenvectors using Gram-Schmidt orthogonalization.",
                "section_type": "proof",
            },
        ],
        "equations": [
            {
                "equation_id": "eq1",
                "latex": "T e_k = \\lambda_k e_k",
                "section_id": "s2",
                "page": 4,
            }
        ],
        "references": [
            {
                "reference_id": "ref1",
                "raw_text": "F. Riesz, Spectral Theory of Compact Operators, 1955.",
            }
        ],
        "math_entities": {
            "definitions": [
                {
                    "id": "def_1.1",
                    "title": "Definition 1.1 (Hilbert Space)",
                    "type": "definition",
                }
            ],
            "theorems": [
                {
                    "id": "thm_2.1",
                    "title": "Theorem 2.1 (Spectral Decomposition Theorem)",
                    "type": "theorem",
                }
            ],
            "lemmas": [
                {
                    "id": "lem_2.2",
                    "title": "Lemma 2.2 (Bounded Eigenvalues)",
                    "type": "lemma",
                }
            ],
            "corollaries": [],
            "proofs": [
                {
                    "id": "prf_2.1",
                    "title": "Proof of Theorem 2.1",
                    "type": "proof",
                }
            ],
        },
    }


def main() -> None:
    """Run verification for all 6 Application Services."""
    print("\n============================================================")
    print(" DAY 6 STEP 0: APPLICATION SERVICE LAYER VERIFICATION")
    print("============================================================\n")

    # 1. Initialize Shared Vector Store and Graph Service
    doc_service = DocumentService(
        upload_dir="uploads",
        parsed_dir="exports/parser_outputs",
    )
    graph_service = GraphService()
    search_service = SearchService(vector_store=doc_service.vector_store)
    chat_service = ChatService(
        vector_store=doc_service.vector_store,
        graph_service=graph_service.backend,
    )
    export_service = ExportService(export_dir="exports/application_service_exports")
    dashboard_service = DashboardService(
        document_service=doc_service,
        graph_service=graph_service,
        vector_store=doc_service.vector_store,
    )

    sample_doc = create_sample_paper_document()

    # -------------------------------------------------------------
    # Test 1: DocumentService
    # -------------------------------------------------------------
    print("[1] Testing DocumentService...")
    store_result = doc_service.store_paper(sample_doc)
    print(f"    Paper Stored:          {store_result['paper_id']} ('{store_result['title']}')")
    print(f"    Vector Chunks Indexed: {store_result['chunk_count']}")
    papers = doc_service.list_papers()
    print(f"    Library Paper Count:   {len(papers)}")

    # -------------------------------------------------------------
    # Test 2: SearchService
    # -------------------------------------------------------------
    print("\n[2] Testing SearchService...")
    search_results = search_service.semantic_search(
        query="What is a Hilbert Space definition?",
        top_k=3,
        filters={"paper_id": "paper_hilbert_01"},
    )
    print(f"    Search Query:          'What is a Hilbert Space definition?'")
    print(f"    Results Found:         {len(search_results)}")
    if search_results:
        print(f"    Top Match Score:       {search_results[0].get('score', 0.0):.4f}")
        print(f"    Top Chunk Text:        \"{search_results[0].get('text', '')[:80]}...\"")
    history = search_service.get_history()
    print(f"    Query History Count:   {len(history)}")

    # -------------------------------------------------------------
    # Test 3: GraphService
    # -------------------------------------------------------------
    print("\n[3] Testing GraphService...")
    dep_graph = graph_service.build_dependency_graph([sample_doc])
    print(f"    Dependency Graph:      {len(dep_graph.nodes)} nodes, {len(dep_graph.edges)} edges")

    notation_graph = graph_service.build_notation_graph([sample_doc])
    print(f"    Notation Graph:        {notation_graph['symbol_count']} symbols, {notation_graph['concept_count']} concepts, {notation_graph['equation_count']} equations")

    lookup_nodes = graph_service.node_lookup(query="Spectral")
    print(f"    Node Lookup ('Spectral'): Found {len(lookup_nodes)} node(s)")

    metrics = graph_service.get_graph_metrics()
    print(f"    Graph Density:         {metrics['density']:.4f}")

    # -------------------------------------------------------------
    # Test 4: ChatService (Complete RAG Pipeline)
    # -------------------------------------------------------------
    print("\n[4] Testing ChatService (RAG Pipeline)...")
    question = "State Theorem 2.1 regarding Spectral Decomposition."
    final_response = chat_service.receive_question(question, top_k=3)
    print(f"    Question:              '{question}'")
    print(f"    Decision Policy:       {final_response.decision.value} (Status: {final_response.status.value})")
    print(f"    Answer Output Text:    \"{final_response.answer_text[:120]}...\"")
    print(f"    Citations Generated:   {len(final_response.citations)}")
    print(f"    Grounding Score:       {final_response.grounding_summary.get('grounding_score', 0.0):.4f}")
    chat_history = chat_service.get_chat_history()
    print(f"    Chat History Count:    {len(chat_history)}")

    # -------------------------------------------------------------
    # Test 5: ExportService
    # -------------------------------------------------------------
    print("\n[5] Testing ExportService...")
    notes_path = export_service.export_research_notes(
        data=final_response,
        format="markdown",
        output_path="exports/application_service_exports/research_notes.md",
    )
    print(f"    Exported Notes (MD):   {notes_path}")

    summaries_json = export_service.export_summaries(
        documents_or_results=papers,
        format="json",
        output_path="exports/application_service_exports/paper_summaries.json",
    )
    print(f"    Exported Summaries (JSON): {summaries_json}")

    csv_path = export_service.export_to_csv(
        data=[{"paper_id": p["paper_id"], "title": p["title"], "chunk_count": p["chunk_count"]} for p in papers],
        output_path="exports/application_service_exports/paper_catalog.csv",
    )
    print(f"    Exported Catalog (CSV): {csv_path}")

    # -------------------------------------------------------------
    # Test 6: DashboardService
    # -------------------------------------------------------------
    print("\n[6] Testing DashboardService...")
    stats = dashboard_service.get_statistics()
    print(f"    Total Papers:          {stats['paper_count']}")
    print(f"    Total Definitions:     {stats['definition_count']}")
    print(f"    Total Theorems:        {stats['theorem_count']}")
    print(f"    Total Lemmas:          {stats['lemma_count']}")
    print(f"    Vector Store Chunks:   {stats['total_vector_chunks']}")
    print(f"    Knowledge Graph Nodes: {stats['graph_nodes']}")

    print("\n============================================================")
    print(" VERIFICATION COMPLETED SUCCESSFULLY FOR ALL 6 SERVICES")
    print("============================================================\n")


if __name__ == "__main__":
    main()
