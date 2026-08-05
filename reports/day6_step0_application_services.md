# Day 6 Step 0: Application Service Layer Technical Report

## Executive Summary

As part of **Day 6 Step 0** for **MathResearch Studio**, an **Application Service Layer** (`src/application/`) was introduced to serve as a clean, decoupled boundary between UI consumers (such as Streamlit) and backend components.

Crucially, **no existing backend modules** (Parser, Knowledge Base, Knowledge Graph, Retrieval, Prompt Builder, LLM Adapter, Answer Generator, Evidence Mapper, Citation Engine, Grounding Verification, Guardrails) were modified. The Application Service Layer strictly orchestrates existing capabilities into reusable, high-level service interfaces.

---

## Service Architecture & Responsibilities

```
                                +----------------------------------+
                                |      Streamlit / Client UI       |
                                +----------------------------------+
                                                 |
         +---------------------------------------+---------------------------------------+
         |               |                       |                   |                   |
         v               v                       v                   v                   v
+-----------------+ +---------------+   +------------------+ +---------------+   +-------------------+
| DocumentService | | SearchService |   |   ChatService    | | GraphService  |   | DashboardService  |
+-----------------+ +---------------+   +------------------+ +---------------+   +-------------------+
         |               |                       |                   |                     |
         +---------------+-----------------------+-------------------+---------------------+
                                                 |
                                                 v
                                +----------------------------------+
                                |          ExportService           |
                                +----------------------------------+
                                                 |
                                                 v
                               +------------------------------------+
                               |          Backend Modules           |
                               | (Parser, Graph, Vector Store, RAG) |
                               +------------------------------------+
```

### 1. `DocumentService` (`src/application/document_service.py`)
Orchestrates PDF ingestion, parsing, chunk vector embedding, graph indexing, and paper library state management.
- `upload_paper(file_source, filename)`: Saves raw uploaded PDFs or byte streams to `uploads/`.
- `parse_paper(file_path, output_dir)`: Invokes PDF parser pipeline (`parse_pdf`) to generate schema-aligned JSON representations.
- `store_paper(parsed_document)`: Processes text chunks into FAISS vector store, updates Knowledge Graph, and registers paper metadata.
- `refresh_library()`: Rescans filesystem outputs and synchronizes stored catalog.
- `list_papers()` & `get_paper(paper_id)`: Provides catalog queries.

### 2. `SearchService` (`src/application/search_service.py`)
Provides semantic vector search, metadata filtering, and query history tracking.
- `semantic_search(query, top_k, filters)`: Converts natural language query to vector embeddings, retrieves nearest neighbors, applies filters, and records search history.
- `apply_filters(results, filters)`: Filters candidate search results by `paper_id`, `section_type` (definition, theorem, proof), `author`, `min_score`, and `entity_type`.
- `get_history()` & `clear_history()`: Manages search query audit log.

### 3. `ChatService` (`src/application/chat_service.py`)
Executes the full 8-stage end-to-end RAG pipeline for researcher questions:
1. `QueryProcessor`: Intent analysis and key term extraction.
2. `HybridRetriever`: Multi-signal vector + graph candidate retrieval.
3. `PromptBuilder`: Context selection and token budget formatting.
4. `AnswerGenerator`: LLM answer synthesis.
5. `EvidenceMapper`: Span alignment and evidence verification.
6. `CitationEngine`: Academic bracket citation markers and bibliography rendering.
7. `GroundingVerifier`: Claim verification and hallucination auditing.
8. `GuardrailDecisionEngine`: Final decision policy evaluation (`RETURN`, `RETURN_WITH_WARNING`, `REFUSE`, etc.) and `FinalResearchResponse` construction.
- `receive_question(question, top_k, filters)`: Executes RAG pipeline and returns `FinalResearchResponse`.
- `get_chat_history()` & `clear_chat_history()`: Session history management.

### 4. `GraphService` (`src/application/graph_service.py`)
Orchestrates mathematical dependency graphs, notation graphs, and statement lookups.
- `build_dependency_graph(documents)`: Ingests documents into statement dependency graph.
- `build_notation_graph(documents)`: Constructs notation graph mapping symbols, variables, operator definitions, and concepts across papers.
- `node_lookup(node_id, query, node_type)`: Performs node queries by ID, text search, or statement type.
- Traversal & Metrics: Re-exports `get_antecedents`, `get_consequents`, `get_proof_chain`, and `get_graph_metrics`.

### 5. `ExportService` (`src/application/export_service.py`)
Provides multi-format data export capabilities:
- `export_research_notes(data, format, output_path)`: Exports research query notes, citations, and answers.
- `export_summaries(documents_or_results, format, output_path)`: Exports paper catalog summaries.
- Low-level exporters: `export_to_json`, `export_to_markdown`, `export_to_csv`.

### 6. `DashboardService` (`src/application/dashboard_service.py`)
Aggregates high-level metrics and intelligence for UI dashboards.
- `get_statistics()`: Aggregates paper count, definition count, theorem count, lemma count, total vector store chunks, and graph topology metrics.
- `get_paper_counts()`, `get_definitions()`, `get_theorems()`, `get_lemmas()`, `get_graph_metrics()`.

---

## Verification & Testing

1. **Verification Script ([scripts/verify_application_services.py](file:///c:/Projects/MathResearchStudio/scripts/verify_application_services.py))**:
   - Verified end-to-end functionality of all 6 application services.
   - Tested document storage, vector indexing, graph construction, semantic search with metadata filters, full RAG chat pipeline execution, JSON/Markdown/CSV exports, and dashboard metrics.

2. **Unit Test Suite ([tests/test_application_services.py](file:///c:/Projects/MathResearchStudio/tests/test_application_services.py))**:
   - Covers unit tests for `DocumentService`, `SearchService`, `ChatService`, `GraphService`, `ExportService`, and `DashboardService`.
