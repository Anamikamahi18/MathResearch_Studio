"""Session state management for MathResearch Studio UI."""

from __future__ import annotations

import logging
from typing import Any

import streamlit as st

from src.ui.config import DEFAULT_APP_CONFIG, AppConfig

logger = logging.getLogger(__name__)


def init_session_state(config: AppConfig | None = None) -> None:
    """Initialize Streamlit session state variables with default values.

    Args:
        config: Optional AppConfig instance.
    """
    cfg = config or DEFAULT_APP_CONFIG

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = cfg.default_page

    if "theme_mode" not in st.session_state:
        st.session_state["theme_mode"] = "dark"

    if "sidebar_expanded" not in st.session_state:
        st.session_state["sidebar_expanded"] = True

    if "user_preferences" not in st.session_state:
        st.session_state["user_preferences"] = {
            "top_k": 5,
            "min_score": 0.5,
            "export_format": "markdown",
        }

    if "session_initialized" not in st.session_state:
        st.session_state["session_initialized"] = True
        logger.info("Initialized Streamlit session state for MathResearch Studio UI")


def get_current_page() -> str:
    """Get the currently selected page key from session state."""
    return st.session_state.get("current_page", DEFAULT_APP_CONFIG.default_page)


def set_current_page(page_key: str) -> None:
    """Set the active page key in session state.

    Args:
        page_key: Route page key string (e.g. 'home', 'upload', 'search').
    """
    if page_key in DEFAULT_APP_CONFIG.pages:
        st.session_state["current_page"] = page_key
        logger.info("Updated session state current_page -> '%s'", page_key)
    else:
        logger.warning("Attempted to set unknown page key: '%s'", page_key)


def get_user_preference(key: str, default: Any = None) -> Any:
    """Retrieve a user preference value from session state."""
    prefs = st.session_state.get("user_preferences", {})
    return prefs.get(key, default)


def set_user_preference(key: str, value: Any) -> None:
    """Set a user preference key-value pair in session state."""
    if "user_preferences" not in st.session_state:
        st.session_state["user_preferences"] = {}
    st.session_state["user_preferences"][key] = value


def get_document_service() -> Any:
    """Retrieve or initialize the shared DocumentService instance in session state."""
    if "doc_service" not in st.session_state or st.session_state["doc_service"] is None:
        from src.application.document_service import DocumentService

        doc_svc = DocumentService()
        doc_svc.refresh_library()
        st.session_state["doc_service"] = doc_svc
        logger.info("Initialized shared DocumentService in session state")
    return st.session_state["doc_service"]


def get_search_service() -> Any:
    """Retrieve or initialize the shared SearchService instance connected to DocumentService vector store."""
    if "search_service" not in st.session_state or st.session_state["search_service"] is None:
        from src.application.search_service import SearchService

        doc_svc = get_document_service()
        search_svc = SearchService(vector_store=doc_svc.vector_store)
        st.session_state["search_service"] = search_svc
        logger.info("Initialized shared SearchService in session state linked to DocumentService vector store")
    return st.session_state["search_service"]


def get_chat_service() -> Any:
    """Retrieve or initialize the shared ChatService instance connected to DocumentService resources."""
    if "chat_service" not in st.session_state or st.session_state["chat_service"] is None:
        from src.application.chat_service import ChatService

        doc_svc = get_document_service()
        chat_svc = ChatService(
            vector_store=doc_svc.vector_store,
            graph_service=doc_svc.graph_service,
        )
        st.session_state["chat_service"] = chat_svc
        logger.info("Initialized shared ChatService in session state linked to DocumentService vector store and graph")
    return st.session_state["chat_service"]


def get_graph_service() -> Any:
    """Retrieve or initialize the shared GraphService instance connected to DocumentService graph."""
    if "graph_service" not in st.session_state or st.session_state["graph_service"] is None:
        from src.application.graph_service import GraphService

        doc_svc = get_document_service()
        graph_svc = GraphService(backend_graph_service=doc_svc.graph_service)
        st.session_state["graph_service"] = graph_svc
        logger.info("Initialized shared GraphService in session state linked to DocumentService graph")
    return st.session_state["graph_service"]


def get_dashboard_service() -> Any:
    """Retrieve or initialize the shared DashboardService instance connected to DocumentService & GraphService."""
    if "dashboard_service" not in st.session_state or st.session_state["dashboard_service"] is None:
        from src.application.dashboard_service import DashboardService

        doc_svc = get_document_service()
        graph_svc = get_graph_service()
        dash_svc = DashboardService(
            document_service=doc_svc,
            graph_service=graph_svc,
            vector_store=doc_svc.vector_store,
        )
        st.session_state["dashboard_service"] = dash_svc
        logger.info("Initialized shared DashboardService in session state linked to DocumentService and GraphService")
    return st.session_state["dashboard_service"]


def get_export_service() -> Any:
    """Retrieve or initialize the shared ExportService instance in session state."""
    if "export_service" not in st.session_state or st.session_state["export_service"] is None:
        from src.application.export_service import ExportService

        exp_svc = ExportService(export_dir="exports")
        st.session_state["export_service"] = exp_svc
        logger.info("Initialized shared ExportService in session state")
    return st.session_state["export_service"]






