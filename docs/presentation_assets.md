# MathResearch Studio v1.0.0 — Presentation Assets Checklist

**Purpose**: Track all visual, data, and supporting assets required for the 12-slide presentation.  
**Status Key**: `[ ]` Not prepared · `[/]` In progress · `[x]` Ready

---

## 1. Architecture Diagram

| Asset | Description | Filename | Status |
|---|---|---|---|
| System architecture block diagram | Layered architecture: UI → Services → Domain → Storage | `assets/diagrams/architecture_diagram.png` | `[ ]` |
| RAG pipeline flow diagram | 8-stage RAG: QueryProcessor → … → GuardrailEngine | `assets/diagrams/rag_pipeline.png` | `[ ]` |
| Module dependency map | Which modules depend on which | `assets/diagrams/module_map.png` | `[ ]` |

**How to create**:
- Use draw.io, Lucidchart, Mermaid, or PowerPoint SmartArt
- Export as PNG at 300 DPI minimum
- Dark background preferred for presentation consistency

---

## 2. Workflow Diagram

| Asset | Description | Filename | Status |
|---|---|---|---|
| End-to-end research workflow | PDF → Parse → Knowledge → Embed → Search → RAG → Export | `assets/diagrams/workflow_diagram.png` | `[ ]` |
| Current (broken) workflow | Manual researcher workflow with ❌ markers | `assets/diagrams/broken_workflow.png` | `[ ]` |
| Before/After comparison | Side-by-side: old workflow vs. MathResearch Studio | `assets/diagrams/before_after.png` | `[ ]` |

---

## 3. Application Screenshots

Capture with application running at `http://localhost:8501`, browser full-screen at 1920×1080, zoom 110%.

| # | Page | Screenshot Filename | Status | Notes |
|---|---|---|---|---|
| 1 | Home / Landing page | `assets/screenshots/slide_home.png` | `[ ]` | Show navigation sidebar and welcome message |
| 2 | Upload Papers | `assets/screenshots/slide_upload.png` | `[ ]` | PDF file selected and ready to upload |
| 3 | Document Library — entity list | `assets/screenshots/slide_library.png` | `[ ]` | Paper expanded showing definitions/theorems |
| 4 | Document Library — definitions | `assets/screenshots/slide_definitions.png` | `[ ]` | Close-up of definition entities |
| 5 | Document Library — theorems | `assets/screenshots/slide_theorems.png` | `[ ]` | Close-up of theorem entities |
| 6 | Semantic Search — results | `assets/screenshots/slide_search.png` | `[ ]` | Query entered, results with relevance scores |
| 7 | AI Research Assistant — question | `assets/screenshots/slide_assistant_q.png` | `[ ]` | Research question typed in input box |
| 8 | AI Research Assistant — answer | `assets/screenshots/slide_assistant_a.png` | `[ ]` | Full 5-section structured response |
| 9 | AI Research Assistant — citations | `assets/screenshots/slide_citations.png` | `[ ]` | Bibliography and grounding score visible |
| 10 | Statistics Dashboard — full view | `assets/screenshots/slide_statistics.png` | `[ ]` | All metric cards and charts |
| 11 | Export Center | `assets/screenshots/slide_export.png` | `[ ]` | All four export format buttons |

---

## 4. Dependency Graph Visualisation

| Asset | Description | Filename | Status |
|---|---|---|---|
| Dependency graph — full view | PyVis interactive graph screenshot showing nodes and edges | `assets/screenshots/slide_graph_full.png` | `[ ]` |
| Dependency graph — node hover | Hover tooltip showing entity label and type | `assets/screenshots/slide_graph_hover.png` | `[ ]` |
| Dependency graph — annotated | Same graph with arrows and labels added in a graphics tool | `assets/diagrams/graph_annotated.png` | `[ ]` |

---

## 5. Performance Table (for Slide 9)

The table below is already documented in `docs/performance.md`. Create a visually formatted version for the slide:

| Asset | Description | Filename | Status |
|---|---|---|---|
| Performance bar chart | 11 operations with latency bars, colour-coded PASS | `assets/charts/performance_chart.png` | `[ ]` |
| Testing summary card | 225 tests / 100% pass / 10 modules / 11 benchmarks | `assets/charts/testing_summary.png` | `[ ]` |

**Data source**: `docs/performance.md` — all values are verified benchmark results.

