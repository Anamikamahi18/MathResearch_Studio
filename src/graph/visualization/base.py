"""Abstract base class interface for mathematical graph visualizers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import networkx as nx

from .config import GraphStyleConfig


class BaseGraphVisualizer(ABC):
    """Abstract interface for mathematical graph visualizers."""

    def __init__(self, style_config: GraphStyleConfig | None = None) -> None:
        """Initialize visualizer with an optional GraphStyleConfig."""
        self._style_config = style_config if style_config is not None else GraphStyleConfig()

    @property
    def style_config(self) -> GraphStyleConfig:
        """Return current style configuration."""
        return self._style_config

    @abstractmethod
    def render(
        self,
        graph: nx.MultiDiGraph,
        output_path: str | Path,
        **kwargs: Any,
    ) -> Path:
        """Render graph visualization to file and return output Path.

        Args:
            graph: NetworkX MultiDiGraph instance.
            output_path: Destination filepath.
            **kwargs: Renderer-specific arguments.

        Returns:
            Path object pointing to rendered output file.
        """
        pass
