"""Unit tests for Day 4 Step 2 Mathematical Entity Extraction pipeline."""

import unittest
from pathlib import Path

from src.graph.entity_extraction import (
    EntityExtractor,
    EntityType,
    ExtractedEntity,
)


class TestExtractedEntityModel(unittest.TestCase):
    """Test suite for ExtractedEntity data model and serialization."""

    def test_entity_creation_and_validation(self) -> None:
        entity = ExtractedEntity(
            entity_id="paper_01_def_001",
            entity_type=EntityType.DEFINITION,
            title="Definition 1.1",
            text="Let X be a topological space.",
            source_paper="paper_01.pdf",
            section_id="s1",
            section_title="Preliminaries",
            page_start=1,
            page_end=2,
            symbols=["X"],
            references=["[1]"],
            dependencies=[],
        )

        self.assertEqual(entity.entity_id, "paper_01_def_001")
        self.assertEqual(entity.entity_type, EntityType.DEFINITION)
        self.assertEqual(entity.symbols, ["X"])
        self.assertEqual(entity.dependencies, [])

        # Test dictionary conversion
        entity_dict = entity.to_dict()
        self.assertEqual(entity_dict["entity_type"], "definition")
        self.assertEqual(entity_dict["title"], "Definition 1.1")

        # Test restore from dictionary
        restored = ExtractedEntity.from_dict(entity_dict)
        self.assertEqual(restored.entity_id, "paper_01_def_001")
        self.assertEqual(restored.entity_type, EntityType.DEFINITION)

    def test_entity_invalid_creation(self) -> None:
        with self.assertRaises(ValueError):
            ExtractedEntity(
                entity_id="",
                entity_type=EntityType.THEOREM,
                title="Theorem 1",
                text="Some text",
                source_paper="p1",
            )

        with self.assertRaises(TypeError):
            ExtractedEntity(
                entity_id="id_001",
                entity_type=EntityType.THEOREM,
                title="Theorem 1",
                text=12345,  # type: ignore
                source_paper="p1",
            )


class TestEntityExtractor(unittest.TestCase):
    """Test suite for EntityExtractor functionality."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.sample_path = Path("exports/parser_outputs/paper_6cd768c13674.json")
        if not cls.sample_path.is_file():
            cls.skipTest(cls, f"Sample parsed JSON not found at {cls.sample_path}")

    def setUp(self) -> None:
        self.extractor = EntityExtractor()

    def test_extract_symbols(self) -> None:
        text = r"Let $f: X \to Y$ be a continuous map where \alpha is real and \[ E = mc^2 \]."
        symbols = self.extractor.extract_symbols(text)
        self.assertIn(r"$f: X \to Y$", symbols)
        self.assertIn(r"\alpha", symbols)
        self.assertIn(r"\[ E = mc^2 \]", symbols)

    def test_extract_references(self) -> None:
        text = "As shown in [1] and Devlin et al. (2019), the method improves performance [2, 3]."
        refs = self.extractor.extract_references(text)
        self.assertIn("[1]", refs)
        self.assertIn("Devlin et al. (2019)", refs)
        self.assertIn("[2, 3]", refs)

    def test_extract_from_mock_document(self) -> None:
        doc = {
            "paper_id": "paper_mock_123",
            "title": "A Mock Paper on Geometry",
            "sections": [
                {
                    "section_id": "s1",
                    "heading": "Introduction & Definitions",
                    "page_start": 1,
                    "page_end": 2,
                    "text": (
                        "Definition 1. A manifold is smooth if transition maps are C-infinity.\n"
                        "Example 1. The n-sphere is a smooth manifold.\n"
                        "Remark 2.1. Note that topological spaces need not be Hausdorff."
                    ),
                }
            ],
            "definitions": [
                {
                    "def_id": "def_001",
                    "label": "Definition 1",
                    "text": "A manifold is smooth if transition maps are C-infinity.",
                    "section_id": "s1",
                    "page": 1,
                }
            ],
            "theorems": [
                {
                    "thm_id": "thm_001",
                    "label": "Theorem 1",
                    "text": "Every compact manifold has finite dimensional de Rham cohomology.",
                    "section_id": "s1",
                    "page": 2,
                }
            ],
            "lemmas": [],
            "corollaries": [],
            "proofs": [
                {
                    "proof_id": "prf_001",
                    "related_to": {"theorem_id": "thm_001"},
                    "text": "Proof. Use Mayer-Vietoris sequences and mathematical induction.",
                    "section_id": "s1",
                    "page": 2,
                }
            ],
        }

        extracted = self.extractor.extract_from_document(doc)
        self.assertGreater(len(extracted), 0)

        # Verify structured entity types
        types_extracted = {e.entity_type for e in extracted}
        self.assertIn(EntityType.DEFINITION, types_extracted)
        self.assertIn(EntityType.THEOREM, types_extracted)
        self.assertIn(EntityType.PROOF, types_extracted)
        self.assertIn(EntityType.EXAMPLE, types_extracted)
        self.assertIn(EntityType.REMARK, types_extracted)

        # Check entity fields
        first_def = next(e for e in extracted if e.entity_type == EntityType.DEFINITION)
        self.assertEqual(first_def.section_id, "s1")
        self.assertEqual(first_def.section_title, "Introduction & Definitions")
        self.assertEqual(first_def.source_paper, "A Mock Paper on Geometry")
        self.assertEqual(first_def.dependencies, [])

    def test_extract_from_file(self) -> None:
        extracted = self.extractor.extract_from_file(self.sample_path)
        self.assertIsInstance(extracted, list)
        for entity in extracted:
            self.assertIsInstance(entity, ExtractedEntity)
            self.assertTrue(entity.entity_id)
            self.assertTrue(entity.text)
            self.assertEqual(entity.dependencies, [])


if __name__ == "__main__":
    unittest.main()
