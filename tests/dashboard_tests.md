# Researcher Dashboard Test Plan & Test Matrix

## 1. Executive Summary

This document specifies the test cases, expected results, and recorded verification observations for the **MathResearch Studio v1 Researcher Dashboard**. The test suite covers UI component rendering, state management, router navigation, service integrations, and end-to-end user workflows.

---

## 2. Dashboard Feature Test Matrix

| Feature | Target Page / Component | Test Scenario | Expected Result | Status |
| :--- | :--- | :--- | :--- | :---: |
| **UI Shell & Navigation** | `src/ui/app.py` | Render Streamlit sidebar router | All 10 navigation buttons render and switch pages correctly | ✅ Pass |
| **PDF Upload** | `src/ui/pages/upload.py` | Upload single/multiple PDF files | File validation succeeds, parsing triggers via `DocumentService`, upload status logs display | ✅ Pass |
| **Document Library** | `src/ui/pages/library.py` | View stored paper catalog | Paper cards display metadata, author lists, section counts, and statement entity totals | ✅ Pass |
| **Semantic Search** | `src/ui/pages/search.py` | Natural language query search | Returns ranked search results with relevance scores, section headings, and chunk previews | ✅ Pass |
| **AI Research Assistant** | `src/ui/pages/assistant.py` | Ask grounded research question | Returns grounded answer, evidence mapping, citations (`[1]`), confidence score, and guardrail status | ✅ Pass |
| **Dependency Graph** | `src/ui/pages/graph.py` | Visualize statement network | PyVis HTML graph renders interactively with zoom/pan, layout options, and node detail cards | ✅ Pass |
| **Notation Dictionary** | `src/ui/pages/notation.py` | Search symbol definitions | Symbol cards display LaTeX notation, domain categories, defining paper, and mathematical meaning | ✅ Pass |
| **Statistics Dashboard** | `src/ui/pages/statistics.py` | View aggregate system metrics | Overview metric cards (10 metrics), distribution progress bars, quick insights, and health status render | ✅ Pass |
| **Export Center** | `src/ui/pages/export.py` | Generate Markdown/JSON/CSV export | Exports generated via `ExportService`, live preview card updates, download button yields valid file payload | ✅ Pass |
| **Empty State Guidance** | All UI Pages | Access page with 0 papers in library | Renders empty state banner with "Upload Papers Now" CTA button redirecting to Upload page | ✅ Pass |

---

## 3. Automated Test Execution Summary

The dashboard functionality is validated across 6 dedicated PyTest test modules:

1. `tests/test_ui_shell.py`: UI Shell structure, router navigation, sidebar components. (**Passed**)
2. `tests/test_upload_library.py`: PDF upload page, drag-and-drop validation, library rendering. (**Passed**)
3. `tests/test_semantic_search.py`: Semantic search page integration with `SearchService`. (**Passed**)
4. `tests/test_ai_assistant.py`: AI Research Assistant page integration with `ChatService`. (**Passed**)
5. `tests/test_graph_ui.py`: Research Graph & Notation Dictionary page integrations with `GraphService`. (**Passed**)
6. `tests/test_dashboard_statistics.py`: Statistics Dashboard page integration with `DashboardService`. (**Passed**)
7. `tests/test_export_center.py`: Export Center page integration with `ExportService`. (**Passed**)

---

## 4. Recorded Verification Observations

- **Zero Direct Backend Calls**: Page rendering logic calls Application Services (`DocumentService`, `SearchService`, `ChatService`, `GraphService`, `DashboardService`, `ExportService`) exclusively.
- **State Persistence**: Session state initialized via `init_session_state()` retains ingested vector embeddings, search history, Q&A turns, graph structures, and export audit trails across page navigation transitions.
- **Graceful Empty State Handling**: When 0 papers exist, pages render clear guidance alerts and direct users to the Upload page.
