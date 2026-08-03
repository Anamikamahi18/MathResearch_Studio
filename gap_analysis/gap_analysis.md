# Gap Analysis

## Overview

This document identifies the practical problems mathematics researchers face when working through large volumes of academic literature and highlights where MathResearch Studio can provide meaningful assistance. The goal is not to automate mathematical discovery, but to reduce friction in reading, organising, searching, and connecting research knowledge.

## What problems do mathematics researchers face when reading many papers?

Mathematics researchers often work across dozens of papers that introduce dense notation, layered definitions, and long proof chains. The main difficulties include understanding unfamiliar terminology, tracing how results depend on earlier lemmas or external references, comparing notational conventions across authors, and retaining key ideas over time. Reading papers is also slow because mathematical writing is highly compressed and often assumes substantial prior background.

## Why are definitions, theorems, and proofs difficult to organise?

Definitions, theorems, lemmas, and proofs are tightly interdependent. A single theorem may rely on many earlier concepts, and those concepts may be defined differently across subfields or papers. Researchers often extract these manually into personal notes, but this process is time-consuming and inconsistent. Proofs add another layer of difficulty because their structure is often informal, spread across paragraphs, and dependent on notation introduced earlier.

## What limitations do current research tools have?

Many current research tools are strong at citation management, general PDF annotation, or broad semantic search, but they usually do not model mathematical content in a structured way. They often treat papers as plain text rather than as collections of definitions, statements, symbols, and proof relationships. Tools focused on symbolic mathematics or theorem proving also do not address the everyday workflow of literature reading and research note organisation.

## Where can AI assist without replacing mathematical reasoning?

AI can assist in extracting document structure, identifying candidate definitions and theorem-like statements, normalising notation references, generating searchable summaries, building dependency graphs, and answering questions grounded in uploaded papers. These tasks support comprehension and navigation. The actual act of verifying proofs, forming conjectures, and producing new mathematics remains with the researcher.

## Which features would genuinely save researchers time?

The most valuable features are likely to be PDF ingestion, automatic extraction of definitions and results, theorem-proof linking, notation dictionaries, paper-level and collection-level search, dependency graph generation, and exportable structured notes. These features reduce repetitive manual note-taking and make it easier to revisit a body of literature after days or weeks.

## What do existing tools miss?

Existing tools often miss the structural richness of mathematical writing. They rarely capture relationships between definitions, lemmas, theorems, and proofs in a form that researchers can browse or query. They also tend to perform poorly on mathematical notation, theorem numbering, and cross-paper comparison of related concepts.

## Why are mathematicians still manually reading papers?

Mathematical papers require careful interpretation, not just information retrieval. Researchers need to judge subtle assumptions, understand proof strategies, resolve notation overload, and decide whether a result is relevant to their own work. Because current tools do not reliably represent these subtleties, manual reading remains essential.

## What is difficult about mathematical notation?

Mathematical notation is highly context-dependent. The same symbol can mean different things across papers, and different authors may use different symbols for the same concept. Notation may also rely on formatting, layout, subscripts, superscripts, and implicit conventions that are hard for generic text-processing systems to interpret correctly.

## What workflow is missing?

A major missing workflow is a research environment that moves seamlessly from paper upload to structured extraction, searchable knowledge, dependency exploration, notation tracking, grounded question answering, and note export. Researchers often assemble this workflow manually using separate tools for storage, annotation, search, and writing.

## Opportunities for MathResearch Studio

- Build a structured reading workflow tailored to mathematical literature rather than general academic PDFs.
- Extract definitions, theorems, lemmas, and proofs into reusable research objects.
- Create dependency graphs that help researchers trace how results build on one another.
- Maintain a notation dictionary that reduces confusion across papers.
- Support search and question answering grounded only in uploaded research documents.
- Generate exportable research notes that researchers can refine for reports, surveys, or thesis writing.
- Reduce time lost to manual note-taking and repeated re-reading of dense papers.
- Provide a practical AI-assisted workflow that complements, rather than replaces, mathematical reasoning.

