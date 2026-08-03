"""Centralized node and edge styling configuration for mathematical graph visualization."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


DEFAULT_NODE_STYLES: dict[str, dict[str, Any]] = {
    "definition": {
        "color": "#1f77b4",  # Blue
        "shape": "box",
        "size": 25,
        "font": {"color": "#ffffff", "size": 14},
    },
    "theorem": {
        "color": "#d62728",  # Red
        "shape": "ellipse",
        "size": 30,
        "font": {"color": "#ffffff", "size": 16, "bold": True},
    },
    "lemma": {
        "color": "#ff7f0e",  # Orange
        "shape": "diamond",
        "size": 25,
        "font": {"color": "#000000", "size": 14},
    },
    "corollary": {
        "color": "#2ca02c",  # Green
        "shape": "box",
        "size": 22,
        "font": {"color": "#ffffff", "size": 13},
    },
    "proof": {
        "color": "#9467bd",  # Purple
        "shape": "square",
        "size": 20,
        "font": {"color": "#ffffff", "size": 12},
    },
    "example": {
        "color": "#17becf",  # Cyan
        "shape": "hexagon",
        "size": 20,
        "font": {"color": "#000000", "size": 12},
    },
    "remark": {
        "color": "#7f7f7f",  # Gray
        "shape": "triangle",
        "size": 18,
        "font": {"color": "#ffffff", "size": 12},
    },
    "reference": {
        "color": "#c7c7c7",  # Light Gray
        "shape": "dot",
        "size": 15,
        "font": {"color": "#333333", "size": 11},
    },
    "paper": {
        "color": "#000000",  # Black
        "shape": "database",
        "size": 35,
        "font": {"color": "#ffffff", "size": 18, "bold": True},
    },
    "section": {
        "color": "#8c564b",  # Brown
        "shape": "folder",
        "size": 22,
        "font": {"color": "#ffffff", "size": 13},
    },
    "stub": {
        "color": "#aec7e8",  # Light Blue
        "shape": "ellipse",
        "size": 15,
        "font": {"color": "#000000", "size": 10},
    },
}


DEFAULT_EDGE_STYLES: dict[str, dict[str, Any]] = {
    "depends_on": {
        "color": "#d62728",  # Red
        "width": 2,
        "dashes": False,
        "arrows": "to",
    },
    "proves": {
        "color": "#9467bd",  # Purple
        "width": 3,
        "dashes": False,
        "arrows": "to",
    },
    "uses_definition": {
        "color": "#1f77b4",  # Blue
        "width": 2,
        "dashes": False,
        "arrows": "to",
    },
    "uses_theorem": {
        "color": "#ff7f0e",  # Orange
        "width": 2,
        "dashes": False,
        "arrows": "to",
    },
    "uses_lemma": {
        "color": "#2ca02c",  # Green
        "width": 2,
        "dashes": False,
        "arrows": "to",
    },
    "extends": {
        "color": "#e377c2",  # Pink
        "width": 2,
        "dashes": True,
        "arrows": "to",
    },
    "references": {
        "color": "#8c564b",  # Brown
        "width": 1,
        "dashes": True,
        "arrows": "to",
    },
    "cites": {
        "color": "#7f7f7f",  # Gray
        "width": 1,
        "dashes": True,
        "arrows": "to",
    },
}


@dataclass
class GraphStyleConfig:
    """Centralized configuration for graph node and edge visual styles."""

    node_styles: dict[str, dict[str, Any]] = field(
        default_factory=lambda: dict(DEFAULT_NODE_STYLES)
    )
    edge_styles: dict[str, dict[str, Any]] = field(
        default_factory=lambda: dict(DEFAULT_EDGE_STYLES)
    )
    height: str = "750px"
    width: str = "100%"
    bgcolor: str = "#ffffff"
    font_color: str = "#000000"
    enable_physics: bool = True

    def get_node_style(self, entity_type: str) -> dict[str, Any]:
        """Return node style for given entity type with fallback."""
        key = str(entity_type).lower()
        return self.node_styles.get(
            key,
            {
                "color": "#17becf",
                "shape": "dot",
                "size": 18,
                "font": {"color": "#000000", "size": 12},
            },
        )

    def get_edge_style(self, relation_type: str) -> dict[str, Any]:
        """Return edge style for given relation type with fallback."""
        key = str(relation_type).lower()
        return self.edge_styles.get(
            key,
            {
                "color": "#7f7f7f",
                "width": 1,
                "dashes": False,
                "arrows": "to",
            },
        )
