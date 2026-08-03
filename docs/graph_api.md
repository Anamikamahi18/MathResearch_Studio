# Graph Module API Specification

## 1. Overview

The `src/graph/` package provides programmatic APIs for mathematical entity extraction, relation extraction, NetworkX dependency graph construction, visualization, and multi-format exporting.

---

## 2. API Endpoints & Core Python Interfaces

### A. Entity Extraction API (`src.graph.entity_extraction.EntityExtractor`)

```python
from src.graph.entity_extraction import EntityExtractor, ExtractedEntity

extractor = EntityExtractor()

# Extract from parsed document dictionary (Schema v1.0)
entities: list[ExtractedEntity] = extractor.extract_from_document(document_dict)

# Extract directly from JSON file path
entities: list[ExtractedEntity] = extractor.extract_from_file("path/to/paper.json")
```

### B. Relation Extraction API (`src.graph.relation_extraction.RelationExtractor`)

```python
from src.graph.relation_extraction import RelationExtractor, ExtractedRelation

rel_extractor = RelationExtractor()

# Extract explicit and implicit relationships between entities
relations: list[ExtractedRelation] = rel_extractor.extract_relations(
    entities=entities,
    document=document_dict
)
```

### C. Graph Construction API (`src.graph.dependency_graph.ResearchGraphBuilder`)

```python
from src.graph.dependency_graph import ResearchGraphBuilder, NetworkXGraphBuilder
import networkx as nx

builder = ResearchGraphBuilder()

# Populate graph
graph: nx.MultiDiGraph = builder.build_graph(entities, relations)

# Compute analytics & statistics
stats: dict[str, Any] = builder.graph_statistics()

# Merge multiple graphs
builder.merge_graph(other_builder)
```

### D. Visualization API (`src.graph.visualization.PyVisGraphVisualizer`)

```python
from src.graph.visualization import PyVisGraphVisualizer, GraphStyleConfig

visualizer = PyVisGraphVisualizer()

# Render interactive HTML visualization
html_path = visualizer.render(
    graph=graph,
    output_path="exports/research_graph.html",
    title="Mathematical Research Graph"
)
```

### E. Graph Export API (`src.graph.graph_export.GraphExportManager`)

```python
from src.graph.graph_export import GraphExportManager

manager = GraphExportManager()

# Export graph into HTML, JSON, Cytoscape JSON, GraphML, GEXF, and Pickle formats
exported_paths: dict[str, Path] = manager.export_all(
    graph=graph,
    output_dir="exports/graph_exports/",
    base_name="research_graph"
)
```

---

## 3. Data Flow Diagram

```text
Parsed Document JSON (Schema v1.0)
           │
           ▼
   EntityExtractor.extract_from_document()
           │
           ├───────────────► List[ExtractedEntity]
           ▼
   RelationExtractor.extract_relations()
           │
           ├───────────────► List[ExtractedRelation]
           ▼
   ResearchGraphBuilder.build_graph()
           │
           ├───────────────► NetworkX MultiDiGraph
           │
           ├───► PyVisGraphVisualizer.render() ────► HTML Interactive Visualization
           └───► GraphExportManager.export_all() ──► Multi-Format Files (JSON, GraphML, GEXF, Pickle)
```
