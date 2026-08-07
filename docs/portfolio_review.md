# MathResearch Studio — Portfolio Review

**Version**: 1.0.0  
**Review Date**: 7 August 2026  
**Purpose**: Honest multi-perspective assessment for portfolio, application, and improvement planning

---

## Perspective 1 — AI/ML Recruiter

*Assessing: technical AI/ML skills, production-readiness, engineering professionalism*

### Strengths

**RAG Pipeline Depth**: The 8-stage RAG pipeline is not a wrapper around a chatbot API. It is a carefully engineered, independently staged AI system with Query Processing, Hybrid Retrieval, Prompt Building, Answer Generation, Evidence Mapping, Citation Engine, Grounding Verification, and Guardrail enforcement — each as a separate, testable module. This demonstrates understanding of production AI architecture, not just API calling.

**Grounding and Safety Design**: Most students adding AI to projects generate responses and display them. This project measures grounding coverage (0–1 score), classifies answers (PASS / WARNING / REFUSE), and can refuse to answer when evidence is insufficient. This is responsible AI engineering — rare in a portfolio project and increasingly demanded in production.

**Mock-First ML Testing**: 225 tests, zero external API calls, zero model load time per test. The `MockLLMAdapter` and `MockEmbeddingProvider` are real patterns from production ML engineering teams. Seeing them in a student portfolio is a strong differentiator.

**Honest Documentation**: `docs/known_issues.md`, `docs/performance.md`, and the bottleneck analysis (CPU-only embedding, 321 ms) show that the builder understands the system's constraints — not just its successes. This is a senior engineer trait.

### Weaknesses

**No Real LLM Integration**: v1.0.0 ships with a `MockLLMAdapter`. A recruiter demonstrating the app will see deterministic canned responses, not a live GPT-4o conversation. This is architecturally correct but visually unimpressive without explanation.

**No GPU / Cloud Deployment**: The system is local-only and CPU-bound. For an AI company with cloud infrastructure, this raises the question of whether the candidate can operate in a cloud-native, GPU-accelerated environment.

**No Evaluation Metrics**: There is no F1 score for entity extraction precision/recall, no MRR for retrieval quality, no RAGAS score for answer quality. Production AI systems are evaluated numerically; this project lacks a quantitative evaluation framework.

### Recommendations

1. Record a live demo video with the application running and narrate the RAG pipeline stages explicitly.
2. Add a one-paragraph "Real LLM Integration" section to the README explaining that the architecture is production-ready and the adapter swap is a 50-line implementation.
3. In interviews, emphasise the grounding score and guardrail design as evidence of responsible AI awareness.

### Overall Impression

**Strong** — a genuinely well-architected AI pipeline project that goes far beyond typical chatbot integrations. The mock-first testing and grounding/guardrail design are rare and impressive. The main gap is a working live demo with a real LLM.

---

## Perspective 2 — Data Science Hiring Manager

*Assessing: data pipeline design, information retrieval, ML integration, practical impact*

### Strengths

**End-to-End Data Pipeline**: Upload → Parse → Extract → Embed → Index → Retrieve → Generate → Verify is a complete, production-style ML data pipeline — not a notebook analysis. The pipeline handles real PDFs, real text, real embeddings, and real retrieval. This is engineering, not experimentation.

**Information Retrieval Architecture**: Hybrid retrieval (FAISS vector similarity + keyword scoring + graph adjacency boosting) is a more sophisticated approach than pure vector search. Weighting the three signals and combining them into a ranked result list reflects real-world information retrieval design.

**SentenceTransformers + FAISS**: The correct embedding + indexing stack for offline, local-first information retrieval. Not over-engineered (no cloud vector database for a single-user tool) and not under-engineered (not using TF-IDF alone).

**Performance Benchmarking**: 11-operation benchmark with `time.perf_counter`, documented bottlenecks, and specific v2.0 solutions shows an engineer who thinks about performance, not just functionality.

### Weaknesses

**No Quantitative Evaluation**: Entity extraction recall is not measured against a gold-standard annotated corpus. Retrieval quality is not measured with Mean Reciprocal Rank. This limits the project's scientific credibility as a data science artefact.

**Dataset Size**: The system is designed for a personal library of dozens of papers, not hundreds of thousands. It would not scale to arXiv-scale without architectural changes (approximate nearest-neighbour, distributed compute).

**No MLflow or Experiment Tracking**: There is no experiment tracking for the embedding model choice, retrieval hyperparameters, or prompt template variations. A data scientist would expect to see ablation studies or at minimum a rationale for each hyperparameter choice.

### Recommendations

