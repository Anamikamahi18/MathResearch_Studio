# MathResearch Studio — Future Research Directions

**Document**: Future Research & Roadmap  
**Version**: 1.0.0  
**Date**: 7 August 2026  
**Status**: Active planning document — reviewed at project closure

---

## Overview

This document identifies research directions for MathResearch Studio beyond v1.0.0, grounded in the literature review (`literature/literature_review.md`), gap analysis (`gap_analysis/gap_analysis.md`), and limitations encountered during v1.0.0 development. It is organised by technical domain and priority horizon.

---

## 1. Formula Recognition

### Current State
MathResearch Studio v1.0.0 operates on the PDF text layer only. Mathematical formulas extracted from LaTeX-generated PDFs appear as Unicode approximations (e.g., σ, ∑, ∂) or as garbled character sequences when ligatures or custom fonts are used. The system cannot parse, interpret, or reason about mathematical expressions as structured objects.

### Research Direction
**Structured formula extraction and semantic indexing** — treating mathematical expressions as queryable entities rather than opaque text strings.

### Specific Problems to Solve
- **Formula detection**: Identify inline and display-mode mathematical expressions in PDF text layers
- **Formula normalisation**: Convert LaTeX source (when available), MathML, or extracted Unicode to a canonical symbolic form
- **Formula embedding**: Learn dense vector representations of mathematical expressions for semantic formula search (e.g., "find all papers that use the same operator in this context")
- **Formula-text alignment**: Align formula entities with their surrounding prose context to understand what each formula expresses

### Relevant Approaches
- **LaTeXML**: Convert `.tex` source to MathML for structured formula access
- **InftyReader / MathSeer**: OCR-based formula detection for scanned documents
- **Tangent-CFT**: Tree-structured formula embedding for mathematical information retrieval
- **Formula2Vec**: Dense embedding of symbolic mathematical expressions

### Research Timeline
- v2.0: Basic inline formula extraction and Unicode normalisation
- v2.1: LaTeXML integration for papers with available `.tex` source
- v3.0: Full symbolic formula embedding and formula search

---

## 2. OCR Improvements

### Current State
v1.0.0 requires text-layer PDFs (LaTeX-generated, digitally typeset). Scanned image PDFs — common for older papers, handwritten notes, and non-Western mathematics literature — produce empty extractions.

### Research Direction
**Multi-modal PDF ingestion pipeline** combining text-layer extraction with OCR fallback for image content.

### Specific Problems to Solve
- **Page type classification**: Automatically distinguish text-layer pages from image-only pages within a single PDF
- **Mathematics-aware OCR**: General OCR (Tesseract) degrades significantly on mathematical notation; dedicated mathematics OCR is needed
- **Layout analysis**: Multi-column layouts, figures, tables, and margin annotations require document layout understanding before text extraction
- **Formula image recognition**: Recognise and convert formula images to LaTeX or MathML

### Relevant Approaches
- **Tesseract 5.x**: Open-source OCR with LSTM backend — adequate for prose, poor for formulas
- **Mathpix API**: Commercial mathematics OCR (formula → LaTeX) with high accuracy
- **Nougat (Meta AI)**: End-to-end neural OCR specifically for scientific documents — produces Markdown with formula markup
- **Layout-Parser**: Deep learning-based document layout analysis

### Research Timeline
- v2.0: Tesseract fallback for image-only PDFs (prose recovery)
- v2.1: Nougat integration for scientific document OCR
- v3.0: Full formula image → LaTeX conversion pipeline

---

## 3. Multi-Paper Reasoning

### Current State
v1.0.0 retrieves and cites from multiple papers in the same query response, but reasoning across papers is limited: the system cannot synthesise claims from Paper A and Paper B into a coherent cross-paper answer, nor can it detect when two papers contradict each other.

### Research Direction
**Cross-paper knowledge synthesis** — enabling the AI assistant to reason about relationships between mathematical claims across the entire uploaded library.

