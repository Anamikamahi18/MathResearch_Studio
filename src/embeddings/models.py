"""Data models for document chunking and vector embeddings."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ChunkMetadata:
    """Provenance and structural metadata associated with a text chunk."""

    paper_id: str
    paper_title: str
    authors: list[str] = field(default_factory=list)
    section_id: str = ""
    section_title: str = ""
    section_type: str = "other"
    page_start: int = 1
    page_end: int = 1
    entity_type: str | None = None

    def __post_init__(self) -> None:
        """Validate metadata field constraints."""
        if not self.paper_id:
            raise ValueError("paper_id cannot be empty")
        if self.page_start < 0 or self.page_end < 0:
            raise ValueError("page_start and page_end cannot be negative")
        if self.page_end < self.page_start:
            raise ValueError("page_end cannot be less than page_start")

    def to_dict(self) -> dict[str, Any]:
        """Convert metadata instance to a plain dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ChunkMetadata:
        """Create a ChunkMetadata instance from a dictionary."""
        return cls(
            paper_id=data.get("paper_id", ""),
            paper_title=data.get("paper_title", ""),
            authors=list(data.get("authors") or []),
            section_id=data.get("section_id", ""),
            section_title=data.get("section_title", ""),
            section_type=data.get("section_type", "other"),
            page_start=int(data.get("page_start", 1)),
            page_end=int(data.get("page_end", 1)),
            entity_type=data.get("entity_type"),
        )


@dataclass
class TextChunk:
    """A segment of text extracted from a paper with associated metadata."""

    chunk_id: str
    text: str
    metadata: ChunkMetadata

    def __post_init__(self) -> None:
        """Validate text chunk fields."""
        if not self.chunk_id:
            raise ValueError("chunk_id cannot be empty")
        if not isinstance(self.text, str):
            raise TypeError("text must be a string")

    def to_dict(self) -> dict[str, Any]:
        """Convert TextChunk instance to a plain dictionary."""
        return {
            "chunk_id": self.chunk_id,
            "text": self.text,
            "metadata": self.metadata.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TextChunk:
        """Create a TextChunk instance from a dictionary."""
        meta_data = data.get("metadata") or {}
        metadata = (
            meta_data
            if isinstance(meta_data, ChunkMetadata)
            else ChunkMetadata.from_dict(meta_data)
        )
        return cls(
            chunk_id=data.get("chunk_id", ""),
            text=data.get("text", ""),
            metadata=metadata,
        )


@dataclass
class EmbeddedChunk:
    """A text chunk coupled with its vector embedding representation."""

    chunk_id: str
    embedding: list[float]
    metadata: ChunkMetadata
    text: str = ""

    def __post_init__(self) -> None:
        """Validate embedded chunk fields."""
        if not self.chunk_id:
            raise ValueError("chunk_id cannot be empty")
        if not isinstance(self.embedding, list):
            raise TypeError("embedding must be a list of floats")

    def to_dict(self) -> dict[str, Any]:
        """Convert EmbeddedChunk instance to a plain dictionary."""
        return {
            "chunk_id": self.chunk_id,
            "text": self.text,
            "embedding": self.embedding,
            "metadata": self.metadata.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EmbeddedChunk:
        """Create an EmbeddedChunk instance from a dictionary."""
        meta_data = data.get("metadata") or {}
        metadata = (
            meta_data
            if isinstance(meta_data, ChunkMetadata)
            else ChunkMetadata.from_dict(meta_data)
        )
        return cls(
            chunk_id=data.get("chunk_id", ""),
            embedding=[float(x) for x in (data.get("embedding") or [])],
            metadata=metadata,
            text=data.get("text", ""),
        )
