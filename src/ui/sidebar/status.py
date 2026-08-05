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

    st.sidebar.divider()

    st.sidebar.markdown(
        f"""
        <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 0.75rem;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.25rem;">
                <span style="font-size: 0.75rem; color: #94A3B8; font-weight: 600;">SYSTEM STATUS</span>
                <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background-color: #10B981;"></span>
            </div>
            <div style="font-size: 0.85rem; color: #F8FAFC; font-weight: 500;">
                System Operational
            </div>
            <div style="font-size: 0.75rem; color: #64748B; margin-top: 0.25rem;">
                MathResearch Studio
            </div>
        </div>

        """,
        unsafe_allow_html=True,
    )
