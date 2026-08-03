"""Verification script for Day 4 Step 4 Mathematical Dependency Graph Builder."""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Add project root directory to path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.graph.dependency_graph import ResearchGraphBuilder
from src.graph.entity_extraction import EntityExtractor
from src.graph.relation_extraction import RelationExtractor


def verify_dependency_graph() -> int:
    """Run entity & relation extraction and NetworkX graph construction on parsed JSON files."""
    parser_outputs_dir = project_root / "exports" / "parser_outputs"
    json_files = sorted(parser_outputs_dir.glob("*.json"))

    if not json_files:
        print(f"No parsed JSON files found at: {parser_outputs_dir}")
        return 1

    print(f"Discovered {len(json_files)} parsed JSON file(s) for graph construction verification.")
    print("=" * 75)

    entity_extractor = EntityExtractor()
    relation_extractor = RelationExtractor()
    master_builder = ResearchGraphBuilder()

    for file_path in json_files:
        print(f"\nProcessing Paper File: {file_path.name}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                doc = json.load(f)

            entities = entity_extractor.extract_from_document(doc)
            relations = relation_extractor.extract_relations(entities, document=doc)

            builder = ResearchGraphBuilder()
            builder.build_graph(entities, relations)
            stats = builder.graph_statistics()

            print(f"  -> Extracted Entities : {len(entities)}")
            print(f"  -> Extracted Relations: {len(relations)}")
            print(f"  -> NetworkX Graph Nodes: {stats['total_nodes']}")
            print(f"  -> NetworkX Graph Edges: {stats['total_edges']}")
            print(f"  -> Node Types Breakdown: {stats['node_count_by_type']}")
            print(f"  -> Edge Types Breakdown: {stats['edge_count_by_type']}")
            print(f"  -> Weakly Connected Components: {stats['connected_components']}")
            print(f"  -> Isolated Nodes: {stats['isolated_nodes']}")
            print(f"  -> Graph Density : {stats['density']}")

            # Merge into master collection graph
            master_builder.merge_graph(builder)

        except Exception as exc:
            print(f"  -> Error processing {file_path.name}: {exc}")
            return 1

    master_stats = master_builder.graph_statistics()
    print("\n" + "=" * 75)
    print("COMBINED MULTI-PAPER GRAPH STATISTICS:")
    print(f"Total Nodes: {master_stats['total_nodes']}")
    print(f"Total Edges: {master_stats['total_edges']}")
    print(f"Node Types : {master_stats['node_count_by_type']}")
    print(f"Edge Types : {master_stats['edge_count_by_type']}")
    print(f"Connected Components: {master_stats['connected_components']}")
    print(f"Isolated Nodes      : {master_stats['isolated_nodes']}")
    print(f"Graph Density       : {master_stats['density']}")
    print("=" * 75)

    return 0


if __name__ == "__main__":
    sys.exit(verify_dependency_graph())
