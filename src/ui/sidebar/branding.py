"""Sidebar branding module for logo and app identity."""

from __future__ import annotations

import streamlit as st

from src.ui.config import DEFAULT_APP_CONFIG, AppConfig


def render_branding(config: AppConfig | None = None) -> None:
    """Render project logo placeholder, title, and tagline in sidebar.

    Args:
        config: Optional AppConfig instance.
    """
    cfg = config or DEFAULT_APP_CONFIG

    st.sidebar.markdown(
        f"""
        <div class="mrs-branding">
            <div style="font-size: 2rem; margin-bottom: 0.25rem;">{cfg.page_icon}</div>
            <h2 class="mrs-branding-title">{cfg.title}</h2>
            <div class="mrs-branding-version">AI Research Workspace</div>
        </div>

        """,
        unsafe_allow_html=True,
    )
