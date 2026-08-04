# RAG QA Test Plan & Scenario Matrix

## Overview

This document specifies the Quality Assurance (QA) test plan for the AI Research Assistant RAG pipeline in **MathResearch Studio**. Test cases evaluate end-to-end performance across retrieval accuracy, prompt building, citation formatting, grounding verification, and guardrail decisions.

---

## RAG QA Test Matrix

| ID | Test Scenario | Input Query | Expected Retrieval | Expected Decision | Expected Output / Citation |
|---|---|---|---|---|---|
| **RAG-01** | Definition Query | *"What is Definition 2.1?"* | Definition 2.1 chunk from Section 2 | `RETURN` / `RETURN_WITH_WARNING` | Grounded definition with inline citation `[1]` and bibliography |
| **RAG-02** | Theorem Query | *"What does Theorem 3 state?"* | Theorem 3 chunk from Section 3 | `RETURN` / `RETURN_WITH_WARNING` | Formal theorem statement with section/page attribution |
| **RAG-03** | Lemma Dependency | *"Which lemma proves theorem 3?"* | Lemma 3.1 chunk from Section 3 | `RETURN` / `RETURN_WITH_WARNING` | Lemma details linked to Theorem 3 |
| **RAG-04** | Document Summary | *"Summarize the paper."* | Core definitions and main theorem chunks | `RETURN` / `RETURN_WITH_WARNING` | Grounded multi-section summary with citations |
| **RAG-05** | Notation Lookup | *"Show notation for λ."* | Chunks containing eigenvalue notation | `RETURN` / `RETURN_WITH_WARNING` | Correct symbol definition ($\lambda_k$) with source passage |
| **RAG-06** | No Evidence Query | *"What is Quantum Superposition?"* | Empty / Below threshold retrieval | `INSUFFICIENT_EVIDENCE` | Polite refusal: *"No relevant mathematical evidence was retrieved..."* |
| **RAG-07** | Off-Topic / Ambiguous | *"xyz 123 ???"* | Unclear query intent | `ASK_FOR_CLARIFICATION` | Request clarification message |
| **RAG-08** | Fabricated Claim | Simulated zero grounding score | Distracted / Hallucinated text | `REFUSE` | Refusal: *"Generated answer statements are unsupported..."* |

---

## Verification Commands

To execute automated RAG verification scripts across the project codebase:

```bash
# Query processing verification
python scripts/verify_query_processing.py

# Hybrid retrieval verification
python scripts/verify_retrieval.py

# Prompt builder verification
python scripts/verify_prompt_builder.py

# LLM adapter verification
python scripts/verify_llm_adapter.py

# Answer generator verification
python scripts/verify_answer_generator.py

# Evidence mapping verification
python scripts/verify_evidence_mapping.py

# Citation engine verification
python scripts/verify_citation_engine.py

# Grounding verification
python scripts/verify_grounding.py

# Guardrails decision verification
python scripts/verify_guardrails.py

# Run RAG unit test suite
pytest tests/test_query_processing.py tests/test_retrieval.py tests/test_prompt_builder.py tests/test_llm_adapter.py tests/test_answer_generator.py tests/test_evidence_mapping.py tests/test_citation_engine.py tests/test_grounding.py tests/test_guardrails.py -v
```
