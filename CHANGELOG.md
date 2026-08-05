# Changelog

All notable changes to this project will be documented in this file.

The project follows Semantic Versioning.

## [Unreleased]

*No unreleased changes at this time.*

---

## [1.0.0] - 2026-08-06

### Release Highlights

First complete, production-quality release of **MathResearch Studio** — a fully integrated AI-powered mathematical research workspace with 225 passing automated tests.

### Added

- Day 7 Step 1: Complete end-to-end integration test documentation (`tests/integration_tests.md`), automated system verification script (`scripts/verify_end_to_end.py`), and full 10-module end-to-end verification (10/10 modules PASS).
- Day 7 Step 2: Comprehensive performance benchmark script (`scripts/benchmark_performance.py`) measuring 11 core operations; performance documentation (`docs/performance.md`) with bottleneck analysis; performance analysis report (`reports/day7_step2_performance_analysis.md`).
- Day 7 Step 3: Bug fixes (export filename sanitization, paper deletion, header anchor links, terminology improvements, notation categorization); code cleanup (removed dead duplicate code block in `library.py`); known issues documentation (`docs/known_issues.md`); bug fix report (`reports/day7_step3_bugfix_cleanup.md`).
- Day 7 Step 4: Complete README overhaul (20 sections including Mermaid architecture diagram, technology stack table, step-by-step installation, project structure, roadmap, contributing, license, acknowledgements); `CONTRIBUTING.md`; `CODE_OF_CONDUCT.md`; `SECURITY.md`; enhanced `.gitignore`; repository polish report (`reports/day7_step4_repository_polish.md`).

### Fixed

- Export Center download filenames sanitized (removed special characters and spaces) to ensure cross-platform compatibility.
- Removed duplicate `if __name__ == "__main__":` entry block in `src/ui/pages/library.py`.
- Disabled auto-generated relative anchor hover links on section heading titles.
- Corrected mathematical concept category classification in `notation.py`.

### Tested

- Full regression suite: **225 / 225 tests passed (100% pass rate)**.
- End-to-end system verification: **10 / 10 modules verified (PASS)**.
- Performance benchmark: **11 / 11 operations measured (all PASS)**.


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
