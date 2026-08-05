"""Header component for MathResearch Studio UI layout."""

from __future__ import annotations

import streamlit as st

from src.ui.config import DEFAULT_APP_CONFIG, AppConfig


def render_header(current_page: str, config: AppConfig | None = None) -> None:
    """Render the top header bar with breadcrumb and application metadata.

    Args:
        current_page: Current page route key.
        config: Optional AppConfig instance.
    """
    cfg = config or DEFAULT_APP_CONFIG
    page_info = cfg.get_page_info(current_page)

    st.markdown(
        f"""
        <div class="mrs-header">
            <div class="mrs-breadcrumb">
                <span>{cfg.title}</span> &nbsp;/&nbsp; 
                <strong style="color: #F8FAFC;">{page_info['icon']} {page_info['label']}</strong>
            </div>
            <div style="font-size: 0.8rem; color: #64748B;">
                <span>{cfg.version}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
