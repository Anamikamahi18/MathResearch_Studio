"""Unit tests for parser JSON export schema guarantees."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.parser.json_export.service import (
    build_parsed_document,
    normalize_document_schema,
    validate_document_schema,
    write_json_output,
)


class TestJsonExport(unittest.TestCase):
    """Validate normalized schema output for NLP and RAG consumers."""

    def test_normalize_document_schema_populates_defaults(self) -> None:
        """Missing optional keys should be populated with schema defaults."""
        document = {
            "paper_id": "paper_test_001",
            "source_file": {
                "file_name": "sample.pdf",
                "file_path": "tests/sample_papers/sample.pdf",
                "file_hash": "abc123",
                "ingested_at": "2026-08-03T00:00:00Z",
            },
            "title": "Sample",
            "abstract": "Short abstract",
            "metadata": {"parser_version": "0.1.0"},
        }

        normalized = normalize_document_schema(document)

        self.assertEqual(normalized["schema_version"], "1.0")
        self.assertEqual(normalized["paper_id"], "paper_test_001")
        self.assertIsInstance(normalized["sections"], list)
        self.assertIsInstance(normalized["definitions"], list)
        self.assertIsInstance(normalized["theorems"], list)
        self.assertIsInstance(normalized["references"], list)
        self.assertIsInstance(normalized["metadata"], dict)

    def test_build_parsed_document_maps_entities(self) -> None:
        """Entity groups should be mapped into schema arrays."""
        entities = {
            "definitions": [{"definition_id": "definition_001", "text": "d"}],
            "theorems": [{"theorem_id": "theorem_001", "text": "t"}],
            "lemmas": [{"lemma_id": "lemma_001", "text": "l"}],
            "corollaries": [{"corollary_id": "corollary_001", "text": "c"}],
            "proofs": [{"proof_id": "proof_001", "text": "p"}],
        }

        document = build_parsed_document(
            paper_id="paper_test_002",
            source_file={
                "file_name": "s.pdf",
                "file_path": "tests/sample_papers/s.pdf",
                "file_hash": "def456",
                "ingested_at": "2026-08-03T00:00:00Z",
            },
            title="Title",
            authors=[{"name": "A", "affiliation": None, "email": None}],
            abstract="Abstract",
            keywords=["math"],
            sections=[{"section_id": "s1", "heading": "Intro"}],
            entities=entities,
            references=[{"reference_id": "r1", "raw_text": "Ref"}],
            equations=[{"equation_id": "e1", "text_repr": "x+y"}],
            metadata={"parser_version": "0.1.0"},
        )

        self.assertEqual(document["definitions"], entities["definitions"])
        self.assertEqual(document["theorems"], entities["theorems"])
        self.assertEqual(document["lemmas"], entities["lemmas"])
        self.assertEqual(document["corollaries"], entities["corollaries"])
        self.assertEqual(document["proofs"], entities["proofs"])

    def test_validate_document_schema_rejects_missing_paper_id(self) -> None:
        """Validation should fail when paper_id is missing or empty."""
        normalized = normalize_document_schema(
            {
                "paper_id": "",
                "source_file": {},
                "title": "Title",
                "metadata": {},
            }
        )

        with self.assertRaises(ValueError):
            validate_document_schema(normalized)

    def test_normalize_document_schema_rejects_bad_metadata_types(
        self,
    ) -> None:
        """Malformed numeric metadata should fail fast during normalization."""
        document = {
            "paper_id": "paper_test_004",
            "source_file": {
                "file_name": "sample.pdf",
                "file_path": "tests/sample_papers/sample.pdf",
                "file_hash": "xyz123",
                "ingested_at": "2026-08-03T00:00:00Z",
            },
            "title": "Sample",
            "abstract": "A",
            "metadata": {
                "extraction_confidence": "not-a-float",
                "page_count": "not-an-int",
            },
        }

        with self.assertRaises(ValueError):
            normalize_document_schema(document)

    def test_write_json_output_persists_normalized_document(self) -> None:
        """Written output should be normalized and valid JSON."""
        document = {
            "paper_id": "paper_test_003",
            "source_file": {
                "file_name": "sample.pdf",
                "file_path": "tests/sample_papers/sample.pdf",
                "file_hash": "ghi789",
                "ingested_at": "2026-08-03T00:00:00Z",
            },
            "title": "Sample",
            "abstract": "A",
            "keywords": "single-keyword",
            "metadata": {},
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = write_json_output(document, Path(tmp_dir))
            payload = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertEqual(payload["paper_id"], "paper_test_003")
        self.assertEqual(payload["keywords"], ["single-keyword"])
        self.assertIn("sections", payload)
        self.assertIn("metadata", payload)


if __name__ == "__main__":
    unittest.main()
