"""UI Configuration settings for MathResearch Studio."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AppConfig:
    """Configuration settings for the Streamlit research dashboard UI."""

    title: str = "MathResearch Studio"
    version: str = "v0.6.1"
    tagline: str = "AI-Powered Mathematical Document & Knowledge Graph Research Environment"
    page_icon: str = "📐"
    sidebar_width: int = 280
    default_page: str = "home"
    layout_mode: str = "wide"
    initial_sidebar_state: str = "expanded"

    # Theme colors
    primary_color: str = "#4F46E5"  # Indigo
    background_color: str = "#0F172A"  # Dark Slate
    secondary_background_color: str = "#1E293B"  # Card Slate
    text_color: str = "#F8FAFC"
    accent_color: str = "#06B6D4"  # Cyan accent

    # Supported navigation pages with labels and icons
    pages: dict[str, dict[str, str]] = field(
        default_factory=lambda: {
            "home": {"label": "Home", "icon": "🏠", "group": "Overview"},
            "upload": {"label": "Upload Papers", "icon": "📤", "group": "Library"},
            "library": {"label": "Library", "icon": "📚", "group": "Library"},
            "search": {"label": "Semantic Search", "icon": "🔍", "group": "Discovery"},
            "assistant": {"label": "AI Assistant", "icon": "💬", "group": "Discovery"},
            "graph": {"label": "Research Graph", "icon": "🕸️", "group": "Knowledge Graph"},
            "notation": {"label": "Notation Dictionary", "icon": "🔣", "group": "Knowledge Graph"},
            "statistics": {"label": "Statistics", "icon": "📊", "group": "Analytics"},
            "export": {"label": "Export", "icon": "💾", "group": "Workspace"},
            "settings": {"label": "Settings", "icon": "⚙️", "group": "Workspace"},
        }
    )

    # Future configuration placeholders
    feature_flags: dict[str, bool] = field(
        default_factory=lambda: {
            "enable_pdf_ocr": True,
            "enable_graph_visualization": True,
            "enable_llm_streaming": False,
            "enable_citation_exporter": True,
        }
    )

    def get_page_info(self, page_key: str) -> dict[str, str]:
        """Retrieve label and icon metadata for a given page key."""
        return self.pages.get(
            page_key,
            {"label": page_key.title(), "icon": "📄", "group": "Workspace"},
        )


# Global default configuration instance
DEFAULT_APP_CONFIG = AppConfig()