### Specific Problems to Solve
- **Cross-paper entity alignment**: Recognise that "Theorem 3.1 in Smith (2020)" and "Lemma 2 in Jones (2023)" express the same mathematical fact under different notation
- **Contradiction detection**: Identify when two papers make incompatible claims about the same mathematical object
- **Proof chain synthesis**: Reconstruct a multi-paper proof chain (e.g., "this result follows from Lemma A in [Paper 1], which was generalised in [Paper 2]")
- **Citation graph reasoning**: Use the citation graph between uploaded papers to understand intellectual lineage

### Relevant Approaches
- **SciFact** (Wadden et al., 2020): Scientific claim verification using evidence retrieval
- **LongDoc RAG**: Extended context RAG for reasoning over multiple long documents
- **Knowledge graph embedding**: Encoding cross-paper relationships as graph embeddings

### Research Timeline
- v2.0: Multi-paper retrieval with source attribution
- v2.1: Basic claim alignment across papers using entity resolution
- v3.0: Full cross-paper contradiction detection and proof chain synthesis

---

## 4. Proof Summarisation

### Current State
v1.0.0 extracts proof text as a raw string entity. The system stores and retrieves proofs but cannot generate summaries of proof strategies, key steps, or proof techniques.

### Research Direction
**Proof-aware text summarisation** — generating concise, mathematically accurate summaries of extracted proof texts.

### Specific Problems to Solve
- **Proof structure parsing**: Identify proof steps (assumption, case analysis, induction base, inductive step, QED marker) from prose text
- **Proof strategy classification**: Classify the high-level proof technique (contradiction, induction, construction, compactness argument, etc.)
- **Summary generation**: Generate a concise 2–3 sentence proof sketch grounded strictly in the extracted text
- **Proof faithfulness**: Ensure that generated summaries do not introduce claims not present in the original proof

### Relevant Approaches
- **PEGASUS** (Zhang et al., 2020): Pre-trained abstractive summariser with gap sentence generation
- **Mathematical discourse parsing**: Adapted parsing of mathematical argument structure
- **Faithfulness metrics**: FactCC, QuestEval for factual consistency in generated summaries

### Research Timeline
- v2.0: Proof strategy classification (rule-based: detect "by contradiction", "by induction", etc.)
- v2.1: Extractive proof sketch (key sentences selected from proof text)
- v3.0: Abstractive proof summarisation with faithfulness scoring

---

## 5. Automatic Notation Extraction

### Current State
v1.0.0 builds a notation dictionary by extracting explicitly defined symbols from the text (e.g., "let σ denote..." patterns). This is reliable for formally defined notation but misses implicit notational conventions and symbols used without explicit definition.

### Research Direction
**Full-paper notational context analysis** — building a complete, paper-specific notation map including implicitly used symbols.

### Specific Problems to Solve
- **Implicit notation detection**: Identify symbols that are used consistently across a paper without being explicitly defined (e.g., n always means the index variable)
- **Context-sensitive disambiguation**: Resolve that σ means covariance matrix in Section 2 but permutation group element in Section 4
- **Cross-paper notation conflict detection**: Alert the researcher when the same symbol means different things in different uploaded papers
- **Notation standardisation suggestion**: Suggest a unified notation convention for a research group working across papers

### Relevant Approaches
- **Word sense disambiguation** adapted to mathematical symbols
- **BIO tagging** for mathematical symbol definition detection
- **Named entity recognition** fine-tuned on mathematics corpora

### Research Timeline
- v2.0: Improved implicit notation extraction using BIO tagging
- v2.1: Cross-paper notation conflict detection
- v3.0: Interactive notation harmonisation interface

---

## 6. Mathematical Knowledge Graphs

### Current State
v1.0.0 builds a **proof dependency graph** within and across uploaded papers — connecting theorems, lemmas, and definitions by dependency edges. The graph is local to the uploaded library.

