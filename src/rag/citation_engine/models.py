"""Data models for Citation Engine layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Citation:
    """Individual citation object representing a mapped evidence reference."""

    citation_id: int
    chunk_id: str
    paper_id: str = ""
    paper_title: str = ""
    authors: list[str] = field(default_factory=list)
    year: str = ""
    section_title: str = ""
    page_start: int = 1
    page_end: int = 1
    retrieval_rank: int = 1
    retrieval_score: float = 0.0
    support_level: str = "DIRECT"
    display_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert Citation to dictionary representation."""
        return {
            "citation_id": self.citation_id,
            "chunk_id": self.chunk_id,
            "paper_id": self.paper_id,
            "paper_title": self.paper_title,
            "authors": self.authors,
            "year": self.year,
            "section_title": self.section_title,
            "page_start": self.page_start,
            "page_end": self.page_end,
            "retrieval_rank": self.retrieval_rank,
            "retrieval_score": self.retrieval_score,
            "support_level": self.support_level,
            "display_text": self.display_text,
        }


@dataclass
class CitationReference:
    """Container representing a single reference item in a bibliography."""

    citation_id: int
    paper_id: str
    paper_title: str
    formatted_bib_entry: str
    authors: list[str] = field(default_factory=list)
    year: str = ""
    section_title: str = ""
    chunk_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert CitationReference to dictionary representation."""
        return {
            "citation_id": self.citation_id,
            "paper_id": self.paper_id,
            "paper_title": self.paper_title,
            "formatted_bib_entry": self.formatted_bib_entry,
            "authors": self.authors,
            "year": self.year,
            "section_title": self.section_title,
            "chunk_id": self.chunk_id,
        }


@dataclass
class CitationMetadata:
    """Metadata container for citation execution and validation results."""

    citation_style: str = "inline"
    total_citations: int = 0
    unique_papers_cited: int = 0
    warnings: list[str] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Convert CitationMetadata to dictionary representation."""
        return {
            "citation_style": self.citation_style,
            "total_citations": self.total_citations,
            "unique_papers_cited": self.unique_papers_cited,
            "warnings": self.warnings,
            "generated_at": self.generated_at,
        }


@dataclass
class CitationBundle:
    """Complete bundle returned by CitationEngine containing annotated answer text and bibliography."""

    question: str
    answer_text: str
    answer_text_with_citations: str
    citations: list[Citation] = field(default_factory=list)
    bibliography: list[str] = field(default_factory=list)
    metadata: CitationMetadata = field(default_factory=CitationMetadata)

    def to_dict(self) -> dict[str, Any]:
        """Convert CitationBundle to dictionary representation."""
        return {
            "question": self.question,
            "answer_text": self.answer_text,
            "answer_text_with_citations": self.answer_text_with_citations,
            "citations": [c.to_dict() for c in self.citations],
            "bibliography": self.bibliography,
            "metadata": self.metadata.to_dict(),
        }
