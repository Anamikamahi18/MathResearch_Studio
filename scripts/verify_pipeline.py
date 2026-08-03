"""End-to-end pipeline verification script for Day 4 Step 4.5."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

# Add project root directory to path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.graph.dependency_graph import ResearchGraphBuilder
from src.graph.entity_extraction import EntityExtractor, EntityType
from src.graph.relation_extraction import RelationExtractor, RelationType


def verify_pipeline() -> int:
    """Run end-to-end extraction and graph construction on all sample papers."""
    parser_outputs_dir = project_root / "exports" / "parser_outputs"
    json_files = sorted(parser_outputs_dir.glob("*.json"))

    if not json_files:
        print(f"No parsed JSON files found at: {parser_outputs_dir}")
        return 1

    print(f"Executing End-to-End Pipeline Verification across {len(json_files)} paper(s).")
    print("=" * 80)

    entity_extractor = EntityExtractor()
    relation_extractor = RelationExtractor()
    master_builder = ResearchGraphBuilder()

    statement_categories = [
        "definitions",
        "theorems",
        "lemmas",
        "corollaries",
        "proofs",
        "examples",
        "remarks",
    ]

    for file_path in json_files:
        print(f"\nPaper Name: {file_path.name}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                doc = json.load(f)

            entities = entity_extractor.extract_from_document(doc)
            relations = relation_extractor.extract_relations(entities, document=doc)

            builder = ResearchGraphBuilder()
            builder.build_graph(entities, relations)
            stats = builder.graph_statistics()

            # Tally statement entity counts for this paper
            e_counts: Counter[str] = Counter()
            for e in entities:
                e_type = (
                    e.entity_type.value
                    if isinstance(e.entity_type, EntityType)
                    else str(e.entity_type)
                )
                e_counts[e_type] += 1

            for cat in statement_categories:
                singular = cat[:-1] if cat.endswith("s") else cat
                print(f"  - {cat.capitalize():12s}: {e_counts[singular]}")

            print(f"  - Relations   : {len(relations)}")
            print(f"  -> Graph Nodes: {stats['total_nodes']} | Grouped: {stats['node_count_by_type']}")
            print(f"  -> Graph Edges: {stats['total_edges']} | Grouped: {stats['edge_count_by_type']}")

            # Merge into combined multi-paper graph
            master_builder.merge_graph(builder)

        except Exception as exc:
            print(f"  -> Error executing pipeline for {file_path.name}: {exc}")
            return 1

    master_stats = master_builder.graph_statistics()
    print("\n" + "=" * 80)
    print("FINAL COMBINED RESEARCH GRAPH STATISTICS:")
    print(f"Total Graph Nodes         : {master_stats['total_nodes']}")
    print(f"Total Graph Edges         : {master_stats['total_edges']}")
    print(f"Node Counts Grouped by Type: {master_stats['node_count_by_type']}")
    print(f"Edge Counts Grouped by Type: {master_stats['edge_count_by_type']}")
    print(f"Weakly Connected Components: {master_stats['connected_components']}")
    print(f"Isolated Nodes             : {master_stats['isolated_nodes']}")
    print(f"Graph Density              : {master_stats['density']}")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(verify_pipeline())
