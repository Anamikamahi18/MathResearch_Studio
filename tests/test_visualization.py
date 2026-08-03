"""Unit tests for Day 4 Step 5 Graph Visualization and Statistics."""

import tempfile
import unittest
from pathlib import Path

import networkx as nx

from src.graph.visualization import (
    BaseGraphVisualizer,
    GraphStatistics,
    GraphStyleConfig,
    PyVisGraphVisualizer,
    calculate_graph_statistics,
)


class TestGraphVisualization(unittest.TestCase):
    """Test suite for graph visualizer interface, PyVis visualizer, and statistics engine."""

    def setUp(self) -> None:
        self.graph = nx.MultiDiGraph()
        self.graph.add_node(
            "p1_def_001",
            entity_id="p1_def_001",
            entity_type="definition",
            title="Definition 1.1",
            text="Let X be a topological space.",
            section_id="s1",
            section_title="Preliminaries",
            source_paper="Paper A",
            page_start=1,
            page_end=1,
            symbols=["X"],
        )
        self.graph.add_node(
            "p1_thm_001",
            entity_id="p1_thm_001",
            entity_type="theorem",
            title="Theorem 2.1",
            text="If X is compact then X is bounded.",
            section_id="s2",
            section_title="Main Results",
            source_paper="Paper A",
            page_start=2,
            page_end=3,
            symbols=["X"],
        )
        self.graph.add_edge(
            "p1_thm_001",
            "p1_def_001",
            key="rel_001",
            relation_id="rel_001",
            relation_type="uses_definition",
            confidence=0.9,
            evidence_text="Using Definition 1.1",
            source_paper="Paper A",
        )

    def test_style_config(self) -> None:
        config = GraphStyleConfig()
        def_style = config.get_node_style("definition")
        thm_style = config.get_node_style("theorem")
        edge_style = config.get_edge_style("uses_definition")

        self.assertEqual(def_style["color"], "#1f77b4")
        self.assertEqual(thm_style["color"], "#d62728")
        self.assertEqual(edge_style["color"], "#1f77b4")

    def test_visualizer_interface_and_render(self) -> None:
        visualizer = PyVisGraphVisualizer()
        self.assertIsInstance(visualizer, BaseGraphVisualizer)

        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "test_graph.html"
            result_path = visualizer.render(self.graph, out_file, title="Test Visualization")

            self.assertTrue(result_path.exists())
            self.assertGreater(result_path.stat().st_size, 0)

            content = result_path.read_text(encoding="utf-8")
            self.assertIn("Definition 1.1", content)
            self.assertIn("Theorem 2.1", content)

    def test_statistics_generation(self) -> None:
        stats = calculate_graph_statistics(self.graph)

        self.assertIsInstance(stats, GraphStatistics)
        self.assertEqual(stats.total_nodes, 2)
        self.assertEqual(stats.total_edges, 1)
        self.assertEqual(stats.node_count_by_type.get("definition"), 1)
        self.assertEqual(stats.node_count_by_type.get("theorem"), 1)
        self.assertEqual(stats.edge_count_by_type.get("uses_definition"), 1)
        self.assertEqual(stats.connected_components, 1)
        self.assertEqual(stats.isolated_nodes, 0)
        self.assertGreaterEqual(stats.density, 0.0)

        stats_dict = stats.to_dict()
        self.assertEqual(stats_dict["total_nodes"], 2)


if __name__ == "__main__":
    unittest.main()
