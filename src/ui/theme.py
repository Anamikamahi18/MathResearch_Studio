"""Theme configuration and custom CSS injection for MathResearch Studio."""

from __future__ import annotations

import streamlit as st

from src.ui.config import DEFAULT_APP_CONFIG, AppConfig


def get_custom_css(config: AppConfig | None = None) -> str:
    """Generate custom CSS injection string for styling the Streamlit UI shell.

    Args:
        config: Optional AppConfig instance.

    Returns:
        Formatted CSS code string.
    """
    cfg = config or DEFAULT_APP_CONFIG

    return f"""
    <style>
    /* Global Page & Container Styling */
    .stApp {{
        background-color: {cfg.background_color};
        color: {cfg.text_color};
        font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}

    /* Top Streamlit Header Bar Fix */
    header[data-testid="stHeader"], [data-testid="stHeader"], .stAppHeader {{
        background-color: transparent !important;
        background: transparent !important;
    }}

    /* Top Padding Adjustment */
    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1280px;
    }}



    /* Card Containers */
    .mrs-card {{
        background-color: {cfg.secondary_background_color};
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}

    .mrs-card:hover {{
        border-color: rgba(99, 102, 241, 0.4);
    }}

    /* Placeholder Badge Callouts */
    .mrs-badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        font-size: 0.75rem;
        font-weight: 600;
        line-height: 1;
        border-radius: 9999px;
        background-color: rgba(79, 70, 229, 0.2);
        color: #818CF8;
        border: 1px solid rgba(129, 140, 248, 0.3);
        margin-bottom: 0.75rem;
    }}

    .mrs-coming-soon {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
        border: 1px dashed rgba(99, 102, 241, 0.3);
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-top: 1rem;
        color: #94A3B8;
        font-size: 0.9rem;
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: #0F172A;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }}

    .mrs-branding {{
        padding: 0.5rem 0 1rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1rem;
    }}

    .mrs-branding-title {{
        font-size: 1.25rem;
        font-weight: 700;
        background: linear-gradient(135deg, #818CF8, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }}

    .mrs-branding-version {{
        font-size: 0.75rem;
        color: #64748B;
        font-weight: 500;
    }}

    /* Header Bar */
    .mrs-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }}

    .mrs-breadcrumb {{
        font-size: 0.875rem;
        color: #94A3B8;
    }}

    /* Footer Bar */
    .mrs-footer {{
        margin-top: 4rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        text-align: center;
        font-size: 0.8rem;
        color: #64748B;
    }}
    </style>
    """


def apply_custom_theme(config: AppConfig | None = None) -> None:
    """Inject custom CSS theme into the active Streamlit app view."""
    css = get_custom_css(config)
    st.markdown(css, unsafe_allow_html=True)
