"""Mathematical relation extraction engine and strategy interface."""

from __future__ import annotations

import json
import logging
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Sequence

from src.graph.entity_extraction import EntityExtractor, ExtractedEntity
from .models import ExtractedRelation, RelationType

logger = logging.getLogger(__name__)

# Rule-based patterns for implicit relation extraction
PROVES_PATTERN = re.compile(
    r"\b(?:Proof|Pf\.)\s+(?:of\s+)?(?:the\s+)?(?P<cat>Theorem|Thm\.|Lemma|Lem\.|Corollary|Cor\.)\s+(?P<num>\d+(?:\.\d+)*)\b",
    re.IGNORECASE,
)

EXTENDS_PATTERN = re.compile(
    r"\b(?:extend|extends|extending|extension of|generalize|generalizes|generalizing)\s+(?:the\s+)?(?P<cat>Theorem|Thm\.|Lemma|Lem\.|Definition|Def\.|Corollary|Cor\.)\s+(?P<num>\d+(?:\.\d+)*)\b",
    re.IGNORECASE,
)

DEPENDS_PATTERN = re.compile(
    r"\b(?:follows from|based on|due to|consequence of|derived from)\s+(?:the\s+)?(?P<cat>Theorem|Thm\.|Lemma|Lem\.|Definition|Def\.|Corollary|Cor\.)\s+(?P<num>\d+(?:\.\d+)*)\b",
    re.IGNORECASE,
)

USES_DEF_PATTERN = re.compile(
    r"\b(?:using|by|via|apply|applying|according to)\s+(?:the\s+)?(?:Definition|Def\.)\s+(?P<num>\d+(?:\.\d+)*)\b",
    re.IGNORECASE,
)

USES_THM_PATTERN = re.compile(
    r"\b(?:using|by|via|apply|applying)\s+(?:the\s+)?(?:Theorem|Thm\.)\s+(?P<num>\d+(?:\.\d+)*)\b",
    re.IGNORECASE,
)

USES_LEM_PATTERN = re.compile(
    r"\b(?:using|by|via|apply|applying)\s+(?:the\s+)?(?:Lemma|Lem\.)\s+(?P<num>\d+(?:\.\d+)*)\b",
    re.IGNORECASE,
)

STATEMENT_REF_PATTERN = re.compile(
    r"\b(?P<cat>Definition|Def\.|Theorem|Thm\.|Lemma|Lem\.|Corollary|Cor\.)\s+(?P<num>\d+(?:\.\d+)*)\b",
    re.IGNORECASE,
)


class BaseRelationExtractor(ABC):
    """Abstract base interface for mathematical relation extraction strategies."""

    @abstractmethod
    def extract_relations(
        self,
        entities: Sequence[ExtractedEntity],
        document: dict[str, Any] | None = None,
    ) -> list[ExtractedRelation]:
        """Extract relationships from a sequence of ExtractedEntity objects and optional document context.

        Args:
            entities: Sequence of ExtractedEntity instances.
            document: Optional raw parsed document dictionary.

        Returns:
            List of ExtractedRelation objects.
        """
        pass


