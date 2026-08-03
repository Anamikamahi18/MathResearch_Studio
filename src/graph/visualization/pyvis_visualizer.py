"""PyVis implementation for interactive mathematical dependency graph visualization."""

from __future__ import annotations

import html
import logging
from pathlib import Path
from typing import Any

import networkx as nx
from pyvis.network import Network

from .base import BaseGraphVisualizer
from .config import GraphStyleConfig

logger = logging.getLogger(__name__)


class PyVisGraphVisualizer(BaseGraphVisualizer):
    """PyVis-backed interactive graph visualizer."""

    def __init__(self, style_config: GraphStyleConfig | None = None) -> None:
        """Initialize visualizer with optional style configuration."""
        super().__init__(style_config=style_config)

    def render(
        self,
        graph: nx.MultiDiGraph,
        output_path: str | Path,
        **kwargs: Any,
    ) -> Path:
        """Render NetworkX MultiDiGraph as an interactive HTML file using PyVis.

        Args:
            graph: NetworkX MultiDiGraph instance.
            output_path: Target HTML filepath.
            **kwargs: Additional options (e.g. title).

        Returns:
            Path object pointing to generated HTML file.
        """
        out_file = Path(output_path).resolve()
        out_file.parent.mkdir(parents=True, exist_ok=True)

        net = Network(
            height=self.style_config.height,
            width=self.style_config.width,
            bgcolor=self.style_config.bgcolor,
            font_color=self.style_config.font_color,
            directed=True,
            notebook=False,
            heading=kwargs.get("title", "Mathematical Research Graph"),
        )

        net.toggle_physics(self.style_config.enable_physics)

        # 1. Add styled nodes
        for node_id, attrs in graph.nodes(data=True):
            e_type = str(attrs.get("entity_type", "unknown")).lower()
            style = self.style_config.get_node_style(e_type)

            title_str = attrs.get("title") or node_id
            text_str = attrs.get("text") or ""
            sec_title = attrs.get("section_title") or attrs.get("section_id") or ""
            paper_str = attrs.get("source_paper") or ""
            symbols = attrs.get("symbols") or []

            # HTML tooltip on hover
            tooltip = f"<b>{html.escape(title_str)}</b><br>"
            tooltip += f"<i>Type:</i> {html.escape(e_type.capitalize())}<br>"
            if sec_title:
                tooltip += f"<i>Section:</i> {html.escape(sec_title)}<br>"
            if paper_str:
                tooltip += f"<i>Paper:</i> {html.escape(paper_str)}<br>"
            if symbols:
                tooltip += f"<i>Symbols:</i> {html.escape(', '.join(symbols))}<br>"
            if text_str:
                snippet = text_str[:200] + ("..." if len(text_str) > 200 else "")
                tooltip += f"<hr><code>{html.escape(snippet)}</code>"

            net.add_node(
                node_id,
                label=title_str,
                title=tooltip,
                color=style["color"],
                shape=style["shape"],
                size=style.get("size", 20),
                font=style.get("font", {"color": "#000000", "size": 12}),
            )

        # 2. Add styled edges
        for u, v, k, attrs in graph.edges(keys=True, data=True):
            r_type = str(attrs.get("relation_type", "unknown")).lower()
            style = self.style_config.get_edge_style(r_type)

            evidence = attrs.get("evidence_text") or ""
            confidence = attrs.get("confidence")

            tooltip = f"<b>Relation:</b> {html.escape(r_type)}<br>"
            if confidence is not None:
                tooltip += f"<b>Confidence:</b> {confidence:.2f}<br>"
            if evidence:
                tooltip += f"<i>Evidence:</i> {html.escape(evidence)}"

            net.add_edge(
                u,
                v,
                title=tooltip,
                label=r_type,
                color=style["color"],
                width=style.get("width", 1),
                dashes=style.get("dashes", False),
                arrows=style.get("arrows", "to"),
            )

        # Save HTML graph
        net.write_html(str(out_file))
        logger.info("Successfully rendered interactive PyVis graph to: %s", out_file)

        return out_file

    @staticmethod
    def to_cytoscape_elements(graph: Any) -> list[dict[str, Any]]:
        """Export graph into Cytoscape.js elements list format."""
        if hasattr(graph, "nodes") and isinstance(graph.nodes, dict):
            # Legacy ResearchGraph object compatibility
            elements: list[dict[str, Any]] = []
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
                            "paper_id": getattr(node, "paper_id", ""),
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

        elif hasattr(graph, "nodes"):
            elements = []
            for n_id, attrs in graph.nodes(data=True):
                elements.append(
                    {
                        "data": {
                            "id": n_id,
                            "label": attrs.get("title") or n_id,
                            "type": str(attrs.get("entity_type", "unknown")),
                        }
                    }
                )
            for u, v, k, attrs in graph.edges(keys=True, data=True):
                elements.append(
                    {
                        "data": {
                            "id": str(k),
                            "source": u,
                            "target": v,
                            "relation": str(attrs.get("relation_type", "unknown")),
                        }
                    }
                )
            return elements

        return []

    @staticmethod
    def to_pyvis_json(graph: Any) -> dict[str, Any]:
        """Export graph into PyVis / vis.js network format dictionary."""
        if hasattr(graph, "nodes") and isinstance(graph.nodes, dict):
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
                        "title": f"<b>{node.label}</b><br/>Type: {n_type}",
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
        elif hasattr(graph, "nodes"):
            nodes = []
            edges = []
            for n_id, attrs in graph.nodes(data=True):
                nodes.append(
                    {
                        "id": n_id,
                        "label": attrs.get("title") or n_id,
                        "group": str(attrs.get("entity_type", "unknown")),
                    }
                )
            for u, v, _, attrs in graph.edges(keys=True, data=True):
                edges.append(
                    {
                        "from": u,
                        "to": v,
                        "label": str(attrs.get("relation_type", "unknown")),
                        "arrows": "to",
                    }
                )
            return {"nodes": nodes, "edges": edges}

        return {"nodes": [], "edges": []}
