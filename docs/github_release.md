# MathResearch Studio v1.0.0 — GitHub Release Description

**Use this content verbatim when creating the GitHub Release at:**  
`https://github.com/Anamikamahi18/MathResearch_Studio/releases/new`

**Tag**: `v1.0.0` (existing) · **Target**: `main` · **Set as latest**: ✅ Yes

---

# MathResearch Studio v1.0.0

> **An AI-Powered Research Workspace for Mathematics**  
> *From PDF to AI-Grounded Mathematical Knowledge — in seconds.*

**Release Date**: 6 August 2026  
**License**: MIT  
**Python**: 3.11+ (3.12 recommended)

---

## 🎉 Release Summary

**MathResearch Studio v1.0.0** is the first complete, production-quality release of an AI-powered mathematical research workspace designed for mathematicians, MSc and PhD students, and academic research groups.

This release delivers a **fully integrated end-to-end research workflow** — from uploading PDF research papers to receiving structured, evidence-backed answers from an AI assistant grounded exclusively in the uploaded literature. The application is validated by **225 automated tests** (100% pass rate) and a complete 10-module end-to-end system verification.

---

## ✨ Highlights

- 📄 **PDF Upload & Document Library** — Upload mathematics PDFs; browse extracted entities per paper
- 🔍 **Mathematical Entity Extraction** — Definitions, theorems, lemmas, proofs extracted automatically
- 🕸️ **Proof Dependency Graph** — Interactive directed graph of mathematical statement dependencies
- 📖 **Notation Dictionary** — Cross-paper symbol and operator reference, organised by category
- 🔎 **Semantic Search** — Natural language search over your entire paper library (FAISS + SentenceTransformers)
- 💬 **AI Research Assistant** — 8-stage RAG pipeline with inline citations and grounding verification
- 📊 **Research Statistics Dashboard** — System-wide metrics, entity distributions, publication timelines
- 💾 **Export Center** — Download research notes in Markdown, JSON, CSV, and PDF

---

## 🚀 Core Features

### PDF Upload & Document Library
Upload mathematics research papers in PDF format. The system automatically parses document text, extracts structural sections, identifies page ranges, and catalogues papers with authors, year, and abstract metadata.

### Mathematical Entity Extraction
The parsing pipeline automatically identifies and extracts:
- **Definitions** — Formal mathematical definitions with section and page references
- **Theorems** — Theorem statements and their logical conditions
- **Lemmas** — Auxiliary mathematical lemmas
- **Proofs** — Formal proof text linked to antecedent theorems

### Proof Dependency Graph
Builds an interactive directed graph of mathematical statement dependencies. Visualize which theorems depend on which lemmas, definitions, and corollaries — across the entire uploaded paper library.

### Notation Dictionary
Automatically constructs a mathematical notation dictionary from all uploaded papers. Browse and search symbols, variables, operators, sets, and matrices organised by domain category.

### Semantic Paper Search
Natural language semantic search across the complete uploaded paper library. Powered by dense 384-dimensional SentenceTransformer embeddings and FAISS cosine similarity search. Results include relevance scores and highlighted passage previews.

### AI Research Assistant — 8-Stage RAG Pipeline
An 8-stage Retrieval-Augmented Generation pipeline answers research questions grounded **exclusively** in uploaded papers:

1. **Query Processing** — Intent classification and mathematical entity extraction
2. **Hybrid Retrieval** — FAISS vector search + keyword matching + graph adjacency boosting
3. **Prompt Building** — Token-budgeted context selection (max 1,500 context tokens)
4. **Answer Generation** — Structured 5-section response (summary, details, definitions, theorems, caveats)
5. **Evidence Mapping** — Sentence-level source alignment (DIRECT / PARTIAL / WEAK)
6. **Citation Engine** — Academic citations (inline `[1]`, author-year `(Smith, 2024)`, academic `[Paper, §Section, p.N]`)
7. **Grounding Verification** — Grounding coverage score (0–1) measuring evidence support
8. **Guardrails** — Response policy enforcement (PASS / WARNING / REFUSE)

---

## 🧪 Testing Summary

| Test Category | Count | Result |
|---|---|---|
| Unit & Integration Tests (pytest) | **225** | **225 Passed (100%)** |
| End-to-End Module Verification | **10** | **10 Passed (100%)** |
| Performance Benchmarks | **11** | **11 Passed (100%)** |

---

## ⚡ Performance Summary

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

All benchmarks measured on CPU (Python 3.12, Windows, x86_64). GPU/ONNX acceleration planned for v2.0.

---

## 📚 Documentation