class RelationExtractor(BaseRelationExtractor):
    """Rule-based mathematical relation extractor implementation."""

    def __init__(self) -> None:
        """Initialize RelationExtractor."""
        self.entity_extractor = EntityExtractor()

    def _normalize_category(self, cat_str: str) -> str:
        """Normalize statement category strings (e.g. Thm. -> theorem)."""
        c = cat_str.lower().rstrip(".")
        if c in ("thm", "theorem"):
            return "theorem"
        if c in ("def", "definition"):
            return "definition"
        if c in ("lem", "lemma"):
            return "lemma"
        if c in ("cor", "corollary"):
            return "corollary"
        if c in ("prf", "proof"):
            return "proof"
        return c

    def _build_label_map(
        self, entities: Sequence[ExtractedEntity]
    ) -> dict[str, str]:
        """Pre-build a lookup map from normalized statement titles/labels to entity IDs."""
        label_map: dict[str, str] = {}
        for entity in entities:
            if not entity.title:
                continue

            clean_title = entity.title.strip().lower()
            label_map[clean_title] = entity.entity_id

            # Also create normalized label variants (e.g., "Theorem 3.2" -> "thm 3.2", "theorem 3.2")
            match = STATEMENT_REF_PATTERN.match(clean_title)
            if match:
                cat = self._normalize_category(match.group("cat"))
                num = match.group("num")
                label_map[f"{cat} {num}"] = entity.entity_id
                label_map[f"{cat}. {num}"] = entity.entity_id
                if cat == "theorem":
                    label_map[f"thm {num}"] = entity.entity_id
                    label_map[f"thm. {num}"] = entity.entity_id
                elif cat == "definition":
                    label_map[f"def {num}"] = entity.entity_id
                    label_map[f"def. {num}"] = entity.entity_id
                elif cat == "lemma":
                    label_map[f"lem {num}"] = entity.entity_id
                    label_map[f"lem. {num}"] = entity.entity_id
                elif cat == "corollary":
                    label_map[f"cor {num}"] = entity.entity_id
                    label_map[f"cor. {num}"] = entity.entity_id

        return label_map

    def extract_relations(
        self,
        entities: Sequence[ExtractedEntity],
        document: dict[str, Any] | None = None,
    ) -> list[ExtractedRelation]:
        """Extract explicit and implicit relationships between mathematical entities.

        Args:
            entities: Sequence of ExtractedEntity instances.
            document: Optional parsed document dictionary adhering to Schema v1.0.

        Returns:
            List of structured ExtractedRelation instances.
        """
        relations: list[ExtractedRelation] = []
        seen_pairs: set[tuple[str, str, str]] = set()
        relation_counter = 1

        if not entities:
            return relations

        source_paper = entities[0].source_paper if entities else ""
        label_map = self._build_label_map(entities)

        # 1. Explicit Metadata Relations (from parser output if document dict provided)
        if document and isinstance(document, dict):
            paper_id = document.get("paper_id") or "unknown_paper"

            # A. Proof -> Statement explicit related_to mappings
            for proof_item in document.get("proofs") or []:
                if not isinstance(proof_item, dict):
                    continue

                proof_raw_id = proof_item.get("proof_id") or "prf_001"
                proof_entity_id = f"{paper_id}_proof_{proof_raw_id}"

                related = proof_item.get("related_to") or {}
                for target_key, target_prefix in [
                    ("theorem_id", "theorem"),
                    ("lemma_id", "lemma"),
                    ("corollary_id", "corollary"),
                ]:
                    target_id_val = related.get(target_key)
                    if target_id_val:
                        target_entity_id = f"{paper_id}_{target_prefix}_{target_id_val}"

                        rel_key = (proof_entity_id, target_entity_id, RelationType.PROVES.value)
                        if rel_key not in seen_pairs:
                            seen_pairs.add(rel_key)
                            rel_id = f"rel_{relation_counter:04d}"
                            relation_counter += 1
                            relations.append(
                                ExtractedRelation(
                                    relation_id=rel_id,
                                    relation_type=RelationType.PROVES,
                                    source_entity_id=proof_entity_id,
                                    target_entity_id=target_entity_id,
                                    confidence=0.95,
                                    evidence_text=proof_item.get("text", "")[:150],
                                    source_paper=source_paper,
                                    metadata={"source": "explicit_parser_metadata"},
                                )
                            )

            # B. Paper -> Bibliography Reference CITES mappings
            paper_node_id = f"paper_{paper_id}"
            for ref_item in document.get("references") or []:
                if not isinstance(ref_item, dict):
                    continue
                ref_id_val = ref_item.get("reference_id") or "ref_001"
                target_ref_id = f"{paper_id}_{ref_id_val}"

                rel_key = (paper_node_id, target_ref_id, RelationType.CITES.value)
                if rel_key not in seen_pairs:
                    seen_pairs.add(rel_key)
                    rel_id = f"rel_{relation_counter:04d}"
                    relation_counter += 1
                    relations.append(
                        ExtractedRelation(
                            relation_id=rel_id,
                            relation_type=RelationType.CITES,
                            source_entity_id=paper_node_id,
                            target_entity_id=target_ref_id,
                            confidence=0.90,
                            evidence_text=ref_item.get("raw_text", "")[:150],
                            source_paper=source_paper,
                            metadata={"source": "explicit_parser_references"},
                        )
                    )

        # 2. Implicit Rule-Based In-Text Relation Extraction
        for entity in entities:
            if not entity.text:
                continue

            text = entity.text

            # A. Proofs relationship ("Proof of Theorem X")
            for match in PROVES_PATTERN.finditer(text):
                cat = self._normalize_category(match.group("cat"))
                num = match.group("num")
                target_label = f"{cat} {num}"
                target_id = label_map.get(target_label)

                if target_id and target_id != entity.entity_id:
                    rel_key = (entity.entity_id, target_id, RelationType.PROVES.value)
                    if rel_key not in seen_pairs:
                        seen_pairs.add(rel_key)
                        rel_id = f"rel_{relation_counter:04d}"
                        relation_counter += 1
                        relations.append(
                            ExtractedRelation(
                                relation_id=rel_id,
                                relation_type=RelationType.PROVES,
                                source_entity_id=entity.entity_id,
                                target_entity_id=target_id,
                                confidence=0.88,
                                evidence_text=match.group(0),
                                source_paper=source_paper,
                                metadata={"rule": "PROVES_PATTERN"},
                            )
                        )

            # B. Extends relationship ("extends Theorem X")
            for match in EXTENDS_PATTERN.finditer(text):
                cat = self._normalize_category(match.group("cat"))
                num = match.group("num")
                target_label = f"{cat} {num}"
                target_id = label_map.get(target_label)

                if target_id and target_id != entity.entity_id:
                    rel_key = (entity.entity_id, target_id, RelationType.EXTENDS.value)
                    if rel_key not in seen_pairs:
                        seen_pairs.add(rel_key)
                        rel_id = f"rel_{relation_counter:04d}"
                        relation_counter += 1
                        relations.append(
                            ExtractedRelation(
                                relation_id=rel_id,
                                relation_type=RelationType.EXTENDS,
                                source_entity_id=entity.entity_id,
                                target_entity_id=target_id,
                                confidence=0.85,
                                evidence_text=match.group(0),
                                source_paper=source_paper,
                                metadata={"rule": "EXTENDS_PATTERN"},
                            )
                        )

            # C. Depends On relationship ("follows from Lemma X")
            for match in DEPENDS_PATTERN.finditer(text):
                cat = self._normalize_category(match.group("cat"))
                num = match.group("num")
                target_label = f"{cat} {num}"
                target_id = label_map.get(target_label)

                if target_id and target_id != entity.entity_id:
                    rel_key = (entity.entity_id, target_id, RelationType.DEPENDS_ON.value)
                    if rel_key not in seen_pairs:
                        seen_pairs.add(rel_key)
                        rel_id = f"rel_{relation_counter:04d}"
                        relation_counter += 1
                        relations.append(
                            ExtractedRelation(
                                relation_id=rel_id,
                                relation_type=RelationType.DEPENDS_ON,
                                source_entity_id=entity.entity_id,
                                target_entity_id=target_id,
                                confidence=0.85,
                                evidence_text=match.group(0),
                                source_paper=source_paper,
                                metadata={"rule": "DEPENDS_PATTERN"},
                            )
                        )

            # D. Uses Definition relationship ("using Definition X")
            for match in USES_DEF_PATTERN.finditer(text):
                num = match.group("num")
                target_label = f"definition {num}"
                target_id = label_map.get(target_label)

                if target_id and target_id != entity.entity_id:
                    rel_key = (entity.entity_id, target_id, RelationType.USES_DEFINITION.value)
                    if rel_key not in seen_pairs:
                        seen_pairs.add(rel_key)
                        rel_id = f"rel_{relation_counter:04d}"
                        relation_counter += 1
                        relations.append(
                            ExtractedRelation(
                                relation_id=rel_id,
                                relation_type=RelationType.USES_DEFINITION,
                                source_entity_id=entity.entity_id,
                                target_entity_id=target_id,
                                confidence=0.85,
                                evidence_text=match.group(0),
                                source_paper=source_paper,
                                metadata={"rule": "USES_DEF_PATTERN"},
                            )
                        )

            # E. Uses Theorem relationship ("using Theorem X")
            for match in USES_THM_PATTERN.finditer(text):
                num = match.group("num")
                target_label = f"theorem {num}"
                target_id = label_map.get(target_label)

                if target_id and target_id != entity.entity_id:
                    rel_key = (entity.entity_id, target_id, RelationType.USES_THEOREM.value)
                    if rel_key not in seen_pairs:
                        seen_pairs.add(rel_key)
                        rel_id = f"rel_{relation_counter:04d}"
                        relation_counter += 1
                        relations.append(
                            ExtractedRelation(
                                relation_id=rel_id,
                                relation_type=RelationType.USES_THEOREM,
                                source_entity_id=entity.entity_id,
                                target_entity_id=target_id,
                                confidence=0.85,
                                evidence_text=match.group(0),
                                source_paper=source_paper,
                                metadata={"rule": "USES_THM_PATTERN"},
                            )
                        )

            # F. Uses Lemma relationship ("using Lemma X")
            for match in USES_LEM_PATTERN.finditer(text):
                num = match.group("num")
                target_label = f"lemma {num}"
                target_id = label_map.get(target_label)

                if target_id and target_id != entity.entity_id:
                    rel_key = (entity.entity_id, target_id, RelationType.USES_LEMMA.value)
                    if rel_key not in seen_pairs:
                        seen_pairs.add(rel_key)
                        rel_id = f"rel_{relation_counter:04d}"
                        relation_counter += 1
                        relations.append(
                            ExtractedRelation(
                                relation_id=rel_id,
                                relation_type=RelationType.USES_LEMMA,
                                source_entity_id=entity.entity_id,
                                target_entity_id=target_id,
                                confidence=0.85,
                                evidence_text=match.group(0),
                                source_paper=source_paper,
                                metadata={"rule": "USES_LEM_PATTERN"},
                            )
                        )

            # G. General In-Text Statement References
            for match in STATEMENT_REF_PATTERN.finditer(text):
                cat = self._normalize_category(match.group("cat"))
                num = match.group("num")
                target_label = f"{cat} {num}"
                target_id = label_map.get(target_label)

                if target_id and target_id != entity.entity_id:
                    rel_type = (
                        RelationType.USES_DEFINITION
                        if cat == "definition"
                        else RelationType.USES_LEMMA
                        if cat == "lemma"
                        else RelationType.USES_THEOREM
                        if cat == "theorem"
                        else RelationType.DEPENDS_ON
                    )

                    rel_key = (entity.entity_id, target_id, rel_type.value)
                    if rel_key not in seen_pairs:
                        seen_pairs.add(rel_key)
                        rel_id = f"rel_{relation_counter:04d}"
                        relation_counter += 1
                        relations.append(
                            ExtractedRelation(
                                relation_id=rel_id,
                                relation_type=rel_type,
                                source_entity_id=entity.entity_id,
                                target_entity_id=target_id,
                                confidence=0.75,
                                evidence_text=match.group(0),
                                source_paper=source_paper,
                                metadata={"rule": "STATEMENT_REF_PATTERN"},
                            )
                        )

            # H. References / Citations in text (e.g. "[1]" or "(Devlin et al., 2019)")
            for ref_marker in entity.references:
                rel_key = (entity.entity_id, ref_marker, RelationType.REFERENCES.value)
                if rel_key not in seen_pairs:
                    seen_pairs.add(rel_key)
                    rel_id = f"rel_{relation_counter:04d}"
                    relation_counter += 1
                    relations.append(
                        ExtractedRelation(
                            relation_id=rel_id,
                            relation_type=RelationType.REFERENCES,
                            source_entity_id=entity.entity_id,
                            target_entity_id=ref_marker,
                            confidence=0.80,
                            evidence_text=ref_marker,
                            source_paper=source_paper,
                            metadata={"rule": "ENTITY_REFERENCES"},
                        )
                    )

        logger.info(
            "Extracted %d relation(s) across %d entity/entities",
            len(relations),
            len(entities),
        )
        return relations

    def extract_from_document(
        self, document: dict[str, Any]
    ) -> tuple[list[ExtractedEntity], list[ExtractedRelation]]:
        """Extract both entities and relations from a parsed document dictionary.

        Args:
            document: Parsed document dictionary adhering to Schema v1.0.

        Returns:
            Tuple of (list of ExtractedEntity, list of ExtractedRelation).
        """
        entities = self.entity_extractor.extract_from_document(document)
        relations = self.extract_relations(entities, document=document)
        return entities, relations

    def extract_from_file(
        self, file_path: str | Path
    ) -> tuple[list[ExtractedEntity], list[ExtractedRelation]]:
        """Load a parsed JSON file and extract both entities and relations.

        Args:
            file_path: Path to parsed document JSON file.

        Returns:
            Tuple of (list of ExtractedEntity, list of ExtractedRelation).
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Parsed JSON file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            document = json.load(f)

        return self.extract_from_document(document)
