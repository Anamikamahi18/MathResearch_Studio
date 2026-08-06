# MathResearch Studio v1.0.0 — Recruiter & Portfolio Demo Guide

**For**: Technical recruiters, hiring managers, MSc/PhD supervisors, professors, research groups  
**Repository**: [github.com/Anamikamahi18/MathResearch_Studio](https://github.com/Anamikamahi18/MathResearch_Studio)  
**Version**: 1.0.0 · Production Release · MIT License · August 2026

---

## Executive Summary

**MathResearch Studio** is a full-stack, AI-powered mathematics research workspace built over 7 development days.  
It solves a real, domain-specific problem — helping mathematicians navigate complex academic literature — using a production-grade software engineering approach backed by 225 automated tests.

This document explains what the project demonstrates, why it is portfolio quality, and what technical skills it proves.

---

## 1. Project Value

### Problem Being Solved

Mathematics researchers face a concrete workflow problem: academic papers contain dense, interdependent mathematical structures — definitions, theorems, lemmas, proofs — that are difficult to navigate, cross-reference, and organise across multiple papers.

Existing tools fall into two categories:

- **Symbolic engines** (Mathematica, Lean, Coq) — prove theorems but do not help researchers understand literature.
- **Reference managers** (Zotero, Mendeley) — organise citations but provide no semantic understanding or AI capabilities.

MathResearch Studio fills this gap with an AI-powered document understanding system.

### Value Delivered

| Capability | Value |
|---|---|
| Automatic mathematical entity extraction | No manual cataloguing of definitions and theorems |
| AI assistant grounded in uploaded papers | Accurate, cited answers — no hallucinations |
| Proof dependency graph | Visual understanding of theorem-lemma relationships |
| Notation dictionary | Cross-paper symbol reference without manual sheets |
| Semantic search | Natural language search over all uploaded papers |
| Research export | Structured notes ready for thesis writing |

---

## 2. AI Components

This project implements **three distinct AI/ML subsystems** from scratch:

### 2.1 Semantic Embedding Pipeline
- **Model**: `all-MiniLM-L6-v2` (SentenceTransformers, Hugging Face)
- **Output**: 384-dimensional dense vectors representing passage semantics
- **Index**: FAISS `IndexFlatIP` with L2 normalisation for cosine similarity
- **Performance**: ~321 ms per paper (CPU inference)
- **Relevance**: Production-grade NLP — the same model family used in semantic search systems at industry scale

### 2.2 Retrieval-Augmented Generation (RAG) Pipeline — 8 Stages
The AI Research Assistant runs a complete, multi-stage RAG pipeline:

| Stage | Component | Function |
|---|---|---|
| 1 | `QueryProcessor` | Intent classification, mathematical entity extraction from query |
| 2 | `HybridRetriever` | FAISS vector search + keyword matching + graph adjacency boosting |
| 3 | `PromptBuilder` | Token-budgeted context assembly (max 1,500 context tokens) |
| 4 | `AnswerGenerator` | Structured 5-section response generation via `LLMAdapter` |
| 5 | `EvidenceMapper` | Sentence-level source alignment (DIRECT / PARTIAL / WEAK) |
| 6 | `CitationEngine` | Multi-format citation insertion (inline, author-year, academic) |
| 7 | `GroundingVerifier` | Grounding coverage score (0–1) measuring evidence support |
| 8 | `GuardrailEngine` | Response policy enforcement (PASS / WARNING / REFUSE) |

**Why this matters**: Building a complete RAG pipeline requires understanding retrieval theory, prompt engineering, citation consistency, grounding verification, and content safety — skills directly transferable to industry AI engineering roles.

### 2.3 Knowledge Graph Construction
- **Library**: NetworkX directed multigraph (`DiGraph`)
- **Visualisation**: PyVis interactive HTML graph
- **Signals**: Theorem-proof antecedent relationships extracted from formal environments
- **Metrics**: Node count, edge count, average degree, graph density

---

## 3. NLP Pipeline

The information extraction pipeline processes mathematics PDFs through several NLP stages:

### 3.1 PDF Text Extraction
- **Tool**: PyMuPDF (`fitz`)
- **Capability**: Text-layer extraction with page-level segmentation, section header detection, and metadata parsing

### 3.2 Mathematical Environment Detection
The parser uses **rule-based NLP** with domain-specific patterns to identify:

| Entity Type | Detection Strategy |
|---|---|
| Definitions | LaTeX environment markers + heuristic section labels |
| Theorems | Formal environment patterns (`Theorem`, `Proposition`, `Corollary`) |
| Lemmas | Auxiliary theorem patterns |
| Proofs | Proof environment markers + `Proof.` prefix detection |

### 3.3 Notation Symbol Extraction
- Identifies Greek letters, operators, set notation, and matrix symbols
- Categorises by domain (Greek Letters, Operators, Sets, Matrices, Variables)
- Cross-references symbols across multiple uploaded papers

### 3.4 Text Chunking Strategy
- Semantic chunking by section and paragraph
- Chunk size calibrated for embedding quality and context window fit
- Deduplication and diversity enforcement in retrieval

---

## 4. RAG Pipeline (Technical Deep-Dive)

### Design Decisions Worth Highlighting

**Why RAG instead of full-document LLM?**

- Prevents "lost-in-the-middle" attention degradation on 30–100 page papers
- Enforces citation precision — every claim is linked to a specific chunk
- Enables hallucination-free responses by constraining context
- Reduces token consumption from O(full paper) to O(3–5 relevant chunks)

**Hybrid Retrieval Formula**:
```
FinalScore = w_semantic × S_semantic
           + w_entity  × S_entity
           + w_intent  × S_intent
           + w_graph   × S_graph
           + S_boost
```

This weighted scoring combines:
- Semantic similarity (dense vector cosine)
- Mathematical entity overlap (symbol and term matching)
- Query intent alignment (definition query → boost definition chunks)
- Graph topology signals (prerequisite lemma boosting)

**Grounding Verification**:
- Every generated answer receives a grounding score (0.0–1.0)
- Score measures what fraction of the answer text is traceable to retrieved evidence
- Scores below threshold trigger a WARNING guardrail label

**Guardrail Engine**:
- `PASS` — fully grounded, evidence-supported response
- `WARNING` — partial grounding, answer contains speculation
- `REFUSE` — insufficient evidence, query cannot be answered from uploads

---

## 5. Information Extraction

The knowledge extraction pipeline demonstrates:

- **Regex-based formal environment parsing** — domain-specific pattern design for LaTeX math
- **Structural PDF analysis** — section detection, page mapping, hierarchy reconstruction
- **Entity classification** — multi-class mathematical statement categorisation
- **Metadata extraction** — title, authors, year, abstract, page count from PDF headers

All extracted entities are stored in a structured JSON schema and immediately available for:
- Graph construction
- Notation dictionary generation
- Export report generation
- RAG context retrieval

---

## 6. Graph Analysis

The Research Graph module demonstrates graph theory applied to academic literature:

- **Node types**: Theorems, Lemmas, Definitions, Proofs
- **Edge semantics**: Logical dependency (A → B = "A is used to prove B")
- **Cross-paper edges**: Dependencies detected across multiple uploaded papers
- **Metrics**: Degree distribution, graph density, connected components
- **Visualisation**: Interactive PyVis graph with drag, zoom, hover

This demonstrates understanding of both graph data structures and research-domain knowledge representation.

---

## 7. Software Engineering Practices

### 7.1 Architecture

**Layered, modular design:**

```
src/
├── parser/          ← PDF parsing and entity extraction
├── embeddings/      ← Embedding pipeline and FAISS vector store
├── graph/           ← NetworkX dependency graph service
├── rag/             ← 8-stage RAG pipeline (8 modules)
├── export/          ← Multi-format export engine
├── application/     ← Service orchestration layer
└── ui/              ← Streamlit pages, layout, state management
```

Each module has:
- A single, well-defined responsibility
- A clean public interface
- No circular dependencies
- Isolated testability

### 7.2 Design Patterns Applied
- **Service layer pattern** — application services orchestrate domain modules
- **Adapter pattern** — `LLMAdapter` abstracts the LLM backend (mock/real)
- **Strategy pattern** — `CitationStyle` enum selects citation format at runtime
- **Repository pattern** — FAISS vector store wraps the index behind a clean API
- **Factory pattern** — `EmbeddingProviderFactory` selects provider by config

### 7.3 Code Quality
- All modules use type annotations (Python type hints throughout)
- Docstrings on all public classes and methods
- Configuration managed via `src/ui/config.py` (no hardcoded values in logic)
- Constants centralised and named (no magic numbers)

---

## 8. Testing

### 8.1 Test Metrics

| Category | Count | Result |
|---|---|---|
| Unit & Integration Tests (pytest) | **225** | **225 Passed (100%)** |
| End-to-End Module Verification | **10** | **10 Passed (100%)** |
| Performance Benchmarks | **11** | **11 Passed (100%)** |

### 8.2 Test Coverage Areas

| Module | Tests Cover |
|---|---|
| PDF Parser | Text extraction, entity detection, malformed input handling |
| Embedding Pipeline | Vector generation, FAISS index insertion, similarity retrieval |
| Graph Service | Node creation, edge addition, dependency detection, metric computation |
| RAG Pipeline | All 8 stages independently tested + integration test |
| Export Engine | Markdown, JSON, CSV generation; filename sanitisation |
| UI Pages | Render tests via Streamlit test utilities |
| Application Services | Service orchestration and dependency injection |

### 8.3 Test Design Quality
- Uses `MockEmbeddingProvider` for offline testing without PyTorch model loading
- Uses `MockLLMAdapter` for deterministic RAG pipeline testing
- Fixtures and parametrize used throughout
- Edge cases covered: empty library, no entities found, malformed PDFs

---

## 9. Performance

All 11 core operations benchmarked with `time.perf_counter`:

| Operation | Latency | Assessment |
|---|---|---|
| PDF Upload | 14 ms | Excellent |
| PDF Parsing | 113 ms | Good (scales with page count) |
| Knowledge Extraction | 0.01 ms | Excellent |
| Embedding Generation | 321 ms | Acceptable (CPU; GPU target: ~30 ms) |
| FAISS Vector Storage | 0.17 ms | Excellent |
| Dependency Graph | 0.28 ms | Excellent |
| Notation Dictionary | 0.20 ms | Excellent |
| Semantic Search | 244 ms | Good (model load + vector search) |
| AI Assistant (RAG) | 34 ms | Excellent |
| Statistics Dashboard | 0.50 ms | Excellent |
| Export Generation | 1.34 ms | Excellent |
| **Average** | **66 ms** | **Production-ready** |

---

## 10. Documentation

| Document | Coverage |
|---|---|
| `README.md` | Full installation, usage, architecture overview (15 KB) |
| `docs/release_notes_v1.0.0.md` | Complete feature list, testing summary, performance |
| `docs/rag_design.md` | RAG system design rationale |
| `docs/parser_design.md` | PDF parsing architecture |
| `docs/embedding_design.md` | Embedding and FAISS design |
| `docs/performance.md` | Benchmark methodology and results |
| `docs/known_issues.md` | Limitations, workarounds, future roadmap |
| `docs/deployment.md` | Deployment instructions |
| `CHANGELOG.md` | Full version history |
| `CONTRIBUTING.md` | Contribution guidelines |
| `SECURITY.md` | Security policy |
| `CODE_OF_CONDUCT.md` | Community standards |

**Total documentation**: 28 files in `docs/`, plus root-level project files.  
**This is a level of documentation rarely seen in student or portfolio projects.**

---

## 11. Repository Quality

### Repository Structure
```
MathResearch_Studio/
├── src/                    ← All production source code
├── tests/                  ← 225 automated tests
├── docs/                   ← 28 documentation files
├── reports/                ← 28 engineering reports
├── scripts/                ← Utility and benchmark scripts
├── assets/                 ← Visual assets
├── architecture/           ← System design diagrams
├── requirements.txt        ← Pinned dependencies
├── README.md               ← 15 KB project overview
├── CHANGELOG.md            ← Version history
├── CONTRIBUTING.md         ← Contribution guide
├── SECURITY.md             ← Security policy
├── LICENSE                 ← MIT license
└── .github/                ← GitHub Actions workflows
```

### Repository Signals
- Clean commit history with meaningful commit messages
- `v1.0.0` tagged release with full release notes
- `MIT` license — open source, recruiter-accessible
- No secrets or credentials in codebase
- `.gitignore` properly configured

---

## 12. Why This Is Portfolio Quality

### The Rare Combination

This project demonstrates the full vertical stack that separates senior engineers from junior developers:

| Layer | What It Proves |
|---|---|
| AI/ML | Built RAG, embeddings, vector search from scratch — not just API calls |
| NLP | Domain-specific information extraction pipeline |
| Software Architecture | Clean layered design, dependency injection, testability |
| Testing | 225 tests, 100% pass rate, mock strategies |
| Documentation | Production-grade docs covering every design decision |
| Domain Knowledge | Mathematics research domain understanding |
| Product Thinking | Solves a real problem for a real audience |

### Differentiation from Typical Student Projects

| Typical Portfolio Project | MathResearch Studio |
|---|---|
| 0–20 tests | 225 tests (100% pass) |
| No documentation | 28 design documents |
| Single-page app | Multi-module, layered architecture |
| API call wrappers | Custom RAG pipeline, custom embedding pipeline |
| No performance data | 11-operation performance benchmark |
| No release | Tagged GitHub Release with release notes |
| Generic domain | Domain-specific: mathematics research |

### Relevant Roles

This project is directly relevant to:
- **AI/ML Engineering** — RAG, embeddings, information retrieval
- **NLP Engineering** — document understanding, information extraction
- **Backend Engineering** — service architecture, testing, performance
- **Research Engineering** — domain-specific AI tooling
- **Full-Stack Development** — complete application from data layer to UI

---

*MathResearch Studio v1.0.0 · Recruiter Demo Guide · 2026*
