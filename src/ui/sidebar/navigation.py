"""Sidebar navigation menu module."""

from __future__ import annotations

import streamlit as st

from src.ui.config import DEFAULT_APP_CONFIG, AppConfig
from src.ui.state import get_current_page, set_current_page


def render_navigation(config: AppConfig | None = None) -> str:
    """Render the sidebar page navigation menu and update active session state.

    Args:
        config: Optional AppConfig instance.

    Returns:
        Currently selected route key.
    """
    cfg = config or DEFAULT_APP_CONFIG
    current_key = get_current_page()

    st.sidebar.markdown("### Navigation")

    # Format list of page selection options
    page_keys = list(cfg.pages.keys())
    page_labels = [
        f"{meta['icon']} {meta['label']}" for meta in cfg.pages.values()
    ]

    # Find active index
    try:
        current_index = page_keys.index(current_key)
    except ValueError:
        current_index = 0

    selected_label = st.sidebar.radio(
        label="Select Navigation Page",
        options=page_labels,
        index=current_index,
        label_visibility="collapsed",
    )

    # Resolve selected key from label
    selected_key = page_keys[page_labels.index(selected_label)]

    if selected_key != current_key:
        set_current_page(selected_key)
        st.rerun()

    return selected_key