## Is the Gap Analysis Complete?

It is complete enough for Version 1 planning, but not complete in the research sense.

For product planning, this document already identifies the main workflow problems, the missing capabilities, and the product opportunities.

For stronger evidence, it should be validated with direct input from mathematicians, especially through short surveys or interviews. That means the analysis is currently a well-grounded working draft, not a final academic study.

## Can You Ask Researchers Directly Through a Google Form?

Yes. In fact, you should.

A Google Form is a good way to validate whether the problems identified here are real, frequent, and important to researchers. It helps convert assumptions into evidence.

### What to ask in the form

- How often do they read new papers?
- What is the hardest part of understanding a paper?
- Which tasks take the most time: reading, note-taking, searching, tracking definitions, or following proofs?
- How do they currently manage definitions, theorems, lemmas, and notation?
- What do they dislike about current tools?
- Would they trust AI assistance for summarization, search, or extraction?
- Which features would save them the most time?
- What would make them stop using such a tool?

### How to use the responses

- Rank the pain points by frequency and severity.
- Compare survey answers with the assumptions in this gap analysis.
- Use the results to refine the MVP scope and feature priorities.
- Quote the most common problems in your README, proposal, or project report.

## Gap Analysis of Existing AI Tools for Researchers

The tools below are useful in general research workflows, but none of them fully solve the day-to-day mathematical literature workflow that MathResearch Studio targets.

### ChatGPT

**Strengths**

- Strong general-purpose reasoning and summarization
- Good for brainstorming, drafting, and explanation
- Can help interpret text passages interactively

**Limitations**

- Not grounded by default in a private paper collection
- Can hallucinate citations or technical claims
- Does not natively track theorem-definition-proof structure across uploaded papers
- Weak at preserving exact mathematical notation and document-level provenance

**Gap for MathResearch Studio**

- Need source-grounded answers tied to uploaded papers only
- Need structured extraction of definitions, theorems, lemmas, and proofs
- Need notebook-like research notes rather than generic chat responses

### Gemini

**Strengths**

- Good general document understanding and multimodal support
- Useful for broad summaries and reasoning over long context
- Often helpful for extracting high-level insights from long documents

**Limitations**

- Still not specialized for mathematical literature workflows
- May summarize well but not organize mathematical entities reliably
- Not designed as a dedicated paper-workspace or knowledge-extraction system

**Gap for MathResearch Studio**

- Need repeatable extraction of mathematical structures from PDFs
- Need searchable collections of papers with math-specific indexing
- Need explicit support for notation dictionaries and dependency graphs

### Perplexity

**Strengths**

- Strong web-connected search and source citation behavior
- Convenient for quick literature discovery
- Good for broad research exploration and topic overview

**Limitations**

- Optimized for web search rather than private paper libraries
- Not focused on deep extraction of math structure from PDFs
- Citation quality depends on visible web sources, not internal research artifacts

**Gap for MathResearch Studio**

- Need closed-world search over uploaded papers
- Need extraction and organization of internal research notes
- Need workflow support for definitions, theorem links, and proof traversal

### Claude

**Strengths**

- Strong long-context reading and summarization
- Good at structured writing and document analysis
- Useful for nuanced explanations and synthesis

**Limitations**

- Still a general assistant rather than a dedicated research workflow system
- May not preserve mathematical structure and provenance as a first-class concept
- Not built around local paper ingestion, graph analysis, or note export for researchers

**Gap for MathResearch Studio**

- Need a research-specific interface for uploaded papers
- Need mathematics-aware extraction and retrieval pipelines
- Need support for organizing and exporting research knowledge over time

### Overall Tool Gap Summary

Existing AI tools are strong at conversation, summarization, and general reasoning, but they do not provide an end-to-end mathematical literature workflow.

What is missing is:

