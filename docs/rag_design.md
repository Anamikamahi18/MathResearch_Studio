# RAG Design Specification - AI Research Assistant

## Executive Overview

This document specifies the design rationale for the **Retrieval-Augmented Generation (RAG)** system built for **MathResearch Studio**. The AI Research Assistant enables mathematics researchers (MSc students, PhD scholars, professors, and research groups) to ask natural language questions over uploaded academic papers, producing source-grounded answers with precise mathematical citations while preventing hallucinations and fabricated claims.

---

## Key Research Questions & Design Rationale

### 1. Why use RAG instead of sending the whole paper to an LLM?

While modern LLMs feature large context windows (e.g. 128k to 1M tokens), sending full academic papers directly to an LLM introduces severe drawbacks for mathematical literature workflows:

1. **Context Window Contamination & "Lost-in-the-Middle" Effect**: Academic papers contain dense proofs, notation definitions, and reference bibliographies. When thousands of tokens of dense text are passed in a single prompt, LLMs exhibit degraded attention over intermediate sections, frequently missing crucial lemmas, constraints, or definition conditions.
2. **Computational Cost & Latency**: Processing 30–100 page preprints or full multi-paper corpora on every user query incurs high token consumption and linear latency spikes ($5\text{s} - 30\text{s}$ per query).
3. **Citation Precision & Traceability**: Raw LLM generation over long contexts fails to pinpoint exact passage locations (section headings, page numbers, chunk identifiers). RAG enables deterministic alignment between individual generated claims and explicit source passages.
4. **Hallucination Mitigation**: Constraining context to top-K retrieved, highly relevant passages ($K \in [3, 5]$) significantly reduces distraction from unrelated paper sections and enforces strict grounding boundaries.

---

### 2. How should retrieved chunks be selected?

Chunk selection in MathResearch Studio employs a **Hybrid Multi-Signal Retrieval Engine** combining:

- **Dense Semantic Retrieval**: Uses fine-tuned scientific text embeddings (`allenai/scibert_scivocab_uncased` or `sentence-transformers/all-MiniLM-L6-v2`) to capture conceptual similarity between the query and paper passages.
- **Entity & Symbol Alignment**: Computes explicit overlap scores for extracted mathematical entities (e.g. *"Hilbert-Schmidt Operator"*, *"Theorem 3"*) and LaTeX/Unicode symbols ($\lambda$, $P_k$).
- **Query Intent Alignment**: Boosts chunks matching the query's structural intent (e.g. boosting `definition` section types for *"Define compactness"* queries).
- **Knowledge Graph Topology**: Integrates Day 4 Research Graph adjacency signals to retrieve prerequisite lemmas and dependency nodes associated with targeted theorems.

#### Weighted Scoring Formula
$$\text{FinalScore} = w_{\text{semantic}} \cdot S_{\text{semantic}} + w_{\text{entity}} \cdot S_{\text{entity}} + w_{\text{intent}} \cdot S_{\text{intent}} + w_{\text{graph}} \cdot S_{\text{graph}} + S_{\text{boost}}$$

---

### 3. How many chunks should be retrieved?

MathResearch Studio enforces dynamic context token budgeting:

- **Default Top-K**: $K = 3 \text{ to } 5$ candidate chunks per query.
- **Token Ceiling**: Maximum 1,500 context tokens per prompt, leaving ample headroom for system prompts (500 tokens) and generated answer completions (1,000 tokens).
- **Deduplication & Diversity**: Chunks are deduplicated by paper ID and section location to ensure multi-angle evidence coverage without repeating redundant preamble text.

---

### 4. How should citations appear?

Citations are rendered using researcher-friendly styles configured via `CitationStyle`:

1. **Inline Numerical (`INLINE`)**: `[1]`, `[2]` inserted directly at the sentence boundary supporting the mathematical statement.
2. **Author-Year (`AUTHOR_YEAR`)**: `(Smith, 2024)` appended to mathematical claims.
3. **Academic Detail (`ACADEMIC`)**: `[Paper Title, Section 2, p. 3]` providing explicit section and page attribution.
4. **Structured Bibliography**: Appended at the end of every answer response, listing:
   $$\text{[1] Author(s) (Year). \textit{Paper Title}, Section Name, pp. X-Y. [Chunk ID: ...]} $$

---

### 5. How should unsupported questions be handled?

When a user query cannot be answered from the uploaded document corpus:

1. **Zero Evidence Detection**: If vector retrieval returns candidate chunks below minimum similarity thresholds ($S < 0.25$), the system skips LLM invocation and triggers an `INSUFFICIENT_EVIDENCE` guardrail decision.
2. **Refusal Response**: The user receives a clear, polite refusal message:
   > *"⚠️ **Insufficient Evidence**: No relevant mathematical evidence was retrieved from the uploaded papers to answer this question."*
3. **No Hallucinated Fallbacks**: The system strictly avoids drawing on pre-trained parametric knowledge when the answer is absent from the uploaded corpus, preserving researcher trust and academic integrity.
