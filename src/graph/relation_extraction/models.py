"""Data models for mathematical relation extraction."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class RelationType(str, Enum):
    """Enumeration of mathematical relationship types."""

    DEPENDS_ON = "depends_on"
    PROVES = "proves"
    USES_DEFINITION = "uses_definition"
    USES_THEOREM = "uses_theorem"
    USES_LEMMA = "uses_lemma"
    EXTENDS = "extends"
    REFERENCES = "references"
    CITES = "cites"


@dataclass
class ExtractedRelation:
    """Structured representation of a relationship between mathematical entities."""

    relation_id: str
    relation_type: RelationType | str
    source_entity_id: str
    target_entity_id: str
    confidence: float = 1.0
    evidence_text: str = ""
    source_paper: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate relation properties."""
        if not self.relation_id:
            raise ValueError("relation_id cannot be empty")
        if not self.source_entity_id:
            raise ValueError("source_entity_id cannot be empty")
        if not self.target_entity_id:
            raise ValueError("target_entity_id cannot be empty")
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError("confidence must be between 0.0 and 1.0")
        if isinstance(self.relation_type, str):
            try:
                self.relation_type = RelationType(self.relation_type.lower())
            except ValueError:
                pass

    def to_dict(self) -> dict[str, Any]:
        """Convert ExtractedRelation instance to a plain dictionary."""
        return {
            "relation_id": self.relation_id,
            "relation_type": (
                self.relation_type.value
                if isinstance(self.relation_type, Enum)
                else str(self.relation_type)
            ),
            "source_entity_id": self.source_entity_id,
            "target_entity_id": self.target_entity_id,
            "confidence": self.confidence,
            "evidence_text": self.evidence_text,
            "source_paper": self.source_paper,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ExtractedRelation:
        """Create an ExtractedRelation instance from a dictionary."""
        return cls(
            relation_id=data.get("relation_id", ""),
            relation_type=data.get("relation_type", RelationType.DEPENDS_ON.value),
            source_entity_id=data.get("source_entity_id", ""),
            target_entity_id=data.get("target_entity_id", ""),
            confidence=float(data.get("confidence", 1.0)),
            evidence_text=data.get("evidence_text", ""),
            source_paper=data.get("source_paper", ""),
            metadata=dict(data.get("metadata") or {}),
        )
