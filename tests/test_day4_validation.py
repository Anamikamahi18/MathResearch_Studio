"""Regression test suite for Day 4.6 Benchmark Validation."""

import json
import unittest
from pathlib import Path

from src.graph.dependency_graph import ResearchGraphBuilder
from src.graph.entity_extraction import EntityExtractor, EntityType
from src.graph.relation_extraction import RelationExtractor, RelationType


class TestDay4Validation(unittest.TestCase):
    """Test suite validating pipeline execution across benchmark paper corpus."""

    def setUp(self) -> None:
        self.benchmark_dir = Path(__file__).resolve().parent / "benchmark_papers"
        self.entity_extractor = EntityExtractor()
        self.relation_extractor = RelationExtractor()
        self.builder = ResearchGraphBuilder()

    def test_benchmark_papers_extraction(self) -> None:
        json_files = sorted(self.benchmark_dir.glob("*.json"))
        self.assertGreaterEqual(len(json_files), 6, "Expected at least 6 benchmark papers!")

        for file_path in json_files:
            with open(file_path, "r", encoding="utf-8") as f:
                doc = json.load(f)

            entities = self.entity_extractor.extract_from_document(doc)
            self.assertGreater(len(entities), 0, f"No entities extracted for {file_path.name}")

            relations = self.relation_extractor.extract_relations(entities, document=doc)
            self.assertGreater(len(relations), 0, f"No relations extracted for {file_path.name}")

            # Check that mathematical statement types are extracted
            e_types = {e.entity_type for e in entities}
            self.assertTrue(
                EntityType.DEFINITION in e_types or EntityType.THEOREM in e_types,
                f"Missing mathematical statement entity in {file_path.name}",
            )

    def test_combined_benchmark_graph_building(self) -> None:
        json_files = sorted(self.benchmark_dir.glob("*.json"))
        master_builder = ResearchGraphBuilder()

        for file_path in json_files:
            with open(file_path, "r", encoding="utf-8") as f:
                doc = json.load(f)

            entities = self.entity_extractor.extract_from_document(doc)
            relations = self.relation_extractor.extract_relations(entities, document=doc)
            master_builder.add_entities(entities)
            master_builder.add_relations(relations)

        stats = master_builder.graph_statistics()
        self.assertGreaterEqual(stats["total_nodes"], 20)
        self.assertGreaterEqual(stats["total_edges"], 20)
        self.assertIn("definition", stats["node_count_by_type"])
        self.assertIn("theorem", stats["node_count_by_type"])
        self.assertIn("lemma", stats["node_count_by_type"])
        self.assertIn("proves", stats["edge_count_by_type"])


if __name__ == "__main__":
    unittest.main()
