# MathResearch Studio v1.0.0 — Release Notes

**Release Date**: 6 August 2026  
**Version**: `1.0.0`  
**Status**: Production Release  
**License**: MIT  

---

## Release Summary

**MathResearch Studio v1.0.0** is the first complete, production-quality release of an AI-powered mathematical research workspace designed for mathematicians, MSc and PhD students, and academic research groups.

This release delivers a **fully integrated end-to-end research workflow** — from uploading PDF research papers to receiving structured, evidence-backed answers from an AI assistant grounded exclusively in the uploaded literature. The application is validated by **225 automated tests** (100% pass rate) and a complete 10-module end-to-end system verification.

---

## Project Motivation

Mathematics researchers spend enormous time reading papers, tracing theorem and definition dependencies, organizing notation across multiple authors, and building notes for surveys, thesis chapters, and grant reports. Existing tools focus on symbolic computation and theorem proving, leaving the **literature understanding and knowledge organization workflow** largely underserved.

**MathResearch Studio** addresses this gap directly — acting as an intelligent, document-grounded research companion rather than a symbolic mathematics engine.

---

## What's New in v1.0.0

This is the inaugural release. All features below are new.

---

## Core Features

### 📄 PDF Upload & Document Library
Upload mathematics research papers in PDF format. The system automatically parses document text, extracts structural sections, identifies page ranges, and catalogs papers with authors, year, and abstract metadata. Previously uploaded papers can be browsed, expanded, and deleted from the **Document Library** page.

### 🔍 Mathematical Entity Extraction
The parsing pipeline automatically identifies and extracts:
- **Definitions** — Formal mathematical definitions with section and page references
- **Theorems** — Theorem statements and their logical conditions
- **Lemmas** — Auxiliary mathematical lemmas
- **Proofs** — Formal proof text linked to antecedent theorems

### 🕸️ Proof Dependency Graph
Builds an interactive directed graph of mathematical statement dependencies. Visualize which theorems depend on which lemmas, definitions, and corollaries — across the entire uploaded paper library. Graph metrics (nodes, edges, average degree, density) are displayed for the full corpus.

### 📖 Notation Dictionary
Automatically constructs a mathematical notation dictionary from all uploaded papers. Browse and search symbols, variables, operators, sets, and matrices organized by domain category.

### 🔎 Semantic Paper Search
Natural language semantic search across the complete uploaded paper library. Powered by dense 384-dimensional SentenceTransformer embeddings and FAISS cosine similarity search. Results include relevance scores and highlighted passage previews.

### 💬 AI Research Assistant
An 8-stage Retrieval-Augmented Generation (RAG) pipeline answers research questions grounded **exclusively** in uploaded papers:
1. **Query Processing** — Intent classification and mathematical entity extraction
2. **Hybrid Retrieval** — FAISS vector search + keyword matching + graph adjacency boosting
3. **Prompt Building** — Token-budgeted context selection
4. **Answer Generation** — Structured 5-section response (summary, details, definitions, theorems, caveats)
5. **Evidence Mapping** — Sentence-level source alignment (DIRECT / PARTIAL / WEAK)
6. **Citation Engine** — Academic citations (inline `[1]`, author-year `(Smith, 2024)`, academic `[Paper, §Section, p.N]`)
7. **Grounding Verification** — Grounding coverage score (0–1) measuring evidence support
8. **Guardrails** — Response policy enforcement (PASS / WARNING / REFUSE)

### 📊 Research Statistics Dashboard
System-wide overview: total papers cataloged, mathematical entities extracted, vector passages indexed, graph nodes and edges, statement type distribution, and publication year distribution.

### 💾 Export Center
Export organized research materials in four formats:
- **Markdown** — Human-readable notes for thesis and survey writing
- **JSON** — Structured data for downstream analysis pipelines
- **CSV** — Spreadsheet-compatible paper metadata
- **PDF** — Printable research summary reports

---

## Testing Summary

| Test Category | Count | Result |
|---|---|---|
| Unit & Integration Tests (pytest) | **225** | **225 Passed (100%)** |
| End-to-End Module Verification | **10** | **10 Passed (100%)** |
| Performance Benchmarks | **11** | **11 Passed (100%)** |

---

## Performance Summary

