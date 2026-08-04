#!/usr/bin/env python3
"""Verification script for Day 5 Step 6: Guardrails Layer."""

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
from src.rag.evidence import EvidenceMapper, EvidenceBundle, EvidenceMetadata
from src.rag.grounding import GroundingVerifier, GroundingReport, GroundingMetadata, Claim
from src.rag.guardrails import DecisionType, GuardrailConfig, GuardrailDecisionEngine
from src.rag.prompt_builder import PromptBuilder, PromptRequest
from src.rag.query_processing import QueryProcessor, QueryAnalysis, QueryIntent
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
    ]


def main() -> None:
    """Run verification for GuardrailDecisionEngine across 6 benchmark research scenarios."""
    print("\n============================================================")
    print(" DAY 5 STEP 6: GUARDRAILS LAYER VERIFICATION")
    print("============================================================\n")

    query_processor = QueryProcessor()
    prompt_builder = PromptBuilder()
    answer_generator = AnswerGenerator()
    evidence_mapper = EvidenceMapper()
    citation_engine = CitationEngine()
    grounding_verifier = GroundingVerifier()
    decision_engine = GuardrailDecisionEngine()

    candidates = create_sample_retrieval_candidates()

    # Scenario 1: High Confidence Definition Query
    print("-" * 65)
    print("[Scenario 1] High Confidence Definition Query ('What is Definition 2.1?')")
    analysis = query_processor.process("What is Definition 2.1?")
    prompt_req = PromptRequest(query=analysis, retrieval_response=candidates, max_context_tokens=300)
    prompt_resp = prompt_builder.build_prompt(prompt_req)
    ans_resp = answer_generator.generate_answer(prompt_resp)
    ev_bundle = evidence_mapper.map_evidence(answer_response=ans_resp, retrieval_response=candidates)
    cit_bundle = citation_engine.generate_citations(answer_response=ans_resp, evidence_bundle=ev_bundle)
    gr_report = grounding_verifier.verify_grounding(answer_response=ans_resp, evidence_bundle=ev_bundle, citation_bundle=cit_bundle)

    final_resp = decision_engine.process_and_build_response(
        answer_response=ans_resp, evidence_bundle=ev_bundle, citation_bundle=cit_bundle, grounding_report=gr_report
    )
    print(f"Decision:               {final_resp.decision.value} (Status: {final_resp.status.value})")
    print(f"Reason:                 {final_resp.reason}")
    print(f"Grounding Score:        {final_resp.grounding_summary.get('grounding_score', 0.0):.4f}")
    print(f"Warnings:               {len(final_resp.warnings)}")
    print(f"Answer Output Preview:  \"{final_resp.answer_text[:120]}...\"")
    print("-" * 65 + "\n")

    # Scenario 2: Supported Theorem Query
    print("-" * 65)
    print("[Scenario 2] Supported Theorem Query ('What does Theorem 3 state?')")
    analysis2 = query_processor.process("What does Theorem 3 state?")
    prompt_req2 = PromptRequest(query=analysis2, retrieval_response=candidates, max_context_tokens=300)
    prompt_resp2 = prompt_builder.build_prompt(prompt_req2)
    ans_resp2 = answer_generator.generate_answer(prompt_resp2)
    ev_bundle2 = evidence_mapper.map_evidence(answer_response=ans_resp2, retrieval_response=candidates)
    cit_bundle2 = citation_engine.generate_citations(answer_response=ans_resp2, evidence_bundle=ev_bundle2)
    gr_report2 = grounding_verifier.verify_grounding(answer_response=ans_resp2, evidence_bundle=ev_bundle2, citation_bundle=cit_bundle2)

    final_resp2 = decision_engine.process_and_build_response(
        answer_response=ans_resp2, evidence_bundle=ev_bundle2, citation_bundle=cit_bundle2, grounding_report=gr_report2
    )
    print(f"Decision:               {final_resp2.decision.value} (Status: {final_resp2.status.value})")
    print(f"Reason:                 {final_resp2.reason}")
    print(f"Grounding Score:        {final_resp2.grounding_summary.get('grounding_score', 0.0):.4f}")

    # Scenario 3: No Evidence Query
    print("\n" + "-" * 65)
    print("[Scenario 3] No Evidence Query (Empty Retrieved Chunks)")
    ans_resp3 = answer_generator.generate_answer(prompt_resp)
    empty_ev_bundle = EvidenceBundle(question="Empty Query", answer_text="", references=[])
    final_resp3 = decision_engine.process_and_build_response(
        answer_response=ans_resp3, evidence_bundle=empty_ev_bundle, citation_bundle=None, grounding_report=None
    )
    print(f"Decision:               {final_resp3.decision.value} (Status: {final_resp3.status.value})")
    print(f"Reason:                 {final_resp3.reason}")
    print(f"Answer Output Text:     \"{final_resp3.answer_text}\"")

    # Scenario 4: Unknown Intent Query
    print("\n" + "-" * 65)
    print("[Scenario 4] Unknown / Off-Topic Query Intent")
    analysis4 = query_processor.process("xyz 123 ???")
    prompt_req4 = PromptRequest(query=analysis4, retrieval_response=candidates, max_context_tokens=300)
    prompt_resp4 = prompt_builder.build_prompt(prompt_req4)
    ans_resp4 = answer_generator.generate_answer(prompt_resp4)
    final_resp4 = decision_engine.process_and_build_response(
        answer_response=ans_resp4, evidence_bundle=ev_bundle, citation_bundle=cit_bundle, grounding_report=gr_report
    )
    print(f"Decision:               {final_resp4.decision.value} (Status: {final_resp4.status.value})")
    print(f"Reason:                 {final_resp4.reason}")
    print(f"Answer Output Text:     \"{final_resp4.answer_text}\"")

    # Scenario 5: Severe Hallucination Simulation
    print("\n" + "-" * 65)
    print("[Scenario 5] Severe Hallucination Simulation (Zero Grounding Score)")
    bad_gr_report = GroundingReport(
        question="Hallucinatory Query",
        answer_text="Completely fabricated mathematical claim.",
        grounding_score=0.0,
        supported_claim_ratio=0.0,
    )
    final_resp5 = decision_engine.process_and_build_response(
        answer_response=ans_resp, evidence_bundle=ev_bundle, citation_bundle=cit_bundle, grounding_report=bad_gr_report
    )
    print(f"Decision:               {final_resp5.decision.value} (Status: {final_resp5.status.value})")
    print(f"Reason:                 {final_resp5.reason}")
    print(f"Answer Output Text:     \"{final_resp5.answer_text}\"")
    print("-" * 65 + "\n")

    print("============================================================")
    print(" GUARDRAILS LAYER VERIFICATION COMPLETE")
    print("============================================================\n")


if __name__ == "__main__":
    main()
