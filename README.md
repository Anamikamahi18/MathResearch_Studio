# MathResearch Studio v1

An AI-powered research workspace for mathematics researchers.

## Project Overview

MathResearch Studio is designed to support the day-to-day workflow of mathematical research rather than automate theorem solving. Version 1 focuses on one complete workflow: turning uploaded research papers into searchable, structured research knowledge.

The platform is intended to help researchers import papers, extract mathematical structure, search across literature, ask source-grounded questions, and export organized notes that can feed into surveys, reports, and thesis work.

## Motivation

Mathematics researchers spend significant time reading papers, tracing definitions, understanding theorem dependencies, organizing notation, and building research notes. Existing tools often focus on symbolic computation or theorem proving, leaving much of the literature-understanding workflow underserved.

MathResearch Studio addresses this gap by focusing on literature understanding, knowledge organization, and research workflow support. This makes it both academically useful and a strong portfolio project demonstrating applied AI, NLP, retrieval, backend engineering, and interface design.

## Objectives

- Build a practical workspace for mathematical literature analysis.
- Support ingestion and organization of research papers in PDF form.
- Extract structured mathematical knowledge from uploaded papers.
- Enable search and question answering grounded only in uploaded sources.
- Export research notes in a reusable structured format.

## Problem Statement

Researchers need a system that helps them understand, organize, and query mathematical literature efficiently. The challenge is to convert dense academic papers into a structured knowledge workflow that preserves definitions, theorems, lemmas, proofs, notation, and dependencies without attempting to replace mathematical reasoning itself.

## Target Users

- MSc students
- PhD scholars
- Professors
- Research groups

## Features

- PDF upload and ingestion
- Text extraction from research papers
- Section detection for structured reading
- Extraction of definitions, theorems, lemmas, and proofs
- Search across uploaded papers
- AI assistant grounded only in uploaded content
- Dependency graph generation for mathematical statements
- Notation dictionary construction
- Export of structured research notes

## Project Architecture

MathResearch Studio is designed as a modular Python system with clear separation of concerns.

- Streamlit provides the interactive user workspace.
- FastAPI exposes backend services and workflow endpoints.
- LangChain powers retrieval and question-answering pipelines.
- FAISS supports semantic indexing and similarity search.
- Internal modules separate parsing, retrieval, graph analysis, exports, and utilities.

See the architecture design in the project documentation for a deeper breakdown of module boundaries and data flow.

## Technology Stack

- Python
- Streamlit
- FastAPI
- LangChain
- FAISS
- NLP
- LLMs
- RAG
- Information extraction
- Graph analysis
- Git
- GitHub
- Software engineering practices

## Installation

### Prerequisites

- Python 3.11+
- Git

### Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install project dependencies.
4. Configure environment variables if required.

```bash
git clone <repository-url>
cd MathResearchStudio
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Environment

Create a local `.env` file for API keys or runtime configuration when the application begins integrating LLM and retrieval services.

## Usage

The intended Version 1 workflow is:

1. Upload one or more mathematics research papers in PDF format.
2. Extract raw text and structural sections.
3. Index the extracted content for search and retrieval.
4. Query the paper collection using the AI assistant.
5. Review extracted concepts and export structured notes.

Implementation of the full runtime workflow is planned as the next development phase.

## Roadmap

### Version 1

- Repository and project scaffolding
- PDF ingestion workflow
- Text extraction pipeline
- Section detection
- Search and retrieval
- Grounded AI assistant
- Notes export

### Version 2

- Improved theorem and proof extraction
- Stronger notation normalization
- Rich dependency graph exploration
- Multi-document relationship analysis
- Collaboration and annotation features
- External literature integrations

## Contribution Guidelines

Contributions are welcome as the project evolves.

### How to contribute

1. Fork the repository.
2. Create a feature branch.
3. Make focused changes with clear commit messages.
4. Add or update documentation where needed.
5. Open a pull request describing the motivation and scope of the change.

### Contribution principles

- Keep changes modular and aligned with the project architecture.
- Prefer small, testable improvements.
- Avoid coupling UI, parsing, and retrieval logic together.
- Document assumptions and external dependencies clearly.

## Future Work

- Better extraction of theorem-like structures from mathematical PDFs
- Metadata-aware retrieval across multiple papers
- Research dashboards for reading progress and topic clustering
- Export formats tailored for thesis and survey writing
- Stronger graph analytics for theorem dependencies
- More robust handling of notation ambiguity across papers

## Screenshots

Placeholder for UI screenshots, workflow diagrams, and sample outputs.

## References

Placeholder for academic papers, libraries, datasets, and technical references used in the project.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

Placeholder for mentors, collaborators, open-source tools, and research inspirations.
