"""Configuration options for Guardrails layer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class GuardrailConfig:
    """Configuration container for Guardrails thresholds and policy flags."""

    minimum_grounding_score: float = 0.50
    minimum_supported_ratio: float = 0.40
    minimum_citation_coverage: float = 0.30
    warning_threshold: float = 0.70
    strict_mode: bool = False
    refuse_on_zero_evidence: bool = True
    ask_clarification_on_unknown_intent: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Convert GuardrailConfig to dictionary representation."""
        return {
            "minimum_grounding_score": self.minimum_grounding_score,
            "minimum_supported_ratio": self.minimum_supported_ratio,
            "minimum_citation_coverage": self.minimum_citation_coverage,
            "warning_threshold": self.warning_threshold,
            "strict_mode": self.strict_mode,
            "refuse_on_zero_evidence": self.refuse_on_zero_evidence,
            "ask_clarification_on_unknown_intent": self.ask_clarification_on_unknown_intent,
        }
