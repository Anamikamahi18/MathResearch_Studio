# MathResearch Studio v1.0.0 — Professional Demonstration Script

**Target Duration**: 7–10 minutes  
**Audience**: Recruiters, MSc/PhD Students, Professors, Research Groups  
**Format**: Live screen demonstration with narration  

---

## Pre-Demo Setup Checklist

Before starting the presentation:

- [ ] Application launched: `streamlit run src/ui/app.py`
- [ ] Browser open at `http://localhost:8501`
- [ ] Sample mathematics PDF paper ready in a known folder
- [ ] Terminal hidden or minimised (no debug output visible)
- [ ] All browser notifications disabled
- [ ] Screen resolution: 1920×1080 (or full-screen browser)
- [ ] Font size increased for visibility (browser zoom: 110–125%)
- [ ] No irrelevant browser tabs open

---

## Section 1 — Introduction

**⏱ Approximate Time: 30 seconds**

> *"Good [morning/afternoon]. Today I'm going to show you MathResearch Studio — an AI-powered research workspace I built from scratch for mathematicians, MSc students, PhD scholars, and academic research groups.*
>
> *This is a full-stack AI application that combines natural language processing, retrieval-augmented generation, and graph analysis — all focused on one specific problem: helping mathematics researchers understand and navigate complex academic literature."*

**Transition**: *"Let me start by explaining the problem I set out to solve."*

---

## Section 2 — Project Motivation

**⏱ Approximate Time: 45 seconds**

> *"If you've ever done academic research in mathematics, you know the workflow. You download fifteen papers from arXiv, open them in PDF viewers, try to cross-reference theorems across authors, track notation that changes from paper to paper, and spend more time searching for a specific lemma than actually doing mathematics.*
>
> *Existing tools — Mathematica, Lean, Coq — are symbolic computation engines. They help you prove theorems. But none of them help you understand, navigate, or organise the mathematical literature you're reading.*
>
> *That's the gap MathResearch Studio fills."*

---

## Section 3 — Problem Statement

**⏱ Approximate Time: 45 seconds**

> *"The core research workflow problem has four components:*
>
> *First — **Notation fragmentation**. The symbol σ means covariance in one paper and a permutation in another. Researchers maintain manual notation sheets.*
>
> *Second — **Theorem dependency tracing**. Understanding why Theorem 4 holds means tracking which lemmas it depends on, which may span three different papers.*
>
> *Third — **Knowledge retrieval**. When you need to find the formal definition of a Hilbert-Schmidt operator across a 400-page reading list, you're doing full-text search by hand.*
>
> *Fourth — **Literature summarisation**. Writing a literature review section means re-reading papers and manually synthesising key results. This is slow, error-prone, and disconnected from the actual evidence."*

---

## Section 4 — Existing Research Workflow Problems

**⏱ Approximate Time: 30 seconds**

> *"The tools researchers currently use for this workflow are:*
>
> - *PDF viewers with manual bookmarks*
> - *Spreadsheets for tracking theorems*
> - *Zotero or Mendeley for references — but no semantic understanding*
> - *ChatGPT — but it hallucinates theorem statements, invents citations, and has no access to your specific papers*
>
> *None of these are document-grounded. None of them understand mathematical structure. MathResearch Studio is built specifically for this."*

---

## Section 5 — Why MathResearch Studio

**⏱ Approximate Time: 30 seconds**

> *"MathResearch Studio is different in three ways:*
>
> *One — it's **document-grounded**. Every answer the AI gives cites the exact paper, section, and page number. No hallucinations.*
>
> *Two — it's **mathematically aware**. The system extracts definitions, theorems, lemmas, and proofs as structured entities — not just raw text.*
>
> *Three — it's **connected**. The dependency graph shows you exactly which mathematical statements depend on which others, across your entire uploaded library."*

---

## Section 6 — System Overview

**⏱ Approximate Time: 45 seconds**

> *"The system is organised into six functional modules:*
>
> 1. **PDF Upload & Document Library** — upload papers, browse extracted knowledge*
> 2. **Mathematical Entity Extraction** — definitions, theorems, lemmas, proofs automatically extracted*
> 3. **Proof Dependency Graph** — interactive directed graph of mathematical dependencies*
> 4. **Notation Dictionary** — auto-generated cross-paper notation reference*
> 5. **Semantic Search** — natural language search across all uploaded papers*
> 6. **AI Research Assistant** — 8-stage RAG pipeline with citations and grounding verification*
>
> *Plus an Export Centre for downloading research notes, and a Statistics Dashboard showing system-wide metrics.*
>
> *Let me show you each of these live."*

---

## Section 7 — Technology Stack

**⏱ Approximate Time: 30 seconds**

