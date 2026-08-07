# MathResearch Studio — Project Retrospective

**Version**: 1.0.0  
**Retrospective Date**: 7 August 2026  
**Development Period**: 7 days (structured day-by-day milestones)  
**Scope**: Complete AI-powered mathematical research workspace

---

## 1. What Went Well

### Architectural Clarity from Day 1
The 6-layer architecture (Parser → Embeddings → Graph → RAG → Services → UI) was defined before a single line of code was written. This paid off continuously across 7 days: adding a new RAG stage, extending export formats, or adding a UI page never required touching unrelated layers. The architecture acted as a stable skeleton that absorbed feature additions without brittleness.

### Mock-First Testing Strategy
Designing `MockLLMAdapter` and `MockEmbeddingProvider` as first-class citizens on Day 1 — not as temporary hacks — was the single most important engineering decision. The 225-test suite runs in under 30 seconds with zero external API calls, zero PyTorch model loading delay (3s saved per test), and zero network dependency. This pattern is used in production ML systems at scale; applying it to a portfolio project demonstrates real professional awareness.

### The 8-Stage RAG Pipeline Decomposition
Breaking the RAG pipeline into 8 independently scoped, independently testable stages (rather than one `answer_query()` function) was the right call. It made each stage replaceable — the `LLMAdapter` can be swapped from `MockLLMAdapter` to `OpenAIAdapter` by changing one environment variable. It made debugging tractable — a failing grounding score can be traced to the `GroundingVerifier` without inspecting the whole pipeline. And it made the architecture explainable to both technical and non-technical audiences.

### Documentation Discipline
Writing a design document before each major module and an engineering report after each milestone created a self-auditing workflow. By Day 7, the 40 documents in `docs/` and 32 reports in `reports/` formed a complete, accurate specification of the system — not as an afterthought, but as a living record of decisions made during development.

### Day 7 as a Full Release Engineering Day
Dedicating the entire final day to QA, testing, performance benchmarking, bug fixing, repository polish, release documentation, demo preparation, presentation preparation, and formal release engineering was essential. Most student projects are "done" when the code runs. Day 7 made this project actually done: documented, tested, validated, and publishable.

---

## 2. Biggest Technical Challenges

### Challenge 1 — Grounding Mathematics Without a Real LLM
The most fundamental tension in the project: building a grounded AI assistant that truthfully refuses to hallucinate, while only having a `MockLLMAdapter` that returns deterministic canned responses. The resolution was to make the architecture correct for a real LLM from day one — the grounding score and guardrail decisions are real, computed from real retrieval results, not mocked. The mock only substitutes the final LLM generation step. When a real LLM is plugged in, the rest of the pipeline is already correct.

### Challenge 2 — Mathematical Entity Extraction Precision
Mathematics papers vary enormously in how they present formal statements. Some use explicit LaTeX theorem environments that produce "Theorem 3.1." in the PDF text. Others use numbered bold-text conventions ("**Theorem** (Compactness)."). Others are fully prose-based. The rule-based extractor was tuned for the most common LaTeX-generated conventions; less standard papers have lower recall. This is an honest, documented limitation — not a hidden deficiency.

### Challenge 3 — PyMuPDF Text Layer Reliability
PDF text extraction is not perfectly reliable. Multi-column layouts, rotated text, embedded mathematical symbols, and ligatures all create extraction artefacts. The parser was designed to be robust to common artefacts (whitespace collapsing, line-end hyphenation) but cannot recover from completely garbled text or image-only PDFs. The known issues documentation is explicit about this.

### Challenge 4 — Keeping FAISS State Across Streamlit Sessions
Streamlit re-runs the entire application script on every user interaction. Maintaining the FAISS index and the in-memory document library across re-runs required careful use of `st.session_state`. The solution — persisting the index to disk at `exports/vector_store/` and reloading it on the next session — works correctly but means that clearing the `exports/` directory resets the vector store. This is documented as a known limitation.

