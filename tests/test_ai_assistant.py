"""Unit test suite for Day 6 Step 4: AI Research Assistant UI page."""

from __future__ import annotations

import pytest
import streamlit as st

from src.application.chat_service import ChatService
from src.application.document_service import DocumentService
from src.rag.guardrails import FinalResearchResponse
from src.rag.guardrails.models import DecisionType, GuardrailStatus
from src.ui.pages import assistant
from src.ui.state import get_chat_service, get_document_service, init_session_state


class TestAIAssistantPageHelpers:
    """Test cases for helper functions in AI Assistant page."""

    def test_render_decision_badge(self):
        bg, fg, label = assistant.render_decision_badge("RETURN")
        assert label == "✅ Passed Guardrails"

        bg, fg, label = assistant.render_decision_badge("RETURN_WITH_WARNING")
        assert label == "⚠️ Return With Warning"

        bg, fg, label = assistant.render_decision_badge("REFUSE")
        assert label == "🛑 Refuse"


class TestAIAssistantPageRendering:
    """Test cases for rendering AI Assistant page views."""

    def test_render_assistant_page_initial(self, tmp_path):
        init_session_state()
        doc_service = DocumentService(upload_dir=tmp_path / "uploads", parsed_dir=tmp_path / "parsed")
        chat_service = ChatService(vector_store=doc_service.vector_store, graph_service=doc_service.graph_service)
        st.session_state["doc_service"] = doc_service
        st.session_state["chat_service"] = chat_service

        # Should render initial welcome view without throwing exception
        assistant.render_assistant_page()

    def test_render_assistant_page_with_active_response(self, tmp_path):
        init_session_state()
        doc_service = DocumentService(upload_dir=tmp_path / "uploads", parsed_dir=tmp_path / "parsed")
        chat_service = ChatService(vector_store=doc_service.vector_store, graph_service=doc_service.graph_service)
        st.session_state["doc_service"] = doc_service
        st.session_state["chat_service"] = chat_service

        mock_response = FinalResearchResponse(
            question="What is a Hilbert Space?",
            answer_text="A Hilbert space is a complete inner product space.",
            decision=DecisionType.RETURN,
            status=GuardrailStatus.PASS,
            reason="Answer is fully grounded in retrieved evidence.",
            citations=["[1] Spectral Theory, p. 12"],
            bibliography=["[1] E. Galois. Spectral Theory. 1832."],
            warnings=[],
            confidence=0.95,
            metadata={
                "retrieved_candidates": [
                    {
                        "chunk_id": "c1",
                        "score": 0.88,
                        "text": "A Hilbert space H is a complete inner product space.",
                        "paper_id": "p1",
                        "paper_title": "Spectral Theory",
                        "section_title": "1. Definitions",
                        "page_start": 12,
                    }
                ]
            },
        )

        st.session_state["active_assistant_question"] = "What is a Hilbert Space?"
        st.session_state["active_assistant_duration_ms"] = 120
        st.session_state["active_assistant_response"] = mock_response

        # Should render active response view without throwing exception
        assistant.render_assistant_page()


class TestChatServiceStateIntegration:
    """Test cases for ChatService session state integration."""

    def test_get_chat_service_initialization(self, tmp_path):
        init_session_state()
        doc_service = DocumentService(upload_dir=tmp_path / "uploads", parsed_dir=tmp_path / "parsed")
        st.session_state["doc_service"] = doc_service
        st.session_state["chat_service"] = None

        chat_svc = get_chat_service()
        assert isinstance(chat_svc, ChatService)
        assert chat_svc.vector_store == doc_service.vector_store
        assert chat_svc.graph_service == doc_service.graph_service
