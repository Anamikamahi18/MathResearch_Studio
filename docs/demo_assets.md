# MathResearch Studio v1.0.0 — Demo Assets Checklist

**Purpose**: Track all visual and supporting assets required for a complete demonstration.  
**Status Key**: `[ ]` Not prepared · `[/]` In progress · `[x]` Ready

---

## 1. Screenshots

Capture the following screenshots with the application running at `http://localhost:8501`.  
**Requirements**: 1920×1080 resolution, browser in full-screen, zoom at 110%, dark theme active.

### Application Pages

| # | Screenshot | Filename | Status | Notes |
|---|---|---|---|---|
| 1 | Home / Landing page | `screenshot_01_home.png` | `[ ]` | Show welcome message and sidebar navigation |
| 2 | Upload Papers — empty state | `screenshot_02_upload_empty.png` | `[ ]` | Before any paper is uploaded |
| 3 | Upload Papers — paper selected | `screenshot_03_upload_selected.png` | `[ ]` | PDF filename shown in widget |
| 4 | Upload Papers — success message | `screenshot_04_upload_success.png` | `[ ]` | After successful upload and parse |
| 5 | Document Library — paper list | `screenshot_05_library_overview.png` | `[ ]` | At least one paper in the list |
| 6 | Document Library — definitions expanded | `screenshot_06_library_definitions.png` | `[ ]` | Expand a paper to show definitions |
| 7 | Document Library — theorems expanded | `screenshot_07_library_theorems.png` | `[ ]` | Expand a paper to show theorems |
| 8 | Document Library — lemmas expanded | `screenshot_08_library_lemmas.png` | `[ ]` | Expand a paper to show lemmas |
| 9 | Proof Dependency Graph — full view | `screenshot_09_graph_full.png` | `[ ]` | Interactive graph with multiple nodes |
| 10 | Proof Dependency Graph — node hover | `screenshot_10_graph_hover.png` | `[ ]` | Hover tooltip showing entity label |
| 11 | Notation Dictionary — symbol table | `screenshot_11_notation.png` | `[ ]` | Symbol table with categories |
| 12 | Semantic Search — query entered | `screenshot_12_search_query.png` | `[ ]` | Query typed, before results |
| 13 | Semantic Search — results returned | `screenshot_13_search_results.png` | `[ ]` | Ranked results with relevance scores |
| 14 | AI Research Assistant — question typed | `screenshot_14_assistant_question.png` | `[ ]` | Research question in input box |
| 15 | AI Research Assistant — full answer | `screenshot_15_assistant_answer.png` | `[ ]` | Complete 5-section structured response |
| 16 | AI Research Assistant — citations | `screenshot_16_assistant_citations.png` | `[ ]` | Bibliography and grounding score visible |
| 17 | Statistics Dashboard — full view | `screenshot_17_statistics.png` | `[ ]` | All metric cards and charts visible |
| 18 | Export Center — format buttons | `screenshot_18_export.png` | `[ ]` | All four export format buttons visible |
| 19 | Export Center — download triggered | `screenshot_19_export_download.png` | `[ ]` | Download notification or file saved |

### Storage Location
Save all screenshots to: `assets/screenshots/` (create folder if it does not exist).

---

## 2. Sample Mathematics Paper

| Asset | Requirement | Status |
|---|---|---|
| Primary PDF paper | Text-layer PDF, 10–20 pages, formal mathematical environments | `[ ]` |
| Backup PDF paper | Alternative paper in case primary fails to parse | `[ ]` |
| Paper metadata note | Author, title, year, key theorems noted separately | `[ ]` |

**Recommended characteristics for demo PDF:**
- Has `\begin{theorem}`, `\begin{definition}`, `\begin{lemma}` environments
- Contains LaTeX-rendered mathematics (not scanned)
- Is 10–25 pages (fast to parse, but enough entities to demonstrate)
- Has a clear abstract mentioning the main result
- Uses Greek-letter notation (α, β, λ, σ) for the notation dictionary demo
- Has theorem-lemma dependencies for the graph demo

