# Mathematics Research Dashboard Design Specification

## 1. Executive Summary & Overview

**MathResearch Studio v1** is an AI-powered research workspace designed for mathematics researchers (MSc students, PhD scholars, professors, and research groups). The core objective is not symbolic calculation or automated theorem proving, but rather supporting the day-to-day literature research workflow: reading papers, extracting definitions and theorems, tracking dependencies, exploring notation, searching semantically, asking source-grounded questions, and exporting structured research notes.

The Streamlit Researcher Dashboard serves as the unified interface connecting the backend modules (Parser, Knowledge Base, Knowledge Graph, RAG Assistant, Guardrails) via the Application Service Layer (`DocumentService`, `SearchService`, `ChatService`, `GraphService`, `DashboardService`, `ExportService`).

---

## 2. Target Users & User Personas

| User Persona | Core Research Goal | Key Dashboard Features Used |
| :--- | :--- | :--- |
| **MSc Student** | Literature review, understanding prerequisite definitions, exploring field background | Library, Semantic Search, Notation Dictionary, AI Assistant |
| **PhD Scholar** | Tracking theorem dependencies, analyzing paper relationships, thesis chapter writing | Research Graph, Semantic Search, Citation Engine, Export Center |
| **Mathematics Professor** | Rapid paper scanning, proof structure verification, seminar preparation | Document Upload, Quick Insights, Theorem Breakdown, Statistics |
| **Research Group** | Shared reference library analysis, domain symbol standardisation | Document Library, Export Center (JSON/CSV/Markdown), Graph Metrics |

---

## 3. User Workflow Model

```
+-----------------------------------------------------------------------------------+
| 1. IMPORT & INGESTION                                                             |
| Upload PDF papers -> File Validation -> Parser Pipeline -> Store Chunks & Graph    |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| 2. KNOWLEDGE EXPLORATION & DISCOVERY                                              |
| Browse Document Library -> View Extracted Definitions/Theorems/Lemmas/Proofs      |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| 3. SEMANTIC SEARCH & RETRIEVAL                                                    |
| Natural Language Search -> Relevance Scoring -> Chunk Preview & Match Highlights   |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| 4. AI RESEARCH ASSISTANT Q&A                                                      |
| Grounded Q&A -> Evidence Mapping -> Citations -> Verification & Guardrails Check |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| 5. DEPENDENCY GRAPH & NOTATION ANALYSIS                                           |
| Interactive Network Visualization -> Theorem Precedents -> Symbol Dictionary       |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| 6. DASHBOARD STATISTICS & EXPORT                                                  |
| System Metrics Overview -> Export Notes (PDF, Markdown, JSON, CSV)               |
+-----------------------------------------------------------------------------------+
```

---

## 4. Main Navigation & Page Breakdown

The dashboard application features a persistent sidebar router supporting 10 dedicated pages:

1. **Home (`src/ui/pages/home.py`)**: Landing page displaying project overview, workflow step cards, Quick Stats overview, and quick action buttons.
2. **Upload Papers (`src/ui/pages/upload.py`)**: Drag-and-drop PDF uploader, file validation, upload progress, parsing status logs, and ingestion triggers.
3. **Document Library (`src/ui/pages/library.py`)**: Filterable paper cards, author & metadata displays, section breakdowns, entity counts (definitions, theorems, lemmas, proofs), and quick deletion/refresh actions.
4. **Semantic Search (`src/ui/pages/search.py`)**: Natural language search box, top-k selector (5, 10, 20), relevance score badges, chunk preview highlights, and query history log.
5. **AI Assistant (`src/ui/pages/assistant.py`)**: Conversational Q&A interface with example research prompts, grounded answers, evidence snippets, multi-style citations, and guardrails status.
6. **Research Graph (`src/ui/pages/graph.py`)**: Interactive dependency graph rendered via PyVis/HTML, zoom/pan controls, node selection, degree statistics, and layout toggles.
7. **Notation Dictionary (`src/ui/pages/notation.py`)**: Alphabetical mathematical symbol dictionary, category filters (Algebra, Analysis, Topology, Geometry), and search lookup.
8. **Statistics Dashboard (`src/ui/pages/statistics.py`)**: System-wide overview metrics (papers, pages, definitions, theorems, lemmas, proofs, symbols, chunks, nodes, edges), distribution charts, and health panel.
9. **Export Center (`src/ui/pages/export.py`)**: Multi-format export builder (Markdown, JSON, CSV, PDF), paper scoping, live preview box, native browser download button, and audit trail.
10. **Settings (`src/ui/pages/settings.py`)**: Theme selection (Dark/Light mode), backend service endpoints, vector store index status, and memory usage indicators.

---

## 5. UI Component Architecture & Design Principles

### Design Principles
- **Modern Science Aesthetic**: Sleek dark-mode interface (`#0F172A` background, `#1E293B` containers, `#6366F1` indigo accents) built for long research sessions.
- **High Information Density**: Structured metric cards, badges, and progress indicators presenting rich mathematical data without clutter.
- **Zero Hallucination Transparency**: Every AI answer and search result prominently displays grounding scores, evidence snippets, and direct paper page citations.
- **Reusability**: Shared components (`render_page_title`, `render_paper_card`, `render_empty_state`, `render_sidebar_nav`) maintain UI consistency.

---

## 6. Future V2 Improvements

- **Multi-Paper Comparative View**: Side-by-side comparison of definitions across competing preprints.
- **PDF Annotation Overlay**: Inline highlighting directly over PDF page views.
- **Collaborative Research Group Workspace**: Real-time shared library annotations and export synchronization.
- **External Literature API Sync**: Automated bibliographic search via arXiv, Semantic Scholar, and OpenAlex.
