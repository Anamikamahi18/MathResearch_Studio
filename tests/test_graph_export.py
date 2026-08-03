"""Unit tests for Day 4 Step 5 Graph Format Exporters."""

import json
import pickle
import tempfile
import unittest
from pathlib import Path

import networkx as nx

from src.graph.graph_export import (
    BaseGraphExporter,
    CytoscapeExporter,
    GEXFExporter,
    GraphExportManager,
    GraphMLExporter,
    JSONExporter,
    PickleExporter,
    PyVisHTMLExporter,
)


class TestGraphExport(unittest.TestCase):
    """Test suite for graph export implementations and format compatibility."""

    def setUp(self) -> None:
        self.graph = nx.MultiDiGraph()
        self.graph.add_node(
            "p1_def_001",
            entity_id="p1_def_001",
            entity_type="definition",
            title="Definition 1.1",
            text="A group G is abelian if xy=yx.",
            symbols=["G", "x", "y"],
        )
        self.graph.add_node(
            "p1_thm_001",
            entity_id="p1_thm_001",
            entity_type="theorem",
            title="Theorem 2.1",
            text="Subgroups of abelian groups are normal.",
            symbols=["G"],
        )
        self.graph.add_edge(
            "p1_thm_001",
            "p1_def_001",
            key="rel_001",
            relation_id="rel_001",
            relation_type="uses_definition",
            confidence=0.95,
        )

    def test_json_exporter(self) -> None:
        exporter = JSONExporter()
        self.assertIsInstance(exporter, BaseGraphExporter)

        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "graph.json"
            res = exporter.export(self.graph, out_file)
            self.assertTrue(res.exists())

            with open(res, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIn("nodes", data)
            self.assertTrue("links" in data or "edges" in data)

    def test_cytoscape_exporter(self) -> None:
        exporter = CytoscapeExporter()
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "cy.json"
            res = exporter.export(self.graph, out_file)
            self.assertTrue(res.exists())

            with open(res, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIn("elements", data)
            self.assertEqual(len(data["elements"]["nodes"]), 2)
            self.assertEqual(len(data["elements"]["edges"]), 1)

    def test_graphml_exporter(self) -> None:
        exporter = GraphMLExporter()
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "graph.graphml"
            res = exporter.export(self.graph, out_file)
            self.assertTrue(res.exists())

            # Load back using NetworkX
            loaded_g = nx.read_graphml(res)
            self.assertEqual(loaded_g.number_of_nodes(), 2)

    def test_gexf_exporter(self) -> None:
        exporter = GEXFExporter()
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "graph.gexf"
            res = exporter.export(self.graph, out_file)
            self.assertTrue(res.exists())

            # Load back using NetworkX
            loaded_g = nx.read_gexf(res)
            self.assertEqual(loaded_g.number_of_nodes(), 2)

    def test_pickle_exporter(self) -> None:
        exporter = PickleExporter()
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "graph.pkl"
            res = exporter.export(self.graph, out_file)
            self.assertTrue(res.exists())

            with open(res, "rb") as f:
                loaded_g = pickle.load(f)
            self.assertEqual(loaded_g.number_of_nodes(), 2)
            self.assertEqual(loaded_g.number_of_edges(), 1)

    def test_pyvis_html_exporter(self) -> None:
        exporter = PyVisHTMLExporter()
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "graph.html"
            res = exporter.export(self.graph, out_file)
            self.assertTrue(res.exists())

    def test_export_manager(self) -> None:
        manager = GraphExportManager()
        with tempfile.TemporaryDirectory() as tmp_dir:
            exported_files = manager.export_all(self.graph, tmp_dir, "test_graph")

            self.assertIn("html", exported_files)
            self.assertIn("json", exported_files)
            self.assertIn("cytoscape", exported_files)
            self.assertIn("graphml", exported_files)
            self.assertIn("gexf", exported_files)
            self.assertIn("pickle", exported_files)

            for key, p in exported_files.items():
                self.assertTrue(p.exists(), f"Export file {key} at {p} does not exist!")


if __name__ == "__main__":
    unittest.main()
