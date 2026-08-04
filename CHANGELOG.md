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
- Day 4 Session 1 completed: Literature review update for MKM, scientific NER, and relation extraction (`literature/literature_review.md`); research graph design specification (`docs/research_graph_design.md`)
- Day 4 Session 2 completed: Graph package module structure (`src/graph/`); mathematical entity schema specification (`docs/entity_schema.md`); entity extraction layer (`src/graph/entity_extraction/`)
- Day 4 Session 3 completed: Research graph architecture specification (`architecture/research_graph.md`); pluggable relation extraction layer (`src/graph/relation_extraction/`); graph testing plan and test scenario matrix (`tests/graph_tests.md`)
- Day 4 Session 4 completed: Graph API specification (`docs/graph_api.md`); research gap analysis update for mathematical dependency networks (`gap_analysis/gap_analysis.md`); NetworkX dependency graph builder (`src/graph/dependency_graph/`)
- Day 4 Session 5 completed: Interactive PyVis graph visualizer (`src/graph/visualization/`); multi-format graph exporters for HTML, JSON, Cytoscape JSON, GraphML, GEXF, and Pickle (`src/graph/graph_export/`); mathematics literature benchmark validation report (`reports/day4_validation_report.md`); full test suite expanded (60/60 tests passing); Kanban updated to Done (`docs/tasks.md`)
- Day 5 Step 1 & 1.5 completed: Query processing layer (`src/rag/query_processing/`) with normalization, intent classification, multi-entity extraction, and symbol preservation.
- Day 5 Step 2, 2.5 & 2.6 completed: Hybrid Retrieval Engine (`src/rag/retrieval/`) combining FAISS vector search, keyword matching, intent boosting, graph adjacency, ranking explainability breakdowns (`RetrievalExplanation`), retrieval statistics (`RetrievalStatistics`), and pluggable scoring engines (`BaseScoringEngine`, `WeightedScoringEngine`).
- Day 5 Step 3 & 3.5 completed: Prompt Builder (`src/rag/prompt_builder/`) with token budgeting (`TokenManager`), context selection (`ContextSelector`), template registry (`TemplateRegistry`), and prompt formatting (`PromptFormatter`); provider-agnostic LLM Adapter layer (`src/rag/llm/`) supporting `MockLLMAdapter` and `LLMAdapterFactory`.
- Day 5 Step 4 & 4.5 completed: Answer Generator (`src/rag/answer_generator/`) with post-processing (`AnswerPostProcessor`), validation (`AnswerValidator`), confidence estimation (`ConfidenceEstimator`), and 5-section response formatting; deterministic sentence-level Evidence Mapping layer (`src/rag/evidence/`) with `AlignmentEngine` (`DIRECT`, `PARTIAL`, `WEAK`, `NONE` support levels) and `CoverageAnalyzer`.
- Day 5 Step 5 completed: Style-configurable Citation Engine (`src/rag/citation_engine/`) supporting `INLINE` (`[1]`), `AUTHOR_YEAR` (`(Smith, 2024)`), and `ACADEMIC` (`[Paper, Section, Page]`) formats with `CitationFormatter`, bibliography generation, hover metadata tooltips (`CitationRenderer`), and `CitationValidator`.
- Day 5 Step 5.5 completed: Grounding Verification layer (`src/rag/grounding/`) with claim extraction (`ClaimExtractor`), claim verification (`ClaimVerifier`), grounding coverage analysis (`GroundingCoverageAnalyzer`), and report generation (`GroundingReportBuilder`).
- Day 5 Step 6 completed: Guardrails Decision Engine layer (`src/rag/guardrails/`) evaluating policy rules (`GuardrailRules`) across 5 decision types (`RETURN`, `RETURN_WITH_WARNING`, `REFUSE`, `ASK_FOR_CLARIFICATION`, `INSUFFICIENT_EVIDENCE`), input payload validation (`GuardrailValidator`), and final response construction (`ResponseBuilder`).
- Day 5 Documentation & Testing completed: Added RAG design specification (`docs/rag_design.md`), prompt engineering strategy (`docs/prompt_strategy.md`), RAG API specification (`docs/rag_api.md`), RAG pipeline architecture diagram (`architecture/rag_pipeline.md`), QA test matrix (`tests/rag_tests.md`), literature review update (`literature/literature_review.md`), gap analysis update (`gap_analysis/gap_analysis.md`), and unit test suite across all 9 RAG modules (109/109 RAG unit tests passing).


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
