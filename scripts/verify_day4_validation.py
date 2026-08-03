"""Verification script for Day 4.6 Mathematical Pipeline Validation on Benchmark Corpus."""

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
from src.graph.graph_export import GraphExportManager
from src.graph.relation_extraction import RelationExtractor, RelationType
from src.graph.visualization import PyVisGraphVisualizer, calculate_graph_statistics


def verify_day4_validation() -> int:
    """Run pipeline validation across benchmark corpus of mathematics research papers."""
    benchmark_dir = project_root / "tests" / "benchmark_papers"
    export_dir = project_root / "exports" / "benchmark_exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    json_files = sorted(benchmark_dir.glob("*.json"))
    if not json_files:
        print(f"No benchmark JSON files found at: {benchmark_dir}")
        return 1

    print(f"Executing Day 4.6 Benchmark Validation across {len(json_files)} Mathematics Research Papers.")
    print("=" * 85)

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

    relation_categories = [
        "uses_definition",
        "depends_on",
        "proves",
        "uses_theorem",
        "uses_lemma",
        "extends",
        "references",
        "cites",
    ]

    paper_summaries: list[dict[str, Any]] = []

    for file_path in json_files:
        print(f"\nProcessing Benchmark Paper: {file_path.name}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                doc = json.load(f)

            title = doc.get("title") or file_path.name
            entities = entity_extractor.extract_from_document(doc)
            relations = relation_extractor.extract_relations(entities, document=doc)

            builder = ResearchGraphBuilder()
            builder.build_graph(entities, relations)
            stats = builder.graph_statistics()

            # Tally entity counts
            e_counts: Counter[str] = Counter()
            for e in entities:
                e_type = (
                    e.entity_type.value
                    if isinstance(e.entity_type, EntityType)
                    else str(e.entity_type)
                )
                e_counts[e_type] += 1

            # Tally relation counts
            r_counts: Counter[str] = Counter()
            for r in relations:
                r_type = (
                    r.relation_type.value
                    if isinstance(r.relation_type, RelationType)
                    else str(r.relation_type)
                )
                r_counts[r_type] += 1

            print(f"  Title: '{title}'")
            print("  Mathematical Statement Entities:")
            for cat in statement_categories:
                singular = cat[:-1] if cat.endswith("s") else cat
                print(f"    - {cat.capitalize():12s}: {e_counts[singular]}")

            print("  Extracted Mathematical Relations:")
            for r_cat in relation_categories:
                print(f"    - {r_cat.capitalize():16s}: {r_counts[r_cat]}")

            print(f"  -> Local Graph: {stats['total_nodes']} Nodes, {stats['total_edges']} Edges, Density {stats['density']}")

            paper_summaries.append(
                {
                    "file_name": file_path.name,
                    "title": title,
                    "entities": dict(e_counts),
                    "relations": dict(r_counts),
                    "graph_stats": stats,
                }
            )

            # Merge into collection builder
            master_builder.merge_graph(builder)

        except Exception as exc:
            print(f"  -> Error validating {file_path.name}: {exc}")
            return 1

    # Multi-paper combined benchmark graph analytics
    combined_graph = master_builder.export_networkx()
    combined_stats = calculate_graph_statistics(combined_graph)

    # Render combined PyVis HTML and export multi-format benchmark exports
    manager = GraphExportManager()
    export_paths = manager.export_all(combined_graph, export_dir, "benchmark_research_graph")

    print("\n" + "=" * 85)
    print("BENCHMARK CORPUS COMBINED GRAPH EVALUATION RESULTS:")
    print(f"  - Total Benchmark Nodes : {combined_stats.total_nodes}")
    print(f"  - Total Benchmark Edges : {combined_stats.total_edges}")
    print(f"  - Node Counts Grouped   : {combined_stats.node_count_by_type}")
    print(f"  - Edge Counts Grouped   : {combined_stats.edge_count_by_type}")
    print(f"  - Graph Density         : {combined_stats.density}")
    print(f"  - Connected Components  : {combined_stats.connected_components}")
    print(f"  - Isolated Nodes        : {combined_stats.isolated_nodes}")
    print(f"  - Avg Node Degree       : {combined_stats.average_degree}")
    print(f"  - Export HTML Path      : {export_paths['html']}")
    print("=" * 85)

    return 0


if __name__ == "__main__":
    sys.exit(verify_day4_validation())
