# Day 6 Step 5: Research Graph Technical Report

## Executive Summary

As part of **Day 6 Step 5** for **MathResearch Studio**, the **Research Graph** UI page (`src/ui/pages/graph.py`) was fully integrated with the **Application Service Layer** (`GraphService`).

All dependency graph construction (`build_dependency_graph()`), statement node lookups (`node_lookup()`), prerequisite and consequent traversals (`get_antecedents()`, `get_consequents()`), and topological metric calculations (`get_graph_metrics()`) are executed strictly through `GraphService` without calling underlying backend graph modules directly.

---

## Architecture & Integration Design

```
                                +-----------------------------------+
                                |      src/ui/pages/graph.py        |
                                |     (Research Graph UI Page)      |
                                +-----------------------------------+
                                                  |
                                                  v
                                +-----------------------------------+
                                |           GraphService            |
                                |    (Application Service Layer)    |
                                +-----------------------------------+
                                                  |
                                                  v
                                +-----------------------------------+
                                |           ResearchGraph           |
                                |     (Nodes, Edges, NetworkX)      |
                                +-----------------------------------+
```

---

## Key Features & Capabilities

### 1. Interactive Dependency Graph Visualization (`src/ui/pages/graph.py`)
- **SVG / HTML Network Canvas**: Renders an interactive, zoomable, and pannable network diagram embedded via `st.components.v1.html`.
- **Layout Control Modes**: Supports layout switches: `Hierarchical (DAG)`, `Force-Directed (Spring)`, `Circular`, and `Grid`.
- **Color-Coded Statement Badges**:
  - 🔵 **Definition**: `#3B82F6` (Blue)
  - 🟢 **Theorem**: `#10B981` (Green)
  - 🟡 **Lemma**: `#F59E0B` (Amber)
  - 🟣 **Proof**: `#8B5CF6` (Purple)
  - ⚪ **Other / Concept**: `#64748B` (Slate)
- **View Controls**: Includes zoom/pan reset button and a prominent "Refresh Graph" toolbar button calling `GraphService.build_dependency_graph()`.

### 2. Multi-Criteria Statement Filtering
- **Statement Type Filter**: Filter graph canvas by `definition`, `theorem`, `lemma`, or `proof`.
- **Paper ID Scope Filter**: Multi-select dropdown filtering nodes and edges to specific library papers.
- **Instant Node Search Bar**: Substring search filtering statement labels, IDs, text excerpts, or paper titles (`GraphService.node_lookup()`).

### 3. Topological Graph Metrics Bar
- **Key Metric Summary Cards**: Total Nodes, Total Edges, Average Node Degree, and Graph Density sourced from `GraphService.get_graph_metrics()`.

### 4. Interactive Node Inspector Drawer
- **Node Selection & Detail Breakdown**: Inspect statement node label, statement type, paper provenance, section title, and page number.
- **Statement Excerpt Preview**: Full text of the mathematical definition, theorem, lemma, or proof.
- **Prerequisite Dependencies List**: Direct incoming antecedents retrieved via `GraphService.get_antecedents(node_id)`.
- **Consequent Statements List**: Direct downstream consequents retrieved via `GraphService.get_consequents(node_id)`.

### 5. Empty & Guidance States
- **No Graph Alert**: Renders an empty state component (`render_empty_state`) when 0 nodes exist in the graph, offering a "Refresh Graph" CTA button and guidance redirecting to PDF Upload.

---

## Verification & Testing

1. **Verification Script ([scripts/verify_graph_ui.py](file:///c:/Projects/MathResearchStudio/scripts/verify_graph_ui.py))**:
   - Verified paper ingestion into Knowledge Graph, dependency graph building (`build_dependency_graph()`), statement node lookups (`node_lookup()`), antecedents & consequents retrieval, graph metrics calculation (`get_graph_metrics()`), and HTML network canvas rendering.

2. **Unit Test Suite ([tests/test_graph_ui.py](file:///c:/Projects/MathResearchStudio/tests/test_graph_ui.py))**:
   - Unit tests covering legend rendering, HTML canvas generation, initial page rendering, populated graph rendering, and `GraphService` session state integration.
