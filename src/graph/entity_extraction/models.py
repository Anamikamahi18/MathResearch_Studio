"""Data models for mathematical entity extraction."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class EntityType(str, Enum):
    """Enumeration of mathematical entity types."""

    DEFINITION = "definition"
    THEOREM = "theorem"
    LEMMA = "lemma"
    COROLLARY = "corollary"
    PROOF = "proof"
    EXAMPLE = "example"
    REMARK = "remark"


@dataclass
class ExtractedEntity:
    """Structured representation of an extracted mathematical statement or entity."""

    entity_id: str
    entity_type: EntityType | str
    title: str
    text: str
    source_paper: str
    section_id: str = ""
    section_title: str = ""
    page_start: int = 1
    page_end: int = 1
    symbols: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate entity properties."""
        if not self.entity_id:
            raise ValueError("entity_id cannot be empty")
        if not isinstance(self.text, str):
            raise TypeError("text must be a string")
        if isinstance(self.entity_type, str):
            try:
                self.entity_type = EntityType(self.entity_type.lower())
            except ValueError:
                pass

    def to_dict(self) -> dict[str, Any]:
        """Convert ExtractedEntity instance to a plain dictionary."""
        return {
            "entity_id": self.entity_id,
            "entity_type": (
                self.entity_type.value
                if isinstance(self.entity_type, Enum)
                else str(self.entity_type)
            ),
            "title": self.title,
            "text": self.text,
            "source_paper": self.source_paper,
            "section_id": self.section_id,
            "section_title": self.section_title,
            "page_start": self.page_start,
            "page_end": self.page_end,
            "symbols": self.symbols,
            "references": self.references,
            "dependencies": self.dependencies,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ExtractedEntity:
        """Create an ExtractedEntity instance from a dictionary."""
        return cls(
            entity_id=data.get("entity_id", ""),
            entity_type=data.get("entity_type", EntityType.DEFINITION.value),
            title=data.get("title", ""),
            text=data.get("text", ""),
            source_paper=data.get("source_paper", ""),
            section_id=data.get("section_id", ""),
            section_title=data.get("section_title", ""),
            page_start=int(data.get("page_start", 1)),
            page_end=int(data.get("page_end", 1)),
            symbols=list(data.get("symbols") or []),
            references=list(data.get("references") or []),
            dependencies=list(data.get("dependencies") or []),
        )
