"""Verification script for Day 4 Step 4.5 Mathematical Entity Extraction."""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

# Add project root directory to path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.graph.entity_extraction import EntityExtractor, EntityType


def verify_entities() -> int:
    """Run EntityExtractor on parsed paper JSONs and print detailed counts per entity type."""
    parser_outputs_dir = project_root / "exports" / "parser_outputs"
    json_files = sorted(parser_outputs_dir.glob("*.json"))

    if not json_files:
        print(f"No parsed JSON files found at: {parser_outputs_dir}")
        return 1

    print(f"Auditing EntityExtractor across {len(json_files)} parsed paper JSON file(s).")
    print("=" * 80)

    extractor = EntityExtractor()
    total_entities = 0
    type_counts: Counter[str] = Counter()

    target_types = [
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
            entities = extractor.extract_from_file(file_path)
            total_entities += len(entities)

            file_counts: Counter[str] = Counter()
            for entity in entities:
                e_type = (
                    entity.entity_type.value
                    if isinstance(entity.entity_type, EntityType)
                    else str(entity.entity_type)
                )
                file_counts[e_type] += 1
                type_counts[e_type] += 1

            for t in target_types:
                singular = t[:-1] if t.endswith("s") else t
                print(f"  - {t.capitalize():12s}: {file_counts[singular]}")

            print(f"  -> Total Extracted Entities: {len(entities)}")

        except Exception as exc:
            print(f"  -> Error auditing {file_path.name}: {exc}")
            return 1

    print("\n" + "=" * 80)
    print("OVERALL ENTITY EXTRACTION COUNTS BY TYPE:")
    for t in target_types:
        singular = t[:-1] if t.endswith("s") else t
        print(f"  - {t.capitalize():12s}: {type_counts[singular]}")
    print(f"GRAND TOTAL ENTITIES: {total_entities}")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(verify_entities())
