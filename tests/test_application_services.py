"""Unit test suite for Day 6 Step 0: Application Service Layer."""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from src.application import (
    ChatService,
    DashboardService,
    DocumentService,
    ExportService,
    GraphService,
    SearchService,
)
from src.embeddings.models import EmbeddedChunk, ChunkMetadata
from src.embeddings.provider import MockEmbeddingProvider
from src.rag.guardrails.models import DecisionType, GuardrailStatus

from src.rag.guardrails.responses import FinalResearchResponse
from src.rag.vector_store import FAISSVectorStore


@pytest.fixture
def sample_paper_dict() -> dict:
    """Fixture providing a valid parsed paper dictionary."""
    return {
        "paper_id": "paper_test_01",
        "metadata": {
            "title": "On Banach Spaces and Spectral Radius",
            "authors": ["S. Banach"],
            "year": 1932,
            "source": "Studia Mathematica",
            "doi": "10.1000/sm.1932.01",
            "keywords": ["Banach space", "Spectral radius"],
            "ingested_at": "2024-08-05T10:00:00Z",
        },
        "sections": [
            {
                "section_id": "s1",
                "heading": "1. Definitions",
                "level": 1,
                "page_start": 1,
                "page_end": 1,
                "text": "Definition 1 (Banach Space). A Banach space is a complete normed vector space.",
                "section_type": "definition",
            },
            {
                "section_id": "s2",
                "heading": "2. Main Theorem",
                "level": 1,
                "page_start": 2,
                "page_end": 3,
                "text": "Theorem 2 (Spectral Radius Formula). The spectral radius r(T) equals lim ||T^n||^(1/n).",
                "section_type": "theorem",
            },
        ],
        "equations": [],
        "references": [],
        "math_entities": {
            "definitions": [{"id": "def_1", "title": "Definition 1 (Banach Space)"}],
            "theorems": [{"id": "thm_2", "title": "Theorem 2 (Spectral Radius Formula)"}],
            "lemmas": [],
            "corollaries": [],
            "proofs": [],
        },
    }


class TestDocumentService:
    """Test cases for DocumentService."""

    def test_upload_and_store_paper(self, tmp_path: Path, sample_paper_dict: dict):
        upload_dir = tmp_path / "uploads"
        parsed_dir = tmp_path / "parsed"
        doc_service = DocumentService(
            upload_dir=upload_dir,
            parsed_dir=parsed_dir,
            embedding_provider=MockEmbeddingProvider(),
        )

        # Upload file
        sample_file = tmp_path / "sample.pdf"
        sample_file.write_bytes(b"%PDF-1.4 test pdf content")

        uploaded_path = doc_service.upload_paper(sample_file)
        assert uploaded_path.exists()
        assert uploaded_path.name == "sample.pdf"

        # Store paper
        store_res = doc_service.store_paper(sample_paper_dict)
        assert store_res["paper_id"] == "paper_test_01"
        assert store_res["chunk_count"] >= 0

        # List papers
        papers = doc_service.list_papers()
        assert len(papers) == 1
        assert papers[0]["paper_id"] == "paper_test_01"

        # Get paper
        retrieved = doc_service.get_paper("paper_test_01")
        assert retrieved is not None
        assert retrieved["title"] == "On Banach Spaces and Spectral Radius"

    def test_refresh_library(self, tmp_path: Path, sample_paper_dict: dict):
        parsed_dir = tmp_path / "parsed"
        parsed_dir.mkdir(parents=True, exist_ok=True)
        json_file = parsed_dir / "paper_test_01.json"
        json_file.write_text(json.dumps(sample_paper_dict), encoding="utf-8")

        doc_service = DocumentService(
            parsed_dir=parsed_dir,
            embedding_provider=MockEmbeddingProvider(),
        )

        library = doc_service.refresh_library()
        assert len(library) >= 1
        assert doc_service.get_paper("paper_test_01") is not None


