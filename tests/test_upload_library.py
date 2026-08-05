"""Unit test suite for Day 6 Step 2: PDF Upload and Document Library pages."""

from __future__ import annotations

import pytest
import streamlit as st

from src.application.document_service import DocumentService
from src.ui.pages import library, upload
from src.ui.state import init_session_state, get_document_service


@pytest.fixture
def mock_paper_summary() -> dict:
    """Fixture providing a sample paper summary dictionary."""
    return {
        "paper_id": "paper_algebra_01",
        "title": "Abstract Algebra and Group Theory",
        "authors": ["E. Galois"],
        "year": 1832,
        "section_count": 3,
        "chunk_count": 5,
        "equation_count": 2,
        "reference_count": 1,
        "raw_document": {
            "paper_id": "paper_algebra_01",
            "metadata": {
                "title": "Abstract Algebra and Group Theory",
                "authors": ["E. Galois"],
                "year": 1832,
            },
            "source_file": {
                "file_name": "galois_algebra.pdf",
            },
            "sections": [
                {
                    "heading": "Abstract",
                    "text": "This paper presents foundational concepts of group theory.",
                }
            ],
            "math_entities": {
                "definitions": [{"id": "d1"}, {"id": "d2"}],
                "theorems": [{"id": "t1"}],
                "lemmas": [{"id": "l1"}],
                "proofs": [{"id": "p1"}],
            },
        },
    }


class TestUploadAndLibraryHelpers:
    """Test cases for helper functions in Upload and Library pages."""

    def test_format_file_size(self):
        assert upload.format_file_size(500) == "0.5 KB"
        assert upload.format_file_size(1024 * 1024 * 2) == "2.00 MB"

    def test_filter_papers_by_keyword(self, mock_paper_summary: dict):
        papers = [mock_paper_summary]

        # Match title
        assert len(library.filter_papers_by_keyword(papers, "Algebra")) == 1

        # Match author
        assert len(library.filter_papers_by_keyword(papers, "Galois")) == 1

        # Match filename
        assert len(library.filter_papers_by_keyword(papers, "galois_algebra")) == 1

        # Case insensitive match
        assert len(library.filter_papers_by_keyword(papers, "GROUP")) == 1

        # Non-matching keyword
        assert len(library.filter_papers_by_keyword(papers, "Calculus")) == 0

    def test_count_math_entity_type(self, mock_paper_summary: dict):
        assert library.count_math_entity_type(mock_paper_summary, "definitions") == 2
        assert library.count_math_entity_type(mock_paper_summary, "theorems") == 1
        assert library.count_math_entity_type(mock_paper_summary, "lemmas") == 1
        assert library.count_math_entity_type(mock_paper_summary, "proofs") == 1


class TestUploadAndLibraryPages:
    """Test cases for rendering Upload and Library pages."""

    def test_render_upload_page(self):
        init_session_state()
        # Should render without raising exception
        upload.render_upload_page()

    def test_render_library_page(self, tmp_path):
        init_session_state()
        doc_service = DocumentService(upload_dir=tmp_path / "uploads", parsed_dir=tmp_path / "parsed")
        st.session_state["doc_service"] = doc_service

        # Should render empty state without raising exception
        library.render_library_page()

    def test_delete_paper(self, tmp_path, mock_paper_summary):
        doc_service = DocumentService(upload_dir=tmp_path / "uploads", parsed_dir=tmp_path / "parsed")
        paper_id = mock_paper_summary["paper_id"]
        doc_service._paper_library[paper_id] = mock_paper_summary
        assert doc_service.get_paper(paper_id) is not None

        # Delete paper
        assert doc_service.delete_paper(paper_id) is True
        assert doc_service.get_paper(paper_id) is None
        assert doc_service.delete_paper(paper_id) is False
