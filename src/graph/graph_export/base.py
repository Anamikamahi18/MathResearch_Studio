"""Abstract base class interface for graph exporters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import networkx as nx


class BaseGraphExporter(ABC):
    """Abstract interface for mathematical graph format exporters."""

    @abstractmethod
    def export(
        self,
        graph: nx.MultiDiGraph,
        output_path: str | Path,
        **kwargs: Any,
    ) -> Path:
        """Export graph to target file format and return output Path.

        Args:
            graph: NetworkX MultiDiGraph instance.
            output_path: Destination filepath.
            **kwargs: Format-specific export parameters.

        Returns:
            Path object pointing to exported file.
        """
        pass
