"""UI Configuration settings for MathResearch Studio."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AppConfig:
    """Configuration settings for the Streamlit research dashboard UI."""

    title: str = "MathResearch Studio"
    version: str = "v1.0.0"
    tagline: str = "Interactive AI Workspace for Mathematical Literature, Theorems & Symbol Relationships"
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
            "upload": {"label": "Upload Math Papers", "icon": "📤", "group": "Library"},
            "library": {"label": "Math Library", "icon": "📚", "group": "Library"},
            "search": {"label": "Math Search", "icon": "🔍", "group": "Discovery"},
            "assistant": {"label": "Math AI Assistant", "icon": "💬", "group": "Discovery"},
            "graph": {"label": "Theorem Graph", "icon": "🕸️", "group": "Knowledge Graph"},
            "notation": {"label": "Notation Dictionary", "icon": "🔣", "group": "Knowledge Graph"},
            "statistics": {"label": "Math Statistics", "icon": "📊", "group": "Analytics"},
            "export": {"label": "Export Center", "icon": "💾", "group": "Workspace"},
            "settings": {"label": "Settings", "icon": "⚙️", "group": "Workspace"},
        }
    )

    # Mathematics arXiv Subject Classifications & Subfield Tags
    arxiv_math_categories: dict[str, str] = field(
        default_factory=lambda: {
            "math.AG": "Algebraic Geometry",
            "math.AT": "Algebraic Topology",
            "math.AP": "Analysis of PDEs",
            "math.CA": "Classical Analysis & ODEs",
            "math.CO": "Combinatorics",
            "math.CT": "Category Theory",
            "math.DG": "Differential Geometry",
            "math.DS": "Dynamical Systems",
            "math.FA": "Functional Analysis",
            "math.GM": "General Mathematics",
            "math.GN": "General Topology",
            "math.GR": "Group Theory",
            "math.HO": "History and Overview",
            "math.IT": "Information Theory",
            "math.KT": "K-Theory and Homology",
            "math.LO": "Logic & Set Theory",
            "math.MP": "Mathematical Physics",
            "math.NA": "Numerical Analysis",
            "math.NT": "Number Theory",
            "math.OA": "Operator Algebras",
            "math.PR": "Probability & Stochastic Processes",
            "math.QA": "Quantum Algebra",
            "math.RT": "Representation Theory",
            "math.SG": "Symplectic Geometry",
            "math.SP": "Spectral Theory",
            "math.ST": "Statistics Theory",
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
