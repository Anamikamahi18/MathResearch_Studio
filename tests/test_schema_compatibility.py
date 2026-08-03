"""Regression tests for Day 4 Step 4.5 Parser Schema and Pipeline Compatibility."""

import unittest

from src.graph.dependency_graph import ResearchGraphBuilder
from src.graph.entity_extraction import EntityExtractor, EntityType, ExtractedEntity
from src.graph.relation_extraction import ExtractedRelation, RelationExtractor, RelationType


class TestSchemaCompatibility(unittest.TestCase):
    """Regression test suite validating parser schema alignment and pipeline flow."""

    def setUp(self) -> None:
        self.doc = {
            "schema_version": "1.0",
            "paper_id": "test_paper_001",
            "title": "On Modular Representation Theory",
            "sections": [
                {
                    "section_id": "s1",
                    "heading": "1. Main Statements",
                    "level": 1,
                    "page_start": 1,
                    "page_end": 1,
                    "text": "Definition 1.1. A module M is simple if it has no proper submodules.\nLemma 2.1. Simple modules have non-zero endomorphism rings.\nTheorem 3.2. Theorem 3.2 follows from Lemma 2.1.\nProof of Theorem 3.2. Apply Lemma 2.1 and Definition 1.1.",
                    "section_type": "theorems",
                    "confidence": 0.9,
                }
            ],
            "definitions": [
                {
                    "def_id": "def_001",
                    "label": "Definition 1.1",
                    "text": "A module M is simple if it has no proper submodules.",
                    "section_id": "s1",
                    "page": 1,
                }
            ],
            "theorems": [
                {
                    "thm_id": "thm_001",
                    "label": "Theorem 3.2",
                    "text": "Theorem 3.2 follows from Lemma 2.1.",
                    "section_id": "s1",
                    "page": 1,
                }
            ],
            "lemmas": [
                {
                    "lem_id": "lem_001",
                    "label": "Lemma 2.1",
                    "text": "Simple modules have non-zero endomorphism rings.",
                    "section_id": "s1",
                    "page": 1,
                }
            ],
            "corollaries": [],
            "proofs": [
                {
                    "proof_id": "prf_001",
                    "label": "Proof of Theorem 3.2",
                    "related_to": {
                        "theorem_id": "thm_001",
                        "lemma_id": None,
                        "corollary_id": None,
                    },
                    "text": "Apply Lemma 2.1 and Definition 1.1.",
                    "section_id": "s1",
                    "page_start": 1,
                    "page_end": 1,
                }
            ],
            "references": [
                {
                    "reference_id": "ref_001",
                    "raw_text": "Richard Brauer. 1941. On Modular Characters.",
                    "title": "On Modular Characters",
                    "authors": ["Richard Brauer"],
                    "year": 1941,
                }
            ],
            "equations": [],
        }
        self.entity_extractor = EntityExtractor()
        self.relation_extractor = RelationExtractor()
        self.builder = ResearchGraphBuilder()

    def test_entity_extraction_schema_alignment(self) -> None:
        entities = self.entity_extractor.extract_from_document(self.doc)
        entity_types = {e.entity_type for e in entities}

        self.assertIn(EntityType.DEFINITION, entity_types)
        self.assertIn(EntityType.THEOREM, entity_types)
        self.assertIn(EntityType.LEMMA, entity_types)
        self.assertIn(EntityType.PROOF, entity_types)

        # Check label formatting
        titles = {e.title for e in entities}
        self.assertIn("Definition 1.1", titles)
        self.assertIn("Theorem 3.2", titles)
        self.assertIn("Lemma 2.1", titles)

    def test_relation_extraction_schema_alignment(self) -> None:
        entities = self.entity_extractor.extract_from_document(self.doc)
        relations = self.relation_extractor.extract_relations(entities, document=self.doc)

        rel_types = {r.relation_type for r in relations}
        self.assertIn(RelationType.PROVES, rel_types)
        self.assertIn(RelationType.CITES, rel_types)

        # Verify Proof -> Theorem PROVES relationship
        proof_rels = [r for r in relations if r.relation_type == RelationType.PROVES]
        self.assertTrue(any(p.target_entity_id.endswith("thm_001") for p in proof_rels))

    def test_end_to_end_graph_construction(self) -> None:
        entities = self.entity_extractor.extract_from_document(self.doc)
        relations = self.relation_extractor.extract_relations(entities, document=self.doc)
        graph = self.builder.build_graph(entities, relations)
        stats = self.builder.graph_statistics()

        self.assertGreaterEqual(stats["total_nodes"], 4)
        self.assertGreaterEqual(stats["total_edges"], 2)
        self.assertIn("definition", stats["node_count_by_type"])
        self.assertIn("theorem", stats["node_count_by_type"])
        self.assertIn("proves", stats["edge_count_by_type"])


if __name__ == "__main__":
    unittest.main()
