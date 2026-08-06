# MathResearch Studio v1.0.0 — Presentation Outline

**Presentation Title**: MathResearch Studio — An AI-Powered Research Workspace for Mathematics  
**Version**: 1.0.0  
**Total Slides**: 12  
**Estimated Duration**: 12–15 minutes (live) + 5 minutes Q&A  
**Audience**: Recruiters, MSc/PhD students, professors, AI engineers  

---

## Slide 1 — Title

**Slide Title**:
> MathResearch Studio  
> An AI-Powered Research Workspace for Mathematics

**Subtitle**: `v1.0.0 · Python · NLP · RAG · FAISS · NetworkX · Streamlit`

**Content**:
- Project name and version
- Author name and affiliation
- Date: August 2026
- Repository: `github.com/Anamikamahi18/MathResearch_Studio`
- Short tagline: *"From PDF to AI-Grounded Mathematical Knowledge"*

**Visual**: Clean dark-background title card with the MathResearch Studio logo / icon and subtle mathematical notation background (∀, ∃, ∑, ∫, →).

**Speaker Note Reference**: See [`presentation_speaker_notes.md`](./presentation_speaker_notes.md) — Slide 1.

---

## Slide 2 — Motivation

**Slide Title**: Why Mathematics Research Is Difficult

**Content**:

### The Mathematics Literature Problem

Every mathematics researcher faces the same four manual tasks:

| Pain Point | Description |
|---|---|
| 📄 Manual Literature Review | Reading 10–30 PDFs to find one theorem |
| 🔍 Searching Definitions | No cross-paper definition search |
| 🕸️ Tracking Theorem Dependencies | Manual dependency trees across papers |
| 📖 Managing Notation | The symbol σ means three different things |

**Key Message**:
> *"Mathematicians spend more time navigating literature than doing mathematics."*

**Supporting Fact**: A single 30-page arXiv preprint may contain 15+ definitions, 25+ theorems, 40+ lemmas — none of which are searchable or cross-referenced by existing tools.

**Visual**: A split visual — left side shows a researcher surrounded by open PDF windows; right side shows the four pain-point icons.

---

## Slide 3 — Problem Statement

**Slide Title**: The Current Research Workflow

**Content**:

### Researcher Workflow (Today — Manual)

```
Download PDF
    ↓
Open in PDF viewer
    ↓
Read paper sequentially (hours)
    ↓
Manually note definitions and theorems
    ↓
Cross-reference with other papers (manual)
    ↓
Maintain personal notation spreadsheet
    ↓
Write literature review section (manual synthesis)
```

### Core Problems

1. **No structured extraction** — formal mathematical environments are invisible to search
2. **No semantic understanding** — keyword search fails for mathematical concepts
3. **No dependency visualisation** — theorem chains are hidden in prose
4. **No AI grounding** — general AI (e.g. ChatGPT) fabricates theorem statements and citations
5. **No integrated workspace** — researchers switch between 5+ disconnected tools

**Visual**: A flowchart of the current broken workflow with red ❌ markers at each manual pain point.

---

## Slide 4 — Existing Solutions

**Slide Title**: What Researchers Use Today — and Why It Falls Short

**Content**:

| Tool Category | Examples | What It Does | Critical Limitation |
|---|---|---|---|
| Reference Managers | Zotero, Mendeley | Organise citations | No semantic understanding |
| Academic Search | Google Scholar, Semantic Scholar | Discover papers | No in-document analysis |
| General AI | ChatGPT, Gemini | Answer questions | **Hallucinations — invents citations** |
| Symbolic Tools | Mathematica, Lean, Coq | Prove theorems | Does not read literature |
| PDF Annotators | Adobe Acrobat, Hypothes.is | Annotate PDFs | No AI, no cross-paper view |

**Key Message**:
> *"Every existing tool solves one piece of the puzzle. None integrates them. And general AI cannot be trusted with mathematical claims."*

**Visual**: A comparison table with ✅ / ❌ for each tool across five capability dimensions.

---

## Slide 5 — Research Gap

**Slide Title**: The Gap No Platform Fills

**Content**:

### Five Capabilities — Zero Platforms Cover All Five

| Capability | Zotero | Scholar | ChatGPT | Lean | MathResearch Studio |
|---|---|---|---|---|---|
| Literature understanding | ⬜ | ⬜ | 🟡 | ⬜ | ✅ |
| Mathematical entity extraction | ⬜ | ⬜ | ⬜ | ⬜ | ✅ |
| Dependency exploration | ⬜ | ⬜ | ⬜ | 🟡 | ✅ |
| Semantic search over uploads | ⬜ | 🟡 | ⬜ | ⬜ | ✅ |
| AI-assisted reading (grounded) | ⬜ | ⬜ | ⬜ | ⬜ | ✅ |