class TestSearchService:
    """Test cases for SearchService."""

    def test_search_and_filters(self, sample_paper_dict: dict):
        vector_store = FAISSVectorStore(dimension=384)

        # Add mock chunk
        chunk = EmbeddedChunk(
            chunk_id="chk_1",
            text="Definition 1 (Banach Space). A Banach space is a complete normed vector space.",
            embedding=[0.1] * 384,
            metadata=ChunkMetadata(
                paper_id="paper_test_01",
                paper_title="On Banach Spaces",
                section_id="s1",
                section_type="definition",
                authors=["S. Banach"],
            ),
        )
        vector_store.add_chunks([chunk])

        search_service = SearchService(vector_store=vector_store)

        # Search without filter
        results = search_service.semantic_search("What is Banach Space?", top_k=3)
        assert len(results) == 1
        assert results[0]["paper_id"] == "paper_test_01"

        # Search with paper_id filter
        filtered_res = search_service.semantic_search(
            "Banach", top_k=3, filters={"paper_id": "paper_test_01"}
        )
        assert len(filtered_res) == 1

        # Search with mismatching filter
        mismatch_res = search_service.semantic_search(
            "Banach", top_k=3, filters={"paper_id": "non_existent_paper"}
        )
        assert len(mismatch_res) == 0

        # Query history
        history = search_service.get_history()
        assert len(history) == 3

        search_service.clear_history()
        assert len(search_service.get_history()) == 0


class TestChatService:
    """Test cases for ChatService."""

    def test_receive_question(self):
        chat_service = ChatService()

        # Submit question through RAG pipeline
        response = chat_service.receive_question("What is a Banach Space?")
        assert isinstance(response, FinalResearchResponse)
        assert response.question == "What is a Banach Space?"
        assert response.decision in list(DecisionType)
        assert response.status in list(GuardrailStatus)

        # Verify chat history
        history = chat_service.get_chat_history()
        assert len(history) == 1
        assert history[0]["question"] == "What is a Banach Space?"

        chat_service.clear_chat_history()
        assert len(chat_service.get_chat_history()) == 0


class TestGraphService:
    """Test cases for GraphService application wrapper."""

    def test_build_graphs_and_lookup(self, sample_paper_dict: dict):
        graph_service = GraphService()

        # Build dependency graph
        dep_graph = graph_service.build_dependency_graph([sample_paper_dict])
        assert len(dep_graph.nodes) > 0

        # Build notation graph
        notation_summary = graph_service.build_notation_graph([sample_paper_dict])
        assert "symbol_count" in notation_summary
        assert "concept_count" in notation_summary
        assert "equation_count" in notation_summary

        # Node lookup by query
        matched_nodes = graph_service.node_lookup(query="Banach")
        assert len(matched_nodes) >= 1

        # Metrics
        metrics = graph_service.get_graph_metrics()
        assert metrics["total_nodes"] > 0
        assert "node_type_breakdown" in metrics


class TestExportService:
    """Test cases for ExportService."""

    def test_export_formats(self, tmp_path: Path, sample_paper_dict: dict):
        export_service = ExportService(export_dir=tmp_path)

        # JSON Export
        json_path = export_service.export_to_json(sample_paper_dict, tmp_path / "out.json")
        assert json_path.exists()
        assert json_path.stat().st_size > 0

        # Markdown Export
        md_path = export_service.export_to_markdown({"summaries": [sample_paper_dict]}, tmp_path / "out.md")
        assert md_path.exists()
        assert md_path.stat().st_size > 0

        # CSV Export
        csv_path = export_service.export_to_csv([{"paper_id": "p1", "title": "t1"}], tmp_path / "out.csv")
        assert csv_path.exists()
        assert csv_path.stat().st_size > 0

        # Research Notes Export
        notes_path = export_service.export_research_notes(
            data={"question": "What is Banach Space?", "answer_text": "A complete normed space."},
            format="markdown",
            output_path=tmp_path / "notes.md",
        )
        assert notes_path.exists()


class TestDashboardService:
    """Test cases for DashboardService."""

    def test_get_statistics(self, tmp_path: Path, sample_paper_dict: dict):
        doc_service = DocumentService(
            upload_dir=tmp_path / "uploads",
            parsed_dir=tmp_path / "parsed",
            embedding_provider=MockEmbeddingProvider(),
        )

        graph_service = GraphService()
        vector_store = FAISSVectorStore()

        doc_service.store_paper(sample_paper_dict)
        graph_service.build_dependency_graph([sample_paper_dict])

        dashboard = DashboardService(
            document_service=doc_service,
            graph_service=graph_service,
            vector_store=vector_store,
        )

        stats = dashboard.get_statistics()
        assert stats["paper_count"] == 1
        assert stats["definition_count"] >= 1
        assert stats["theorem_count"] >= 1
        assert "graph_nodes" in stats
