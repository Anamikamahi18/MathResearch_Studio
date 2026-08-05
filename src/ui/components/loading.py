"""Loading and spinner UI helper component."""

from __future__ import annotations

import streamlit as st


def render_loading_spinner(message: str = "Processing mathematical context...") -> None:
    """Render a standard loading spinner block.

    Args:
        message: Informational spinner text.
    """
    with st.spinner(message):
        st.markdown(
            f"""
            <div style="text-align: center; color: #94A3B8; font-size: 0.9rem; padding: 1rem;">
                <span>⚙️ {message}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
