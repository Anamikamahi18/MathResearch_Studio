"""Footer component for MathResearch Studio UI layout."""

from __future__ import annotations

import streamlit as st

from src.ui.config import DEFAULT_APP_CONFIG, AppConfig


def render_footer(config: AppConfig | None = None) -> None:
    """Render the application footer bar.

    Args:
        config: Optional AppConfig instance.
    """
    cfg = config or DEFAULT_APP_CONFIG

    st.markdown(
        f"""
        <div class="mrs-footer">
            <p><strong>{cfg.title}</strong> {cfg.version} &bull; Deepmind Agentic AI Architecture</p>
            <p style="margin-top: 0.25rem;">Built with Streamlit &bull; Python 3.12</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