> *"Before the live demo, here's a quick overview of the engineering stack:*
>
> - **Frontend**: Streamlit — a Python web framework ideal for data-science tooling*
> - **PDF Parsing**: PyMuPDF — fast, reliable text extraction*
> - **Embeddings**: SentenceTransformers `all-MiniLM-L6-v2` — 384-dimensional dense vectors*
> - **Vector Search**: FAISS (Facebook AI Research) — cosine similarity at scale*
> - **Graph Analysis**: NetworkX directed graph with PyVis visualisation*
> - **AI Pipeline**: Custom 8-stage RAG with evidence mapping, citation engine, and guardrails*
> - **Testing**: 225 pytest unit and integration tests — 100% pass rate*"*

---

## Section 8 — Live Demonstration

**⏱ Approximate Time: 4–5 minutes**

*Follow the [`docs/demo_walkthrough.md`](./demo_walkthrough.md) step-by-step guide for the live portion.*

**Recommended live demo sequence:**

### 8.1 — Launch & Home Page (20 sec)
> *"Here's the application running locally. The home page shows the system at a glance — any papers already in the library, quick statistics, and navigation to every module."*

### 8.2 — Upload a Mathematics Paper (30 sec)
> *"I'll upload a PDF research paper — this one is [describe paper briefly: author, topic, pages]. I click Upload Papers, drag the PDF, and the system immediately begins parsing."*

### 8.3 — Document Library & Knowledge Extraction (45 sec)
> *"The Document Library shows what was extracted. Notice the paper is catalogued with title, authors, and year. Expanding it reveals every definition, theorem, lemma, and proof the parser identified — each tagged with its section name and page number.*
>
> *This is not keyword extraction. The parser identifies formal mathematical environments from the PDF structure."*

### 8.4 — Proof Dependency Graph (30 sec)
> *"The Dependency Graph visualises theorem-lemma relationships as a directed graph. Nodes represent mathematical statements. Edges represent logical dependencies — which theorems this lemma is used to prove.*
>
> *You can see at a glance how knowledge is structured in this paper."*

### 8.5 — Notation Dictionary (20 sec)
> *"The Notation Dictionary extracts all mathematical symbols found across every uploaded paper — Greek letters, operators, sets — and organises them by category. Perfect for thesis writing."*

### 8.6 — Semantic Search (30 sec)
> *"Here's semantic search. I type a natural language query — for example, 'compactness of bounded operators' — and the system retrieves the most relevant passages from all uploaded papers, ranked by cosine similarity. Results include a relevance score and a highlighted excerpt."*

### 8.7 — AI Research Assistant (60 sec)
> *"This is the core feature. I ask the AI assistant a research question — [type a specific question relevant to the uploaded paper].*
>
> *Watch what happens: the system runs eight stages — query processing, hybrid retrieval, context selection, answer generation, evidence mapping, citation insertion, grounding verification, and guardrails.*
>
> *The answer arrives in under 100 milliseconds in demo mode. It's structured into: a direct summary, detailed explanation, relevant definitions, relevant theorems, and a caveats section.*
>
> *Crucially — every claim in the answer is cited. You can see [1], [2] inline, and a full bibliography at the bottom. The grounding score tells you what fraction of the answer is supported by retrieved evidence."*

### 8.8 — Statistics Dashboard (20 sec)
> *"The Statistics Dashboard shows system-wide metrics — total papers, entities extracted, vector passages indexed, graph node and edge counts, and publication year distribution."*

### 8.9 — Export Centre (20 sec)
> *"Finally, the Export Centre. I can download my entire research session — notes, extracted entities, paper metadata — in Markdown, JSON, CSV, or PDF formats. Ready to paste into a thesis chapter."*

---

## Section 9 — Future Roadmap

**⏱ Approximate Time: 30 seconds**

> *"Version 1.0.0 ships with a deterministic offline AI adapter. The roadmap for v2.0 includes:*
>
> - *Real LLM integration — OpenAI GPT-4o, Anthropic Claude, Ollama Llama 3*
> - *GPU/ONNX accelerated embedding — 10x faster than CPU inference*
> - *Cloud vector database — Pinecone or Milvus for enterprise scale*
> - *arXiv and Semantic Scholar direct import*
> - *3D interactive dependency graph with WebGL*
> - *Mobile-responsive interface*"*

---

## Section 10 — Closing

**⏱ Approximate Time: 20 seconds**

> *"MathResearch Studio v1.0.0 is a production-quality AI research tool backed by 225 automated tests, full documentation, and a clean modular codebase.*
>
> *The repository is available at github.com/Anamikamahi18/MathResearch_Studio — it includes the full source code, architectural design documents, performance benchmarks, and release notes.*
>
> *Thank you. I'm happy to answer any questions, or dive deeper into any part of the system."*

---

## Speaker Notes

- Speak slowly — technical concepts need time to land.
- Do not rush the AI assistant section — it's the most impressive part.
- If a live step fails, use the backup screenshots from `docs/demo_assets.md`.
- Keep mouse movements deliberate — slow and smooth is more professional than fast and erratic.
- Pause for 2 seconds after each module transition to let the viewer process what they're seeing.

---

*MathResearch Studio v1.0.0 · Demo Script · 2026*
