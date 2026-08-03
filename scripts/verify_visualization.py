"""Verification script for Day 4 Step 5 Visualization and Graph Export Layer."""

from __future__ import annotations

import json
import pickle
import sys
from pathlib import Path

import networkx as nx

# Add project root directory to path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.graph.dependency_graph import ResearchGraphBuilder
from src.graph.entity_extraction import EntityExtractor
from src.graph.graph_export import GraphExportManager
from src.graph.relation_extraction import RelationExtractor
from src.graph.visualization import calculate_graph_statistics


def verify_visualization() -> int:
    """Build mathematical research graph, render PyVis visualization, and export to all formats."""
    parser_outputs_dir = project_root / "exports" / "parser_outputs"
    export_dir = project_root / "exports" / "graph_exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    json_files = sorted(parser_outputs_dir.glob("*.json"))
    if not json_files:
        print(f"No parsed JSON files found at: {parser_outputs_dir}")
        return 1

    print(f"Loading {len(json_files)} paper(s) for graph visualization and multi-format export verification.")
    print("=" * 80)

    entity_extractor = EntityExtractor()
    relation_extractor = RelationExtractor()
    master_builder = ResearchGraphBuilder()

    for file_path in json_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                doc = json.load(f)

            entities = entity_extractor.extract_from_document(doc)
            relations = relation_extractor.extract_relations(entities, document=doc)
            master_builder.add_entities(entities)
            master_builder.add_relations(relations)

        except Exception as exc:
            print(f"Error loading {file_path.name}: {exc}")
            return 1

    graph = master_builder.export_networkx()
    stats = calculate_graph_statistics(graph)

    print("COMBINED MATHEMATICAL RESEARCH GRAPH STATISTICS:")
    print(f"  - Total Nodes       : {stats.total_nodes}")
    print(f"  - Total Edges       : {stats.total_edges}")
    print(f"  - Node Counts       : {stats.node_count_by_type}")
    print(f"  - Edge Counts       : {stats.edge_count_by_type}")
    print(f"  - Density           : {stats.density}")
    print(f"  - Components        : {stats.connected_components}")
    print(f"  - Isolated Nodes    : {stats.isolated_nodes}")
    print(f"  - Avg Node Degree   : {stats.average_degree}")
    print(f"  - Largest Component : {stats.largest_connected_component_size}")
    print("=" * 80)

    # Export graph into all formats using GraphExportManager
    manager = GraphExportManager()
    exported_paths = manager.export_all(graph, export_dir, "research_graph")

    print("\nMULTIFORMAT GRAPH EXPORT FILE VERIFICATION:")
    for fmt, file_path in exported_paths.items():
        file_size_kb = file_path.stat().st_size / 1024.0
        print(f"  - {fmt.upper():10s} -> {file_path.name:30s} ({file_size_kb:.2f} KB)")

    print("\nVERIFYING LOADABILITY OF EXPORTED FILES:")
    try:
        # 1. HTML check
        html_file = exported_paths["html"]
        assert html_file.exists() and html_file.stat().st_size > 0, "HTML export empty!"
        print("  [OK] PyVis HTML export verified.")

        # 2. JSON check
        json_file = exported_paths["json"]
        with open(json_file, "r", encoding="utf-8") as f:
            j_data = json.load(f)
        assert "nodes" in j_data and ("links" in j_data or "edges" in j_data), "Invalid node-link JSON!"
        print("  [OK] NetworkX JSON export verified.")

        # 3. Cytoscape check
        cy_file = exported_paths["cytoscape"]
        with open(cy_file, "r", encoding="utf-8") as f:
            cy_data = json.load(f)
        assert "elements" in cy_data, "Invalid Cytoscape JSON!"
        print("  [OK] Cytoscape JSON export verified.")

        # 4. GraphML check
        gml_file = exported_paths["graphml"]
        loaded_gml = nx.read_graphml(gml_file)
        assert loaded_gml.number_of_nodes() == stats.total_nodes, "GraphML node count mismatch!"
        print("  [OK] GraphML export verified.")

        # 5. GEXF check
        gexf_file = exported_paths["gexf"]
        loaded_gexf = nx.read_gexf(gexf_file)
        assert loaded_gexf.number_of_nodes() == stats.total_nodes, "GEXF node count mismatch!"
        print("  [OK] GEXF export verified.")

        # 6. Pickle check
        pkl_file = exported_paths["pickle"]
        with open(pkl_file, "rb") as f:
            loaded_pkl = pickle.load(f)
        assert loaded_pkl.number_of_nodes() == stats.total_nodes, "Pickle node count mismatch!"
        print("  [OK] Pickle export verified.")

    except Exception as exc:
        print(f"\n[FAIL] Loadability verification failed: {exc}")
        return 1

    print("\n" + "=" * 80)
    print("ALL VISUALIZATION AND GRAPH EXPORT VERIFICATIONS SUCCEEDED!")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(verify_visualization())
