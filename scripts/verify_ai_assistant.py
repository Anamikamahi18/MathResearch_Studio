#!/usr/bin/env python3
"""Verification script for Day 6 Step 4: AI Research Assistant UI."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.application.chat_service import ChatService
from src.application.document_service import DocumentService
from src.rag.guardrails import FinalResearchResponse
from src.ui.pages.assistant import render_decision_badge

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def create_mock_parsed_paper() -> dict:
    """Create mock parsed document dict for testing assistant RAG pipeline."""
    return {
        "paper_id": "paper_topology_002",
        "metadata": {
            "title": "Fixed Point Theorems in Metric Spaces",
            "authors": ["S. Banach"],
            "year": 1922,
            "source": "Fundamenta Mathematicae",
            "doi": "10.1000/fm.1922",
            "keywords": ["Fixed Point Theorem", "Metric Space", "Contraction Mapping"],
            "ingested_at": "2024-08-05T10:00:00Z",
        },
        "sections": [
            {
                "section_id": "s1",
                "heading": "1. Banach Fixed Point Theorem",
                "level": 1,
                "page_start": 1,
                "page_end": 4,
                "text": "Theorem 1.1 (Banach Fixed Point Theorem). Let (X, d) be a complete metric space and let T: X -> X be a contraction mapping. Then T has a unique fixed point x* in X.",
                "section_type": "theorem",
            },
        ],
        "equations": [],
        "references": [],
        "source_file": {
            "file_name": "banach_fixed_point.pdf",
            "file_path": "uploads/banach_fixed_point.pdf",
        },
        "math_entities": {
            "definitions": [],
            "theorems": [{"id": "thm_1.1", "title": "Theorem 1.1 (Banach Fixed Point Theorem)"}],
            "lemmas": [],
            "corollaries": [],
            "proofs": [],
        },
    }


def main() -> None:
    """Run verification for AI Assistant page integrations and ChatService."""
    print("\n============================================================")
    print(" DAY 6 STEP 4: AI RESEARCH ASSISTANT VERIFICATION")
    print("============================================================\n")

    doc_service = DocumentService(
        upload_dir="uploads",
        parsed_dir="exports/parser_outputs",
    )
    chat_service = ChatService(
        vector_store=doc_service.vector_store,
        graph_service=doc_service.graph_service,
    )

    sample_doc = create_mock_parsed_paper()

    # 1. Ingest document into vector store
    print("[1] Ingesting sample paper into FAISS vector store...")
    store_metrics = doc_service.store_paper(sample_doc)
    print(f"    Paper ID:           '{store_metrics['paper_id']}'")
    print(f"    Vector Chunks:      {store_metrics['chunk_count']}")

    # 2. Test Question Submission via ChatService.receive_question()
    print("\n[2] Submitting Research Question to ChatService...")
    question = "State the Banach Fixed Point Theorem."
    response = chat_service.receive_question(question=question, top_k=5)

    assert isinstance(response, FinalResearchResponse), "Expected FinalResearchResponse object"
    print(f"    Question:           '{response.question}'")
    print(f"    Decision:           {response.decision.value}")
    print(f"    Status:             {response.status.value}")
    print(f"    Confidence:         {response.confidence:.2f}")
    print(f"    Answer Preview:     '{response.answer_text[:120]}...'")

    # 3. Test Decision Badge Style Helper
    print("\n[3] Verifying Decision Badge Styling...")
    bg, fg, label = render_decision_badge("ACCEPT")
    assert label == "✅ Passed Guardrails"
    bg, fg, label = render_decision_badge("MODIFY")
    assert label == "⚠️ Modified / Caution"
    bg, fg, label = render_decision_badge("REJECT")
    assert label == "🛑 Rejected / Flagged"
    print("    Decision badge helper verified for ACCEPT, MODIFY, and REJECT")

    # 4. Test Conversation History Logging & Clearing
    print("\n[4] Verifying Q&A Conversation History...")
    history = chat_service.get_chat_history()
    print(f"    Conversation Turns Logged: {len(history)}")
    assert len(history) >= 1, "Expected at least 1 turn in conversation history"

    chat_service.clear_chat_history()
    cleared_history = chat_service.get_chat_history()
    print(f"    Cleared Conversation Turns: {len(cleared_history)}")
    assert len(cleared_history) == 0, "Expected conversation history to be cleared"

    print("\n============================================================")
    print(" VERIFICATION COMPLETED SUCCESSFULLY FOR AI ASSISTANT UI")
    print("============================================================\n")


if __name__ == "__main__":
    main()
