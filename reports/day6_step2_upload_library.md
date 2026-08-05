# Day 6 Step 2: PDF Upload & Document Library Technical Report

## Executive Summary

As part of **Day 6 Step 2** for **MathResearch Studio**, the **PDF Upload** (`src/ui/pages/upload.py`) and **Document Library** (`src/ui/pages/library.py`) Streamlit UI views were fully integrated with the **Application Service Layer** (`DocumentService`).

All PDF uploading, parsing, vector embedding, graph indexing, library refreshing, paper catalog queries, and keyword searching are exclusively routed through `DocumentService` without modifying any backend components or invoking backend modules directly.

---

## Architecture & Integration Design

```
                                +-----------------------------------+
                                |      Streamlit UI Pages           |
                                | - upload.py       - library.py    |
                                +-----------------------------------+
                                                  |
                                                  v
                                +-----------------------------------+
                                |          DocumentService          |
                                |     (Application Service Layer)   |
                                +-----------------------------------+
                                                  |
         +----------------------------------------+----------------------------------------+
         |                                        |                                        |
         v                                        v                                        v
+------------------+                    +-------------------+                    +--------------------+
|  Parser Pipeline |                    | Embedding Pipeline |                    |    Graph Service   |
|   (parse_pdf)    |                    | (FAISS VectorStore) |                    |  (ResearchGraph)   |
+------------------+                    +-------------------+                    +--------------------+
```

---

## Key Features & Capabilities

### 1. PDF Upload Page (`src/ui/pages/upload.py`)
- **Drag & Drop Uploader**: Supports single or batch PDF file uploads via `st.file_uploader(accept_multiple_files=True, type=['pdf'])`.
- **Validation & Size Formatting**: Validates PDF file extensions and displays file sizes formatted in KB/MB.
- **Service Integration Pipeline**:
  1. `DocumentService.upload_paper(file_bytes, filename)`: Saves file to `uploads/`.
  2. `DocumentService.parse_paper(saved_path)`: Invokes parser to extract metadata, section hierarchies, equations, references, and math entities.
  3. `DocumentService.store_paper(parsed_doc)`: Generates FAISS vector embeddings, indexes chunks, updates Knowledge Graph, and catalogs paper.
- **Real-Time Progress & Feedback**: Displays spinners (`st.spinner`), progress cards, and summary callouts showing paper title, vector chunk count, and graph node/edge counts.
- **Error Handling & Redirection**: Renders styled error banners (`render_error_banner`) for unreadable files and provides a CTA button to navigate directly to the Document Library.

### 2. Document Library Page (`src/ui/pages/library.py`)
- **Catalog Management & Refresh**: Includes a "Refresh Library" button executing `DocumentService.refresh_library()` to rescan disk outputs and synchronize the in-memory catalog.
- **Keyword Search Filter**: Instant keyword search bar filtering catalog papers by Title, Author, Filename, or Paper ID.
- **Aggregated Metric Summary Bar**: Displays real-time metric cards for Total Papers, Total Definitions, Total Theorems, Total Lemmas, and Total Vector Store Chunks.
- **Empty State Handling**: If 0 papers are loaded, renders `render_empty_state()` with guidance and a CTA button routing to Upload.
- **Detailed Paper Cards & Entity Badges**: Displays cards for each paper with authors, year, filename, section/chunk/equation/reference counts, and entity count badges (Definitions, Theorems, Lemmas, Proofs).
- **Expandable Paper Details Drawer**:
  - Metadata summary (DOI, Source, Year, Keywords).
  - Abstract / First section text preview.
  - Interactive raw JSON structure inspection viewer (`st.json`).

---

## Verification & Testing

1. **Verification Script ([scripts/verify_upload_library.py](file:///c:/Projects/MathResearchStudio/scripts/verify_upload_library.py))**:
   - Verified paper storing via `DocumentService.store_paper()`, catalog listing (`list_papers()`), keyword search filtering (`filter_papers_by_keyword()`), math entity counting (`count_math_entity_type()`), and library rescan (`refresh_library()`).

2. **Unit Test Suite ([tests/test_upload_library.py](file:///c:/Projects/MathResearchStudio/tests/test_upload_library.py))**:
   - Comprehensive unit tests covering file size formatting, keyword filtering across title/author/filename/case-insensitivity, math entity extraction counting, and Upload/Library page rendering.
