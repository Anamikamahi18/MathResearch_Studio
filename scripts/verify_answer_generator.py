#!/usr/bin/env python3
"""Verification script for Day 5 Step 4: Answer Generator Layer."""

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

from src.rag.answer_generator import AnswerGenerator
from src.rag.prompt_builder import PromptBuilder, PromptRequest
from src.rag.query_processing import QueryProcessor
from src.rag.retrieval.models import RetrievalExplanation, RetrievalResult

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def create_sample_retrieval_candidates() -> list[RetrievalResult]:
    """Create sample mathematical retrieval candidate results."""
    return [
        RetrievalResult(
            chunk_id="paper1_def_2.1",
            text="Definition 2.1 (Hilbert-Schmidt Operator). An operator T on a Hilbert space H is Hilbert-Schmidt if sum_i ||T e_i||^2 < infinity.",
            paper_id="paper_spectral_01",
            paper_title="Spectral Theory of Hilbert Space Operators",
            section_title="2. Basic Definitions",
            section_type="definition",
            semantic_score=0.8900,
            final_score=0.9450,
            explanation=RetrievalExplanation(
                semantic_score=0.89, entity_score=1.0, intent_score=1.0, graph_score=0.5, boost_score=1.0, final_score=0.945
            ),
        ),
        RetrievalResult(
            chunk_id="paper1_thm_3",
            text="Theorem 3 (Spectral Decomposition). Let T be a compact self-adjoint operator on H. Then T = sum_k lambda_k P_k where lambda_k are real eigenvalues.",
            paper_id="paper_spectral_01",
            paper_title="Spectral Theory of Hilbert Space Operators",
            section_title="3. Main Theorems",
            section_type="theorem",
            semantic_score=0.8500,
            final_score=0.9200,
            explanation=RetrievalExplanation(
                semantic_score=0.85, entity_score=1.0, intent_score=1.0, graph_score=0.8, boost_score=1.0, final_score=0.920
            ),
        ),
        RetrievalResult(
            chunk_id="paper1_lem_3.1",
            text="Lemma 3.1 (Eigenvalue Boundedness). If T is a compact operator on H, then its sequence of non-zero eigenvalues converges to 0.",
            paper_id="paper_spectral_01",
            paper_title="Spectral Theory of Hilbert Space Operators",
            section_title="3. Main Theorems",
            section_type="lemma",
            semantic_score=0.8100,
            final_score=0.8850,
            explanation=RetrievalExplanation(
                semantic_score=0.81, entity_score=1.0, intent_score=0.8, graph_score=1.0, boost_score=0.8, final_score=0.885
            ),
        ),
        RetrievalResult(
            chunk_id="paper1_sec_notation",
            text="Notation: We write sigma(T) for the spectrum of T, and lambda in C for eigenvalues. <x, y> denotes the inner product.",
            paper_id="paper_spectral_01",
            paper_title="Spectral Theory of Hilbert Space Operators",
            section_title="1. Introduction & Notation",
            section_type="notation",
            semantic_score=0.7800,
            final_score=0.8600,
            explanation=RetrievalExplanation(
                semantic_score=0.78, entity_score=0.8, intent_score=1.0, graph_score=0.2, boost_score=0.8, final_score=0.860
            ),
        ),
        RetrievalResult(
            chunk_id="paper1_abstract",
            text="Abstract: This paper presents fundamental results on Hilbert space operators, spectral decompositions, and compact operator norms.",
            paper_id="paper_spectral_01",
            paper_title="Spectral Theory of Hilbert Space Operators",
            section_title="Abstract",
            section_type="summary",
            semantic_score=0.7500,
            final_score=0.8400,
            explanation=RetrievalExplanation(
                semantic_score=0.75, entity_score=0.5, intent_score=1.0, graph_score=0.1, boost_score=0.5, final_score=0.840
            ),
        ),
    ]


def main() -> None:
    """Run verification for AnswerGenerator across 5 benchmark query intents."""
    print("\n============================================================")
    print(" DAY 5 STEP 4: ANSWER GENERATOR VERIFICATION")
    print("============================================================\n")

    query_processor = QueryProcessor()
    prompt_builder = PromptBuilder()
    answer_generator = AnswerGenerator()

    candidates = create_sample_retrieval_candidates()

    benchmark_queries = [
        ("Definition Query", "What is Definition 2.1?"),
        ("Theorem Query", "What does Theorem 3 state?"),
        ("Dependency Query", "Which lemma proves theorem 3?"),
        ("Summary Query", "Summarize the paper."),
        ("Notation Query", "Show notation for λ."),
    ]

    for label, query_str in benchmark_queries:
        # Step 1: Query Analysis
        analysis = query_processor.process(query_str)
        # Step 2: Prompt Construction
        prompt_req = PromptRequest(query=analysis, retrieval_response=candidates, max_context_tokens=300)
        prompt_resp = prompt_builder.build_prompt(prompt_req)
        # Step 3: Answer Generation
        answer_resp = answer_generator.generate_answer(prompt_resp)

        print("-" * 60)
        print(f"[{label}] Query: '{query_str}'")
        print(f"Intent:            {analysis.intent.value.upper()}")
        print(f"Provider / Model:  {answer_resp.metadata.provider} / {answer_resp.metadata.model}")
        print(f"Confidence Score:  {answer_resp.metadata.confidence_score:.2f}")
        print(f"Total Tokens:      {answer_resp.metadata.total_tokens}")
        print(f"Warnings ({len(answer_resp.warnings)}):     {answer_resp.warnings}")
        print(f"Sections ({len(answer_resp.sections)}):     {[s.title for s in answer_resp.sections]}")

        print("\n--- FORMATTED ANSWER RESPONSE ---")
        answer_lines = answer_resp.formatted_answer.split("\n")
        snippet = "\n".join(answer_lines[:25])
        print(snippet)
        if len(answer_lines) > 25:
            print("... [Remaining formatted answer lines truncated for display] ...")
        print("-" * 60 + "\n")

    print("============================================================")
    print(" ANSWER GENERATOR VERIFICATION COMPLETE")
    print("============================================================\n")


if __name__ == "__main__":
    main()