| Document | Description |
|---|---|
| [`README.md`](https://github.com/Anamikamahi18/MathResearch_Studio/blob/main/README.md) | Complete project overview, installation, usage guide |
| [`docs/release_notes_v1.0.0.md`](https://github.com/Anamikamahi18/MathResearch_Studio/blob/main/docs/release_notes_v1.0.0.md) | Full release notes |
| [`docs/deployment.md`](https://github.com/Anamikamahi18/MathResearch_Studio/blob/main/docs/deployment.md) | Local and cloud deployment instructions |
| [`docs/performance.md`](https://github.com/Anamikamahi18/MathResearch_Studio/blob/main/docs/performance.md) | Performance benchmarks and bottleneck analysis |
| [`docs/known_issues.md`](https://github.com/Anamikamahi18/MathResearch_Studio/blob/main/docs/known_issues.md) | Resolved bugs, limitations, workarounds |
| [`CHANGELOG.md`](https://github.com/Anamikamahi18/MathResearch_Studio/blob/main/CHANGELOG.md) | Full version history |
| [`CONTRIBUTING.md`](https://github.com/Anamikamahi18/MathResearch_Studio/blob/main/CONTRIBUTING.md) | Contribution guidelines |
| [`SECURITY.md`](https://github.com/Anamikamahi18/MathResearch_Studio/blob/main/SECURITY.md) | Security policy |

---

## 📦 Installation

### Requirements
- Python 3.11+ (3.12 recommended)
- Git

### Setup

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

# 5. Launch the research dashboard
streamlit run src/ui/app.py
```

Open **http://localhost:8501** in your browser.

---

## ⚠️ Known Limitations

1. **CPU-only embedding inference** — SentenceTransformers runs on CPU by default. Papers over 50 pages may take 300–500 ms to embed. *Workaround: upload shorter or split PDFs.*
2. **Scanned image PDFs** — PyMuPDF requires text-layer PDFs. *Workaround: pre-process with Tesseract or Adobe Acrobat.*
3. **Local FAISS index storage** — Vector index lives at `exports/vector_store/`. *Workaround: click **Refresh Library** to rebuild.*
4. **Offline LLM adapter** — v1.0.0 ships with a deterministic `MockLLMAdapter`. Real LLM integration (OpenAI, Ollama) requires the `LLM_PROVIDER` environment variable.
5. **Cloud deployment constraints** — PyTorch + SentenceTransformers (~1.5 GB) exceeds free-tier cloud limits. Designed for local deployment in v1.0.0.

Full details: [`docs/known_issues.md`](https://github.com/Anamikamahi18/MathResearch_Studio/blob/main/docs/known_issues.md)

---

## 🔭 Future Roadmap

### Version 2.0 (Planned)
- GPU/ONNX accelerated embedding inference (10× faster)
- Real LLM API integration (OpenAI GPT-4o, Anthropic Claude, Ollama Llama 3)
- Cloud vector database adapter (Pinecone / Milvus)
- Interactive 3D dependency graph visualisation (WebGL)
- Multi-paper cross-reference relationship analysis
- arXiv and Semantic Scholar paper import integrations
- Mobile-responsive Streamlit interface

---

## 📸 Screenshots

> *Screenshots will be added following the post-release demo recording session.*  
> See [`docs/demo_assets.md`](https://github.com/Anamikamahi18/MathResearch_Studio/blob/main/docs/demo_assets.md) for the full screenshot capture checklist.

---

## 🎬 Demo Video

> *A full walkthrough video demonstrating all key features will be linked here following the demo recording.*  
> See [`docs/demo_script.md`](https://github.com/Anamikamahi18/MathResearch_Studio/blob/main/docs/demo_script.md) for the complete demo script.

---

## 📄 Release Assets

| Asset | Status |
|---|---|
| Source code (zip) | ✅ Auto-generated by GitHub |
| Source code (tar.gz) | ✅ Auto-generated by GitHub |
| `docs/release_notes_v1.0.0.md` | ✅ Available in repository |
| Screenshots | ⏳ Pending — to be uploaded post-recording |
| Demo video | ⏳ Pending — to be linked post-recording |

---

## 🙏 Acknowledgements

- **SentenceTransformers / Hugging Face** — `all-MiniLM-L6-v2` model for fast, high-quality sentence embeddings
- **FAISS (Facebook AI Research)** — Efficient cosine similarity vector search at scale
- **PyMuPDF (Artifex Software)** — Reliable, fast PDF text extraction
- **NetworkX** — Graph analysis and dependency modelling
- **PyVis** — Interactive network graph visualisation
- **Streamlit** — The framework powering the interactive researcher dashboard

---

*MathResearch Studio v1.0.0 · MIT License · © 2026 Anamika Mahi*