1. Add a brief "Evaluation" section to the README with a quantitative result — even one simple measurement (e.g., "Semantic search returns the expected passage in top-3 results for 95% of test queries on the benchmark set").
2. Document why `all-MiniLM-L6-v2` was chosen over alternatives (`bge-small-en`, `multilingual-e5-small`) — this shows deliberate model selection.

### Overall Impression

**Good** — a solid end-to-end ML pipeline with real embedding and retrieval engineering. Stronger evaluation methodology and documented model selection rationale would elevate it significantly.

---

## Perspective 3 — Mathematics Professor

*Assessing: domain accuracy, mathematical correctness, research workflow fit, academic value*

### Strengths

**Correct Problem Identification**: The tool addresses genuine pain points in mathematical literature review — notation disambiguation, theorem dependency tracing, definition location — that existing tools do not address. This reflects real domain understanding.

**Grounded AI Design**: The refusal to generate mathematical answers not grounded in the uploaded papers is academically correct. A hallucinated mathematical claim is worse than no claim. The `GuardrailEngine`'s REFUSE decision is the right behaviour for a mathematical research tool.

**Honest Scope**: v1.0.0 targets the literature understanding workflow — not theorem proving, not automated formalisation. This is a realistic and appropriate scope for v1.0.0. The distinction from Lean/Coq is clearly articulated in the documentation.

**Notation Dictionary**: Cross-paper notation disambiguation is a genuinely useful feature. The ability to look up "what does σ mean in this specific paper" addresses a real cognitive load reduction need.

### Weaknesses

**No Validation on Real Mathematics Papers**: The system has not been demonstrated or evaluated on actual published arXiv mathematics papers. Its behaviour on papers from specific sub-fields (algebraic topology, analytic number theory, functional analysis) is unknown.

**Informal Notation Not Handled**: Papers that present theorems without explicit formal environments ("We now show that...") will not have those theorems extracted. This is a significant limitation for many real mathematics papers.

**No LaTeX Formula Understanding**: The system operates on the text layer of PDFs. Mathematical formulas appear as garbled character sequences or Unicode symbols after PDF text extraction. The system cannot parse or interpret mathematical expressions.

**Citations Are Structural, Not Mathematical**: The citation engine produces page and section references, not mathematical cross-references (e.g., "this step follows from Lemma 2.3 of [Smith 2021]"). A mathematician expects mathematical citation, not just document citation.

### Recommendations

1. Test with 5–10 real arXiv papers from different sub-fields and document which entity types are extracted successfully and which are missed.
2. Add a clear "Scope Boundary" section to the README stating explicitly what the system cannot do: parse formulas, verify proofs, understand informal statements.
3. Consider adding a "confidence" annotation to extracted entities (high/medium/low) based on whether they came from a formal theorem environment or heuristic detection.

### Overall Impression

**Promising** — the concept is correct and the scope is honest. The tool would provide genuine value to a researcher building a literature review in a field with standard LaTeX conventions. The limitations are real but appropriately documented. Validation on real mathematics papers is the most important next step.

---

## Perspective 4 — MSc Student (Potential User / Collaborator)

*Assessing: usability, setup friction, practical research utility, extensibility for final projects*

### Strengths

**Works Offline**: No API keys required, no cloud accounts, no subscription costs. This is essential for a student tool — the mock LLM means the application runs fully locally on any laptop.

**Clear Installation**: `git clone` → `pip install -r requirements.txt` → `streamlit run src/ui/app.py`. Three commands. No Docker, no Kubernetes, no cloud setup. This is realistic for an MSc student's laptop.

**8 Research Pages**: The UI covers the full research workflow — upload, browse, search, ask, graph, notation, stats, export. An MSc student building a literature review can use every single page.

**Export Functionality**: Being able to download research notes as Markdown for inclusion in a thesis draft, or as JSON for downstream analysis, is directly useful for dissertation writing.

**Open Source + MIT License**: Free to use, free to modify, free to build on. An MSc student could fork the project, add their own entity types (e.g., "conjecture", "example"), and use it as the technical component of their own project.

### Weaknesses

**Setup Still Requires Technical Confidence**: `python -m venv venv`, `pip install`, terminal commands — a mathematics MSc student with limited programming background may find this daunting. No GUI installer exists.

**PyTorch Size**: `pip install -r requirements.txt` downloads ~1.5 GB including PyTorch. On a slow university network, this is a 15–30 minute install.

**No Tutorial PDF**: The application needs a real PDF to be useful. A first-time user who uploads a scanned image PDF and gets no extracted entities will be confused. A bundled sample PDF with clear results would greatly improve onboarding.

