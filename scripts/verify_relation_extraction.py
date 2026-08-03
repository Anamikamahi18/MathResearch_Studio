"""Verification script for Day 4 Step 3 Mathematical Relation Extraction."""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

# Add project root directory to path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.graph.relation_extraction import RelationExtractor, RelationType


def verify_relation_extraction() -> int:
    """Run relation extraction on parsed JSON files in exports/parser_outputs/ and report counts."""
    parser_outputs_dir = project_root / "exports" / "parser_outputs"
    json_files = sorted(parser_outputs_dir.glob("*.json"))

    if not json_files:
        print(f"No parsed JSON files found at: {parser_outputs_dir}")
        return 1

    print(f"Discovered {len(json_files)} parsed JSON file(s) for relation extraction verification.")
    print("=" * 75)

    extractor = RelationExtractor()
    grand_total_entities = 0
    grand_total_relations = 0
    total_rel_counts: Counter[str] = Counter()

    for file_path in json_files:
        print(f"\nProcessing Paper: {file_path.name}")
        try:
            entities, relations = extractor.extract_from_file(file_path)
            grand_total_entities += len(entities)
            grand_total_relations += len(relations)

            print(f"  -> Total Extracted Entities : {len(entities)}")
            print(f"  -> Total Extracted Relations: {len(relations)}")

            file_rel_counts: Counter[str] = Counter()
            for rel in relations:
                r_type = (
                    rel.relation_type.value
                    if isinstance(rel.relation_type, RelationType)
                    else str(rel.relation_type)
                )
                file_rel_counts[r_type] += 1
                total_rel_counts[r_type] += 1

            if file_rel_counts:
                print("  -> Relations Grouped by Type:")
                for r_type, count in sorted(file_rel_counts.items()):
                    print(f"     - {r_type}: {count}")

            if relations:
                sample = relations[0]
                print(f"  -> Sample Relation:")
                print(f"     Relation ID: {sample.relation_id}")
                print(f"     Type: {sample.relation_type}")
                print(f"     Source Entity: {sample.source_entity_id}")
                print(f"     Target Entity: {sample.target_entity_id}")
                print(f"     Confidence: {sample.confidence}")
                print(f"     Evidence: {sample.evidence_text[:80]}...")

        except Exception as exc:
            print(f"  -> Error processing {file_path.name}: {exc}")
            return 1

    print("\n" + "=" * 75)
    print("RELATION EXTRACTION OVERALL SUMMARY ACROSS ALL PAPERS:")
    print(f"Total Entities Extracted : {grand_total_entities}")
    print(f"Total Relations Extracted: {grand_total_relations}")
    print("Relation Counts Grouped by Type:")
    for r_type, count in sorted(total_rel_counts.items()):
        print(f"  - {r_type}: {count}")
    print("=" * 75)

    return 0


if __name__ == "__main__":
    sys.exit(verify_relation_extraction())
