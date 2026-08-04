#!/usr/bin/env python3
"""Verification script for Day 5 Step 2.5: Retrieval Explainability & Statistics."""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Ensure UTF-8 output encoding on Windows stdout/stderr
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from config.retrieval_config import RetrievalConfig
from src.embeddings.models import ChunkMetadata, EmbeddedChunk
from src.embeddings.provider import SentenceTransformerEmbeddingProvider
from src.graph.models import GraphEdge, GraphNode, NodeType, RelationType, ResearchGraph
from src.graph.service import GraphService
from src.rag.query_processing import QueryProcessor
from src.rag.retrieval import HybridRetriever, RetrievalEngine
from src.rag.vector_store import FAISSVectorStore

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


def populate_demo_knowledge_base() -> tuple[SentenceTransformerEmbeddingProvider, FAISSVectorStore, GraphService]:
    """Create a populated embedding provider, FAISS store, and ResearchGraph for verification."""
    provider = SentenceTransformerEmbeddingProvider(model_name="all-MiniLM-L6-v2")
    vector_store = FAISSVectorStore(dimension=384)
    graph_service = GraphService()

    # Sample mathematical research paper chunks
    sample_chunks_data = [
        {
            "chunk_id": "paper1_def_2.1",
            "text": "Definition 2.1 (Compact Operator). An operator T on a Hilbert space H is compact if the image of any bounded subset under T is relatively compact.",
            "paper_id": "paper1",
            "paper_title": "Spectral Theory of Hilbert Space Operators",
            "section_id": "sec2",
            "section_title": "2. Basic Definitions",
            "section_type": "definition",
            "page_start": 2,
            "page_end": 2,
        },
        {
            "chunk_id": "paper1_thm_3",
            "text": "Theorem 3 (Spectral Theorem for Compact Operators). Let T be a compact self-adjoint operator on H. Then there exists an orthonormal basis of eigenvectors for H.",
            "paper_id": "paper1",
            "paper_title": "Spectral Theory of Hilbert Space Operators",
            "section_id": "sec3",
            "section_title": "3. Main Theorems",
            "section_type": "theorem",
            "page_start": 5,
            "page_end": 6,
        },
        {
            "chunk_id": "paper1_lem_3.1",
            "text": "Lemma 3 (Eigenvalue Approximation). Every compact operator T can be approximated in norm by finite rank operators, proving Theorem 3.",
            "paper_id": "paper1",
            "paper_title": "Spectral Theory of Hilbert Space Operators",
            "section_id": "sec3",
            "section_title": "3. Main Theorems",
            "section_type": "lemma",
            "page_start": 4,
            "page_end": 5,
        },
        {
            "chunk_id": "paper1_thm_2",
            "text": "Theorem 2 (Bounded Inverse Theorem). If a bounded linear operator T between Banach spaces is bijective, then its inverse T^{-1} is bounded.",
            "paper_id": "paper1",
            "paper_title": "Spectral Theory of Hilbert Space Operators",
            "section_id": "sec2",
            "section_title": "2. Basic Definitions",
            "section_type": "theorem",
            "page_start": 3,
            "page_end": 4,
        },
        {
            "chunk_id": "paper1_thm_4",
            "text": "Theorem 4 (Fredholm Alternative). For any compact operator T and non-zero scalar lambda, T - lambda I is invertible or has non-trivial kernel.",
            "paper_id": "paper1",
            "paper_title": "Spectral Theory of Hilbert Space Operators",
            "section_id": "sec3",
            "section_title": "3. Main Theorems",
            "section_type": "theorem",
            "page_start": 7,
            "page_end": 8,
        },
        {
            "chunk_id": "paper1_prf_thm_4",
            "text": "Proof of Theorem 4. We apply the finite dimension argument to the kernel of T - lambda I and compute the index of the operator.",
            "paper_id": "paper1",
            "paper_title": "Spectral Theory of Hilbert Space Operators",
            "section_id": "sec3",
            "section_title": "3. Main Theorems",
            "section_type": "proof",
            "page_start": 8,
            "page_end": 9,
        },
        {
            "chunk_id": "paper1_sec_notation",
            "text": "Notation: We denote by λ the spectral parameter, σ(T) the spectrum of T, ∇ the gradient operator, and ℝ the real continuum.",
            "paper_id": "paper1",
            "paper_title": "Spectral Theory of Hilbert Space Operators",
            "section_id": "sec1",
            "section_title": "1. Introduction & Notation",
            "section_type": "other",
            "page_start": 1,
            "page_end": 1,
        },
        {
            "chunk_id": "paper1_abstract",
            "text": "Abstract & Summary. This paper provides a comprehensive summary of compact operator theory on Hilbert spaces, establishing spectral decompositions and Fredholm properties.",
            "paper_id": "paper1",
            "paper_title": "Spectral Theory of Hilbert Space Operators",
            "section_id": "sec0",
            "section_title": "Abstract",
            "section_type": "summary",
            "page_start": 1,
            "page_end": 1,
        },
    ]

    # Generate embeddings and add to vector store
    embedded_chunks: list[EmbeddedChunk] = []
    for item in sample_chunks_data:
        vector = provider.embed_text(item["text"])
        meta = ChunkMetadata(
            paper_id=item["paper_id"],
            paper_title=item["paper_title"],
            authors=["A. Mathematician"],
            section_id=item["section_id"],
            section_title=item["section_title"],
            section_type=item["section_type"],
            page_start=item["page_start"],
            page_end=item["page_end"],
            entity_type=item["section_type"],
        )
        embedded_chunks.append(
            EmbeddedChunk(
                chunk_id=item["chunk_id"],
                text=item["text"],
                embedding=vector,
                metadata=meta,
            )
        )

    vector_store.add_chunks(embedded_chunks)

    # Populate Day 4 Research Graph
    graph = ResearchGraph()
    for item in sample_chunks_data:
        node = GraphNode(
            node_id=item["chunk_id"],
            node_type=item["section_type"],
            label=item["section_title"],
            text=item["text"],
            paper_id=item["paper_id"],
            section_id=item["section_id"],
        )
        graph.add_node(node)

    # Add dependency edge: Lemma 3.1 proves Theorem 3
    graph.add_edge(
        GraphEdge(
            edge_id="e_lem_thm",
            source_id="paper1_lem_3.1",
            target_id="paper1_thm_3",
            relation_type=RelationType.PROVES,
        )
    )
    graph_service.graph = graph

    return provider, vector_store, graph_service