### Challenge 5 — Token Budget Management in the Prompt Builder
The `PromptBuilder` must assemble a context window that fits within the LLM's token budget while including the most relevant retrieved passages. The implementation uses a fixed 1,500-token context budget with a greedy selection strategy (add passages in relevance order until budget is exhausted). A more sophisticated approach would use dynamic token counting per model (different LLMs have different tokenisers). This is a documented v2.0 improvement.

---

## 3. Architecture Decisions

### Decision 1 — Service Layer Pattern (Chosen)
**Alternatives considered**: Direct calls from UI pages to domain modules; a single `AppController` class.  
**Choice**: Six application services (`DocumentService`, `SearchService`, etc.), each owning one bounded context.  
**Rationale**: UI pages should orchestrate, not implement. Service boundaries align with bounded contexts (upload, search, RAG, graph, stats, export) — making each service independently testable and replaceable.  
**Outcome**: Every service has a dedicated test file. Adding a new UI page requires only calling existing service methods — zero new domain logic.

### Decision 2 — Adapter Pattern for LLM (Chosen)
**Alternatives considered**: Direct OpenAI API calls; no abstraction.  
**Choice**: `LLMAdapter` abstract interface with `MockLLMAdapter` and planned `OpenAIAdapter`.  
**Rationale**: An LLM API dependency in the test suite creates flakiness, cost, and rate-limiting. The adapter pattern lets the test suite run on the mock; production swaps in a real adapter.  
**Outcome**: 225 tests pass with zero API calls. Switching to a real LLM is one environment variable change.

### Decision 3 — FAISS over a Vector Database (Chosen)
**Alternatives considered**: Pinecone, pgvector, Milvus.  
**Choice**: FAISS `IndexFlatIP` with local disk persistence.  
**Rationale**: For a single-user, offline, local application with a corpus of dozens of papers, cloud vector databases add latency (network round trips), cost, and account management complexity. FAISS is free, fast, and sufficient for the target scale.  
**Outcome**: ~0.17 ms FAISS storage, ~244 ms search (dominated by embedding generation, not FAISS). A `VectorStoreAdapter` interface is already in place for a future cloud backend swap.

### Decision 4 — Streamlit over FastAPI (Chosen for v1.0.0)
**Alternatives considered**: FastAPI + React frontend; Flask; Gradio.  
**Choice**: Streamlit as the complete UI framework.  
**Rationale**: A FastAPI + React stack is appropriate for a multi-user production service but adds ~2 weeks of additional frontend engineering for a single-user research tool. Streamlit delivers a complete interactive UI in pure Python, which aligns with the mathematics researcher target persona (Python-literate, not frontend engineers).  
**Outcome**: 8 fully functional research pages delivered in Day 6. FastAPI is deferred to v2.0 as a backend for multi-user deployment.

---

## 4. Tradeoffs

| Decision | Benefit | Cost |
|---|---|---|
| MockLLMAdapter | Fast, reliable tests | Responses are deterministic/canned in v1.0.0 |
| Rule-based entity extraction | No training data needed | Lower recall on non-standard LaTeX conventions |
| FAISS local index | Fast, offline, free | Index resets if exports/ cleared |
| Streamlit UI | Fast development, pure Python | Not suited for multi-user or API-driven deployment |
| CPU-only embedding | No GPU required | 321 ms per paper — tolerable for offline research use |
| Fixed 1,500 token budget | Predictable context window | Not optimal for very long queries |

---

## 5. Testing Strategy

### Principle: Tests Should Be Fast and Independent
Every test that touches embedding uses `MockEmbeddingProvider` — avoiding PyTorch model load. Every test that touches LLM generation uses `MockLLMAdapter` — avoiding API calls. Tests complete in under 30 seconds.

### Principle: Test at Multiple Granularities
- **Unit tests**: individual functions and class methods with controlled inputs
- **Integration tests**: service-level orchestration (e.g., `DocumentService.upload_paper` calling `Parser` + `EmbeddingPipeline`)
- **End-to-end verification**: `scripts/verify_end_to_end.py` — 10 complete workflows from upload to export

