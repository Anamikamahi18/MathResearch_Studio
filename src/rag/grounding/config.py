"""Configuration options for Grounding Verification layer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class GroundingConfig:
    """Configuration container for grounding verification thresholds and options."""

    grounding_threshold: float = 0.50
    min_evidence_coverage: float = 0.50
    min_citation_coverage: float = 0.40
    strict_mode: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert GroundingConfig to dictionary representation."""
        return {
            "grounding_threshold": self.grounding_threshold,
            "min_evidence_coverage": self.min_evidence_coverage,
            "min_citation_coverage": self.min_citation_coverage,
            "strict_mode": self.strict_mode,
        }
