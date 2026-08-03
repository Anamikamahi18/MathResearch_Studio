"""Unit tests for parser section detection taxonomy and behavior."""

from __future__ import annotations

import unittest
from pathlib import Path

from src.parser.pdf_loader.service import load_pdf
from src.parser.section_detector.service import (
    _detect_heading,
    detect_sections,
)


class TestSectionDetector(unittest.TestCase):
    """Validate section heading classification and segmentation."""

    SAMPLE_PAPERS_DIR = Path("tests/sample_papers")

    def test_synthetic_taxonomy_headings(self) -> None:
        """Requested math-paper section classes are recognized."""
        expected = {
            "Abstract": "abstract",
            "1 Introduction": "introduction",
            "2 Preliminaries": "preliminaries",
            "3 Definitions": "definitions",
            "4 Lemmas": "lemmas",
            "5 Theorems": "theorems",
            "6 Proofs": "proofs",
            "7 Results": "results",
            "8 Conclusion": "conclusion",
            "References": "references",
        }

        for heading, section_type in expected.items():
            (
                is_heading,
                _,
                _,
                actual_type,
                confidence,
            ) = _detect_heading(heading)
            self.assertTrue(is_heading, msg=f"Expected heading: {heading}")
            self.assertEqual(section_type, actual_type)
            self.assertGreaterEqual(confidence, 0.9)

    def test_non_heading_noise_lines_rejected(self) -> None:
        """Common noisy lines should not be treated as headings."""
        noise_lines = [
            "Patrick Lewis, Ethan Perez, Aleksandra Piktus",
            "This paper introduces a retrieval augmented model for QA.",
            "https://arxiv.org/abs/2005.11401",
        ]

        for line in noise_lines:
            (
                is_heading,
                _,
                _,
                section_type,
                confidence,
            ) = _detect_heading(line)
            self.assertFalse(is_heading, msg=f"Unexpected heading: {line}")
            self.assertIsNone(section_type)
            self.assertEqual(confidence, 0.0)

    def test_detect_sections_hierarchy_and_types(self) -> None:
        """Hierarchy and section labels should be assigned
        deterministically."""
        pages = [
            {
                "page": 1,
                "text": "\n".join(
                    [
                        "1 Introduction",
                        "Intro text.",
                        "1.1 Preliminaries",
                        "Prelim text.",
                        "1.2 Definitions",
                        "Definition text.",
                        "2 Theorems",
                        "Theorem text.",
                        "3 References",
                        "[1] Ref.",
                    ]
                ),
            }
        ]

        sections = detect_sections(pages)
        by_heading = {section["heading"]: section for section in sections}

        self.assertEqual(
            by_heading["Introduction"]["section_type"],
            "introduction",
        )
        self.assertEqual(
            by_heading["Preliminaries"]["section_type"],
            "preliminaries",
        )
        self.assertEqual(
            by_heading["Definitions"]["section_type"],
            "definitions",
        )
        self.assertEqual(
            by_heading["Theorems"]["section_type"],
            "theorems",
        )
        self.assertEqual(
            by_heading["References"]["section_type"],
            "references",
        )

        intro_id = by_heading["Introduction"]["section_id"]
        self.assertEqual(
            by_heading["Preliminaries"]["parent_section_id"],
            intro_id,
        )
        self.assertEqual(
            by_heading["Definitions"]["parent_section_id"],
            intro_id,
        )

    def test_real_sample_has_core_sections_and_reasonable_count(self) -> None:
        """Real sample parse should include key sections without
        over-segmentation."""
        doc = load_pdf(Path("tests/sample_papers/paper_01_rag.pdf"))
        sections = detect_sections(doc["pages"])
        types = {section.get("section_type", "other") for section in sections}

        self.assertIn("abstract", types)
        self.assertIn("introduction", types)
        self.assertIn("references", types)
        self.assertLessEqual(len(sections), 40)

    def test_all_sample_papers_have_core_section_types(self) -> None:
        """All sample PDFs should expose stable core section types."""
        sample_files = sorted(self.SAMPLE_PAPERS_DIR.glob("*.pdf"))
        self.assertEqual(len(sample_files), 5)

        corpus_types: set[str] = set()
        for sample_file in sample_files:
            doc = load_pdf(sample_file)
            sections = detect_sections(doc["pages"])
            types = {
                section.get("section_type", "other") for section in sections
                }

            self.assertIn("abstract", types, msg=sample_file.name)
            self.assertIn("introduction", types, msg=sample_file.name)
            self.assertIn("references", types, msg=sample_file.name)
            self.assertLessEqual(len(sections), 40, msg=sample_file.name)

            corpus_types.update(types)

        self.assertIn("results", corpus_types)
        self.assertIn("conclusion", corpus_types)


if __name__ == "__main__":
    unittest.main()
