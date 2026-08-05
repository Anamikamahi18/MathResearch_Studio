# Known Issues & Version Limitations - MathResearch Studio v1.0.0

This document outlines the resolved issues, current system limitations, known workarounds, and planned enhancements for future releases of **MathResearch Studio**.

---

## 1. Resolved Issues (Version 1.0.0)

| Issue ID | Category | Description | Resolution |
|---|---|---|---|
| **BUG-001** | Export Center | Filenames containing `&` or spaces (e.g. `paper_metadata_&_summaries.md`) caused OS file download handlers to fail opening. | Sanitized export filenames (`paper_summaries.md`, `search_history.md`) with explicit UTF-8 MIME types (`text/markdown`, `application/json`). |
| **BUG-002** | Library UI | Uploaded papers could not be removed directly from the literature library interface. | Added a `delete_paper(paper_id)` method in `DocumentService` and a **"🗑️ Delete Paper"** action button in `library.py`. |
| **BUG-003** | UI Headers | Hovering over section titles rendered broken relative anchor links (`#research-overview`). | Suppressed header anchor links across all UI pages by setting `anchor=False` in `render_page_title`. |
| **BUG-004** | Terminology | UI pages contained complex engineering jargon ("Top-K Vector Chunks", "Graph Density", "MIME Map"). | Replaced technical terms with intuitive mathematician-friendly language ("Matching Passages", "Proof Step Connections", "Research Material"). |
| **BUG-005** | Statistics | Total indexed vector passage count defaulted to 0 if FAISS index had not been auto-saved. | Fallback added to sum passage chunk counts dynamically across cataloged papers in `DashboardService`. |

---

## 2. Current System Limitations & Workarounds

### 1. CPU Model Inference Latency
- **Limitation**: SentenceTransformers (`all-MiniLM-L6-v2`) runs on CPU by default. Batch embedding generation for papers over 50 pages takes ~300-500 ms per paper.
- **Workaround**: Upload smaller or split PDF documents (under 20 pages) for instant ingestion.

### 2. PDF Optical Character Recognition (OCR)
- **Limitation**: PyMuPDF extracts text directly from standard text PDFs. Scanned image-only PDFs without text layers cannot extract formal mathematical environments.
- **Workaround**: Pre-process scanned PDFs with an OCR tool (e.g. Tesseract or Adobe Acrobat) prior to uploading.

### 3. In-Memory Vector Store Persistence
- **Limitation**: `FAISSVectorStore` relies on local disk persistence at `exports/vector_store/index.faiss`. Clearing the `exports/` folder deletes the vector index.
- **Workaround**: Re-ingest or click **"🔄 Refresh Library"** on the Library page to auto-rebuild vector embeddings from saved parsed JSON outputs.

---

## 3. Future Enhancements & Version 2 Roadmap

1. **GPU Acceleration & ONNX Runtime**: Support CUDA GPU acceleration and ONNX quantized models for 10x faster vector embedding generation.
2. **Cloud Vector Database Adapter**: Add optional Pinecone / Milvus vector database adapters for enterprise-scale multi-million vector searches.
3. **Interactive 3D Graph Visualization**: Upgrade 2D dependency graph rendering to interactive 3D WebGL graph view.
4. **Multi-Model LLM API Key Selector**: Enable real-time switching between OpenAI GPT-4o, Anthropic Claude 3.5 Sonnet, and local Ollama Llama 3 models directly from the UI toolbar.
