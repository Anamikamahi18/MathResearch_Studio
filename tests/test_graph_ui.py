"""Unit test suite for Day 6 Step 5: Research Graph UI page."""

from __future__ import annotations

import pytest
import streamlit as st

from src.application.document_service import DocumentService
from src.application.graph_service import GraphService
from src.ui.pages import graph
from src.ui.state import get_document_service, get_graph_service, init_session_state


class TestResearchGraphPageHelpers:
    """Test cases for helper functions in Research Graph page."""

    def test_render_graph_legend(self):
        # Should render legend without exception
        graph.render_graph_legend()

    def test_generate_interactive_graph_html(self):
        nodes = [
            {"node_id": "n1", "label": "Def 1.1", "node_type": "definition"},
            {"node_id": "n2", "label": "Thm 2.1", "node_type": "theorem"},
        ]
        edges = [
            {"source_id": "n1", "target_id": "n2", "relation_type": "depends_on"}
        ]

        html_code = graph.generate_interactive_graph_html(
            nodes=nodes,
            edges=edges,
            layout="Hierarchical (DAG)",
            height=400,
        )

        assert "<svg id=\"graph-svg\">" in html_code
        assert "n1" in html_code
        assert "n2" in html_code


class TestResearchGraphPageRendering:
    """Test cases for rendering Research Graph page views."""

    def test_render_graph_page_initial(self, tmp_path):
        init_session_state()
        doc_service = DocumentService(upload_dir=tmp_path / "uploads", parsed_dir=tmp_path / "parsed")
        graph_service = GraphService(backend_graph_service=doc_service.graph_service)
        st.session_state["doc_service"] = doc_service
        st.session_state["graph_service"] = graph_service

        # Should render empty graph view without throwing exception
        graph.render_graph_page()

    def test_render_graph_page_with_nodes(self, tmp_path):
        init_session_state()
        doc_service = DocumentService(upload_dir=tmp_path / "uploads", parsed_dir=tmp_path / "parsed")
        graph_service = GraphService(backend_graph_service=doc_service.graph_service)
        st.session_state["doc_service"] = doc_service
        st.session_state["graph_service"] = graph_service

        mock_paper = {
            "paper_id": "paper_test_01",
            "metadata": {"title": "Test Math Paper", "authors": ["A. Author"], "year": 2024},
            "sections": [
                {
                    "section_id": "s1",
                    "heading": "1. Intro",
                    "text": "Definition 1.1 (Metric Space). A set X with a metric d.",
                    "section_type": "definition",
                }
            ],
            "equations": [],
            "references": [],
            "source_file": {"file_name": "test.pdf", "file_path": "uploads/test.pdf"},
            "math_entities": {
                "definitions": [{"id": "d1", "title": "Definition 1.1 (Metric Space)"}],
                "theorems": [],
                "lemmas": [],
                "corollaries": [],
                "proofs": [],
            },
        }

        doc_service.store_paper(mock_paper)

        # Should render populated graph view without throwing exception
        graph.render_graph_page()


class TestGraphServiceStateIntegration:
    """Test cases for GraphService session state integration."""

    def test_get_graph_service_initialization(self, tmp_path):
        init_session_state()
        doc_service = DocumentService(upload_dir=tmp_path / "uploads", parsed_dir=tmp_path / "parsed")
        st.session_state["doc_service"] = doc_service
        st.session_state["graph_service"] = None

        graph_svc = get_graph_service()
        assert isinstance(graph_svc, GraphService)
        assert graph_svc.backend == doc_service.graph_service
