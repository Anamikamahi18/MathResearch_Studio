# Navigation & UI/UX Architecture Specification

## 1. Overview

The navigation framework for **MathResearch Studio v1** is implemented in `src/ui/router.py`, `src/ui/sidebar/`, and `src/ui/layout.py`. It provides a clean, responsive, single-page application (SPA) navigation structure hosted inside Streamlit.

---

## 2. Navigation Structure & Page Map

```
                             +-----------------------------+
                             |   Streamlit Navigation App  |
                             |      (src/ui/app.py)        |
                             +-----------------------------+
                                            |
                                            v
                             +-----------------------------+
                             |     Sidebar Router System   |
                             |    (src/ui/sidebar/nav.py)  |
                             +-----------------------------+
                                            |
         +----------------------------------+----------------------------------+
         |                                  |                                  |
         v                                  v                                  v
+------------------+               +------------------+               +------------------+
| Main Navigation  |               |  Research Tools  |               | System Workspace |
+------------------+               +------------------+               +------------------+
| 🏠 Home          |               | 🔍 Semantic Search|               | 📊 Statistics    |
| 📥 Upload Papers |               | 🤖 AI Assistant  |               | 📤 Export Center |
| 📚 Library       |               | 🕸️ Research Graph|               | ⚙️ Settings      |
|                  |               | 🔣 Notation Dict |               |                  |
+------------------+               +------------------+               +------------------+
```

---

## 3. Page Routing Map & Service Dependencies

| Page Name | File Path | Route Key | Icon | Application Service Layer Dependencies |
| :--- | :--- | :--- | :--- | :--- |
| **Home** | `src/ui/pages/home.py` | `home` | 🏠 | `DocumentService`, `DashboardService` |
| **Upload Papers** | `src/ui/pages/upload.py` | `upload` | 📥 | `DocumentService` |
| **Document Library** | `src/ui/pages/library.py` | `library` | 📚 | `DocumentService` |
| **Semantic Search** | `src/ui/pages/search.py` | `search` | 🔍 | `SearchService`, `DocumentService` |
| **AI Assistant** | `src/ui/pages/assistant.py` | `assistant` | 🤖 | `ChatService`, `DocumentService` |
| **Research Graph** | `src/ui/pages/graph.py` | `graph` | 🕸️ | `GraphService`, `DocumentService` |
| **Notation Dictionary** | `src/ui/pages/notation.py` | `notation` | 🔣 | `GraphService`, `DocumentService` |
| **Statistics Dashboard** | `src/ui/pages/statistics.py` | `statistics` | 📊 | `DashboardService`, `DocumentService` |
| **Export Center** | `src/ui/pages/export.py` | `export` | 📤 | `ExportService`, `DocumentService` |
| **Settings** | `src/ui/pages/settings.py` | `settings` | ⚙️ | `DocumentService` |

---

## 4. UI/UX Best Practices for AI-Powered Research Software

### 1. Minimal Cognitive Load
- Mathematical preprints are dense. The interface uses clean typography (Inter / Roboto sans-serif fonts), generous line heights, and muted dark mode colors (`#0F172A`, `#1E293B`, `#334155`) to reduce visual fatigue during long analysis sessions.

### 2. Immediate Source Verification
- Avoid ungrounded AI text generation. Every search hit and AI response features clickable metadata badges showing:
  - Paper Title & ID
  - Section Heading
  - Page Number
  - Confidence Score (`0.0 - 1.0`)

### 3. Clear State Feedback
- Provide visual feedback for long operations (PDF parsing, embedding generation, graph rendering, export generation):
  - Streamlit progress bars & spinners (`st.spinner`, `st.progress`)
  - Status alert banners (`st.success`, `st.error`, `st.warning`, `st.info`)
  - Empty state banners (`render_empty_state`) with direct call-to-action buttons redirecting researchers to the Upload page.

### 4. Seamless State Persistence
- All application services (`DocumentService`, `SearchService`, `ChatService`, `GraphService`, `DashboardService`, `ExportService`) are cached in `st.session_state` via lazy-initialized getters (`src/ui/state.py`), ensuring that navigating between pages preserves vector indexes, search logs, chat history, graph structures, and export audit trails without reloading from disk.
