"""Graph visualization package for MathResearch Studio."""

from .base import BaseGraphVisualizer
from .config import DEFAULT_EDGE_STYLES, DEFAULT_NODE_STYLES, GraphStyleConfig
from .pyvis_visualizer import PyVisGraphVisualizer
from .statistics import GraphStatistics, calculate_graph_statistics

GraphVisualizer = PyVisGraphVisualizer

__all__ = [
    "BaseGraphVisualizer",
    "PyVisGraphVisualizer",
    "GraphVisualizer",
    "GraphStyleConfig",
    "GraphStatistics",
    "calculate_graph_statistics",
    "DEFAULT_NODE_STYLES",
    "DEFAULT_EDGE_STYLES",
]
