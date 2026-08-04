"""Data models for Guardrails layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class DecisionType(str, Enum):
    """Guardrails decision outcomes."""

    RETURN = "RETURN"
    RETURN_WITH_WARNING = "RETURN_WITH_WARNING"
    REFUSE = "REFUSE"
    ASK_FOR_CLARIFICATION = "ASK_FOR_CLARIFICATION"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class GuardrailStatus(str, Enum):
    """Guardrail evaluation status."""

    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"


@dataclass
class GuardrailDecision:
    """Decision output produced by GuardrailDecisionEngine."""

    decision_type: DecisionType
    status: GuardrailStatus
    reason: str
    warnings: list[str] = field(default_factory=list)
    violated_rules: list[str] = field(default_factory=list)
    grounding_score: float = 0.0
    citation_coverage: float = 0.0
    supported_claim_ratio: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert GuardrailDecision to dictionary representation."""
        return {
            "decision_type": self.decision_type.value,
            "status": self.status.value,
            "reason": self.reason,
            "warnings": self.warnings,
            "violated_rules": self.violated_rules,
            "grounding_score": self.grounding_score,
            "citation_coverage": self.citation_coverage,
            "supported_claim_ratio": self.supported_claim_ratio,
        }


@dataclass
class GuardrailMetadata:
    """Metadata container for Guardrails evaluation execution."""

    evaluation_time_ms: float = 0.0
    strict_mode: bool = False
    rules_evaluated_count: int = 0
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Convert GuardrailMetadata to dictionary representation."""
        return {
            "evaluation_time_ms": self.evaluation_time_ms,
            "strict_mode": self.strict_mode,
            "rules_evaluated_count": self.rules_evaluated_count,
            "generated_at": self.generated_at,
        }


@dataclass
class GuardrailReport:
    """Complete evaluation report detailing guardrail rule execution and decision path."""

    question: str
    decision: GuardrailDecision
    evaluated_rules: list[str] = field(default_factory=list)
    decision_path: list[str] = field(default_factory=list)
    metadata: GuardrailMetadata = field(default_factory=GuardrailMetadata)

    def to_dict(self) -> dict[str, Any]:
        """Convert GuardrailReport to dictionary representation."""
        return {
            "question": self.question,
            "decision": self.decision.to_dict(),
            "evaluated_rules": self.evaluated_rules,
            "decision_path": self.decision_path,
            "metadata": self.metadata.to_dict(),
        }
