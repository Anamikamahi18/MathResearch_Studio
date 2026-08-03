"""Unit tests for Day 4 Research Graph construction, citation resolution, and RAG integration."""

import unittest
from pathlib import Path
from unittest.mock import MagicMock

from src.graph import (
    CitationLinker,
    DependencyExtractor,
    GraphAugmentedRetriever,
    GraphEdge,
    GraphNode,
    GraphService,
    GraphVisualizer,
    NodeType,
    RelationType,
    ResearchGraph,
    ResearchGraphBuilder,
)


class TestGraphModels(unittest.TestCase):
    """Test suite for GraphNode, GraphEdge, and ResearchGraph container."""

    def test_node_creation_and_serialization(self) -> None:
        node = GraphNode(
            node_id="thm_001",
            node_type=NodeType.THEOREM,
            label="Theorem 1.1",
            text="Let X be a compact space.",
            paper_id="paper_01",
            section_id="s1",
            page_start=1,
            page_end=2,
        )
        self.assertEqual(node.node_id, "thm_001")
        self.assertEqual(node.node_type, NodeType.THEOREM)
        node_dict = node.to_dict()
        self.assertEqual(node_dict["node_type"], "theorem")

        restored_node = GraphNode.from_dict(node_dict)
        self.assertEqual(restored_node.node_id, "thm_001")
        self.assertEqual(restored_node.label, "Theorem 1.1")

    def test_edge_creation_and_serialization(self) -> None:
        edge = GraphEdge(
            edge_id="e1",
            source_id="prf_001",
            target_id="thm_001",
            relation_type=RelationType.PROVES,
            confidence=0.9,
        )
        self.assertEqual(edge.source_id, "prf_001")
        edge_dict = edge.to_dict()
        self.assertEqual(edge_dict["relation_type"], "PROVES")

        restored_edge = GraphEdge.from_dict(edge_dict)
        self.assertEqual(restored_edge.target_id, "thm_001")

    def test_research_graph_operations(self) -> None:
        graph = ResearchGraph()
        n1 = GraphNode(node_id="n1", node_type=NodeType.DEFINITION, label="Def 1")
        n2 = GraphNode(node_id="n2", node_type=NodeType.LEMMA, label="Lem 1")
        n3 = GraphNode(node_id="n3", node_type=NodeType.THEOREM, label="Thm 1")
        graph.add_node(n1)
        graph.add_node(n2)
        graph.add_node(n3)

        graph.add_edge(
            GraphEdge(
                edge_id="e1",
                source_id="n2",
                target_id="n1",
                relation_type=RelationType.USES_DEFINITION,
            )
        )
        graph.add_edge(
            GraphEdge(
                edge_id="e2",
                source_id="n3",
                target_id="n2",
                relation_type=RelationType.USES_LEMMA,
            )
        )

        self.assertEqual(len(graph.nodes), 3)
        self.assertEqual(len(graph.edges), 2)

        antecedents = graph.get_antecedents("n3")
        self.assertEqual(len(antecedents), 1)
        self.assertEqual(antecedents[0].node_id, "n2")

        all_antecedents = graph.get_all_antecedents("n3")
        self.assertEqual(len(all_antecedents), 2)
        antecedent_ids = [n.node_id for n in all_antecedents]
        self.assertIn("n1", antecedent_ids)
        self.assertIn("n2", antecedent_ids)

        all_consequents = graph.get_all_consequents("n1")
        self.assertEqual(len(all_consequents), 2)
        consequent_ids = [n.node_id for n in all_consequents]
        self.assertIn("n2", consequent_ids)
        self.assertIn("n3", consequent_ids)


class TestGraphExtractorAndBuilder(unittest.TestCase):
    """Test suite for DependencyExtractor, ResearchGraphBuilder, and GraphService."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.sample_path = Path("exports/parser_outputs/paper_6cd768c13674.json")
        if not cls.sample_path.is_file():
            cls.skipTest(cls, f"Sample parsed JSON not found at {cls.sample_path}")

    def test_extractor_on_sample_paper(self) -> None:
        extractor = DependencyExtractor()
        builder = ResearchGraphBuilder(extractor=extractor)
        graph = builder.build_from_file(self.sample_path)

        self.assertGreater(len(graph.nodes), 0)
        self.assertGreater(len(graph.edges), 0)

        paper_nodes = [n for n in graph.nodes.values() if n.node_type == NodeType.PAPER]
        self.assertEqual(len(paper_nodes), 1)

        section_nodes = [n for n in graph.nodes.values() if n.node_type == NodeType.SECTION]
        self.assertGreater(len(section_nodes), 0)

        ref_nodes = [n for n in graph.nodes.values() if n.node_type == NodeType.REFERENCE]
        self.assertGreater(len(ref_nodes), 0)

    def test_citation_linker(self) -> None:
        graph = ResearchGraph()
        p1 = GraphNode(node_id="paper_p1", node_type=NodeType.PAPER, label="Paper One", paper_id="p1")
        p2 = GraphNode(node_id="paper_p2", node_type=NodeType.PAPER, label="Paper Two", paper_id="p2")
        ref = GraphNode(
            node_id="p1_ref_001",
            node_type=NodeType.REFERENCE,
            label="Paper Two",
            text="Paper Two full text citation",
            paper_id="p1",
        )
        graph.add_node(p1)
        graph.add_node(p2)
        graph.add_node(ref)

        linker = CitationLinker()
        added_edges = linker.resolve_cross_paper_citations(graph)
        self.assertEqual(added_edges, 1)

    def test_graph_service_operations(self) -> None:
        service = GraphService()
        service.build_from_file(self.sample_path)

        export_dict = service.export_graph()
        self.assertIn("nodes", export_dict)
        self.assertIn("edges", export_dict)
        self.assertGreater(export_dict["node_count"], 0)

        sections = service.filter_nodes_by_type(NodeType.SECTION)
        self.assertGreater(len(sections), 0)

        save_dir = Path("exports/test_graph_dir")
        save_path = service.save(save_dir)
        self.assertTrue(save_path.is_file())

        loaded_service = GraphService()
        loaded_service.load(save_dir)
        self.assertEqual(len(loaded_service.graph.nodes), len(service.graph.nodes))

        if save_path.is_file():
            save_path.unlink()
        if save_dir.is_dir():
            save_dir.rmdir()

    def test_graph_visualization(self) -> None:
        service = GraphService()
        service.build_from_file(self.sample_path)

        cy_elements = GraphVisualizer.to_cytoscape_elements(service.graph)
        self.assertGreater(len(cy_elements), 0)

        pyvis_data = GraphVisualizer.to_pyvis_json(service.graph)
        self.assertIn("nodes", pyvis_data)
        self.assertIn("edges", pyvis_data)

    def test_graph_augmented_retriever(self) -> None:
        service = GraphService()
        service.build_from_file(self.sample_path)

        mock_retriever = MagicMock()
        mock_retriever.retrieve.return_value = [
            {
                "chunk_id": "paper_6cd768c13674_s1_c001",
                "score": 0.85,
                "text": "Abstract text chunk",
                "paper_id": "paper_6cd768c13674",
                "section_id": "s1",
                "entity_type": "section_text",
            }
        ]

        graph_retriever = GraphAugmentedRetriever(
            retriever=mock_retriever,
            graph_service=service,
        )

        results = graph_retriever.retrieve("scibert NLP model", top_k=1)
        self.assertEqual(len(results), 1)
        self.assertIn("graph_context", results[0])


if __name__ == "__main__":
    unittest.main()
