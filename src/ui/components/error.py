"""Error and exception UI display component."""

from __future__ import annotations

import streamlit as st


def render_error_banner(
    title: str = "Application Error",
    message: str = "An unexpected issue occurred while rendering the page.",
    details: str | None = None,
) -> None:
    """Render a styled error notification banner.

    Args:
        title: Error headline.
        message: Friendly error description.
        details: Optional technical exception details.
    """
    st.error(f"**{title}**: {message}")
    if details:
        with st.expander("Technical Exception Details"):
            st.code(details, language="text")
