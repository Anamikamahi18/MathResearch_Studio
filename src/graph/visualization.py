"""Graph visualization export adapters module."""

from __future__ import annotations

import logging
from typing import Any

from .models import NodeType, ResearchGraph

logger = logging.getLogger(__name__)


class GraphVisualizer:
    """Exports ResearchGraph instances into frontend and rendering formats (PyVis, Cytoscape, D3)."""

    @staticmethod
    def to_cytoscape_elements(graph: ResearchGraph) -> list[dict[str, Any]]:
        """Export graph into Cytoscape.js elements JSON format.

        Returns:
            List of element dictionaries formatted for Cytoscape.js.
        """
        elements: list[dict[str, Any]] = []

        # Color scheme by node type
        color_map = {
            NodeType.PAPER.value: "#4C72B0",
            NodeType.SECTION.value: "#55A868",
            NodeType.DEFINITION.value: "#C44E52",
            NodeType.THEOREM.value: "#8172B0",
            NodeType.LEMMA.value: "#CCB974",
            NodeType.COROLLARY.value: "#64B5CD",
            NodeType.PROOF.value: "#8C8C8C",
            NodeType.EQUATION.value: "#E1974C",
            NodeType.REFERENCE.value: "#B07AA1",
            NodeType.OTHER.value: "#999999",
        }

        for node in graph.nodes.values():
            n_type = (
                node.node_type.value
                if hasattr(node.node_type, "value")
                else str(node.node_type)
            )
            elements.append(
                {
                    "data": {
                        "id": node.node_id,
                        "label": node.label or node.node_id,
                        "type": n_type,
                        "paper_id": node.paper_id,
                        "color": color_map.get(n_type, "#999999"),
                    }
                }
            )

        for edge in graph.edges.values():
            r_type = (
                edge.relation_type.value
                if hasattr(edge.relation_type, "value")
                else str(edge.relation_type)
            )
            elements.append(
                {
                    "data": {
                        "id": edge.edge_id,
                        "source": edge.source_id,
                        "target": edge.target_id,
                        "relation": r_type,
                        "confidence": edge.confidence,
                    }
                }
            )

        return elements

    @staticmethod
    def to_pyvis_json(graph: ResearchGraph) -> dict[str, Any]:
        """Export graph into PyVis / vis.js network format.

        Returns:
            Dictionary containing 'nodes' and 'edges' lists formatted for vis.js.
        """
        nodes: list[dict[str, Any]] = []
        edges: list[dict[str, Any]] = []

        for node in graph.nodes.values():
            n_type = (
                node.node_type.value
                if hasattr(node.node_type, "value")
                else str(node.node_type)
            )
            nodes.append(
                {
                    "id": node.node_id,
                    "label": node.label or node.node_id,
                    "title": f"<b>{node.label}</b><br/>Type: {n_type}<br/>Paper: {node.paper_id}",
                    "group": n_type,
                }
            )

        for edge in graph.edges.values():
            r_type = (
                edge.relation_type.value
                if hasattr(edge.relation_type, "value")
                else str(edge.relation_type)
            )
            edges.append(
                {
                    "from": edge.source_id,
                    "to": edge.target_id,
                    "label": r_type,
                    "arrows": "to",
                }
            )

        return {"nodes": nodes, "edges": edges}