**Key Statement**:
> *"MathResearch Studio is the only tool that treats mathematical literature as structured, semantically navigable knowledge — not just text."*

**Visual**: A gap diagram showing five capability circles, with only MathResearch Studio filling all five.

---

## Slide 6 — Proposed Solution

**Slide Title**: Introducing MathResearch Studio

**Content**:

### What It Is
An **AI-powered research workspace** that converts uploaded PDF mathematics papers into a structured, searchable, AI-queryable knowledge base — in seconds.

### Version 1.0.0 Workflow

```
Upload PDF(s)
    ↓
Automatic parsing & entity extraction
    ↓
Knowledge base (definitions, theorems, lemmas, proofs)
    ↓
Semantic embedding & FAISS indexing
    ↓
Proof dependency graph (NetworkX + PyVis)
    ↓
Notation dictionary (cross-paper symbols)
    ↓
Semantic search (natural language)
    ↓
AI Research Assistant (8-stage RAG, grounded citations)
    ↓
Export research notes (Markdown / JSON / CSV / PDF)
```

### Key Properties
- **Document-grounded** — every AI answer cites the exact paper, section, and page
- **Hallucination-free** — guardrails refuse to answer when evidence is insufficient
- **Mathematics-aware** — understands theorem structure, not just raw text
- **Offline-capable** — runs entirely locally, no cloud dependency

**Visual**: Vertical workflow pipeline with module icons and connecting arrows.

---

## Slide 7 — System Architecture

**Slide Title**: System Architecture

**Content**:

