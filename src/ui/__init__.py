"""Streamlit UI package for MathResearch Studio."""

from src.ui.config import AppConfig, DEFAULT_APP_CONFIG
from src.ui.layout import render_app_layout
from src.ui.router import PageRouter
from src.ui.state import init_session_state, get_current_page, set_current_page

__all__ = [
    "render_app_layout",
    "PageRouter",
    "AppConfig",
    "DEFAULT_APP_CONFIG",
    "init_session_state",
    "get_current_page",
    "set_current_page",
]
