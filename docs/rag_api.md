# RAG API Specification - AI Research Assistant

## Endpoint Overview

The RAG API provides backend interfaces for processing user questions, executing hybrid document retrieval, constructing prompts, generating grounded answers, mapping evidence, rendering citations, verifying grounding, and enforcing guardrails.

---

## 1. Primary RAG Query Endpoint

### `POST /api/v1/rag/query`

#### Request Payload
```json
{
  "question": "What is Definition 2.1?",
  "paper_ids": ["paper_spectral_01"],
  "citation_style": "inline",
  "max_context_tokens": 1500,
  "strict_mode": false
}
```

#### Field Descriptions
- `question` (string, required): The researcher's natural language question.
- `paper_ids` (array of strings, optional): Filter retrieval to specific uploaded paper IDs.
- `citation_style` (string, optional): One of `"inline"`, `"author_year"`, or `"academic"`. Defaults to `"inline"`.
- `max_context_tokens` (integer, optional): Maximum tokens allocated for retrieved context. Defaults to `1500`.
- `strict_mode` (boolean, optional): Enforce strict grounding thresholds in Guardrails. Defaults to `false`.

---

#### Response Payload (`FinalResearchResponse`)
```json
{
  "question": "What is Definition 2.1?",
  "answer_text": "### Direct Answer\nDefinition 2.1 (Hilbert-Schmidt Operator) states that an operator T on a Hilbert space H is Hilbert-Schmidt if sum_i ||T e_i||^2 < infinity [1].\n\n---\n## References\n- [1] Spectral (2024). *Spectral Theory of Hilbert Space Operators*, Section 2. Basic Definitions, pp. 1-1.",
  "decision": "RETURN",
  "status": "PASS",
  "reason": "Answer is fully grounded, cited, and verified against mathematical evidence.",
  "citations": ["[1]"],
  "bibliography": [
    "[1] Spectral (2024). *Spectral Theory of Hilbert Space Operators*, Section 2. Basic Definitions, pp. 1-1. [Chunk ID: paper1_def_2.1]"
  ],
  "warnings": [],
  "grounding_summary": {
    "grounding_score": 0.85,
    "supported_claim_ratio": 0.80,
    "evidence_coverage": 0.90,
    "citation_coverage": 0.90
  },
  "confidence": 0.93,
  "metadata": {
    "query_text": "What is Definition 2.1?",
    "intent": "definition",
    "generated_at": "2026-08-04T17:00:00Z"
  }
}
```

---

## 2. Processing Pipeline Summary

```
User Question
  │
  ▼
[QueryProcessor] ──► Normalization, Intent Detection, Entity & Symbol Extraction
  │
  ▼
[HybridRetriever] ──► Vector Search + Keyword + Graph Adjacency + Ranking
  │
  ▼
[PromptBuilder] ──► Token Budgeting, Context Injection & System Prompt Assembly
  │
  ▼
[LLMAdapter] ──► Provider Agnostic Inference (MockLLMAdapter / OpenAI / Anthropic)
  │
  ▼
[AnswerGenerator] ──► Answer Post-Processing & Confidence Estimation
  │
  ▼
[EvidenceMapper] ──► Sentence Alignment & Coverage Analysis
  │
  ▼
[CitationEngine] ──► Inline Citation Formatting & Bibliography Generation
  │
  ▼
[GroundingVerifier] ──► Sentence Claim Extraction & Support Level Verification
  │
  ▼
[GuardrailEngine] ──► Policy Rule Decision (RETURN / REFUSE / INSUFFICIENT_EVIDENCE)
  │
  ▼
FinalResearchResponse
```