### Principle: Test Failure Modes, Not Just Happy Paths
The `test_guardrails.py` file (9,789 bytes, the largest test file) tests specifically the REFUSE and WARNING decision paths — the cases where the system correctly declines to answer rather than hallucinating. These are the most important tests in the suite.

### Lessons for v2.0
- Add a property-based testing layer (Hypothesis) for the RAG pipeline
- Add regression tests using a gold-standard annotated PDF corpus
- Track test execution time trends to detect performance regressions

---

## 6. Documentation Strategy

### Write Design Docs Before Code
Every major module (parser, embeddings, RAG pipeline, graph engine, export) had a design document written before implementation began. This forced design decisions to be made explicitly rather than emergently, and created a reference that prevented ad-hoc changes mid-implementation.

### Write Engineering Reports After Each Step
After every Day 7 step (integration testing, performance analysis, bug fix, repository polish, release documentation, deployment, demo, presentation, release), a structured engineering report was written. These reports form an audit trail — a record of what was verified, what was found, and what was resolved.

### Document Limitations Honestly
The `docs/known_issues.md` file does not minimise limitations — it documents them clearly with impact assessments and workarounds. This is not weakness; it is professionalism. A project that knows and communicates its limitations is far more trustworthy than one that presents only successes.

### Lessons for v2.0
- Create an `ADR/` (Architecture Decision Records) directory for formal decision documentation
- Add automated documentation generation (e.g., pdoc or Sphinx) for API reference docs
- Version documentation alongside code with a `docs/` changelog

---

## 7. Release Engineering Lessons

### Release Day Is a Full Engineering Day
Day 7 began with a plan to "polish and release" and grew into a complete professional release package: 9 structured steps, 225 tests, 11 performance benchmarks, 5 bug fixes, complete README overhaul, 5 governance documents, release notes, GitHub Release body, pre-release verification, demo preparation, and presentation package. This is what release engineering actually looks like at a professional level.

### Git Tags Are Not Optional
Publishing code without a `git tag v1.0.0` means there is no permanent, named reference to the release commit. Anyone cloning the repository six months later cannot reproduce the exact v1.0.0 state without the tag. Tags take 30 seconds and are essential.

### The GitHub Release Page Is the Public Face
The repository's README is what repeat visitors see. The GitHub Release page is what new visitors — recruiters, professors, collaborators — see first when clicking "Releases." Writing a professional, comprehensive GitHub Release body (`docs/github_release.md`) before publication is release engineering, not optional.

---

## 8. What Would Change in Version 2

### Architecture Changes
1. **FastAPI backend**: Move application services to REST endpoints. Streamlit becomes one of multiple possible frontends.
2. **Cloud vector store**: Replace FAISS local index with a `VectorStoreAdapter` backed by Pinecone or Milvus.
3. **Real LLM adapter**: Implement `OpenAIAdapter`, `OllamaAdapter`, and `AnthropicAdapter` behind the existing `LLMAdapter` interface.
4. **Database layer**: Replace in-memory document store with SQLite (single-user) or PostgreSQL (multi-user) persistence.

### Engineering Changes
1. **Property-based testing**: Add Hypothesis for RAG pipeline invariant testing.
2. **Docker image**: Package the entire application as a Docker container for one-command deployment.
3. **CI/CD pipeline**: GitHub Actions for automated test runs on every push.
4. **GPU embedding inference**: ONNX Runtime or CTranslate2 for 10× faster embedding.

### UX Changes
1. **Better PDF failure messages**: Detect and report scanned image PDFs before attempting extraction.
2. **Incremental library building**: Add papers to an existing FAISS index without rebuilding from scratch.
3. **Query history**: Persist AI assistant conversations across sessions.
4. **Comparative search**: Search across only a selected subset of uploaded papers.

---

*MathResearch Studio v1.0.0 · Project Retrospective · 7 August 2026*
