"""Verification script for Day 4 Step 4.5 Mathematical Relation Extraction."""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

# Add project root directory to path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.graph.relation_extraction import RelationExtractor, RelationType


def verify_relations() -> int:
    """Run RelationExtractor on parsed paper JSONs and print detailed counts per relation type."""
    parser_outputs_dir = project_root / "exports" / "parser_outputs"
    json_files = sorted(parser_outputs_dir.glob("*.json"))

    if not json_files:
        print(f"No parsed JSON files found at: {parser_outputs_dir}")
        return 1

    print(f"Auditing RelationExtractor across {len(json_files)} parsed paper JSON file(s).")
    print("=" * 80)

    extractor = RelationExtractor()
    grand_total_entities = 0
    grand_total_relations = 0
    type_counts: Counter[str] = Counter()

    target_relation_types = [
        "proves",
        "depends_on",
        "uses_definition",
        "uses_theorem",
        "uses_lemma",
        "extends",
        "references",
        "cites",
    ]

    for file_path in json_files:
        print(f"\nPaper Name: {file_path.name}")
        try:
            entities, relations = extractor.extract_from_file(file_path)
            grand_total_entities += len(entities)
            grand_total_relations += len(relations)

            print(f"  -> Total Extracted Entities : {len(entities)}")
            print(f"  -> Total Extracted Relations: {len(relations)}")

            file_counts: Counter[str] = Counter()
            for rel in relations:
                r_type = (
                    rel.relation_type.value
                    if isinstance(rel.relation_type, RelationType)
                    else str(rel.relation_type)
                )
                file_counts[r_type] += 1
                type_counts[r_type] += 1

            for r in target_relation_types:
                print(f"  - {r.capitalize():16s}: {file_counts[r]}")

            # Specific proof and dependency verification
            proof_links = [r for r in relations if r.relation_type == RelationType.PROVES]
            dep_links = [
                r for r in relations
                if r.relation_type in (RelationType.DEPENDS_ON, RelationType.USES_DEFINITION, RelationType.USES_LEMMA, RelationType.USES_THEOREM)
            ]

            if proof_links:
                print(f"  -> Verified Proof Links ({len(proof_links)}):")
                for p in proof_links[:2]:
                    print(f"     [Proof -> Statement] {p.source_entity_id} --PROVES--> {p.target_entity_id}")

            if dep_links:
                print(f"  -> Verified Dependency Links ({len(dep_links)}):")
                for d in dep_links[:2]:
                    print(f"     [Dependency] {d.source_entity_id} --{d.relation_type.upper()}--> {d.target_entity_id}")

        except Exception as exc:
            print(f"  -> Error auditing {file_path.name}: {exc}")
            return 1

    print("\n" + "=" * 80)
    print("OVERALL RELATION EXTRACTION COUNTS BY TYPE:")
    for r in target_relation_types:
        print(f"  - {r.capitalize():16s}: {type_counts[r]}")
    print(f"GRAND TOTAL ENTITIES : {grand_total_entities}")
    print(f"GRAND TOTAL RELATIONS: {grand_total_relations}")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(verify_relations())
