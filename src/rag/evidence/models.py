"""Data models for Evidence Mapping layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class EvidenceReference:
    """Retrieved document chunk reference associated with generated answer content."""

    chunk_id: str
    paper_id: str = ""
    paper_title: str = ""
    section_title: str = ""
    page_start: int = 1
    page_end: int = 1
    retrieval_rank: int = 1
    retrieval_score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert EvidenceReference to dictionary representation."""
        return {
            "chunk_id": self.chunk_id,
            "paper_id": self.paper_id,
            "paper_title": self.paper_title,
            "section_title": self.section_title,
            "page_start": self.page_start,
            "page_end": self.page_end,
            "retrieval_rank": self.retrieval_rank,
            "retrieval_score": self.retrieval_score,
        }


@dataclass
class EvidenceSpan:
    """Individual sentence from generated answer mapped to supporting evidence chunks."""

    sentence_index: int
    sentence_text: str
    supported_by_chunks: list[str] = field(default_factory=list)
    support_level: str = "NONE"  # DIRECT, PARTIAL, WEAK, NONE
    support_type: str = "none"  # entity_match, symbol_match, token_overlap, none
    alignment_score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert EvidenceSpan to dictionary representation."""
        return {
            "sentence_index": self.sentence_index,
            "sentence_text": self.sentence_text,
            "supported_by_chunks": self.supported_by_chunks,
            "support_level": self.support_level,
            "support_type": self.support_type,
            "alignment_score": self.alignment_score,
        }


@dataclass
class EvidenceMetadata:
    """Metadata container describing evidence mapping details."""

    mapping_version: str = "v1.0"
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    average_alignment_score: float = 0.0
    direct_support_count: int = 0
    partial_support_count: int = 0
    weak_support_count: int = 0
    no_support_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Convert EvidenceMetadata to dictionary representation."""
        return {
            "mapping_version": self.mapping_version,
            "generated_at": self.generated_at,
            "average_alignment_score": self.average_alignment_score,
            "direct_support_count": self.direct_support_count,
            "partial_support_count": self.partial_support_count,
            "weak_support_count": self.weak_support_count,
            "no_support_count": self.no_support_count,
        }


@dataclass
class EvidenceBundle:
    """Complete bundle associating generated answer text with supporting evidence and metrics."""

    question: str
    answer_text: str
    references: list[EvidenceReference] = field(default_factory=list)
    spans: list[EvidenceSpan] = field(default_factory=list)
    coverage_score: float = 0.0
    supported_sentence_count: int = 0
    total_sentence_count: int = 0
    unsupported_sentences: list[str] = field(default_factory=list)
    unused_chunks: list[str] = field(default_factory=list)
    metadata: EvidenceMetadata = field(default_factory=EvidenceMetadata)

    def to_dict(self) -> dict[str, Any]:
        """Convert EvidenceBundle to dictionary representation."""
        return {
            "question": self.question,
            "answer_text": self.answer_text,
            "references": [r.to_dict() for r in self.references],
            "spans": [s.to_dict() for s in self.spans],
            "coverage_score": self.coverage_score,
            "supported_sentence_count": self.supported_sentence_count,
            "total_sentence_count": self.total_sentence_count,
            "unsupported_sentences": self.unsupported_sentences,
            "unused_chunks": self.unused_chunks,
            "metadata": self.metadata.to_dict(),
        }
