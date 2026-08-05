"""Sidebar system status module."""

from __future__ import annotations

import streamlit as st

from src.ui.config import DEFAULT_APP_CONFIG, AppConfig


def render_status(config: AppConfig | None = None) -> None:
    """Render system version and status readiness badge in sidebar.

    Args:
        config: Optional AppConfig instance.
    """
    cfg = config or DEFAULT_APP_CONFIG

    st.sidebar.caption("MathResearch Studio v1.0.0 &bull; Ready")
