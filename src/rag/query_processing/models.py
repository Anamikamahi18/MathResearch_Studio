"""Data models for query processing in the RAG pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class QueryIntent(str, Enum):
    """Enumeration of user query intents for mathematical RAG."""

    DEFINITION = "definition"
    THEOREM = "theorem"
    LEMMA = "lemma"
    PROOF = "proof"
    EXAMPLE = "example"
    REMARK = "remark"
    SUMMARY = "summary"
    COMPARISON = "comparison"
    CITATION = "citation"
    DEPENDENCY = "dependency"
    NOTATION = "notation"
    GENERAL_QUESTION = "general_question"
    UNKNOWN = "unknown"


@dataclass
class ReferencedEntity:
    """Structured representation of a mathematical entity referenced in a query."""

    entity_type: str
    identifier: str | None = None
    normalized_label: str = ""
    raw_text: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate entity properties and construct normalized label if not provided."""
        if not self.entity_type:
            raise ValueError("entity_type cannot be empty")
        if not self.normalized_label:
            if self.identifier:
                self.normalized_label = f"{self.entity_type.capitalize()} {self.identifier}".strip()
            else:
                self.normalized_label = self.entity_type.capitalize()

    def to_dict(self) -> dict[str, Any]:
        """Convert ReferencedEntity to dictionary representation."""
        return {
            "entity_type": self.entity_type,
            "identifier": self.identifier,
            "normalized_label": self.normalized_label,
            "raw_text": self.raw_text,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ReferencedEntity:
        """Create a ReferencedEntity from a dictionary."""
        return cls(
            entity_type=str(data.get("entity_type", "")),
            identifier=data.get("identifier"),
            normalized_label=str(data.get("normalized_label", "")),
            raw_text=str(data.get("raw_text", "")),
            metadata=dict(data.get("metadata") or {}),
        )


@dataclass
class QueryAnalysis:
    """Complete analysis result returned by QueryProcessor."""

    original_query: str
    normalized_query: str
    intent: QueryIntent | str
    operations: list[str] = field(default_factory=list)
    referenced_entities: list[ReferencedEntity] = field(default_factory=list)
    symbols: list[str] = field(default_factory=list)
    language: str = "en"
    metadata: dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    confidence_type: str = "rule_based"

    def __post_init__(self) -> None:
        """Validate QueryAnalysis properties."""
        if isinstance(self.intent, str):
            try:
                self.intent = QueryIntent(self.intent.lower())
            except ValueError:
                pass

    def to_dict(self) -> dict[str, Any]:
        """Convert QueryAnalysis instance to dictionary."""
        return {
            "original_query": self.original_query,
            "normalized_query": self.normalized_query,
            "intent": self.intent.value if isinstance(self.intent, Enum) else str(self.intent),
            "operations": self.operations,
            "referenced_entities": [e.to_dict() for e in self.referenced_entities],
            "symbols": self.symbols,
            "language": self.language,
            "metadata": self.metadata,
            "confidence": self.confidence,
            "confidence_type": self.confidence_type,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> QueryAnalysis:
        """Create QueryAnalysis from a dictionary."""
        intent_raw = data.get("intent", QueryIntent.UNKNOWN.value)
        intent_val: QueryIntent | str = intent_raw
        if isinstance(intent_raw, str):
            try:
                intent_val = QueryIntent(intent_raw.lower())
            except ValueError:
                intent_val = intent_raw

        raw_entities = data.get("referenced_entities") or []
        entities = [
            ReferencedEntity.from_dict(e) if isinstance(e, dict) else e
            for e in raw_entities
        ]

        return cls(
            original_query=str(data.get("original_query", "")),
            normalized_query=str(data.get("normalized_query", "")),
            intent=intent_val,
            operations=list(data.get("operations") or []),
            referenced_entities=entities,
            symbols=list(data.get("symbols") or []),
            language=str(data.get("language", "en")),
            metadata=dict(data.get("metadata") or {}),
            confidence=float(data.get("confidence", 1.0)),
            confidence_type=str(data.get("confidence_type", "rule_based")),
        )