| Operation | Measured Latency |
|---|---|
| PDF Upload | ~14 ms |
| PDF Parsing | ~113 ms |
| Knowledge Extraction | ~0.01 ms |
| Embedding Generation | ~321 ms |
| FAISS Vector Storage | ~0.17 ms |
| Dependency Graph Construction | ~0.28 ms |
| Notation Dictionary Generation | ~0.20 ms |
| Semantic Search | ~244 ms |
| AI Assistant (8-stage RAG) | ~34 ms |
| Statistics Dashboard Load | ~0.50 ms |
| Export File Generation | ~1.34 ms |
| **Average** | **~66 ms** |

Full performance documentation: [`docs/performance.md`](./performance.md)

---

## Known Limitations

1. **CPU-only embedding inference**: SentenceTransformers runs on CPU by default. Papers over 50 pages may take 300–500 ms to embed. *Workaround: upload shorter or split PDFs.*
2. **Scanned image PDFs**: PyMuPDF requires text-layer PDFs. Scanned image-only PDFs must be pre-processed with an OCR tool. *Workaround: use Tesseract or Adobe Acrobat before uploading.*
3. **Local FAISS index storage**: The vector index lives at `exports/vector_store/`. Clearing the folder deletes the index. *Workaround: re-ingest papers or click **Refresh Library**.*
4. **Offline LLM adapter**: v1.0.0 ships with a deterministic `MockLLMAdapter`. Real LLM integration (OpenAI, Ollama) requires the `LLM_PROVIDER` environment variable and appropriate API keys.

Full details: [`docs/known_issues.md`](./known_issues.md)

---

## Installation

### Requirements
- Python 3.11+ (3.12 recommended)
- Git

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/Anamikamahi18/MathResearch_Studio.git
cd MathResearch_Studio

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify (all 225 tests should pass)
python -m pytest
```

---

## Quick Start

```bash
# Launch the research dashboard
streamlit run src/ui/app.py
```

Open **http://localhost:8501** in your browser.

**First-use workflow:**
1. Go to **📤 Upload Papers** → upload your PDF research papers.
2. Go to **📚 Document Library** → browse extracted definitions, theorems, and lemmas.
3. Go to **🔎 Semantic Search** → search for passages across your library.
4. Go to **💬 AI Research Assistant** → ask questions grounded in your papers.
5. Go to **💾 Export Center** → download your organized research notes.

---

## Documentation

| Document | Description |
|---|---|
| [`README.md`](../README.md) | Complete project overview, installation, and usage guide |
| [`docs/deployment.md`](./deployment.md) | Detailed deployment instructions |
| [`docs/performance.md`](./performance.md) | Performance benchmarks and bottleneck analysis |
| [`docs/known_issues.md`](./known_issues.md) | Resolved bugs, limitations, and workarounds |
| [`CHANGELOG.md`](../CHANGELOG.md) | Full version history |
| [`CONTRIBUTING.md`](../CONTRIBUTING.md) | Contribution guidelines |
| [`SECURITY.md`](../SECURITY.md) | Security policy and vulnerability reporting |

---

## Future Roadmap

### Version 2.0 (Planned)
- GPU/ONNX accelerated embedding inference (10× faster)
- Real LLM API integration (OpenAI GPT-4o, Anthropic Claude 3.5, Ollama Llama 3)
- Cloud vector database adapter (Pinecone / Milvus)
- Interactive 3D dependency graph visualization (WebGL)
- Multi-paper cross-reference relationship analysis
- arXiv and Semantic Scholar paper import integrations
- Mobile-responsive Streamlit interface

### Long-Term Vision
A comprehensive AI-powered mathematics research platform serving MSc students, PhD scholars, university research groups, and mathematical institutes worldwide.

---

## Acknowledgements

- **SentenceTransformers / Hugging Face** — `all-MiniLM-L6-v2` model for fast, high-quality sentence embeddings.
- **FAISS (Facebook AI Research)** — Efficient cosine similarity vector search at scale.
- **PyMuPDF (Artifex Software)** — Reliable, fast PDF text extraction.
- **NetworkX** — Graph analysis and dependency modeling.
- **PyVis** — Interactive network graph visualization.
- **Streamlit** — The framework powering the interactive researcher dashboard.

---

*MathResearch Studio v1.0.0 · MIT License · 2026*