### Research Direction
**Global mathematical knowledge graph** — a structured knowledge base of mathematical entities and relationships spanning the published mathematics literature.

### Specific Problems to Solve
- **Knowledge graph schema**: Define the ontology for mathematical entities (Field, Sub-field, Mathematical Object, Property, Relation, Proof Technique) and relationship types (IS-A, DEPENDS-ON, GENERALISES, EQUIVALENT-TO, CONTRADICTS)
- **Automated knowledge extraction**: Scale entity and relation extraction to arXiv-scale corpora (hundreds of thousands of papers)
- **Knowledge base population**: Continuously update the graph as new papers are published
- **Reasoning over the graph**: Enable queries like "find all theorems that generalise the Hahn-Banach theorem" or "which lemmas are used in more than 50 papers in functional analysis?"

### Relevant Approaches
- **Wikidata Mathematics sub-graph**: Existing structured data about mathematical concepts as a seed
- **OpenAlex**: Academic graph API providing paper-to-paper citation relationships at scale
- **Freebase/Wikidata-style knowledge graph construction** adapted for mathematics
- **Neo4j**: Graph database backend for a persistent, queryable knowledge graph

### Research Timeline
- v2.0: Local knowledge graph across uploaded library with enhanced relation types
- v2.1: Export local knowledge graph to RDF/JSON-LD for external tool consumption
- v3.0: Cloud-hosted global mathematics knowledge graph with API access

---

## 7. Collaboration Tools

### Current State
v1.0.0 is a single-user, local application. Research groups cannot share uploaded libraries, annotation notes, or search history across team members.

### Research Direction
**Multi-user collaborative research workspace** — enabling research groups to build a shared mathematics knowledge base.

### Specific Problems to Solve
- **Shared paper library**: Multiple researchers can upload papers to a shared library accessible to all group members
- **Annotation and notes**: Researchers can annotate extracted entities (highlight errors, add cross-references, add commentary)
- **Version control for annotations**: Track who annotated what and when, with the ability to revert
- **Real-time collaboration**: Simultaneous access to the AI assistant by multiple researchers without conflicts
- **Role-based access control**: Library owner, contributor, and viewer roles with appropriate permissions

### Relevant Approaches
- **FastAPI + PostgreSQL**: Backend architecture for multi-user support
- **WebSockets**: Real-time collaborative UI updates
- **JWT authentication**: Secure multi-user access control
- **Operational Transforms / CRDTs**: Conflict-free concurrent annotation editing

### Research Timeline
- v2.0: Multi-user library sharing (read-only for non-owners)
- v2.1: Collaborative annotation with attribution
- v3.0: Full real-time collaborative workspace with RBAC

---

## 8. LaTeX Export

### Current State
v1.0.0 exports research notes in Markdown, JSON, CSV, and PDF. Markdown is useful for general writing but does not produce LaTeX-formatted output directly usable in academic paper drafting.

### Research Direction
**LaTeX export pipeline** — generating ready-to-include LaTeX fragments from extracted mathematical entities and research notes.

### Specific Problems to Solve
- **Theorem/definition LaTeX generation**: Export extracted theorems and definitions as `\begin{theorem}...\end{theorem}` environments
- **Citation generation**: Export citations in BibTeX format matched to uploaded papers
- **Bibliography generation**: Produce a `.bib` file for the entire uploaded library
- **Survey section draft**: Generate a LaTeX survey section draft from extracted entities organised by topic
- **Notation table**: Export the notation dictionary as a LaTeX `\nomenclature` or custom table environment

### Relevant Approaches
- **Jinja2 templating**: Generate LaTeX source from structured Python objects
- **pylatex library**: Programmatic LaTeX document construction
- **BibTeX Python libraries**: `bibtexparser` for bibliography management

