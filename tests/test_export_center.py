"""Unit test suite for Day 6 Step 8: Export Center UI page."""

from __future__ import annotations

import pytest
import streamlit as st

from src.application.document_service import DocumentService
from src.application.export_service import ExportService
from src.ui.pages import export
from src.ui.state import get_export_service, init_session_state


class TestExportCenterPageHelpers:
    """Test cases for helper functions in Export Center page."""

    def test_get_mime_type(self):
        assert export.get_mime_type("markdown") == "text/markdown"
        assert export.get_mime_type("json") == "application/json"
        assert export.get_mime_type("csv") == "text/csv"
        assert export.get_mime_type("pdf") == "application/pdf"

    def test_format_bytes_to_kb(self):
        assert export.format_bytes_to_kb(450) == "450 B"
        assert export.format_bytes_to_kb(2048) == "2.0 KB"
        assert export.format_bytes_to_kb(1024 * 1024 * 3) == "3.00 MB"


class TestExportCenterPageRendering:
    """Test cases for rendering Export Center page views."""

    def test_render_export_page_empty(self, tmp_path):
        init_session_state()
        doc_service = DocumentService(upload_dir=tmp_path / "uploads", parsed_dir=tmp_path / "parsed")
        export_service = ExportService(export_dir=tmp_path / "exports")

        st.session_state["doc_service"] = doc_service
        st.session_state["export_service"] = export_service

        # Should render empty export page without throwing exception
        export.render_export_page()

    def test_render_export_page_populated(self, tmp_path):
        init_session_state()
        doc_service = DocumentService(upload_dir=tmp_path / "uploads", parsed_dir=tmp_path / "parsed")
        export_service = ExportService(export_dir=tmp_path / "exports")

        st.session_state["doc_service"] = doc_service
        st.session_state["export_service"] = export_service

        mock_paper = {
            "paper_id": "paper_export_test_01",
            "metadata": {"title": "Export Test Paper", "authors": ["A. Tester"], "year": 2024},
            "sections": [
                {
                    "section_id": "s1",
                    "heading": "1. Intro",
                    "page_start": 1,
                    "page_end": 3,
                    "text": "Definition 1.1 (Test). Sample definition.",
                    "section_type": "definition",
                }
            ],
            "equations": [],
            "references": [],
            "source_file": {"file_name": "test.pdf", "file_path": "uploads/test.pdf"},
            "math_entities": {
                "definitions": [{"id": "d1", "title": "Definition 1.1 (Test)"}],
                "theorems": [],
                "lemmas": [],
                "corollaries": [],
                "proofs": [],
            },
        }

        doc_service.store_paper(mock_paper)

        # Should render populated export controls & preview without throwing exception
        export.render_export_page()


class TestExportServiceStateIntegration:
    """Test cases for ExportService session state integration."""

    def test_get_export_service_initialization(self, tmp_path):
        init_session_state()
        st.session_state["export_service"] = None

        exp_svc = get_export_service()
        assert isinstance(exp_svc, ExportService)
