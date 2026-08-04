# Prompt Engineering Strategy - AI Research Assistant

## Overview

This document specifies the prompt engineering strategy for **MathResearch Studio**. The prompt strategy is optimized for question answering over mathematical research papers while preserving mathematical notation ($\text{\LaTeX}$, Unicode symbols), equations, theorem numbering, and document context.

---

## Prompt Architecture & Templates

### 1. System Prompt

The system prompt establishes strict behavior boundaries, mathematical formatting rules, and grounding constraints:

```text
You are MathResearch Studio AI Assistant, a specialized research assistant for mathematics literature.

Instructions:
1. Answer the user's question strictly using ONLY the provided mathematical context passages.
2. Preserve all mathematical notation, LaTeX equations, theorem numbering, and symbol definitions exactly as written in the context.
3. Organize your response into structured research sections:
   - Direct Answer
   - Supporting Evidence & Mathematical Reasoning
   - Limitations or Assumptions
4. Do NOT invent theorem numbers, definitions, or mathematical proofs not present in the context.
5. If the supplied context does not contain sufficient information to answer the query, state clearly that information is unavailable.
```

---

### 2. User Prompt & Context Injection Template

Retrieved passages are structured into clean, tagged context blocks with explicit metadata:

```text
--- MATHEMATICAL CONTEXT PASSAGES ---

[Passage 1]
Paper: Spectral Theory of Hilbert Space Operators
Section: 2. Basic Definitions (Page 1)
Chunk ID: paper1_def_2.1
Content:
Definition 2.1 (Hilbert-Schmidt Operator). An operator T on a Hilbert space H is Hilbert-Schmidt if sum_i ||T e_i||^2 < infinity.

[Passage 2]
Paper: Spectral Theory of Hilbert Space Operators
Section: 3. Main Theorems (Page 3)
Chunk ID: paper1_thm_3
Content:
Theorem 3 (Spectral Decomposition). Let T be a compact self-adjoint operator on H. Then T = sum_k lambda_k P_k where lambda_k are real eigenvalues.

--- USER QUESTION ---
Query Intent: definition
Entities: Hilbert-Schmidt Operator (Definition 2.1)
Question: What is Definition 2.1?

--- INSTRUCTIONS FOR ANSWER ---
Provide a complete, accurate, and grounded mathematical answer using the passages above.
```

---

## Formatting & Notation Rules

1. **LaTeX & Unicode Preservation**: Mathematical symbols ($\lambda$, $\sum$, $\infty$, $\mathcal{H}$) and equations ($T = \sum_k \lambda_k P_k$) must be preserved without alteration or unescaped markdown syntax errors.
2. **Section Structuring**: Answers are formatted with standard markdown headers (`### Direct Answer`, `### Supporting Evidence`) for clean parsing by the UI and downstream post-processors.
3. **Refusal Formatting**: If evidence is insufficient, the system emits standard refusal tokens handled by the Guardrails layer.
