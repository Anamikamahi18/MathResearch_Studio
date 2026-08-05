"""Unit test suite for Day 6 Step 3: Semantic Search UI page."""

from __future__ import annotations

import pytest
import streamlit as st

from src.application.document_service import DocumentService
from src.application.search_service import SearchService
from src.ui.pages import search
from src.ui.state import get_document_service, get_search_service, init_session_state


class TestSemanticSearchPageHelpers:
    """Test cases for helper functions in Semantic Search page."""

    def test_get_score_badge_style(self):
        bg, fg, label = search.get_score_badge_style(0.92)
        assert label == "High Match"

        bg, fg, label = search.get_score_badge_style(0.62)
        assert label == "Moderate Match"

        bg, fg, label = search.get_score_badge_style(0.32)
        assert label == "Low Match"


class TestSemanticSearchPageRendering:
    """Test cases for rendering Semantic Search page views."""

    def test_render_search_page_initial(self, tmp_path):
        init_session_state()
        doc_service = DocumentService(upload_dir=tmp_path / "uploads", parsed_dir=tmp_path / "parsed")
        search_service = SearchService(vector_store=doc_service.vector_store)
        st.session_state["doc_service"] = doc_service
        st.session_state["search_service"] = search_service

        # Should render initial page view without throwing exception
        search.render_search_page()

    def test_render_search_page_with_results(self, tmp_path):
        init_session_state()
        doc_service = DocumentService(upload_dir=tmp_path / "uploads", parsed_dir=tmp_path / "parsed")
        search_service = SearchService(vector_store=doc_service.vector_store)
        st.session_state["doc_service"] = doc_service
        st.session_state["search_service"] = search_service

        # Set mock active search result state
        st.session_state["active_search_query"] = "Hilbert Space"
        st.session_state["active_search_duration_ms"] = 42
        st.session_state["active_search_results"] = [
            {
                "chunk_id": "c1",
                "score": 0.88,
                "text": "A Hilbert space H is a complete inner product space.",
                "paper_id": "paper_hilbert_01",
                "paper_title": "Spectral Theory",
                "section_title": "1. Definitions",
                "section_type": "definition",
                "page_start": 1,
                "page_end": 2,
            }
        ]

        # Should render result cards without throwing exception
        search.render_search_page()


class TestSearchServiceStateIntegration:
    """Test cases for SearchService session state integration."""

    def test_get_search_service_initialization(self, tmp_path):
        init_session_state()
        doc_service = DocumentService(upload_dir=tmp_path / "uploads", parsed_dir=tmp_path / "parsed")
        st.session_state["doc_service"] = doc_service
        st.session_state["search_service"] = None

        search_svc = get_search_service()
        assert isinstance(search_svc, SearchService)
        assert search_svc.vector_store == doc_service.vector_store
