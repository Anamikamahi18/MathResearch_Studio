"""GraphService application service for dependency graph management, notation graph building, and node lookup."""

from __future__ import annotations

import logging
from typing import Any

from src.graph.builder import ResearchGraphBuilder
from src.graph.models import NodeType, ResearchGraph
from src.graph.service import GraphService as BackendGraphService

logger = logging.getLogger(__name__)


class GraphService:
    """Application service for dependency graph orchestration, notation graph building, and node lookup."""

    def __init__(
        self,
        backend_graph_service: BackendGraphService | None = None,
    ) -> None:
        """Initialize GraphService with backend GraphService or builder.

        Args:
            backend_graph_service: Optional backend GraphService instance from Day 4.
        """
        self.backend = backend_graph_service or BackendGraphService()
        self.builder = ResearchGraphBuilder()

    def build_dependency_graph(
        self,
        documents: list[dict[str, Any]] | None = None,
    ) -> ResearchGraph:
        """Build or update the mathematical statement dependency graph.

        Args:
            documents: Optional list of parsed paper dictionaries to ingest.

        Returns:
            Constructed ResearchGraph instance.
        """
        if documents:
            self.backend.build_from_collection(documents)

        logger.info(
            "Dependency graph built: %d nodes, %d edges",
            len(self.backend.graph.nodes),
            len(self.backend.graph.edges),
        )
        return self.backend.graph

    def build_notation_graph(
        self,
        documents: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Construct a notation graph mapping symbols, variables, operator definitions, and concepts.

        Args:
            documents: Optional list of parsed paper dictionaries.

        Returns:
            Dictionary representation of notation graph (symbols, concepts, equations, and connections).
        """
        if documents:
            self.backend.build_from_collection(documents)

        graph = self.backend.graph
        symbol_nodes: list[dict[str, Any]] = []
        concept_nodes: list[dict[str, Any]] = []
        equation_nodes: list[dict[str, Any]] = []
        notation_edges: list[dict[str, Any]] = []

        for node_id, node in graph.nodes.items():
            n_dict = node.to_dict()
            n_type = str(node.node_type.value if hasattr(node.node_type, "value") else node.node_type).lower()

            if n_type == "symbol":
                symbol_nodes.append(n_dict)
            elif n_type == "concept":
                concept_nodes.append(n_dict)
            elif n_type == "equation":
                equation_nodes.append(n_dict)

        # Collect edges involving symbols or concepts
        for edge in graph.edges.values():
            src_node = graph.nodes.get(edge.source_id)
            tgt_node = graph.nodes.get(edge.target_id)
            if src_node and tgt_node:
                src_type = str(src_node.node_type.value if hasattr(src_node.node_type, "value") else src_node.node_type).lower()
                tgt_type = str(tgt_node.node_type.value if hasattr(tgt_node.node_type, "value") else tgt_node.node_type).lower()
                if any(t in ("symbol", "concept", "equation") for t in (src_type, tgt_type)):
                    notation_edges.append(edge.to_dict())

        notation_graph_summary = {
            "symbols": symbol_nodes,
            "concepts": concept_nodes,
            "equations": equation_nodes,
            "symbol_count": len(symbol_nodes),
            "concept_count": len(concept_nodes),
            "equation_count": len(equation_nodes),
            "edges": notation_edges,
            "edge_count": len(notation_edges),
        }

        logger.info(
            "Notation graph constructed: %d symbols, %d concepts, %d equations, %d notation edges",
            len(symbol_nodes),
            len(concept_nodes),
            len(equation_nodes),
            len(notation_edges),
        )

        return notation_graph_summary

    def node_lookup(
        self,
        node_id: str | None = None,
        query: str | None = None,
        node_type: str | None = None,
    ) -> list[dict[str, Any]]:
        """Look up graph nodes by node_id, text/label search query, or node type filter.

        Args:
            node_id: Exact node identifier.
            query: Substring search query for node label, text, or paper_id.
            node_type: Specific statement type filter ("definition", "theorem", "lemma", "proof", etc.).

        Returns:
            List of matching node dictionaries.
        """
        # Exact node_id lookup
        if node_id:
            single = self.backend.get_node(node_id)
            return [single] if single else []

        graph = self.backend.graph
        matched: list[dict[str, Any]] = []

        for nid, node in graph.nodes.items():
            n_dict = node.to_dict()

            # Node type filter
            if node_type:
                curr_type = str(node.node_type.value if hasattr(node.node_type, "value") else node.node_type).lower()
                if curr_type != node_type.lower():
                    continue

            # Query filter
            if query:
                q_lower = query.lower()
                label = (node.label or "").lower()
                text = (node.text or "").lower()
                paper_id = (node.paper_id or "").lower()
                if not (q_lower in label or q_lower in text or q_lower in paper_id):
                    continue

            matched.append(n_dict)

        return matched

    def get_antecedents(self, node_id: str) -> list[dict[str, Any]]:
        """Retrieve direct prerequisite definitions, lemmas, and theorems for a node."""
        return self.backend.get_antecedents(node_id)

    def get_consequents(self, node_id: str) -> list[dict[str, Any]]:
        """Retrieve direct downstream statements depending on a node."""
        return self.backend.get_consequents(node_id)

    def get_proof_chain(self, statement_id: str) -> dict[str, Any]:
        """Retrieve proof chain for a theorem or lemma."""
        return self.backend.get_proof_chain(statement_id)

    def get_graph_metrics(self) -> dict[str, Any]:
        """Return graph topological metrics and node/edge breakdowns."""
        graph = self.backend.graph

        type_counts: dict[str, int] = {}
        for node in graph.nodes.values():
            t_str = str(node.node_type.value if hasattr(node.node_type, "value") else node.node_type).lower()
            type_counts[t_str] = type_counts.get(t_str, 0) + 1

        rel_counts: dict[str, int] = {}
        for edge in graph.edges.values():
            r_str = str(edge.relation_type.value if hasattr(edge.relation_type, "value") else edge.relation_type).lower()
            rel_counts[r_str] = rel_counts.get(r_str, 0) + 1

        return {
            "total_nodes": len(graph.nodes),
            "total_edges": len(graph.edges),
            "node_type_breakdown": type_counts,
            "relation_type_breakdown": rel_counts,
            "density": float(len(graph.edges) / (len(graph.nodes) * (len(graph.nodes) - 1))) if len(graph.nodes) > 1 else 0.0,
        }
