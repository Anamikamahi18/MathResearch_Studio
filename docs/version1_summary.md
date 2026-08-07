# MathResearch Studio — Version 1.0.0 Summary

**Version**: 1.0.0  
**Release Date**: 6 August 2026  
**Repository**: [github.com/Anamikamahi18/MathResearch_Studio](https://github.com/Anamikamahi18/MathResearch_Studio)  
**License**: MIT  

---

## 1. Project Vision

Mathematics research is dense, formal, and notation-heavy. Researchers spend hours cross-referencing theorems across papers, tracing proof dependencies, reconciling notation conventions between authors, and manually organising findings into notes. No existing tool addresses this workflow holistically — theorem provers verify formal proofs but cannot read natural-language PDFs; reference managers store papers but do not understand their content; general AI assistants hallucinate mathematical claims without grounding them in the actual source text.

**MathResearch Studio** was built to fill this gap: an AI-powered local research workspace that transforms uploaded PDF papers into a structured, searchable, and query-ready knowledge environment — grounded strictly in the uploaded literature.

---

## 2. Objectives Achieved

| Objective | Status |
|---|---|
| Parse PDF mathematics papers into structured entities | ✅ |
| Extract definitions, theorems, lemmas, proofs automatically | ✅ |
| Build a semantic vector search over uploaded paper collections | ✅ |
| Answer research questions grounded exclusively in uploaded papers | ✅ |
| Visualise theorem-to-proof dependency chains as interactive graphs | ✅ |
| Organise mathematical notation into a searchable dictionary | ✅ |
| Export organised research notes in multiple formats | ✅ |
| Deliver a full-featured Streamlit UI with 8 pages | ✅ |
| Achieve 225 automated tests at 100% pass rate | ✅ |
| Benchmark 11 core operations with documented results | ✅ |
| Publish a complete professional release documentation package | ✅ |

All 11 stated v1.0.0 objectives were fully achieved.

---

## 3. Core Research Workflow

The primary workflow MathResearch Studio enables:

```
1. Upload PDF mathematics papers
        ↓
2. Automatic text extraction (PyMuPDF)
        ↓
3. Mathematical entity extraction
   (definitions, theorems, lemmas, proofs)
        ↓
4. Passage embedding + FAISS vector indexing
        ↓
5. Browse the Document Library
        ↓
6. Semantic search across all papers
        ↓
7. Ask the AI Research Assistant
   (8-stage RAG pipeline → grounded answer + citations)
        ↓
8. Explore the Proof Dependency Graph
        ↓
9. Browse the Notation Dictionary
        ↓
10. Export research notes (MD / JSON / CSV / PDF)
```

Each step runs locally, offline, without any external API calls. No data ever leaves the researcher's machine.

---

## 4. Major Features

### PDF Upload & Document Library
Drag-and-drop PDF upload with automatic parsing and cataloguing. The Document Library provides a per-paper browser of all extracted entities with section and page references.

### Mathematical Entity Extraction
Rule-based NLP pipeline detects formal mathematical environments (theorem/definition/lemma/proof blocks) from PDF text layers. Extracts entity type, full text, section location, and page number for every formal statement in the paper.

### Semantic Paper Search
Dense vector search using SentenceTransformers `all-MiniLM-L6-v2` (384-dimensional embeddings) stored in a FAISS `IndexFlatIP` index. Returns the most semantically similar passages across all uploaded papers, ranked by cosine similarity, with a relevance score displayed to the researcher.

### AI Research Assistant — 8-Stage RAG Pipeline
The centrepiece of MathResearch Studio. A fully custom Retrieval-Augmented Generation pipeline answers research questions grounded strictly in uploaded papers:

| Stage | Module | Function |
|---|---|---|
| 1 | QueryProcessor | Intent classification, entity extraction from query |
| 2 | HybridRetriever | FAISS + keyword + graph adjacency hybrid scoring |
| 3 | PromptBuilder | Token-budgeted context assembly (max 1,500 tokens) |
| 4 | LLMAdapter | Pluggable LLM interface (MockLLMAdapter in v1.0.0) |
| 5 | AnswerGenerator | Structured 5-section response generation |
| 6 | EvidenceMapper | Sentence-level source alignment (DIRECT/PARTIAL/WEAK) |
| 6b | CitationEngine | Academic citation formatting (inline, author-year, academic) |
| 7 | GroundingVerifier | Evidence coverage score (0–1) computation |
| 8 | GuardrailEngine | PASS / WARNING / REFUSE policy enforcement |

### Proof Dependency Graph
NetworkX directed multigraph where nodes are mathematical statements and edges represent logical dependency relationships. Rendered as an interactive HTML network using PyVis, embedded in the Streamlit UI.

### Notation Dictionary
Cross-paper symbol extraction identifying variables, operators, Greek letters, sets, and matrix notation. Organised by domain category with search and filter functionality.

### Research Statistics Dashboard
Real-time system metrics: papers catalogued, entities extracted by type, vector passages indexed, graph topology statistics, and publication year distribution.

### Export Center
One-click download of research materials in four formats:
- **Markdown** — readable notes for writing workflows
- **JSON** — structured data for downstream processing
- **CSV** — spreadsheet-compatible paper metadata
- **PDF** — printable research summaries

---

## 5. Architecture Overview

MathResearch Studio follows a strict 6-layer architecture with no circular dependencies:

```
┌─────────────────────────────────────┐
│  Streamlit UI (src/ui/)             │  Layer 6 — Presentation
│  8 research pages + router + shell  │
├─────────────────────────────────────┤
│  Application Services               │  Layer 5 — Orchestration
│  (src/application/)                 │
│  DocumentService, SearchService,    │
│  ChatService, GraphService,         │
│  DashboardService, ExportService    │
├─────────────────────────────────────┤
│  RAG Pipeline (src/rag/)            │  Layer 4 — AI / Generation
│  8-stage pipeline                   │
├─────────────────────────────────────┤
│  Graph Engine (src/graph/)          │  Layer 3 — Knowledge Graph
│  NetworkX + PyVis + Notation Dict   │
├─────────────────────────────────────┤
│  Embeddings (src/embeddings/)       │  Layer 2 — Vector Semantics
│  SentenceTransformers + FAISS       │
├─────────────────────────────────────┤
│  Parser (src/parser/)               │  Layer 1 — Ingestion
│  PyMuPDF + Entity Extraction        │
└─────────────────────────────────────┘
         ↕ Storage
  uploads/  exports/  exports/vector_store/
```

**Design Principles Applied**:
- Single Responsibility: every class has one well-defined purpose
- Adapter Pattern: `LLMAdapter` interface decouples AI from the RAG pipeline
- Repository Pattern: `FAISSVectorStore` encapsulates all vector operations
- Service Layer Pattern: application services orchestrate domain modules
- Strategy Pattern: `CitationStyle` enum selects citation format at runtime

---

## 6. Technology Stack

| Category | Technology | Version / Notes |
|---|---|---|
| Language | Python | 3.12 |
| UI Framework | Streamlit | Interactive research dashboard |
| PDF Parsing | PyMuPDF (fitz) | Text layer extraction |
| Embeddings | SentenceTransformers | `all-MiniLM-L6-v2` — 384-d |
| Vector Search | FAISS | `IndexFlatIP` — cosine similarity |
| Graph Engine | NetworkX | Directed multigraph |
| Graph Visualisation | PyVis | HTML interactive network |
| AI / LLM | MockLLMAdapter | Offline; pluggable for GPT-4o / Ollama |
| Testing | pytest | 225 tests, fixtures, parametrize |
| Version Control | Git / GitHub | Public repository, tagged release |

---

## 7. Testing Summary

| Category | Result |
|---|---|
| Total pytest tests | **225** |
| Pass rate | **100%** |
| Test files | **32** |
| Modules tested | **10** |
| End-to-end verification | **10 / 10 PASS** |
| Performance benchmarks | **11 / 11 PASS** |
| Bugs found and fixed before release | **5** |
| Mock providers (no external deps) | MockLLMAdapter, MockEmbeddingProvider |

---

## 8. Performance Summary

| Operation | Latency |
|---|---|
| PDF Upload | ~14 ms |
| PDF Parsing | ~113 ms |
| Knowledge Extraction | ~0.01 ms |
| Embedding Generation | ~321 ms ⭐ primary bottleneck |
| FAISS Vector Storage | ~0.17 ms |
| Dependency Graph Build | ~0.28 ms |
| Notation Dictionary Build | ~0.20 ms |
| Semantic Search | ~244 ms |
| AI Research Assistant | ~34 ms |
| Statistics Dashboard | ~0.50 ms |
| Export Generation | ~1.34 ms |
| **Average** | **~66 ms** |

⭐ Embedding generation (321 ms) uses CPU-only inference. GPU/ONNX planned for v2.0 (projected 10× speedup).

---

## 9. Known Limitations

| Limitation | Impact | v2.0 Plan |
|---|---|---|
| CPU-only embedding inference | ~321 ms per paper | GPU/ONNX acceleration |
| Text-layer PDFs only | Scanned images fail | Tesseract OCR integration |
| MockLLMAdapter only | Deterministic mock responses | Real LLM integration |
| Local FAISS index | Resets if `exports/` cleared | Persistent cloud vector DB |
| Single-user, local only | No collaboration | Multi-user cloud backend |
| English-only | Non-English papers untested | Multilingual model |
| No Docker container | Manual install required | Docker image for v2.0 |

Full details: [`docs/known_issues.md`](known_issues.md)

---

## 10. Version 2 Roadmap

### Near-Term (v2.0)
- GPU/ONNX accelerated embedding inference — 10× faster
- Real LLM integration: OpenAI GPT-4o, Anthropic Claude, Ollama Llama 3
- Cloud vector database adapter: Pinecone or Milvus
- Persistent user library (SQLite or PostgreSQL backend)
- arXiv and Semantic Scholar direct paper import
- Docker container for one-command deployment

### Medium-Term (v2.1)
- Interactive 3D dependency graph (WebGL / D3.js)
- Multi-paper cross-reference relationship analysis
- Collaborative annotation and shared research notes
- Mobile-responsive interface
- LaTeXML formula annotation integration

### Long-Term Vision
Building MathResearch Studio into a comprehensive AI-powered mathematics research platform used by MSc students, PhD scholars, university research groups, and mathematical institutes worldwide — open-source, locally deployable, and researcher-controlled.

---

## 11. Key Lessons

### What Structured Day-by-Day Planning Enables
Building a 159-file, 225-test Python application in 7 days requires rigid daily milestones. Beginning each day with a design document and ending with an engineering report prevented scope creep and ensured that every module was documented before the next began.

### Mock Providers Are Not Optional
The `MockLLMAdapter` and `MockEmbeddingProvider` were designed on Day 1. Without them, 225 tests would be slow (3s model load per test × 225 = 11 minutes) and brittle (API calls would fail in CI). These are production-grade testing patterns, not shortcuts.

### Grounding Before Generation
The most important architectural decision was placing the `GroundingVerifier` and `GuardrailEngine` as independent pipeline stages after answer generation — not as afterthoughts. Refusing to answer when evidence is insufficient is harder to build than generating a fluent but hallucinated response. It is also far more valuable for a research tool.

### Documentation Is Code
The 40 design documents in `docs/` and 32 engineering reports in `reports/` are not overhead — they are the artefact that makes the code trustworthy, reproducible, and extensible. An MSc project without documentation is not a project; it is a script.

---

*MathResearch Studio v1.0.0 · Version Summary · 7 August 2026*
