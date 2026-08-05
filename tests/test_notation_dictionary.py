"""Unit test suite for Day 6 Step 6: Notation Dictionary UI page."""

from __future__ import annotations

import pytest
import streamlit as st

from src.application.document_service import DocumentService
from src.application.graph_service import GraphService
from src.ui.pages import notation
from src.ui.state import get_document_service, get_graph_service, init_session_state


class TestNotationDictionaryPageHelpers:
    """Test cases for helper functions in Notation Dictionary page."""

    def test_classify_notation_category(self):
        assert notation.classify_notation_category({"label": "f(x)", "text": "Function mapping"}) == "Function"
        assert notation.classify_notation_category({"label": "Hilbert Space H", "text": "Set"}) == "Set"
        assert notation.classify_notation_category({"label": "Matrix M", "text": "Operator"}) == "Matrix"
        assert notation.classify_notation_category({"node_type": "concept", "label": "Entropy"}) == "Concept"

    def test_extract_all_notation_items(self):
        notation_graph = {
            "symbols": [{"node_id": "s1", "label": "Symbol 1"}],
            "concepts": [{"node_id": "c1", "label": "Concept 1"}],
            "equations": [],
        }
        all_nodes = [
            {"node_id": "s1", "label": "Symbol 1"},  # duplicate, should be skipped
            {"node_id": "d1", "node_type": "definition", "label": "Def 1"},
        ]

        items = notation.extract_all_notation_items(notation_graph, all_nodes)
        assert len(items) == 3
        node_ids = set(i["node_id"] for i in items)
        assert node_ids == {"s1", "c1", "d1"}


class TestNotationDictionaryPageRendering:
    """Test cases for rendering Notation Dictionary page views."""

    def test_render_notation_page_initial(self, tmp_path):
        init_session_state()
        doc_service = DocumentService(upload_dir=tmp_path / "uploads", parsed_dir=tmp_path / "parsed")
        graph_service = GraphService(backend_graph_service=doc_service.graph_service)
        st.session_state["doc_service"] = doc_service
        st.session_state["graph_service"] = graph_service

        # Should render empty dictionary view without throwing exception
        notation.render_notation_page()

    def test_render_notation_page_with_items(self, tmp_path):
        init_session_state()
        doc_service = DocumentService(upload_dir=tmp_path / "uploads", parsed_dir=tmp_path / "parsed")
        graph_service = GraphService(backend_graph_service=doc_service.graph_service)
        st.session_state["doc_service"] = doc_service
        st.session_state["graph_service"] = graph_service

        mock_paper = {
            "paper_id": "paper_test_02",
            "metadata": {"title": "Test Notation Paper", "authors": ["B. Author"], "year": 2024},
            "sections": [
                {
                    "section_id": "s1",
                    "heading": "1. Definitions",
                    "text": "Definition 1.1 (Function f). Let f: X -> Y be a mapping.",
                    "section_type": "definition",
                }
            ],
            "equations": [],
            "references": [],
            "source_file": {"file_name": "test.pdf", "file_path": "uploads/test.pdf"},
            "math_entities": {
                "definitions": [{"id": "d1", "title": "Definition 1.1 (Function f)"}],
                "theorems": [],
                "lemmas": [],
                "corollaries": [],
                "proofs": [],
            },
        }

        doc_service.store_paper(mock_paper)

        # Should render populated dictionary view without throwing exception
        notation.render_notation_page()
