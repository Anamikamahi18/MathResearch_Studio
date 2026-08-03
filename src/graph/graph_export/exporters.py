"""Graph format exporters for JSON, Cytoscape JSON, GraphML, GEXF, Pickle, and PyVis HTML."""

from __future__ import annotations

import json
import logging
import pickle
from pathlib import Path
from typing import Any

import networkx as nx

from src.graph.visualization.pyvis_visualizer import PyVisGraphVisualizer

from .base import BaseGraphExporter

logger = logging.getLogger(__name__)


def _sanitize_attributes_for_xml(graph: nx.MultiDiGraph) -> nx.MultiDiGraph:
    """Create a copy of graph with non-primitive attribute types stringified for GraphML/GEXF compatibility."""
    g_copy = nx.MultiDiGraph()

    for n, attrs in graph.nodes(data=True):
        clean_attrs: dict[str, Any] = {}
        for k, v in attrs.items():
            if isinstance(v, (list, dict, set, tuple)):
                clean_attrs[k] = json.dumps(v)
            elif v is None:
                clean_attrs[k] = ""
            else:
                clean_attrs[k] = v
        g_copy.add_node(n, **clean_attrs)

    for u, v, k, attrs in graph.edges(keys=True, data=True):
        clean_attrs: dict[str, Any] = {}
        for ek, ev in attrs.items():
            if isinstance(ev, (list, dict, set, tuple)):
                clean_attrs[ek] = json.dumps(ev)
            elif ev is None:
                clean_attrs[ek] = ""
            else:
                clean_attrs[ek] = ev
        g_copy.add_edge(u, v, key=str(k), **clean_attrs)

    return g_copy


class JSONExporter(BaseGraphExporter):
    """Exports NetworkX MultiDiGraph as node-link JSON format."""

    def export(
        self,
        graph: nx.MultiDiGraph,
        output_path: str | Path,
        **kwargs: Any,
    ) -> Path:
        out_file = Path(output_path).resolve()
        out_file.parent.mkdir(parents=True, exist_ok=True)

        data = nx.node_link_data(graph)
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logger.info("Exported JSON graph to: %s", out_file)
        return out_file


class CytoscapeExporter(BaseGraphExporter):
    """Exports NetworkX MultiDiGraph as Cytoscape elements JSON format."""

    def export(
        self,
        graph: nx.MultiDiGraph,
        output_path: str | Path,
        **kwargs: Any,
    ) -> Path:
        out_file = Path(output_path).resolve()
        out_file.parent.mkdir(parents=True, exist_ok=True)

        nodes = []
        for n_id, attrs in graph.nodes(data=True):
            node_data = {"id": n_id, "name": attrs.get("title") or n_id}
            node_data.update(attrs)
            nodes.append({"data": node_data})

        edges = []
        for u, v, k, attrs in graph.edges(keys=True, data=True):
            edge_data = {
                "id": str(k),
                "source": u,
                "target": v,
                "interaction": attrs.get("relation_type", "relates_to"),
            }
            edge_data.update(attrs)
            edges.append({"data": edge_data})

        cy_data = {"elements": {"nodes": nodes, "edges": edges}}
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(cy_data, f, indent=2)

        logger.info("Exported Cytoscape JSON graph to: %s", out_file)
        return out_file


class GraphMLExporter(BaseGraphExporter):
    """Exports NetworkX MultiDiGraph to GraphML format."""

    def export(
        self,
        graph: nx.MultiDiGraph,
        output_path: str | Path,
        **kwargs: Any,
    ) -> Path:
        out_file = Path(output_path).resolve()
        out_file.parent.mkdir(parents=True, exist_ok=True)

        g_clean = _sanitize_attributes_for_xml(graph)
        nx.write_graphml(g_clean, str(out_file))

        logger.info("Exported GraphML graph to: %s", out_file)
        return out_file


class GEXFExporter(BaseGraphExporter):
    """Exports NetworkX MultiDiGraph to GEXF format."""

    def export(
        self,
        graph: nx.MultiDiGraph,
        output_path: str | Path,
        **kwargs: Any,
    ) -> Path:
        out_file = Path(output_path).resolve()
        out_file.parent.mkdir(parents=True, exist_ok=True)

        g_clean = _sanitize_attributes_for_xml(graph)
        nx.write_gexf(g_clean, str(out_file))

        logger.info("Exported GEXF graph to: %s", out_file)
        return out_file


class PickleExporter(BaseGraphExporter):
    """Exports NetworkX MultiDiGraph to binary Python pickle format."""

    def export(
        self,
        graph: nx.MultiDiGraph,
        output_path: str | Path,
        **kwargs: Any,
    ) -> Path:
        out_file = Path(output_path).resolve()
        out_file.parent.mkdir(parents=True, exist_ok=True)

        with open(out_file, "wb") as f:
            pickle.dump(graph, f)

        logger.info("Exported Pickle graph to: %s", out_file)
        return out_file


class PyVisHTMLExporter(BaseGraphExporter):
    """Exports NetworkX MultiDiGraph as PyVis interactive HTML."""

    def export(
        self,
        graph: nx.MultiDiGraph,
        output_path: str | Path,
        **kwargs: Any,
    ) -> Path:
        visualizer = PyVisGraphVisualizer()
        return visualizer.render(graph, output_path, **kwargs)


class GraphExportManager:
    """Unified manager for exporting graphs to multiple formats."""

    def __init__(self) -> None:
        self.exporters: dict[str, BaseGraphExporter] = {
            "json": JSONExporter(),
            "cytoscape": CytoscapeExporter(),
            "graphml": GraphMLExporter(),
            "gexf": GEXFExporter(),
            "pickle": PickleExporter(),
            "html": PyVisHTMLExporter(),
        }

    def export_all(
        self,
        graph: nx.MultiDiGraph,
        output_dir: str | Path,
        base_name: str = "research_graph",
    ) -> dict[str, Path]:
        """Export graph into all supported formats inside output_dir.

        Args:
            graph: NetworkX MultiDiGraph instance.
            output_dir: Destination directory path.
            base_name: Base filename prefix.

        Returns:
            Dictionary mapping format key to exported file Path.
        """
        out_dir = Path(output_dir).resolve()
        out_dir.mkdir(parents=True, exist_ok=True)

        exported_files: dict[str, Path] = {}

        exported_files["html"] = self.exporters["html"].export(
            graph, out_dir / f"{base_name}.html"
        )
        exported_files["json"] = self.exporters["json"].export(
            graph, out_dir / f"{base_name}.json"
        )
        exported_files["cytoscape"] = self.exporters["cytoscape"].export(
            graph, out_dir / f"{base_name}_cytoscape.json"
        )
        exported_files["graphml"] = self.exporters["graphml"].export(
            graph, out_dir / f"{base_name}.graphml"
        )
        exported_files["gexf"] = self.exporters["gexf"].export(
            graph, out_dir / f"{base_name}.gexf"
        )
        exported_files["pickle"] = self.exporters["pickle"].export(
            graph, out_dir / f"{base_name}.pkl"
        )

        return exported_files
