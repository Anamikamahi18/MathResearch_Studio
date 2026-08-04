#!/usr/bin/env python3
"""Verification script for Day 5 Step 4.5: Evidence Mapping Layer."""

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
from src.rag.evidence import EvidenceMapper
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
            matched_entities=["Hilbert-Schmidt Operator", "Definition 2.1"],
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
            matched_entities=["Theorem 3", "Spectral Decomposition"],
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
            matched_entities=["Lemma 3.1"],
            explanation=RetrievalExplanation(
                semantic_score=0.81, entity_score=1.0, intent_score=0.8, graph_score=1.0, boost_score=0.8, final_score=0.885
            ),
        ),
    ]


def main() -> None:
    """Run verification for EvidenceMapper across 5 benchmark query intents."""
    print("\n============================================================")
    print(" DAY 5 STEP 4.5: EVIDENCE MAPPING VERIFICATION")
    print("============================================================\n")

    query_processor = QueryProcessor()
    prompt_builder = PromptBuilder()
    answer_generator = AnswerGenerator()
    evidence_mapper = EvidenceMapper()

    candidates = create_sample_retrieval_candidates()

    benchmark_queries = [
        ("Definition Query", "What is Definition 2.1?"),
        ("Theorem Query", "What does Theorem 3 state?"),
        ("Dependency Query", "Which lemma proves theorem 3?"),
        ("Summary Query", "Summarize the paper."),
        ("Notation Query", "Show notation for λ."),
    ]

    for label, query_str in benchmark_queries:
        # Step 1: Processing & Generation Pipeline
        analysis = query_processor.process(query_str)
        prompt_req = PromptRequest(query=analysis, retrieval_response=candidates, max_context_tokens=300)
        prompt_resp = prompt_builder.build_prompt(prompt_req)
        answer_resp = answer_generator.generate_answer(prompt_resp)

        # Step 2: Evidence Mapping Execution
        bundle = evidence_mapper.map_evidence(answer_response=answer_resp, retrieval_response=candidates)

        print("-" * 60)
        print(f"[{label}] Query: '{query_str}'")
        print(f"Total Sentences:    {bundle.total_sentence_count}")
        print(f"Supported Sentences:{bundle.supported_sentence_count}")
        print(f"Coverage Score:     {bundle.coverage_score:.2%}")
        print(f"Avg Alignment:      {bundle.metadata.average_alignment_score:.4f}")
        print(f"Direct Support:     {bundle.metadata.direct_support_count}")
        print(f"Partial Support:    {bundle.metadata.partial_support_count}")
        print(f"Weak Support:       {bundle.metadata.weak_support_count}")
        print(f"No Support:         {bundle.metadata.no_support_count}")
        print(f"Unused Chunks:      {bundle.unused_chunks}")

        print("\n--- SENTENCE ALIGNMENT SPANS ---")
        for span in bundle.spans[:4]:  # Show first 4 spans
            sent_disp = span.sentence_text[:70] + "..." if len(span.sentence_text) > 70 else span.sentence_text
            print(f"[{span.sentence_index}] Level: {span.support_level:7s} | Score: {span.alignment_score:.4f} | Type: {span.support_type:15s} | Chunks: {span.supported_by_chunks}")
            print(f"    Text: \"{sent_disp}\"")
        print("-" * 60 + "\n")

    print("============================================================")
    print(" EVIDENCE MAPPING VERIFICATION COMPLETE")
    print("============================================================\n")


if __name__ == "__main__":
    main()
