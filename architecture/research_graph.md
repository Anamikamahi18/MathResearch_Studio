# Research Graph Architecture & Pipeline Specification

## 1. Overview

The **Research Graph Architecture** provides a modular, end-to-end framework for extracting, linking, storing, and visualizing mathematical knowledge from PDF literature.

---

## 2. End-to-End Workflow Diagram

```text
  ┌────────────────────────────────────────────────────────┐
  │ 1. Document Input                                      │
  │    Parsed PDF Document JSON (Schema v1.0)               │
  └───────────────────────────┬────────────────────────────┘
                              │
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │ 2. Entity Extraction Layer                             │
  │    src/graph/entity_extraction/                         │
  │    - Statement Header Parsing (Def, Thm, Lem, Cor, Pf) │
  │    - Multi-line Paragraph Accumulation                 │
  │    - LaTeX Symbol Extraction                            │
  └───────────────────────────┬────────────────────────────┘
                              │
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │ 3. Relation Extraction Layer                           │
  │    src/graph/relation_extraction/                      │
  │    - Explicit Metadata Relations (proves, cites)       │
  │    - Implicit Text Relations (depends_on, uses_def)    │
  └───────────────────────────┬────────────────────────────┘
                              │
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │ 4. Dependency Graph Builder                            │
  │    src/graph/dependency_graph/                         │
  │    - NetworkX MultiDiGraph Construction                │
  │    - Node & Edge Attribute Metadata Preservation       │
  │    - Multi-Paper Graph Merging                         │
  └───────────────────────────┬────────────────────────────┘
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
  ┌────────────────────────┐    ┌────────────────────────┐
  │ 5. Visualization Layer │    │ 6. Multi-Format Export │
  │    PyVis Interactive   │    │    JSON, Cytoscape,    │
  │    HTML Renderer       │    │    GraphML, GEXF, PKL   │
  └────────────────────────┘    └────────────────────────┘
```

---

## 3. Component Architectural Responsibilities

### 1. Document Input
Accepts structured JSON output produced by the Day 2 document parser (`src/parser/`). Ensures backward compatibility with Schema v1.0 formats.

### 2. Entity Extraction (`src/graph/entity_extraction/`)
Converts raw section blocks into strongly typed `ExtractedEntity` objects. Standardizes canonical titles (`"Definition 1.1"`), extracts LaTeX symbols, and tracks page spans.

### 3. Relation Extraction (`src/graph/relation_extraction/`)
Detects directional dependencies between entities. Uses rule-based regex patterns and explicit metadata targets to output `ExtractedRelation` objects.

### 4. Graph Construction (`src/graph/dependency_graph/`)
Uses `NetworkX` `MultiDiGraph` to assemble nodes and edges. Implements `BaseGraphBuilder` strategy interface to allow future graph database replacements (e.g., Neo4j).

### 5. Graph Query & Retrieval Integration (`src/graph/rag_connector.py`)
Enables proof chain traversals (`get_all_antecedents`, `get_all_consequents`) to augment semantic vector retrieval with topological graph dependencies.

### 6. Visualization & Export (`src/graph/visualization/` & `src/graph/graph_export/`)
Generates interactive HTML visualizations via PyVis and exports node-link data across 6 standard graph interchange formats.