**Suggested sources:**
- [arXiv.org](https://arxiv.org) — search for *"functional analysis"*, *"operator theory"*, *"linear algebra"*
- Recommend papers with 2020–2026 dates for the publication year chart to look populated

---

## 3. Sample Search Queries

Prepare these queries to paste or type during the demo:

| # | Query | Target Page | Expected Result |
|---|---|---|---|
| 1 | `compactness of bounded linear operators` | Semantic Search | Passages about compactness |
| 2 | `proof of convergence theorem` | Semantic Search | Passages about convergence proofs |
| 3 | `definition of metric space` | Semantic Search | Passage containing metric space definition |
| 4 | `What is the main theorem in this paper?` | AI Assistant | Summary of main theorem with citations |
| 5 | `What conditions are required for convergence?` | AI Assistant | Detailed answer with theorem citations |
| 6 | `Explain the key definitions used in the main proof` | AI Assistant | Definitions section populated |
| 7 | `unrelated question about machine learning` | AI Assistant | Guardrail REFUSE / insufficient evidence response |

Store in: `assets/demo_queries.txt`

---

## 4. Exported Research Notes (Pre-prepared Backup)

If the live export fails during demo, have pre-generated backup files ready:

| Export Format | Filename | Status |
|---|---|---|
| Markdown | `assets/exports/backup_research_notes.md` | `[ ]` |
| JSON | `assets/exports/backup_research_data.json` | `[ ]` |
| CSV | `assets/exports/backup_paper_metadata.csv` | `[ ]` |

**How to generate**: Run the full workflow once before the demo, download all four formats, and save to `assets/exports/`.

---

## 5. Repository & GitHub Assets

| Asset | URL / Location | Status |
|---|---|---|
| GitHub repository page | `https://github.com/Anamikamahi18/MathResearch_Studio` | `[ ]` |
| README.md preview | Repository root → README.md renders on GitHub | `[ ]` |
| GitHub Release page | `…/releases/tag/v1.0.0` | `[ ]` |
| Release notes content | `docs/release_notes_v1.0.0.md` | `[x]` |
| GitHub tag `v1.0.0` | `git push origin v1.0.0` | `[ ]` |

---

## 6. Presentation Slides (Optional Supplement)

If presenting alongside slides (not required for a live demo):

| Slide | Content | Status |
|---|---|---|
| Title slide | Project name, version, author | `[ ]` |
| Problem statement | 4 research workflow pain points | `[ ]` |
| System overview diagram | Architecture block diagram | `[ ]` |
| Tech stack | Icons + names (Streamlit, PyMuPDF, FAISS, etc.) | `[ ]` |
| Live demo placeholder | "Live Demonstration" title slide | `[ ]` |
| Future roadmap | v2.0 bullet list | `[ ]` |
| Closing / contact | Repository link, license, date | `[ ]` |

---

## 7. Demo Environment Backup

| Item | Purpose | Status |
|---|---|---|
| Pre-uploaded library | App with 2 papers already in library for fast demo | `[ ]` |
| Pre-built FAISS index | `exports/vector_store/index.faiss` backed up | `[ ]` |
| `.env` file ready | If LLM_PROVIDER env vars are needed | `[ ]` |
| Virtual environment tested | `venv\Scripts\activate` + `streamlit run src/ui/app.py` runs clean | `[ ]` |

---

## Overall Asset Readiness Summary

| Category | Total Items | Ready | Remaining |
|---|---|---|---|
| Screenshots | 19 | 0 | 19 |
| Sample papers | 2 | 0 | 2 |
| Sample queries | 7 | 7 | 0 |
| Exported notes (backup) | 3 | 0 | 3 |
| Repository assets | 5 | 1 | 4 |
| Slides (optional) | 7 | 0 | 7 |

---

*MathResearch Studio v1.0.0 · Demo Assets Checklist · 2026*
