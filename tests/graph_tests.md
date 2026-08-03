# Research Graph Test Scenarios & Verification Matrix

## 1. Overview

This document records the test cases, test scenarios, expected results, and actual verification outcomes for the Day 4 Mathematical Research Graph module (`src/graph/`).

---

## 2. Test Execution & Scenario Verification Matrix

| Test Scenario ID | Test Description | Target Components | Expected Result | Recorded Status |
| :---: | :--- | :--- | :--- | :---: |
| **TS-01** | **Definition connected to Theorem** | `EntityExtractor`, `RelationExtractor`, `ResearchGraphBuilder` | Definition entity linked to Theorem via `uses_definition` edge with confidence >= 0.8. | **SUCCESS** |
| **TS-02** | **Lemma linked to Theorem** | `RelationExtractor`, `ResearchGraphBuilder` | Lemma linked to Theorem via `uses_lemma` or `depends_on` edge. | **SUCCESS** |
| **TS-03** | **Proof linked to Theorem** | `RelationExtractor` (`proof.related_to`) | Proof block linked to target Theorem via `proves` edge. | **SUCCESS** |
| **TS-04** | **Citation relationship** | `RelationExtractor` (`CITES`) | Paper or statement linked to Reference node via `cites` edge. | **SUCCESS** |
| **TS-05** | **Multiple papers connected** | `ResearchGraphBuilder.merge_graph()` | Graph builder merges independent multi-paper graphs into unified collection graph. | **SUCCESS** |
| **TS-06** | **Metadata preservation** | `NetworkXGraphBuilder` | Node and edge attributes preserve title, section, page, symbols, and evidence text. | **SUCCESS** |
| **TS-07** | **Interactive Visualization** | `PyVisGraphVisualizer` | Generates self-contained interactive HTML file with node hover tooltips and physics controls. | **SUCCESS** |
| **TS-08** | **Multi-Format Export** | `GraphExportManager` | Exports valid files for JSON, Cytoscape JSON, GraphML, GEXF, and Pickle. | **SUCCESS** |

---

## 3. Automated Test Suite Summary

- **Total Test Cases**: 60 unit and integration tests across `tests/`.
- **Test File Coverage**:
  - `tests/test_entity_extraction.py`: 6 tests passed.
  - `tests/test_relation_extraction.py`: 5 tests passed.
  - `tests/test_dependency_graph.py`: 6 tests passed.
  - `tests/test_schema_compatibility.py`: 3 tests passed.
  - `tests/test_visualization.py`: 3 tests passed.
  - `tests/test_graph_export.py`: 7 tests passed.
  - `tests/test_day4_validation.py`: 2 tests passed.
  - `tests/test_graph.py`: 8 tests passed.
  - Parsing, embeddings, search tests: 20 tests passed.
- **Suite Execution Result**: **60/60 PASSED (100% OK)**.
