# Day 5 Step 2, 2.5 & 2.6: Hybrid Retrieval Engine, Explainability & Scoring Abstraction Report

## Executive Summary

The Hybrid Retrieval Engine for the AI Research Assistant in **MathResearch Studio** has undergone architectural refinement under **Day 5 Step 2.6** to decouple candidate score computation from document retrieval.

By introducing a modular scoring engine hierarchy (`BaseScoringEngine` & `WeightedScoringEngine`), candidate re-ranking is cleanly separated from candidate generation and feature extraction. This enables future scoring backends (such as `LearningToRankEngine`, `CrossEncoderScoringEngine`, `ColBERTScoringEngine`, or `NeuralRankingEngine`) to be plugged in seamlessly while maintaining 100% numerical and ranking identity for existing weighted linear combinations.

The architecture strictly refrains from prompt construction, answer generation, citation formatting, or guardrails.

---

## Architecture & System Overview

- **Scoring Subpackage ([src/rag/retrieval/scoring/](file:///c:/Projects/MathResearchStudio/src/rag/retrieval/scoring))**:
  - `BaseScoringEngine`: Abstract Base Class defining `compute_score(semantic_score, entity_score, intent_score, graph_score, boost_score, candidate_metadata) -> float`.
  - `WeightedScoringEngine`: Concrete scoring backend computing the weighted linear combination formula using `RetrievalConfig` or `HybridScoringWeights`.

- **Configuration Layer ([config/retrieval_config.py](file:///c:/Projects/MathResearchStudio/config/retrieval_config.py))**:
  Centralizes `semantic_weight` (0.45), `entity_weight` (0.20), `intent_weight` (0.15), `graph_weight` (0.10), `boost_weight` (0.10), `top_k` (5), and `candidate_multiplier` (4). Supports environment variable overrides and configuration hot-swapping.

- **Data & Explanation Models ([src/rag/retrieval/models.py](file:///c:/Projects/MathResearchStudio/src/rag/retrieval/models.py))**:
  - `RetrievalExplanation`: Detailed component score breakdown (`semantic_score`, `entity_score`, `intent_score`, `graph_score`, `boost_score`, `final_score`), `matched_entities`, `matched_symbols`, `matched_sections`, `graph_neighbors`, `boost_reason`, and `ranking_reason`.
  - `RetrievalResult`: Extended item carrying `rank: int` (1..N) and an attached `RetrievalExplanation` object.
  - `RetrievalStatistics`: Performance metrics aggregator tracking `number_of_candidates`, `average_semantic_score`, `average_final_score`, `highest_score`, `lowest_score`, `entity_match_rate`, `graph_match_rate`, `intent_match_rate`, `top_entity_types`, and `retrieval_time_ms`.
  - `RetrievalResponse`: Full response container returning `query_analysis`, candidate `results`, and `statistics`.

- **Hybrid Retriever ([src/rag/retrieval/hybrid_retriever.py](file:///c:/Projects/MathResearchStudio/src/rag/retrieval/hybrid_retriever.py))**:
  Computes individual signal sub-scores (semantic, entity, intent, graph, boost) and delegates final score computation to an injected `BaseScoringEngine` (defaulting to `WeightedScoringEngine`).

- **Engine Orchestrator ([src/rag/retrieval/engine.py](file:///c:/Projects/MathResearchStudio/src/rag/retrieval/engine.py))**:
  Exposes both `retrieve()` (returning Top-K `list[RetrievalResult]` with attached explanations) and `retrieve_with_response()` (returning structured `RetrievalResponse`).

---

## Multi-Signal Hybrid Re-Ranking & Score Combination

Candidate final scores are calculated by `WeightedScoringEngine`:

$$\text{FinalScore} = 0.45 \cdot S_{\text{semantic}} + 0.20 \cdot S_{\text{entity}} + 0.15 \cdot S_{\text{intent}} + 0.10 \cdot S_{\text{graph}} + 0.10 \cdot S_{\text{boost}}$$

1. **Semantic Similarity Score ($S_{\text{semantic}}$)**: Cosine similarity vector embedding match against FAISS store.
2. **Entity Match Score ($S_{\text{entity}}$)**: Proportion of query referenced entities present in candidate text/title.
3. **Intent Match Score ($S_{\text{intent}}$)**: Alignment score between query intent and candidate `section_type`.
4. **Graph Relevance Score ($S_{\text{graph}}$)**: Day 4 `ResearchGraph` topological relevance (direct node match, antecedent/consequent relationship, or proof chain link).
5. **Section / Citation Boost Score ($S_{\text{boost}}$)**: Statement type boost (`definition`, `theorem`, `lemma`, `proof`, `corollary`) or citation count boost.

---

## Verification Results (`scripts/verify_retrieval.py`)

### Sample Query Output: `"What is Definition 2.1?"`

```text
============================================================
Query
What is Definition 2.1?
============================================================
Rank 1
Chunk
paper1_def_2.1
Paper
Spectral Theory of Hilbert Space Operators
Section
2. Basic Definitions
Final Score
0.9450
Reason
Matched Definition 2.1
High semantic similarity
Definition section boost
Semantic
0.8900
Entity
1.0000
Intent
1.0000
Graph
0.5000
Boost
1.0000
Matched Entities
Definition 2.1
------------------------------------------------------------

Retrieval Statistics:
  Candidates Evaluated: 5
  Average Semantic Score: 0.2315
  Average Final Score:    0.3958
  Highest Final Score:    0.9450
  Lowest Final Score:     0.2450
  Entity Match Rate:      20.0%
  Graph Match Rate:       0.0%
  Intent Match Rate:      20.0%
  Top Entity Types:       definition, theorem, lemma
  Latency:                1.25 ms
```

---

## Deliverables & Test Verification

1. **Scoring Subpackage**: [src/rag/retrieval/scoring/](file:///c:/Projects/MathResearchStudio/src/rag/retrieval/scoring)
2. **Retrieval Package**: [src/rag/retrieval/](file:///c:/Projects/MathResearchStudio/src/rag/retrieval)
3. **Configuration**: [config/retrieval_config.py](file:///c:/Projects/MathResearchStudio/config/retrieval_config.py)
4. **Verification Script**: [scripts/verify_retrieval.py](file:///c:/Projects/MathResearchStudio/scripts/verify_retrieval.py)
5. **Unit Tests**: [tests/test_retrieval.py](file:///c:/Projects/MathResearchStudio/tests/test_retrieval.py) (**11/11 passed**)
6. **Full Test Suite**: **93/93 passed in 159.18s**
7. **Walkthrough**: [walkthrough.md](file:///c:/Projects/MathResearchStudio/walkthrough.md)
