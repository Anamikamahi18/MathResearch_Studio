"""Data models for Grounding Verification layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Claim:
    """Represents an extracted sentence claim evaluated for evidence grounding."""

    claim_id: int
    claim_text: str
    sentence_index: int
    support_level: str = "UNSUPPORTED"  # SUPPORTED, PARTIAL, UNSUPPORTED
    evidence_chunk_ids: list[str] = field(default_factory=list)
    citation_ids: list[int] = field(default_factory=list)
    verification_score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert Claim to dictionary representation."""
        return {
            "claim_id": self.claim_id,
            "claim_text": self.claim_text,
            "sentence_index": self.sentence_index,
            "support_level": self.support_level,
            "evidence_chunk_ids": self.evidence_chunk_ids,
            "citation_ids": self.citation_ids,
            "verification_score": self.verification_score,
        }


@dataclass
class GroundingMetadata:
    """Metadata container for grounding verification execution."""

    verification_version: str = "v1.0"
    grounding_threshold: float = 0.50
    verification_time_ms: float = 0.0
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Convert GroundingMetadata to dictionary representation."""
        return {
            "verification_version": self.verification_version,
            "grounding_threshold": self.grounding_threshold,
            "verification_time_ms": self.verification_time_ms,
            "generated_at": self.generated_at,
        }


@dataclass
class GroundingReport:
    """Complete report output by GroundingVerifier assessing answer grounding quality."""

    question: str
    answer_text: str
    grounding_score: float = 0.0
    supported_claim_ratio: float = 0.0
    unsupported_claim_ratio: float = 0.0
    evidence_coverage: float = 0.0
    citation_coverage: float = 0.0
    claims: list[Claim] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: GroundingMetadata = field(default_factory=GroundingMetadata)

    def to_dict(self) -> dict[str, Any]:
        """Convert GroundingReport to dictionary representation."""
        return {
            "question": self.question,
            "answer_text": self.answer_text,
            "grounding_score": self.grounding_score,
            "supported_claim_ratio": self.supported_claim_ratio,
            "unsupported_claim_ratio": self.unsupported_claim_ratio,
            "evidence_coverage": self.evidence_coverage,
            "citation_coverage": self.citation_coverage,
            "claims": [c.to_dict() for c in self.claims],
            "warnings": self.warnings,
            "metadata": self.metadata.to_dict(),
        }
