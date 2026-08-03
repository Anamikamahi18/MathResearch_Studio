# Changelog

All notable changes to this project will be documented in this file.

The project follows Semantic Versioning.

## [Unreleased]

### Added

- Repository initialized and connected to GitHub
- Python virtual environment created
- Required packages installed and `requirements.txt` generated
- Initial project folder structure created
- Documentation scaffolding added for README, MVP scope, tasks, literature review, gap analysis, and architecture
- MIT License, `.gitignore`, and `CHANGELOG.md` added
- Day 2 Session 1 completed: scientific document parsing literature update and parser architecture design
- Day 2 Session 2 completed: parser submodule folder structure and JSON schema specification
- Day 2 Session 3 completed: document pipeline workflow, sample paper test set, and parser test-case tracking
- Day 2 Session 4 completed: parser-focused gap analysis update and parser limitations documentation
- Day 2 pipeline implementation completed with parser modules for PDF loading, metadata extraction, section detection, reference parsing, equation detection, and schema-normalized JSON export
- Centralized parser reliability policy enforcement in code constants and helper functions (warning codes, confidence deltas, quality thresholds, parse-state resolution)
- Parser reliability and schema tests expanded and validated for Day 2 behavior
- Day 3 Session 1 completed: embedding data models (`ChunkMetadata`, `TextChunk`, `EmbeddedChunk`), embedding architecture documentation (`docs/embedding_design.md`), literature review update for dense retrieval and MIR (`literature/literature_review.md`)
- Day 3 Session 2 completed: `EmbeddingProvider` abstract interface and `SentenceTransformerEmbeddingProvider` implementation (`src/embeddings/provider.py`), section-aware and math entity-preserving chunker (`src/embeddings/chunker.py`), chunking strategy specification (`docs/chunking_strategy.md`)
- Day 3 Session 3 completed: embedding pipeline orchestrator (`src/embeddings/pipeline.py`), FAISS vector store with L2 normalized cosine similarity (`src/rag/vector_store.py`), vector database architecture documentation (`architecture/vector_database.md`), semantic search test cases (`tests/search_tests.md`)
- Day 3 Session 4 completed: semantic retriever layer (`src/rag/retriever.py`), search API specification (`docs/search_api.md`), Day 3 retrieval gap analysis update (`gap_analysis/gap_analysis.md`)
- Day 3 Session 5 completed: Day 3 summary report (`docs/day3_report.md`), unit tests for semantic retrieval (`tests/test_retriever.py`), Kanban updates (`docs/tasks.md`)

## [1.0.0] - Planned

### Milestone Focus

First complete MVP workflow for mathematical research paper ingestion, extraction, retrieval, and note export.

### Expected Deliverables

- PDF upload and ingestion
- Text extraction from research papers
- Basic section detection
- Search across uploaded documents
- Grounded AI assistant over uploaded papers
- Structured note export
- Streamlit frontend and FastAPI backend integration
- Local FAISS-based retrieval pipeline

## [1.1.0] - Planned

### Milestone Focus

Improve usability, extraction quality, and retrieval accuracy after the MVP is stable.

### Expected Deliverables

- Better metadata extraction
- Improved section and theorem-like statement detection
- More reliable chunking and embeddings workflow
- Cleaner UI flows for search and assistant features
- Stronger export formatting for research notes
- Initial notation dictionary support

## [2.0.0] - Planned

### Milestone Focus

Expand from a basic research assistant into a richer mathematical knowledge workspace.

### Expected Deliverables

- Dependency graph generation across extracted definitions, lemmas, theorems, and proofs
- Better notation tracking across papers
- Multi-paper knowledge organization improvements
- Stronger retrieval and filtering features
- More advanced graph exploration and document relationships
- Improved persistence beyond basic local storage

## [3.0.0] - Planned

### Milestone Focus

Evolve the platform into a broader collaborative and extensible research environment.

### Expected Deliverables

- Collaboration-oriented workflows for research groups
- Advanced mathematical knowledge graph capabilities
- Larger-scale research library support
- Integration with external literature and citation sources
- More powerful analytics and research dashboards
- Extensible plugin or provider architecture for future AI and retrieval components
