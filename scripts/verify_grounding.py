#!/usr/bin/env python3
"""Verification script for Day 5 Step 5.5: Grounding Verification Layer."""

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
from src.rag.citation_engine import CitationEngine
from src.rag.evidence import EvidenceMapper
from src.rag.grounding import GroundingVerifier
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
    """Run verification for GroundingVerifier across 5 benchmark query intents."""
    print("\n============================================================")
    print(" DAY 5 STEP 5.5: GROUNDING VERIFICATION LAYER VERIFICATION")
    print("============================================================\n")

    query_processor = QueryProcessor()
    prompt_builder = PromptBuilder()
    answer_generator = AnswerGenerator()
    evidence_mapper = EvidenceMapper()
    citation_engine = CitationEngine()
    grounding_verifier = GroundingVerifier()

    candidates = create_sample_retrieval_candidates()

    benchmark_queries = [
        ("Definition Query", "What is Definition 2.1?"),
        ("Theorem Query", "What does Theorem 3 state?"),
        ("Lemma Query", "Explain Lemma 3.1."),
        ("Summary Query", "Summarize the paper."),
        ("Notation Query", "Show notation for λ."),
    ]

    for label, query_str in benchmark_queries:
        # Full RAG pipeline execution up to Grounding
        analysis = query_processor.process(query_str)
        prompt_req = PromptRequest(query=analysis, retrieval_response=candidates, max_context_tokens=300)
        prompt_resp = prompt_builder.build_prompt(prompt_req)
        answer_resp = answer_generator.generate_answer(prompt_resp)
        evidence_bundle = evidence_mapper.map_evidence(answer_response=answer_resp, retrieval_response=candidates)
        citation_bundle = citation_engine.generate_citations(answer_response=answer_resp, evidence_bundle=evidence_bundle)

        # Step 5.5: Grounding Verification Execution
        report = grounding_verifier.verify_grounding(
            answer_response=answer_resp,
            evidence_bundle=evidence_bundle,
            citation_bundle=citation_bundle,
        )

        print("-" * 65)
        print(f"[{label}] Query: '{query_str}'")
        print(f"Grounding Score:         {report.grounding_score:.4f}")
        print(f"Supported Claim Ratio:   {report.supported_claim_ratio:.2%}")
        print(f"Unsupported Claim Ratio: {report.unsupported_claim_ratio:.2%}")
        print(f"Evidence Coverage:       {report.evidence_coverage:.2%}")
        print(f"Citation Coverage:       {report.citation_coverage:.2%}")
        print(f"Total Claims Evaluated:  {len(report.claims)}")
        print(f"Verification Time:       {report.metadata.verification_time_ms:.2f} ms")

        print("\n--- CLAIM VERIFICATION BREAKDOWN ---")
        for claim in report.claims[:4]:  # Show first 4 claims
            claim_disp = claim.claim_text[:65] + "..." if len(claim.claim_text) > 65 else claim.claim_text
            print(f"  [Claim #{claim.claim_id}] Level: {claim.support_level:11s} | Score: {claim.verification_score:.4f} | Citations: {claim.citation_ids}")
            print(f"    Text: \"{claim_disp}\"")

        print("\n--- GROUNDING WARNINGS ---")
        if report.warnings:
            for w in report.warnings[:3]:
                print(f"  ⚠️ Warning: {w}")
        else:
            print("  ✅ Zero grounding warnings. Answer fully grounded.")

        print("-" * 65 + "\n")

    print("============================================================")
    print(" GROUNDING VERIFICATION VERIFICATION COMPLETE")
    print("============================================================\n")


if __name__ == "__main__":
    main()
