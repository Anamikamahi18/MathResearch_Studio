# Researcher Dashboard System Architecture

## 1. Overview & Architectural Boundaries

The **Researcher Dashboard** for **MathResearch Studio v1** provides a clean modular architecture separating the Streamlit User Interface, the Application Service Layer, and the underlying backend subsystems (PDF Parser, Vector Store, Knowledge Graph, RAG Assistant, and Export Service).

---

## 2. Component Architecture Diagram

```
+---------------------------------------------------------------------------------------------------+
|                                 STREAMLIT USER INTERFACE LAYER                                    |
|                                       (src/ui/app.py)                                             |
|                                                                                                   |
|  +--------------+  +--------------+  +--------------+  +--------------+  +-------------------+  |
|  |   Home Page  |  |  Upload Page |  | Library Page |  |  Search Page |  | AI Assistant Page |  |
|  +--------------+  +--------------+  +--------------+  +--------------+  +-------------------+  |
|  +--------------+  +--------------+  +--------------+  +--------------+  +-------------------+  |
|  |  Graph Page  |  | Notation Page|  | Statistics   |  |  Export Page |  |   Settings Page   |  |
|  +--------------+  +--------------+  +--------------+  +--------------+  +-------------------+  |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                  APPLICATION SERVICE LAYER                                        |
|                                       (src/application/)                                          |
|                                                                                                   |
|  +------------------+  +----------------+  +----------------+  +----------------+  +-------------+  |
|  | DocumentService  |  | SearchService  |  |  ChatService   |  |  GraphService  |  | ExportSvc   |  |
|  +------------------+  +----------------+  +----------------+  +----------------+  +-------------+  |
|  +----------------------------------------------------------------------------------------------+  |
|  |                                   DashboardService                                           |  |
|  +----------------------------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------------------------+
                                                  |
         +--------------------+-------------------+--------------------+--------------------+
         |                    |                   |                    |                    |
         v                    v                   v                    v                    v
+-----------------+  +-----------------+  +---------------+  +-------------------+  +---------------+
|   PDF Parser    |  | Vector Database |  | KnowledgeGraph|  |   RAG Assistant   |  | Storage Layer |
| (src/parser/)   |  |  (FAISS Index)  |  | (NetworkX/PyVis|  |  (src/rag/)       |  | (uploads/ /   |
|                 |  | (src/database/) |  |  src/graph/)  |  |                   |  |  exports/)    |
+-----------------+  +-----------------+  +---------------+  +-------------------+  +---------------+
```

---

## 3. Layer Responsibilities & Data Flow

### 1. User Interface Layer (`src/ui/`)
- Pure presentation and layout using Vanilla Streamlit components and CSS (`src/ui/theme.py`, `src/ui/layout.py`).
- Session state initialization and page routing (`src/ui/state.py`, `src/ui/router.py`).
- **No direct calls to backend modules**: All page views interact strictly via Application Services.

### 2. Application Service Layer (`src/application/`)
- **`DocumentService`**: Paper uploading, parsing orchestration, document catalog management, library refresh.
- **`SearchService`**: Semantic search execution, relevance scoring, filter scoping, search query history log.
- **`ChatService`**: Q&A prompt execution, RAG context retrieval, grounded answer generation, citations, chat history.
- **`GraphService`**: Mathematical dependency graph construction, notation dictionary compilation, node lookup.
- **`DashboardService`**: Aggregate system statistics, statement type distributions, publication breakdowns, insights calculation.
- **`ExportService`**: Markdown, JSON, CSV, and PDF file generation and serialization.

### 3. Backend Subsystems (`src/parser/`, `src/database/`, `src/graph/`, `src/rag/`)
- Core business logic, mathematical NLP parsing, embedding model execution, vector retrieval, graph network analysis, evidence mapping, and guardrails.
