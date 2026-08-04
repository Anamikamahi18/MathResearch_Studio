#!/usr/bin/env python3
"""Verification script for Day 5 Step 3.5: Provider-Agnostic LLM Adapter Layer."""

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

from src.rag.llm import LLMAdapterFactory, LLMRequest
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
    ]


def main() -> None:
    """Run verification for LLM Adapter pipeline."""
    print("\n============================================================")
    print(" DAY 5 STEP 3.5: LLM ADAPTER LAYER VERIFICATION")
    print("============================================================\n")

    # 1. Pipeline Component Initialization
    query_processor = QueryProcessor()
    prompt_builder = PromptBuilder()

    adapter = LLMAdapterFactory.get_adapter(provider_name="mock", model_name="mock-math-v1")
    candidates = create_sample_retrieval_candidates()

    sample_query = "What is Definition 2.1?"
    print(f"Sample User Query: '{sample_query}'")
    print(f"Active Adapter:   {adapter.__class__.__name__}")
    print(f"Health Check:     {adapter.health_check()}")
    print(f"Streaming:        {adapter.supports_streaming()}\n")

    # 2. Step 1: Query Processing & Prompt Construction
    analysis = query_processor.process(sample_query)
    prompt_req = PromptRequest(query=analysis, retrieval_response=candidates, max_context_tokens=300)
    prompt_resp = prompt_builder.build_prompt(prompt_req)

    # 3. Step 2: Transform PromptResponse to LLMRequest
    llm_req = LLMRequest.from_prompt_response(
        prompt_response=prompt_resp,
        provider="mock",
        model="mock-math-v1",
        temperature=0.0,
    )

    # 4. Step 3: LLM Adapter Execution
    llm_resp = adapter.generate(llm_req)

    # 5. Display Pipeline Metadata & Results
    print("-" * 60)
    print(" PIPELINE EXECUTION VERIFICATION")
    print("-" * 60)
    print(f"Provider:            {llm_resp.metadata.provider}")
    print(f"Model Name:          {llm_resp.metadata.model}")
    print(f"Latency:             {llm_resp.metadata.latency_ms:.2f} ms")
    print(f"Prompt Tokens:       {llm_resp.metadata.prompt_tokens}")
    print(f"Completion Tokens:   {llm_resp.metadata.completion_tokens}")
    print(f"Total Tokens:        {llm_resp.metadata.total_tokens}")
    print(f"Finish Reason:       {llm_resp.metadata.finish_reason}")
    print(f"Prompt Version:      {llm_req.metadata.get('prompt_version')}")
    print(f"Included Chunks:     {llm_req.metadata.get('included_chunks')}")
    print(f"Context Coverage:    {llm_req.metadata.get('context_coverage'):.2%}")
    print("\n--- RAW LLM RESPONSE TEXT ---")
    print(llm_resp.raw_text)
    print("-" * 60 + "\n")

    print("============================================================")
    print(" LLM ADAPTER VERIFICATION COMPLETE")
    print("============================================================\n")


if __name__ == "__main__":
    main()
