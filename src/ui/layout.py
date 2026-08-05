"""Application layout master orchestrator."""

from __future__ import annotations

import streamlit as st

from src.ui import components, sidebar
from src.ui.config import DEFAULT_APP_CONFIG, AppConfig
from src.ui.router import PageRouter
from src.ui.state import init_session_state
from src.ui.theme import apply_custom_theme


def render_app_layout(config: AppConfig | None = None) -> None:
    """Render master application layout structure: Header, Sidebar, Main Content, Footer.

    Args:
        config: Optional AppConfig instance.
    """
    cfg = config or DEFAULT_APP_CONFIG

    # 1. Initialize Streamlit Page Configuration
    st.set_page_config(
        page_title=cfg.title,
        page_icon=cfg.page_icon,
        layout=cfg.layout_mode,
        initial_sidebar_state=cfg.initial_sidebar_state,
    )

    # 2. Initialize Session State & Inject Custom CSS Theme
    init_session_state(cfg)
    apply_custom_theme(cfg)

    # 3. Render Sidebar (Branding, Navigation, System Status)
    sidebar.render_branding(cfg)
    current_page = sidebar.render_navigation(cfg)
    sidebar.render_status(cfg)

    # 4. Main Page Container & Header Bar
    components.render_header(current_page, cfg)

    # 5. Route and Render Main Content View
    router = PageRouter()
    router.render_current_page()

    # 6. Render Footer Bar
    components.render_footer(cfg)
