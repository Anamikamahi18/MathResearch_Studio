"""Page title component for standardized section headings."""

from __future__ import annotations

import streamlit as st


def render_page_title(
    title: str,
    subtitle: str | None = None,
    icon: str | None = None,
    badge: str | None = None,
) -> None:
    """Render a standardized page title block with icon, subtitle, and badge.

    Args:
        title: Main page title text.
        subtitle: Optional descriptive subtitle.
        icon: Optional icon emoji or symbol.
        badge: Optional badge text (e.g. "Placeholder", "Step 1 Shell").
    """
    icon_prefix = f"{icon} " if icon else ""

    if badge:
        st.markdown(f'<span class="mrs-badge">{badge}</span>', unsafe_allow_html=True)

    st.title(f"{icon_prefix}{title}", anchor=False)

    if subtitle:
        st.caption(subtitle)

    st.divider()
