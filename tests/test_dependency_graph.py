"""Unit tests for Day 4 Step 4 NetworkX Dependency Graph Builder."""

import unittest

import networkx as nx

from src.graph.dependency_graph import (
    BaseGraphBuilder,
    NetworkXGraphBuilder,
    ResearchGraphBuilder,
)
from src.graph.entity_extraction import EntityType, ExtractedEntity
from src.graph.relation_extraction import ExtractedRelation, RelationType


class TestDependencyGraphBuilder(unittest.TestCase):
    """Test suite for NetworkXGraphBuilder functionality and requirements."""

    def setUp(self) -> None:
        self.builder = NetworkXGraphBuilder()
        self.entity1 = ExtractedEntity(
            entity_id="p1_def_001",
            entity_type=EntityType.DEFINITION,
            title="Definition 1.1",
            text="Let X be a topological space.",
            source_paper="Paper A",
            section_id="s1",
            section_title="Preliminaries",
            page_start=1,
            page_end=1,
            symbols=["X"],
            references=["[1]"],
        )
        self.entity2 = ExtractedEntity(
            entity_id="p1_thm_001",
            entity_type=EntityType.THEOREM,
            title="Theorem 2.1",
            text="If X is compact then X is bounded.",
            source_paper="Paper A",
            section_id="s2",
            section_title="Main Results",
            page_start=2,
            page_end=3,
            symbols=["X"],
            references=[],
        )
        self.relation1 = ExtractedRelation(
            relation_id="rel_001",
            relation_type=RelationType.USES_DEFINITION,
            source_entity_id="p1_thm_001",
            target_entity_id="p1_def_001",
            confidence=0.85,
            evidence_text="Using Definition 1.1",
            source_paper="Paper A",
            metadata={"rule": "USES_DEF_PATTERN"},
        )

    def test_interface_compliance(self) -> None:
        self.assertIsInstance(self.builder, BaseGraphBuilder)

    def test_graph_creation_and_node_insertion(self) -> None:
        self.builder.add_entities([self.entity1, self.entity2])
        nx_graph = self.builder.export_networkx()

        self.assertIsInstance(nx_graph, nx.MultiDiGraph)
        self.assertEqual(nx_graph.number_of_nodes(), 2)

        # Check metadata preservation
        node_attrs = nx_graph.nodes["p1_def_001"]
        self.assertEqual(node_attrs["entity_id"], "p1_def_001")
        self.assertEqual(node_attrs["entity_type"], "definition")
        self.assertEqual(node_attrs["title"], "Definition 1.1")
        self.assertEqual(node_attrs["text"], "Let X be a topological space.")
        self.assertEqual(node_attrs["source_paper"], "Paper A")
        self.assertEqual(node_attrs["section_id"], "s1")
        self.assertEqual(node_attrs["section_title"], "Preliminaries")
        self.assertEqual(node_attrs["page_start"], 1)
        self.assertEqual(node_attrs["page_end"], 1)
        self.assertEqual(node_attrs["symbols"], ["X"])
        self.assertEqual(node_attrs["references"], ["[1]"])

    def test_edge_insertion_and_metadata_preservation(self) -> None:
        self.builder.add_entities([self.entity1, self.entity2])
        self.builder.add_relations([self.relation1])

        nx_graph = self.builder.export_networkx()
        self.assertEqual(nx_graph.number_of_edges(), 1)

        edge_data = nx_graph.get_edge_data("p1_thm_001", "p1_def_001", key="rel_001")
        self.assertIsNotNone(edge_data)
        self.assertEqual(edge_data["relation_id"], "rel_001")
        self.assertEqual(edge_data["relation_type"], "uses_definition")
        self.assertEqual(edge_data["confidence"], 0.85)
        self.assertEqual(edge_data["evidence_text"], "Using Definition 1.1")
        self.assertEqual(edge_data["source_paper"], "Paper A")
        self.assertEqual(edge_data["metadata"], {"rule": "USES_DEF_PATTERN"})

    def test_duplicate_handling(self) -> None:
        # Inserting entity with updated title
        self.builder.add_entities([self.entity1])

        updated_entity1 = ExtractedEntity(
            entity_id="p1_def_001",
            entity_type=EntityType.DEFINITION,
            title="Definition 1.1 (Updated)",
            text="Let X be a topological space.",
            source_paper="Paper A",
        )
        self.builder.add_entities([updated_entity1])

        nx_graph = self.builder.export_networkx()
        self.assertEqual(nx_graph.number_of_nodes(), 1)
        self.assertEqual(nx_graph.nodes["p1_def_001"]["title"], "Definition 1.1 (Updated)")

    def test_graph_statistics(self) -> None:
        self.builder.build_graph([self.entity1, self.entity2], [self.relation1])
        stats = self.builder.graph_statistics()

        self.assertEqual(stats["total_nodes"], 2)
        self.assertEqual(stats["total_edges"], 1)
        self.assertEqual(stats["node_count_by_type"]["definition"], 1)
        self.assertEqual(stats["node_count_by_type"]["theorem"], 1)
        self.assertEqual(stats["edge_count_by_type"]["uses_definition"], 1)
        self.assertEqual(stats["connected_components"], 1)
        self.assertEqual(stats["isolated_nodes"], 0)
        self.assertGreaterEqual(stats["density"], 0.0)

    def test_graph_merging(self) -> None:
        b1 = NetworkXGraphBuilder()
        b1.add_entities([self.entity1])

        b2 = NetworkXGraphBuilder()
        b2.add_entities([self.entity2])
        b2.add_relations([self.relation1])

        b1.merge_graph(b2)
        stats = b1.graph_statistics()

        self.assertEqual(stats["total_nodes"], 2)
        self.assertEqual(stats["total_edges"], 1)


if __name__ == "__main__":
    unittest.main()