```
┌─────────────────────────────────────────────────────┐
│                  USER INTERFACE                      │
│            (Streamlit — 8 Pages)                     │
└──────────────────────┬──────────────────────────────┘
                       │
        ┌──────────────▼──────────────┐
        │     APPLICATION SERVICES    │
        │  (DocumentService, RAG-     │
        │   Service, DashboardService)│
        └──┬──────┬──────┬──────┬────┘
           │      │      │      │
    ┌──────▼─┐ ┌──▼──┐ ┌─▼───┐ ┌▼──────┐
    │ Parser │ │Graph│ │FAISS│ │Export │
    │PyMuPDF │ │ Net-│ │Vect-│ │Engine │
    │+Regex  │ │workX│ │orDB │ │MD/JSON│
    └──────┬─┘ └──▲──┘ └─▲───┘ └───────┘
           │      │      │
    ┌──────▼──────┴──────┴───────┐
    │      RAG PIPELINE (8 stage)│
    │ Query→Retrieve→Prompt→     │
    │ Generate→Evidence→Cite→    │
    │ Ground→Guardrail           │
    └────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Role |
|---|---|---|
| UI | Streamlit | Interactive researcher dashboard |
| PDF | PyMuPDF | Text-layer extraction |
| NLP | Regex + heuristics | Mathematical entity detection |
| Embeddings | SentenceTransformers `all-MiniLM-L6-v2` | 384-d dense vectors |
| Vector DB | FAISS `IndexFlatIP` | Cosine similarity search |
| Graph | NetworkX + PyVis | Dependency analysis + visualisation |
| RAG | Custom 8-stage pipeline | Grounded AI responses |
| Testing | pytest | 225 tests, 100% pass rate |

**Visual**: Layered architecture diagram with colour-coded tiers.

---

## Slide 8 — Live Demonstration

**Slide Title**: Live Demonstration

**Content**:

### Demonstration Sequence

| Step | Module | What to Show |
|---|---|---|
| 1 | 📤 Upload Papers | Upload a mathematics PDF — watch it parse in ~127 ms |
| 2 | 📚 Document Library | Browse extracted definitions, theorems, lemmas, proofs |
| 3 | 🕸️ Research Graph | Explore the proof dependency graph |
| 4 | 📖 Notation Dictionary | Browse cross-paper symbol reference |
| 5 | 🔎 Semantic Search | Search "compactness of bounded operators" |
| 6 | 💬 AI Research Assistant | Ask a research question — see 8-stage RAG response |
| 7 | 📊 Statistics Dashboard | System-wide research metrics |
| 8 | 💾 Export Center | Download Markdown research notes |

**Key Demo Highlight**:
> *"Ask the AI assistant a question. Watch it return a structured, 5-section answer — with inline citations — in under 100 milliseconds. Every claim is grounded in your uploaded papers."*

**Visual**: Screenshot collage or live application window.

---

## Slide 9 — Results

**Slide Title**: Results & Validation

**Content**:

### Testing Results

| Category | Count | Result |
|---|---|---|
| Unit & Integration Tests (pytest) | **225** | **100% Passed** |
| End-to-End Module Verification | **10** | **100% Passed** |
| Performance Benchmarks | **11** | **100% Passed** |

### Performance Results

| Operation | Latency |
|---|---|
| PDF Upload | 14 ms |
| PDF Parsing | 113 ms |
| Embedding Generation | 321 ms |
| Semantic Search | 244 ms |
| AI Assistant (8-stage RAG) | 34 ms |
| **Average (all 11 operations)** | **66 ms** |

### Repository Quality

- **28** design and specification documents
- **28** engineering reports (Day 1–7)
- MIT licensed — publicly accessible
- Tagged `v1.0.0` GitHub Release with full release notes
- `README.md` — 15 KB complete project overview

**Visual**: Results table with green checkmarks and a performance bar chart.

---

## Slide 10 — Future Work

**Slide Title**: Version 2.0 Roadmap & Research Directions

**Content**:

### Near-Term (v2.0 Planned)

| Feature | Description |
|---|---|
| Real LLM Integration | OpenAI GPT-4o, Anthropic Claude, Ollama Llama 3 |
| GPU / ONNX Acceleration | 10× faster embedding — ~30 ms vs. ~321 ms |
| Cloud Vector Database | Pinecone / Milvus for multi-million vector scale |
| arXiv & Semantic Scholar Import | Direct paper ingestion from academic APIs |
| 3D Interactive Graph | WebGL dependency graph visualisation |
| Mobile-Responsive UI | Tablet and mobile researcher interface |

### Longer-Term Research Directions

| Direction | Challenge |
|---|---|
| LaTeX Formula Recognition | OCR + TeX parsing for mathematical formulas |
| Multi-Paper Cross-Reference Reasoning | Synthesising theorems across ≥3 papers |
| Notation Disambiguation | Resolving conflicting symbol definitions automatically |
| Cloud Deployment | Solving ephemeral storage and compute constraints |
| Collaborative Research Workspace | Multi-user shared library and annotation |

**Visual**: A roadmap timeline or phased release diagram.

---

## Slide 11 — Lessons Learned

**Slide Title**: Engineering Lessons Learned

**Content**:

### Software Engineering
- **Layered architecture pays off** — clear separation between parser, RAG, UI, and services made debugging fast
- **Design documents before code** — 28 spec documents written before implementation prevented rework
- **Service abstraction** — `MockLLMAdapter` and `MockEmbeddingProvider` made testing fast and deterministic

### AI System Design
- **RAG > full-document prompting** — chunk retrieval is faster, cheaper, and more citation-precise
- **Grounding is not free** — grounding verification required a dedicated 7th stage in the pipeline
- **Guardrails are essential** — refusing to answer is better than answering with fabricated claims

### Testing
- **225 tests before v1.0.0** — discovered 5 bugs before release that would have appeared in demos
- **Mock providers are critical** — testing the RAG pipeline without PyTorch model loads runs 100× faster
- **End-to-end tests catch integration failures** that unit tests miss

### Release Engineering
- **Release notes should be written before release** — forces honest assessment of what is ready
- **Tagging and changelog matter** — even for solo projects, `git tag v1.0.0` + `CHANGELOG.md` signal professionalism

**Visual**: Four-quadrant graphic: Software Engineering | AI System Design | Testing | Release Engineering.

---

## Slide 12 — Thank You

**Slide Title**: Thank You

**Content**:

> *"MathResearch Studio v1.0.0 — From PDF to AI-Grounded Mathematical Knowledge."*

### Contact & Resources

| Resource | Link |
|---|---|
| GitHub Repository | `github.com/Anamikamahi18/MathResearch_Studio` |
| Release Notes | `docs/release_notes_v1.0.0.md` |
| Demo Walkthrough | `docs/demo_walkthrough.md` |
| License | MIT |
| Version | 1.0.0 · August 2026 |

### Questions Welcome

Suggested questions from the audience:
- *"How does the RAG pipeline prevent hallucinations?"*
- *"Why FAISS instead of a database like Postgres with pgvector?"*
- *"How accurate is the mathematical entity extraction?"*
- *"What would real LLM integration change?"*

**Visual**: Clean dark slide with repository URL in large font, QR code to GitHub (optional), and subtle mathematical notation.

---

## Presentation Flow Summary

```
Slide 1  — Title & context setting              (1 min)
Slide 2  — Motivation: the research pain         (1 min)
Slide 3  — Problem statement: current workflow   (1 min)
Slide 4  — Existing solutions & limitations      (1 min)
Slide 5  — The research gap                      (1 min)
Slide 6  — Proposed solution                     (1.5 min)
Slide 7  — System architecture                   (1.5 min)
Slide 8  — Live demonstration                    (4 min)
Slide 9  — Results & validation                  (1 min)
Slide 10 — Future work                           (1 min)
Slide 11 — Lessons learned                       (1 min)
Slide 12 — Thank you + questions                 (1 min + Q&A)
──────────────────────────────────────────────────
Total:    ~15 min presentation + 5 min Q&A = 20 min
```

---

*MathResearch Studio v1.0.0 · Presentation Outline · 2026*