### Research Timeline
- v2.0: BibTeX export for uploaded papers
- v2.1: Theorem/definition LaTeX environment export
- v3.0: Full survey section draft generation in LaTeX

---

## 9. Research Timeline

### Version 1.x (Immediate)
- v1.0.0: ✅ **Current release** — Core workflow complete
- v1.0.1: GitHub Actions CI, issue templates, sample PDF, mock LLM clarity
- v1.1.0: Real LLM adapter (OpenAI / Ollama), improved entity extraction recall

### Version 2.x (6–12 months)
- v2.0: GPU/ONNX embedding, real LLM integration, Docker, SQLite persistence, BibTeX export
- v2.1: Nougat OCR integration, cross-paper entity alignment, BIO notation tagger
- v2.2: LaTeX theorem/definition export, proof strategy classification

### Version 3.x (12–24 months)
- v3.0: Full real-time collaborative workspace, global knowledge graph, formula embedding search
- v3.1: Proof summarisation (faithfulness-validated), multi-paper contradiction detection
- v3.2: LaTeX survey section draft generation, full notation harmonisation interface

### Long-Term Vision (24+ months)
Building MathResearch Studio into a **comprehensive AI-powered mathematics research platform** — open-source, locally deployable and cloud-optionally deployable, used by MSc students, PhD scholars, university research groups, and mathematical institutes — serving as the definitive infrastructure for AI-assisted mathematical literature understanding.

---

## 10. AI-Assisted Proof Exploration

### Current State
v1.0.0's AI Research Assistant answers questions grounded in uploaded papers but cannot assist with proof construction, explore alternative proof approaches, or suggest related lemmas that might be relevant to an ongoing proof.

### Research Direction
**Interactive proof exploration assistant** — guiding a mathematician through the landscape of potentially relevant mathematical results while they are actively working on a proof.

### Specific Problems to Solve
- **Proof goal formalisation**: Allow the researcher to state their current proof goal in natural language ("I need to show that a compact subset of a Hausdorff space is closed")
- **Relevant lemma retrieval**: Retrieve lemmas and theorems from the uploaded library most likely to be applicable to the stated proof goal
- **Proof strategy suggestion**: Suggest high-level proof approaches ("consider contradiction", "apply the result in [Paper X, Theorem 3.2]") grounded in the library
- **Circular dependency detection**: Warn the researcher if the suggested proof path would create a logical circularity
- **Unknown result detection**: Identify when the proof goal requires a result not present in the current library, and suggest a search query for external databases

### Relevant Approaches
- **Premise selection** (from automated theorem proving literature): Selecting likely-useful premises for a given goal
- **Lean / Mathlib tactic suggestion**: Adapted for natural language mathematics
- **Semantic similarity of proof goals** to library theorems

### Research Timeline
- v2.1: Relevant lemma retrieval given a stated proof goal
- v2.2: Basic proof strategy suggestion from library patterns
- v3.0: Full interactive proof exploration assistant

---

## References

The following literature informs the research directions above:

| Research Direction | Key Reference |
|---|---|
| Formula recognition | Tangent-CFT (Mansouri et al., 2021); MathSeer (Davila et al., 2021) |
| OCR for mathematics | Nougat (Blecher et al., 2023, arXiv:2308.13418) |
| Multi-paper reasoning | SciFact (Wadden et al., 2020); QASPER (Dasigi et al., 2021) |
| Proof summarisation | PEGASUS (Zhang et al., 2020); FRANK (Pagnoni et al., 2021) |
| Notation extraction | MathAlign (Novikova et al., 2022) |
| Knowledge graphs | OpenAlex; Wikidata Mathematics |
| Proof exploration | Premise selection (Irving et al., 2016); Lean4 Mathlib |
| LaTeX export | pylatex, Jinja2, bibtexparser |

Full bibliography: [`literature/literature_review.md`](../literature/literature_review.md)

---

*MathResearch Studio v1.0.0 · Future Research Directions · 7 August 2026*