- Reliable paper ingestion for mathematical PDFs
- Structured extraction of definitions, theorems, lemmas, and proofs
- Notation dictionaries across papers
- Dependency graphs for mathematical concepts
- Search grounded only in uploaded research material
- Exportable research notes tailored to mathematicians

## Research Questions to Validate Next

- Which parts of reading papers are most painful for mathematicians?
- How often do they need to revisit older papers and reconstruct notation?
- Would they trust AI for extraction if every answer showed supporting evidence?
- What minimum workflow would make them adopt a new tool?
- Which existing AI tool do they already use, and what do they still do manually?

## Appendix A: Survey Instrument

Use the Google Form-ready survey draft in [research_survey.md](research_survey.md) as the primary instrument for validating the gap analysis with mathematicians.

Recommended use:

- Copy the section headings into Google Forms as form sections.
- Paste the numbered questions as individual form questions.
- Keep the listed options for multiple-choice items.
- Use the short-answer prompts for open feedback and follow-up contact details.
- After collecting responses, feed the results back into this gap analysis to refine the opportunity list and the MVP scope.

## Day 2 Session 4: Parsing Reliability Gap Update

### Why do existing PDF parsers struggle with mathematical notation?

Most generic PDF parsers are optimized for linear prose, not symbolic mathematics. Mathematical notation depends on 2D layout, super/subscripts, equation alignment, and operator precedence that are often flattened or reordered during extraction. Multi-column papers and mixed text-equation regions further break token ordering, making extracted output unreliable for downstream theorem or proof analysis.

### How are equations represented differently from plain text?

Plain text is usually sequential and can be represented as a simple token stream. Equations, in contrast, are spatial structures where position carries meaning. For example, fractions, matrices, limits, and nested expressions depend on vertical and horizontal layout relationships, not just token sequence. A parser that treats equations as plain text often loses semantics and mathematical correctness.

### Which parsing errors matter most to mathematicians?

- Symbol corruption (for example, confusing similar symbols)
- Loss of subscript/superscript structure
- Broken theorem-proof boundaries
- Incorrect section assignment for statements
- Equation token order errors
- Missing references and citation links
- Page provenance loss (cannot trace extracted claim to source location)

These errors directly affect trust, because a small notation error can change the meaning of a statement.

### What could make MathResearch Studio more reliable than generic PDF readers?

- Use a multi-path extraction strategy: text-layer first, OCR/multimodal fallback when needed
- Preserve provenance metadata for every extracted unit (page, section, offsets, confidence)
- Separate extraction stages (metadata, sections, entities, equations, references) for targeted quality control
- Add confidence scoring and warning flags to surface uncertain outputs
- Keep schema-stable JSON contracts so validation and QA tooling can be consistent
- Support human-in-the-loop correction for low-confidence or high-impact fields

### Reliability Opportunities for Version 1

- Prioritize correctness for core fields before broad feature expansion
- Expose parser quality indicators in the UI
- Build small gold-standard test sets from mathematics papers for regression checks
- Track parser failure modes in `tests/test_cases.md` and iterate by error category

---

## Day 3: Embedding & Vector Retrieval Gap Analysis

### Why is keyword search insufficient for mathematics?

Traditional keyword search (e.g., BM25, exact substring matching) fails significantly in mathematical research workflows:

* **Vocabulary & Terminology Mismatch**: Mathematicians frequently describe the same underlying conceptual structure using different terms across subfields (e.g., *"compact manifold"* vs. *"closed bounded smooth manifold"*, or *"isomorphism"* vs. *"bijective structure-preserving map"*).
* **Paraphrased Queries**: Researchers search by high-level conceptual questions (e.g., *"methods for bounding eigenvalues of Laplacian operators"*) rather than exact paper phrasing.
* **Notation Discrepancies**: Latex string variations (e.g., `\frac{a}{b}`, `a/b`, `a b^{-1}`) frustrate keyword indexing engines, rendering string matching fragile for mathematical search.

### What are the main problems with embeddings for mathematical content?