**Mock LLM Produces Canned Responses**: The AI Research Assistant currently returns the same structured template regardless of the question. A student who uploads a paper and asks "What is the main theorem?" will receive the same mock response structure as if they asked "What are the open problems?". This is confusing without understanding the MockLLMAdapter architecture.

### Recommendations

1. Include a sample mathematics PDF in the repository (or link to a public arXiv PDF) for instant demo without uploading.
2. Add a clear note in the UI (or README) that v1.0.0 uses a mock LLM and real AI responses require setting `LLM_PROVIDER=openai` with an API key.
3. Add a `Makefile` or `setup.bat` / `setup.sh` script to reduce setup to one command.

### Overall Impression

**Usable** — a student with basic Python knowledge can install and run this in under an hour. The tool provides genuine research workflow value. The mock LLM communication could be clearer. An included sample PDF would dramatically improve first-run experience.

---

## Perspective 5 — Open-Source Contributor

*Assessing: code quality, contribution barriers, extensibility, maintenance burden, community readiness*

### Strengths

**`CONTRIBUTING.md`**: Clear, complete contribution guide with PR workflow, branch naming conventions, test requirements, and commit message guidelines. Low barrier to entry.

**`CODE_OF_CONDUCT.md`**: Community standards defined. Safe contribution environment communicated.

**`SECURITY.md`**: Responsible disclosure process documented. v1.0.0 supported. This matters for a project accepting external contributions.

**Clean Architecture with Clear Extension Points**: Adding a new LLM adapter is one class. Adding a new citation format is one enum value + one match branch. Adding a new UI page is one Python file. The architecture is explicitly designed for extension.

**225 Tests**: Any contributor can make a change and immediately know whether they broke something. This is the single most important factor for an open-source project's long-term health.

**MIT License**: No barriers to contribution or commercial use. Maximally permissive.

### Weaknesses

**No `CHANGELOG` Entry for Contribution Workflow**: The `CONTRIBUTING.md` explains how to contribute, but the `CHANGELOG.md` does not mention that external contributions are welcome. First-time contributors read changelogs to understand project activity.

**No Issue Templates**: GitHub Issue templates (bug report, feature request) are absent. Contributors filing their first issue will produce inconsistent, hard-to-triage reports.

**No GitHub Actions CI**: There is no automated test run on pull requests. A contributor cannot verify that their changes pass CI before opening a PR. This is a significant gap for an open-source project.

**No `CHANGELOG` Update Guidance**: `CONTRIBUTING.md` should instruct contributors to update `CHANGELOG.md` in the `[Unreleased]` section as part of every PR.

**No Module-Level Docstrings in Some Files**: Contributor discoverability would benefit from consistent module-level docstrings explaining what each `src/` subdirectory does.

### Recommendations

1. Add GitHub Actions workflow file (`.github/workflows/test.yml`) to run `pytest` on every push and pull request.
2. Add GitHub Issue templates (`.github/ISSUE_TEMPLATE/bug_report.md`, `feature_request.md`).
3. Add a `CHANGELOG` update requirement to `CONTRIBUTING.md`.
4. Add module-level `__doc__` strings to every `__init__.py` in `src/`.

### Overall Impression

**Good Foundation** — a well-structured, well-tested, openly licensed codebase with clear contribution documentation. The main gaps (CI, issue templates) are easy to add and would make this a genuinely welcoming open-source project. The architecture is clean enough that a competent Python developer can navigate and extend it without needing to understand the full codebase first.

---

## Cross-Perspective Summary

| Perspective | Score | Primary Strength | Primary Gap |
|---|---|---|---|
| AI/ML Recruiter | ⭐⭐⭐⭐ | RAG pipeline depth + mock-first testing | No real LLM demo, no eval metrics |
| Data Science Manager | ⭐⭐⭐½ | End-to-end pipeline + benchmarking | No quantitative evaluation |
| Mathematics Professor | ⭐⭐⭐ | Correct problem + grounding design | Not tested on real math papers |
| MSc Student | ⭐⭐⭐⭐ | Offline, clear install, full workflow | Mock LLM confusion, no sample PDF |
| Open-Source Contributor | ⭐⭐⭐⭐ | Tests + architecture + MIT license | No CI, no issue templates |

**Overall Portfolio Rating**: ⭐⭐⭐⭐ — **Strong portfolio project** that demonstrates end-to-end AI engineering skills, software architecture thinking, professional release practices, and honest technical communication. The gaps are real but addressable, and most are planned for v2.0.

---

*MathResearch Studio v1.0.0 · Portfolio Review · 7 August 2026*
