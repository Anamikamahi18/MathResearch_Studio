"""Research graph builder engine module."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Sequence

from .citation_linker import CitationLinker
from .extractor import DependencyExtractor
from .models import ResearchGraph

logger = logging.getLogger(__name__)


class ResearchGraphBuilder:
    """Builds and accumulates ResearchGraph instances from parsed paper documents."""

    def __init__(
        self,
        extractor: DependencyExtractor | None = None,
        citation_linker: CitationLinker | None = None,
    ) -> None:
        """Initialize graph builder with an extractor and optional citation linker.

        Args:
            extractor: Optional DependencyExtractor instance.
            citation_linker: Optional CitationLinker instance.
        """
        self.extractor = extractor or DependencyExtractor()
        self.citation_linker = citation_linker or CitationLinker()

    def build_from_document(self, document: dict[str, Any]) -> ResearchGraph:
        """Build a ResearchGraph from a single parsed document dictionary.

        Args:
            document: Parsed document dictionary adhering to Schema v1.0.

        Returns:
            Populated ResearchGraph instance.
        """
        graph = ResearchGraph()
        self.add_document_to_graph(document, graph)
        return graph

    def build_from_file(self, file_path: str | Path) -> ResearchGraph:
        """Load a parsed document JSON file and build a ResearchGraph.

        Args:
            file_path: Path to parsed document JSON file.

        Returns:
            Populated ResearchGraph instance.
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Parsed JSON file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            document = json.load(f)

        return self.build_from_document(document)

    def add_document_to_graph(
        self, document: dict[str, Any], graph: ResearchGraph
    ) -> None:
        """Extract and add nodes and edges from a document into an existing graph.

        Args:
            document: Parsed document dictionary.
            graph: Target ResearchGraph instance.
        """
        nodes, edges = self.extractor.extract(document)

        for node in nodes:
            graph.add_node(node)

        for edge in edges:
            try:
                graph.add_edge(edge)
            except KeyError as exc:
                logger.warning("Skipping edge '%s': %s", edge.edge_id, exc)

    def build_from_collection(
        self, documents_or_paths: Sequence[dict[str, Any] | str | Path]
    ) -> ResearchGraph:
        """Build a multi-paper ResearchGraph from a collection of documents or paths.

        Args:
            documents_or_paths: Sequence of parsed document dicts or file paths.

        Returns:
            Populated multi-paper ResearchGraph instance.
        """
        graph = ResearchGraph()
        for item in documents_or_paths:
            if isinstance(item, (str, Path)):
                path = Path(item)
                if path.is_file():
                    with open(path, "r", encoding="utf-8") as f:
                        doc = json.load(f)
                    self.add_document_to_graph(doc, graph)
            elif isinstance(item, dict):
                self.add_document_to_graph(item, graph)

        # Resolve cross-paper citations across the accumulated corpus
        self.citation_linker.resolve_cross_paper_citations(graph)

        logger.info(
            "Built multi-paper graph: %d nodes, %d edges",
            len(graph.nodes),
            len(graph.edges),
        )
        return graph