**Chart values:**
```
PDF Upload:      13.91 ms
PDF Parsing:    112.59 ms
Knowledge:        0.01 ms
Embedding:      321.13 ms
FAISS Storage:    0.17 ms
Graph Build:      0.28 ms
Notation Dict:    0.20 ms
Semantic Search: 243.68 ms
AI Assistant:     33.72 ms
Dashboard Load:   0.50 ms
Export Gen:       1.34 ms
Average:         66.14 ms
```

---

## 6. Future Roadmap Visual (for Slide 10)

| Asset | Description | Filename | Status |
|---|---|---|---|
| v2.0 roadmap timeline | Horizontal timeline: v1.0 → v2.0 → Long-term | `assets/diagrams/roadmap.png` | `[ ]` |
| Feature comparison table | v1.0 vs. v2.0 capabilities side-by-side | `assets/charts/v1_vs_v2.png` | `[ ]` |

---

## 7. Repository Screenshot (for Slides 1, 9, 12)

| Asset | Description | Filename | Status |
|---|---|---|---|
| GitHub repository main page | `github.com/Anamikamahi18/MathResearch_Studio` landing | `assets/screenshots/github_repo.png` | `[ ]` |
| GitHub release page | `v1.0.0` release with release notes | `assets/screenshots/github_release.png` | `[ ]` |
| README preview | Top section of README as rendered on GitHub | `assets/screenshots/github_readme.png` | `[ ]` |
| GitHub test badge | If CI badge is configured | `assets/screenshots/github_badge.png` | `[ ]` |

---

## 8. Slide Template & Design

| Asset | Description | Status |
|---|---|---|
| Presentation template | Dark theme, consistent fonts, accent colours | `[ ]` |
| Font: Inter or Roboto | Clean sans-serif for all slides | `[ ]` |
| Accent colour: `#6366F1` (indigo) | Matching the MathResearch Studio brand | `[ ]` |
| Background: `#0F172A` (dark slate) | Consistent with the Streamlit dark theme | `[ ]` |
| Icon set | Mathematics icons (∑, ∫, ∂, ∀) for decorative use | `[ ]` |

---

## 9. Notation Dictionary Screenshot

| Asset | Description | Filename | Status |
|---|---|---|---|
| Notation page — symbol table | Full notation dictionary with categories | `assets/screenshots/slide_notation.png` | `[ ]` |

---

## 10. Comparison Table Asset (for Slides 4, 5)

| Asset | Description | Filename | Status |
|---|---|---|---|
| Tool comparison table | Zotero / Scholar / ChatGPT / Lean vs. MathResearch Studio | `assets/charts/tool_comparison.png` | `[ ]` |
| Research gap radar chart | Five capabilities, MathResearch Studio fills all | `assets/charts/gap_radar.png` | `[ ]` |

---

## Overall Assets Readiness Summary

| Category | Total Items | Ready | Remaining |
|---|---|---|---|
| Architecture diagrams | 3 | 0 | 3 |
| Workflow diagrams | 3 | 0 | 3 |
| Application screenshots | 11 | 0 | 11 |
| Dependency graph views | 3 | 0 | 3 |
| Performance charts | 2 | 0 | 2 |
| Roadmap visuals | 2 | 0 | 2 |
| Repository screenshots | 4 | 0 | 4 |
| Slide template | 1 | 0 | 1 |
| Notation screenshot | 1 | 0 | 1 |
| Comparison charts | 2 | 0 | 2 |
| **Total** | **32** | **0** | **32** |

> [!NOTE]
> All data needed to generate these assets is available in the project documentation. The assets themselves require a graphics tool or screenshot session.

---

## Quick Asset Generation Guide

### Screenshots
1. Launch application: `streamlit run src/ui/app.py`
2. Upload a sample mathematics PDF
3. Navigate to each page and capture per the table above
4. Save to `assets/screenshots/` with exact filenames listed

### Diagrams
- Use [draw.io](https://draw.io) (free, no install required)
- Import from `docs/presentation_outline.md` ASCII diagrams as starting points
- Export as PNG 300 DPI

### Charts
- Use Python + matplotlib or Excel from values in `docs/performance.md`
- Or use Canva / PowerPoint to design the performance bar chart

---

*MathResearch Studio v1.0.0 · Presentation Assets Checklist · 2026*
