"""Empty state visual component for Streamlit pages."""

from __future__ import annotations

import streamlit as st


def render_empty_state(
    title: str = "No Data Found",
    message: str = "There are currently no items to display in this view.",
    icon: str = "📭",
    action_label: str | None = None,
) -> bool:
    """Render a clean empty state card with icon, message, and optional CTA button.

    Args:
        title: Headline text.
        message: Detailed explanation.
        icon: Emoji/symbol for visual accent.
        action_label: Optional label for CTA button.

    Returns:
        True if action button was clicked, False otherwise.
    """
    st.markdown(
        f"""
        <div class="mrs-card" style="text-align: center; padding: 2.5rem 1.5rem;">
            <div style="font-size: 3rem; margin-bottom: 0.75rem;">{icon}</div>
            <h3 style="margin-bottom: 0.5rem; color: #F8FAFC;">{title}</h3>
            <p style="color: #94A3B8; font-size: 0.95rem; max-width: 480px; margin: 0 auto 1.25rem auto;">
                {message}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if action_label:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            return bool(st.button(action_label, use_container_width=True))

    return False
