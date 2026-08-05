"""Unit test suite for Day 6 Step 1: Streamlit UI Application Shell."""

from __future__ import annotations

import pytest
import streamlit as st

from src.application.document_service import DocumentService
from src.embeddings.provider import MockEmbeddingProvider
from src.ui import pages
from src.ui.config import AppConfig, DEFAULT_APP_CONFIG
from src.ui.components import (
    render_empty_state,
    render_error_banner,
    render_footer,
    render_header,
    render_loading_spinner,
    render_page_title,
)
from src.ui.router import PageRouter
from src.ui.state import get_current_page, init_session_state, set_current_page
from src.ui.theme import get_custom_css


@pytest.fixture(autouse=True)
def setup_mock_services(tmp_path):
    """Fixture initializing session state with MockEmbeddingProvider for UI shell testing."""
    init_session_state()
    doc_svc = DocumentService(
        upload_dir=tmp_path / "uploads",
        parsed_dir=tmp_path / "parsed",
        embedding_provider=MockEmbeddingProvider(),
    )
    st.session_state["doc_service"] = doc_svc



class TestUIConfig:
    """Test cases for UI AppConfig settings."""

    def test_default_config_properties(self):
        cfg = DEFAULT_APP_CONFIG
        assert cfg.title == "MathResearch Studio"
        assert cfg.version == "v1.0.0"
        assert cfg.default_page == "home"
        assert len(cfg.pages) == 10

    def test_get_page_info(self):
        cfg = DEFAULT_APP_CONFIG
        info = cfg.get_page_info("search")
        assert info["label"] == "Math Search"
        assert info["icon"] == "🔍"

        unknown_info = cfg.get_page_info("unknown_page")
        assert unknown_info["label"] == "Unknown_Page"


class TestUIState:
    """Test cases for session state management."""

    def test_init_session_state(self):
        init_session_state()
        assert st.session_state.get("current_page") == "home"
        assert st.session_state.get("theme_mode") == "dark"
        assert st.session_state.get("sidebar_expanded") is True

    def test_get_and_set_current_page(self):
        init_session_state()
        assert get_current_page() == "home"

        set_current_page("assistant")
        assert get_current_page() == "assistant"

        # Setting invalid page should not update route
        set_current_page("non_existent")
        assert get_current_page() == "assistant"


class TestPageRouter:
    """Test cases for PageRouter."""

    def test_router_mappings(self):
        router = PageRouter()
        expected_routes = [
            "home",
            "upload",
            "library",
            "search",
            "assistant",
            "graph",
            "notation",
            "statistics",
            "export",
            "settings",
        ]

        for route in expected_routes:
            assert route in router._routes
            assert callable(router._routes[route])

    def test_render_current_page(self):
        init_session_state()
        set_current_page("home")
        router = PageRouter()
        # Should execute without throwing exception
        router.render_current_page()


class TestUITheme:
    """Test cases for theme CSS generation."""

    def test_get_custom_css(self):
        css = get_custom_css()
        assert "mrs-card" in css
        assert "mrs-badge" in css
        assert "mrs-branding" in css


class TestPagesAndComponents:
    """Test cases verifying placeholder page rendering and reusable components."""

    @pytest.mark.parametrize(
        "render_fn",
        [
            pages.render_home_page,
            pages.render_upload_page,
            pages.render_library_page,
            pages.render_search_page,
            pages.render_assistant_page,
            pages.render_graph_page,
            pages.render_notation_page,
            pages.render_statistics_page,
            pages.render_export_page,
            pages.render_settings_page,
        ],
    )
    def test_placeholder_pages_render(self, render_fn):
        init_session_state()
        # Should render without throwing exception
        render_fn()


    def test_components_render(self):
        render_page_title(title="Test Title", subtitle="Test Subtitle", icon="🧪", badge="Test")
        render_header("home")
        render_footer()
        render_empty_state(title="Empty", message="No item")
        render_loading_spinner("Loading...")
        render_error_banner(title="Error", message="Test error")