Dense vector embeddings represent text as continuous vectors in floating-point space, but encounter distinct challenges when applied to symbolic mathematics:

* **Loss of Exact Symbol Precision**: Dense embeddings map text into continuous semantic space, which excels at broad topical matching but often blurs fine-grained symbolic differences (e.g., confusing `$x > 0$` with `$x \ge 0$`, or `$f(x)$` with `$f'(x)$`).
* **General-Domain Bias**: Models like `all-MiniLM-L6-v2` or `text-embedding-3-small` are pre-trained primarily on web text and Wikipedia, lacking specialized pre-training on raw LaTeX syntax, complex mathematical proofs, and abstract notation.
* **Context Length Truncation**: Standard embedding encoders impose fixed token limits (e.g., 256–512 tokens). Long proofs or extensive mathematical derivations must be chunked, risking loss of broader contextual premises.

### What unique challenges does mathematical notation present to vector retrieval?

* **Spatial and 2D Layout Semantics**: Mathematical formulas depend on 2D spatial relationships (superscripts, subscripts, fractions, matrices, summation limits) that generic linear text embedders flatten into 1D strings, losing mathematical semantics.
* **Notation Overload & Variable Re-use**: Variable names are reused constantly across different papers and subdomains (e.g., $E$ representing energy, expectation, or an elliptic curve depending on context), creating embedding ambiguity without surrounding context.
* **LaTeX Syntactic Noise**: Variations in command syntax, formatting macros, and whitespace introduce vector noise that degrades cosine similarity scoring.

### Why do theorems with identical mathematical meaning have low vector similarity under different notation?

When two authors prove the exact same theorem using different variable conventions (e.g., Author A proving $A^2 + B^2 = C^2$ for right triangles, while Author B proves $x^2 + y^2 = z^2$), standard embedding models treat the differing character tokens as separate semantic concepts:

* **Token-Level Disparities**: WordPiece and BPE tokenizers split unrecognized notation into separate subword tokens, driving the embedding vectors apart.
* **Lack of Structural Isomorphism Awareness**: Standard sentence transformers measure surface-level linguistic co-occurrence rather than structural mathematical isomorphism.
* **Symbol Variable Instantiation**: Embeddings fail to recognize alpha-equivalence (renaming bound variables) without explicit symbolic normalization or AST parsing.

### What are the primary limitations of dense retrieval in technical literature?

* **Inability to Enforce Exact Formula Matching**: Dense retrieval cannot guarantee exact matches for specific mathematical formulas, variable constraints, or citation IDs.
* **Lack of Logical Deduction Ability**: Vector similarity search measures semantic proximity, not logical validity. It retrieves text that *sounds* related, regardless of whether the mathematical argument is logically sound or relevant to a proof step.
* **Uncertain Similarity Thresholds**: Cosine similarity scores vary across paper domains, making it difficult to establish a single universal threshold for "relevant" vs. "irrelevant" mathematical chunks.

### Ideas for Version 2 & Future Enhancements

1. **Hybrid Retrieval (BM25 + FAISS Dense Search)**: Combine BM25 sparse keyword indexing for exact symbol/variable matching with FAISS dense vector search for conceptual discovery, merged via Reciprocal Rank Fusion (RRF).
2. **LaTeX & Notation Normalization Engine**: Pre-process mathematical text using a notation canonicalizer (e.g., converting equivalent LaTeX expressions into a standard canonical form before chunking and embedding).
3. **Formula-Aware & AST Embeddings**: Incorporate formula Abstract Syntax Tree (AST) representations alongside text embeddings to enable structural formula matching.
4. **Cross-Encoder Re-Ranking Layer**: Implement a secondary Cross-Encoder re-ranker trained on scientific query-passage pairs to re-score top-20 retrieved candidates for high-precision mathematical ranking.
5. **Theorem-Proof Entity Filtering**: Extend search endpoints to allow explicit filtering by `entity_type` (`definition`, `theorem`, `lemma`, `proof`) to narrow results to formal statement objects.