def run_verification() -> None:
    """Run verification suite for RetrievalEngine with explainability and statistics."""
    provider, vector_store, graph_service = populate_demo_knowledge_base()

    config = RetrievalConfig(
        semantic_weight=0.45,
        entity_weight=0.20,
        intent_weight=0.15,
        graph_weight=0.10,
        boost_weight=0.10,
        top_k=5,
    )
    hybrid_retriever = HybridRetriever(
        provider=provider,
        vector_store=vector_store,
        graph_service=graph_service,
        weights=config,
    )
    query_processor = QueryProcessor()
    engine = RetrievalEngine(retriever=hybrid_retriever, query_processor=query_processor)

    test_queries = [
        "What is Definition 2.1?",
        "Which lemma proves theorem 3?",
        "Summarize the paper.",
        "Compare theorem 2 and theorem 4.",
        "Show notation for λ.",
    ]

    for q_str in test_queries:
        print("=" * 60)
        print("Query")
        print(q_str)
        print("=" * 60)

        response = engine.retrieve_with_response(query=q_str, top_k=5)

        for res in response.results:
            exp = res.explanation
            reason_lines = exp.ranking_reason.split(" | ") if exp and exp.ranking_reason else ["Standard relevance match"]

            print(f"Rank {res.rank}")
            print(f"Chunk\n{res.chunk_id}")
            print(f"Paper\n{res.paper_title or res.paper_id or 'paper1'}")
            print(f"Section\n{res.section_title or res.section_type}")
            print(f"Final Score\n{res.final_score:.4f}")
            print("Reason")
            for r in reason_lines:
                print(r)

            if exp:
                print(f"Semantic\n{exp.semantic_score:.4f}")
                print(f"Entity\n{exp.entity_score:.4f}")
                print(f"Intent\n{exp.intent_score:.4f}")
                print(f"Graph\n{exp.graph_score:.4f}")
                print(f"Boost\n{exp.boost_score:.4f}")
                if exp.matched_entities:
                    print(f"Matched Entities\n{', '.join(exp.matched_entities)}")
                if exp.graph_neighbors:
                    print(f"Graph Neighbors\n{', '.join(exp.graph_neighbors)}")
            print("-" * 60)

        stats = response.statistics
        print("\nRetrieval Statistics:")
        print(f"  Candidates Evaluated: {stats.number_of_candidates}")
        print(f"  Average Semantic Score: {stats.average_semantic_score:.4f}")
        print(f"  Average Final Score:    {stats.average_final_score:.4f}")
        print(f"  Highest Final Score:    {stats.highest_score:.4f}")
        print(f"  Lowest Final Score:     {stats.lowest_score:.4f}")
        print(f"  Entity Match Rate:      {stats.entity_match_rate * 100:.1f}%")
        print(f"  Graph Match Rate:       {stats.graph_match_rate * 100:.1f}%")
        print(f"  Intent Match Rate:      {stats.intent_match_rate * 100:.1f}%")
        print(f"  Top Entity Types:       {', '.join(stats.top_entity_types)}")
        print(f"  Latency:                {stats.retrieval_time_ms:.2f} ms")
        print("\n")


if __name__ == "__main__":
    run_verification()
