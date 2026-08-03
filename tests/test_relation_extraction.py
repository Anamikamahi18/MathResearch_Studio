"""Unit tests for Day 4 Step 3 Mathematical Relation Extraction pipeline."""

import unittest
from pathlib import Path

from src.graph.entity_extraction import EntityType, ExtractedEntity
from src.graph.relation_extraction import (
    BaseRelationExtractor,
    ExtractedRelation,
    RelationExtractor,
    RelationType,
)


class TestExtractedRelationModel(unittest.TestCase):
    """Test suite for ExtractedRelation model validation and serialization."""

    def test_relation_creation_and_validation(self) -> None:
        relation = ExtractedRelation(
            relation_id="rel_001",
            relation_type=RelationType.USES_DEFINITION,
            source_entity_id="p1_thm_001",
            target_entity_id="p1_def_001",
            confidence=0.85,
            evidence_text="Using Definition 1.1",
            source_paper="Paper 1",
            metadata={"rule": "USES_DEF_PATTERN"},
        )

        self.assertEqual(relation.relation_id, "rel_001")
        self.assertEqual(relation.relation_type, RelationType.USES_DEFINITION)
        self.assertEqual(relation.confidence, 0.85)

        # Test dictionary conversion
        rel_dict = relation.to_dict()
        self.assertEqual(rel_dict["relation_type"], "uses_definition")
        self.assertEqual(rel_dict["source_entity_id"], "p1_thm_001")

        # Test restore from dictionary
        restored = ExtractedRelation.from_dict(rel_dict)
        self.assertEqual(restored.relation_id, "rel_001")
        self.assertEqual(restored.relation_type, RelationType.USES_DEFINITION)

    def test_relation_invalid_creation(self) -> None:
        with self.assertRaises(ValueError):
            ExtractedRelation(
                relation_id="",
                relation_type=RelationType.DEPENDS_ON,
                source_entity_id="e1",
                target_entity_id="e2",
            )

        with self.assertRaises(ValueError):
            ExtractedRelation(
                relation_id="r1",
                relation_type=RelationType.DEPENDS_ON,
                source_entity_id="e1",
                target_entity_id="e2",
                confidence=1.5,  # Invalid confidence > 1.0
            )


class TestRelationExtractor(unittest.TestCase):
    """Test suite for RelationExtractor rules and interface compliance."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.sample_path = Path("exports/parser_outputs/paper_6cd768c13674.json")
        if not cls.sample_path.is_file():
            cls.skipTest(cls, f"Sample parsed JSON not found at {cls.sample_path}")

    def setUp(self) -> None:
        self.extractor = RelationExtractor()

    def test_interface_compliance(self) -> None:
        self.assertIsInstance(self.extractor, BaseRelationExtractor)

    def test_extracted_rule_patterns(self) -> None:
        # Create mock entities representing Definition 1.3, Lemma 2.1, Theorem 4, Theorem 5
        def1 = ExtractedEntity(
            entity_id="p1_def_001",
            entity_type=EntityType.DEFINITION,
            title="Definition 1.3",
            text="A topological space X is compact if every open cover has a finite subcover.",
            source_paper="Paper A",
        )
        lem1 = ExtractedEntity(
            entity_id="p1_lem_001",
            entity_type=EntityType.LEMMA,
            title="Lemma 2.1",
            text="Using Definition 1.3, we show that closed subsets of compact spaces are compact.",
            source_paper="Paper A",
        )
        thm1 = ExtractedEntity(
            entity_id="p1_thm_001",
            entity_type=EntityType.THEOREM,
            title="Theorem 3.2",
            text="Theorem 3.2 follows from Lemma 2.1.",
            source_paper="Paper A",
        )
        thm2 = ExtractedEntity(
            entity_id="p1_thm_002",
            entity_type=EntityType.THEOREM,
            title="Theorem 5",
            text="We extend Theorem 3.2 to Hausdorff spaces.",
            source_paper="Paper A",
        )
        prf1 = ExtractedEntity(
            entity_id="p1_prf_001",
            entity_type=EntityType.PROOF,
            title="Proof of Theorem 3.2",
            text="Proof of Theorem 3.2. Apply Lemma 2.1 directly.",
            source_paper="Paper A",
        )

        entities = [def1, lem1, thm1, thm2, prf1]
        relations = self.extractor.extract_relations(entities)

        self.assertGreater(len(relations), 0)

        # Check relation types extracted
        rel_types = {r.relation_type for r in relations}

        # 1. uses_definition: Lemma 2.1 using Definition 1.3
        self.assertIn(RelationType.USES_DEFINITION, rel_types)
        use_def_rel = next(r for r in relations if r.relation_type == RelationType.USES_DEFINITION)
        self.assertEqual(use_def_rel.source_entity_id, "p1_lem_001")
        self.assertEqual(use_def_rel.target_entity_id, "p1_def_001")

        # 2. depends_on: Theorem 3.2 follows from Lemma 2.1
        self.assertIn(RelationType.DEPENDS_ON, rel_types)
        dep_rel = next(r for r in relations if r.relation_type == RelationType.DEPENDS_ON)
        self.assertEqual(dep_rel.source_entity_id, "p1_thm_001")
        self.assertEqual(dep_rel.target_entity_id, "p1_lem_001")

        # 3. extends: Theorem 5 extends Theorem 3.2
        self.assertIn(RelationType.EXTENDS, rel_types)
        ext_rel = next(r for r in relations if r.relation_type == RelationType.EXTENDS)
        self.assertEqual(ext_rel.source_entity_id, "p1_thm_002")
        self.assertEqual(ext_rel.target_entity_id, "p1_thm_001")

        # 4. proves: Proof of Theorem 3.2
        self.assertIn(RelationType.PROVES, rel_types)
        prf_rel = next(r for r in relations if r.relation_type == RelationType.PROVES)
        self.assertEqual(prf_rel.source_entity_id, "p1_prf_001")
        self.assertEqual(prf_rel.target_entity_id, "p1_thm_001")

    def test_extract_from_file(self) -> None:
        entities, relations = self.extractor.extract_from_file(self.sample_path)
        self.assertIsInstance(entities, list)
        self.assertIsInstance(relations, list)
        for rel in relations:
            self.assertIsInstance(rel, ExtractedRelation)
            self.assertTrue(rel.relation_id)
            self.assertTrue(rel.source_entity_id)
            self.assertTrue(rel.target_entity_id)


if __name__ == "__main__":
    unittest.main()
