"""Unit test suite for Day 6 Step 7: Statistics Dashboard UI page."""

from __future__ import annotations

import pytest
import streamlit as st

from src.application.dashboard_service import DashboardService
from src.application.document_service import DocumentService
from src.application.graph_service import GraphService
from src.ui.pages import statistics
from src.ui.state import get_dashboard_service, init_session_state


class TestStatisticsDashboardPageRendering:
    """Test cases for rendering Statistics Dashboard page views."""

    def test_render_statistics_page_empty(self, tmp_path):
        init_session_state()
        doc_service = DocumentService(upload_dir=tmp_path / "uploads", parsed_dir=tmp_path / "parsed")
        graph_service = GraphService(backend_graph_service=doc_service.graph_service)
        dash_service = DashboardService(
            document_service=doc_service,
            graph_service=graph_service,
            vector_store=doc_service.vector_store,
        )

        st.session_state["doc_service"] = doc_service
        st.session_state["graph_service"] = graph_service
        st.session_state["dashboard_service"] = dash_service

        # Should render empty dashboard state without throwing exception
        statistics.render_statistics_page()

    def test_render_statistics_page_populated(self, tmp_path):
        init_session_state()
        doc_service = DocumentService(upload_dir=tmp_path / "uploads", parsed_dir=tmp_path / "parsed")
        graph_service = GraphService(backend_graph_service=doc_service.graph_service)
        dash_service = DashboardService(
            document_service=doc_service,
            graph_service=graph_service,
            vector_store=doc_service.vector_store,
        )

        st.session_state["doc_service"] = doc_service
        st.session_state["graph_service"] = graph_service
        st.session_state["dashboard_service"] = dash_service

        mock_paper = {
            "paper_id": "paper_stats_test_01",
            "metadata": {"title": "Topology and Analysis", "authors": ["C. Gauss"], "year": 1827},
            "sections": [
                {
                    "section_id": "s1",
                    "heading": "1. Curvature",
                    "page_start": 1,
                    "page_end": 5,
                    "text": "Definition 1.1 (Gaussian Curvature). The product of principal curvatures.",
                    "section_type": "definition",
                }
            ],
            "equations": [],
            "references": [],
            "source_file": {"file_name": "gauss.pdf", "file_path": "uploads/gauss.pdf"},
            "math_entities": {
                "definitions": [{"id": "d1", "title": "Definition 1.1 (Gaussian Curvature)"}],
                "theorems": [],
                "lemmas": [],
                "corollaries": [],
                "proofs": [],
            },
        }

        doc_service.store_paper(mock_paper)

        # Should render populated dashboard metrics & charts without throwing exception
        statistics.render_statistics_page()


class TestDashboardServiceStateIntegration:
    """Test cases for DashboardService session state integration."""

    def test_get_dashboard_service_initialization(self, tmp_path):
        init_session_state()
        doc_service = DocumentService(upload_dir=tmp_path / "uploads", parsed_dir=tmp_path / "parsed")
        graph_service = GraphService(backend_graph_service=doc_service.graph_service)

        st.session_state["doc_service"] = doc_service
        st.session_state["graph_service"] = graph_service
        st.session_state["dashboard_service"] = None

        dash_svc = get_dashboard_service()
        assert isinstance(dash_svc, DashboardService)
        assert dash_svc.document_service == doc_service
        assert dash_svc.graph_service == graph_service
