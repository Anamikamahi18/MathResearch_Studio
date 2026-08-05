"""High-level graph query service module."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from .builder import ResearchGraphBuilder
from .models import GraphNode, NodeType, RelationType, ResearchGraph

logger = logging.getLogger(__name__)


class GraphService:
    """High-level service for querying mathematical statement dependencies and exporting graphs."""

    DEFAULT_GRAPH_DIR = Path("exports/graph")

    def __init__(self, graph: ResearchGraph | None = None) -> None:
        """Initialize graph service with an optional existing graph.

        Args:
            graph: Optional ResearchGraph instance.
        """
        self.graph = graph or ResearchGraph()
        self.builder = ResearchGraphBuilder()

    def build_from_document(self, document: dict[str, Any]) -> None:
        """Build/update graph from a parsed document dictionary."""
        self.builder.add_document_to_graph(document, self.graph)

    def build_from_file(self, file_path: str | Path) -> None:
        """Build/update graph from a parsed document JSON file."""
        self.graph = self.builder.build_from_file(file_path)

    def build_from_collection(
        self, documents_or_paths: list[dict[str, Any] | str | Path]
    ) -> None:
        """Build/update multi-paper graph from a collection of documents or paths."""
        self.graph = self.builder.build_from_collection(documents_or_paths)

    def get_node(self, node_id: str) -> dict[str, Any] | None:
        """Retrieve node details by node_id."""
        node = self.graph.get_node(node_id)
        return node.to_dict() if node else None

    def get_antecedents(self, node_id: str) -> list[dict[str, Any]]:
        """Get prerequisite definitions, lemmas, and theorems for a node."""
        antecedents = self.graph.get_antecedents(node_id)
        return [node.to_dict() for node in antecedents]

    def get_consequents(self, node_id: str) -> list[dict[str, Any]]:
        """Get downstream statements that depend on a given node."""
        consequents = self.graph.get_consequents(node_id)
        return [node.to_dict() for node in consequents]

    def get_all_antecedents(
        self, node_id: str, max_depth: int = 5
    ) -> list[dict[str, Any]]:
        """Recursively get all prerequisite definitions, lemmas, and theorems for a node."""
        antecedents = self.graph.get_all_antecedents(node_id, max_depth=max_depth)
        return [node.to_dict() for node in antecedents]

    def get_all_consequents(
        self, node_id: str, max_depth: int = 5
    ) -> list[dict[str, Any]]:
        """Recursively get all downstream statements depending on a node."""
        consequents = self.graph.get_all_consequents(node_id, max_depth=max_depth)
        return [node.to_dict() for node in consequents]

    def get_proof_chain(self, statement_id: str) -> dict[str, Any]:
        """Retrieve full proof chain for a theorem or lemma including supporting proofs and antecedents."""
        target_node = self.graph.get_node(statement_id)
        if not target_node:
            return {"statement": None, "proofs": [], "antecedents": []}

        # Find incoming proof edges (proofs that prove this statement)
        in_edges = self.graph.get_in_edges(statement_id)
        proof_nodes = [
            self.graph.nodes[edge.source_id].to_dict()
            for edge in in_edges
            if edge.source_id in self.graph.nodes
            and edge.relation_type in (RelationType.PROVES, RelationType.PROVES.value)
        ]

        antecedents = self.get_antecedents(statement_id)

        return {
            "statement": target_node.to_dict(),
            "proofs": proof_nodes,
            "antecedents": antecedents,
        }

    def filter_nodes_by_type(
        self, node_type: NodeType | str
    ) -> list[dict[str, Any]]:
        """Retrieve all nodes matching a specific node type (e.g. theorem, definition)."""
        target_type = (
            node_type.value if isinstance(node_type, NodeType) else str(node_type)
        )
        matched = [
            node.to_dict()
            for node in self.graph.nodes.values()
            if (
                node.node_type.value
                if isinstance(node.node_type, NodeType)
                else str(node.node_type)
            )
            == target_type
        ]
        return matched

    def export_graph(self) -> dict[str, Any]:
        """Export the complete graph structure as a plain dictionary."""
        return self.graph.to_dict()

    def save(self, directory: str | Path | None = None) -> Path:
        """Save graph structure to graph.json on disk."""
        dir_path = Path(directory) if directory else self.DEFAULT_GRAPH_DIR
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / "graph.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.graph.to_dict(), f, indent=2, ensure_ascii=False)

        logger.info("Saved ResearchGraph to: %s", file_path)
        return file_path

    def load(self, directory: str | Path | None = None) -> None:
        """Load graph structure from graph.json on disk."""
        dir_path = Path(directory) if directory else self.DEFAULT_GRAPH_DIR
        file_path = dir_path / "graph.json"

        if not file_path.is_file():
            raise FileNotFoundError(f"Graph file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.graph = ResearchGraph.from_dict(data)
        logger.info(
            "Loaded ResearchGraph from '%s' (%d nodes, %d edges)",
            file_path,
            len(self.graph.nodes),
            len(self.graph.edges),
        )
