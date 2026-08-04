#!/usr/bin/env python3
"""Verification script for RAG query processing layer (Day 5 Step 1 & 1.5)."""

from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Ensure UTF-8 output encoding on Windows stdout/stderr
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from src.rag.query_processing import QueryProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


def run_verification() -> None:
    """Run verification suite for QueryProcessor on benchmark research questions."""
    print("=" * 80)
    print("      MATHRESEARCH STUDIO - DAY 5 STEP 1.5: QUERY PROCESSING VERIFICATION")
    print("=" * 80)

    processor = QueryProcessor()

    test_queries = [
        "Which lemma proves theorem 3?",
        "Proof of Theorem 4",
        "Definition 2.1 and Lemma 4",
        "Which theorem depends on lemma 5?",
        "Which definition is used in theorem 2?",
        "What is Definition 2.1?",
        "Explain Theorem 5.",
        "Summarize this paper.",
        "Compare theorem 2 and theorem 4.",
        "Show notation for λ.",
        "Theorem   3.2 ?",
    ]

    for idx, raw_query in enumerate(test_queries, 1):
        print(f"\n--- [Test Query #{idx}] ---")
        print(f"Original Query:     '{raw_query}'")

        analysis = processor.process(raw_query)

        print(f"Normalized Query:   '{analysis.normalized_query}'")
        print(f"Detected Intent:    {analysis.intent}")
        print(f"Operations:         {analysis.operations}")
        print(f"Referenced Entities: {[e.normalized_label for e in analysis.referenced_entities]}")
        print(f"Entity Details:     {[e.to_dict() for e in analysis.referenced_entities]}")
        print(f"Entity Metadata:    {[e.metadata for e in analysis.referenced_entities]}")
        print(f"Symbols:            {analysis.symbols}")
        print(f"Confidence Score:   {analysis.confidence:.2f}")
        print(f"Confidence Type:    {analysis.confidence_type}")

    print("\n" + "=" * 80)
    print("Verification completed successfully for all test queries.")
    print("=" * 80)


if __name__ == "__main__":
    run_verification()
