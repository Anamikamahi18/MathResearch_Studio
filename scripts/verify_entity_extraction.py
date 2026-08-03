"""Verification script for Day 4 Step 2 Mathematical Entity Extraction."""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

# Add project root directory to path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.graph.entity_extraction import EntityExtractor, EntityType


def verify_extraction() -> int:
    """Run entity extraction on parsed JSON files in exports/parser_outputs/ and report results."""
    parser_outputs_dir = project_root / "exports" / "parser_outputs"
    json_files = sorted(parser_outputs_dir.glob("*.json"))

    if not json_files:
        print(f"No parsed JSON files found at: {parser_outputs_dir}")
        return 1

    print(f"Discovered {len(json_files)} parsed JSON file(s) for entity extraction verification.")
    print("=" * 70)

    extractor = EntityExtractor()
    total_entities = 0
    type_counts: Counter[str] = Counter()

    for file_path in json_files:
        print(f"\nProcessing File: {file_path.name}")
        try:
            entities = extractor.extract_from_file(file_path)
            print(f"  -> Total Extracted Entities: {len(entities)}")

            file_type_counts: Counter[str] = Counter()
            for entity in entities:
                e_type = (
                    entity.entity_type.value
                    if isinstance(entity.entity_type, EntityType)
                    else str(entity.entity_type)
                )
                file_type_counts[e_type] += 1
                type_counts[e_type] += 1
                total_entities += 1

            for e_type, count in sorted(file_type_counts.items()):
                print(f"     - {e_type.capitalize()}: {count}")

            if entities:
                sample = entities[0]
                print(f"  -> Sample Entity ID: {sample.entity_id}")
                print(f"     Title: {sample.title}")
                print(f"     Type: {sample.entity_type}")
                print(f"     Section: {sample.section_title} ({sample.section_id})")
                print(f"     Pages: {sample.page_start}-{sample.page_end}")
                print(f"     Symbols Extracted: {len(sample.symbols)}")
                print(f"     References Extracted: {len(sample.references)}")
                print(f"     Dependencies: {sample.dependencies}")

        except Exception as exc:
            print(f"  -> Error processing {file_path.name}: {exc}")
            return 1

    print("\n" + "=" * 70)
    print("ENTITY EXTRACTION SUMMARY ACROSS ALL PAPERS:")
    print(f"Total Extracted Entities: {total_entities}")
    for e_type, count in sorted(type_counts.items()):
        print(f"  - {e_type.capitalize()}: {count}")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(verify_extraction())
