"""GuardrailReportBuilder for constructing comprehensive GuardrailReport objects."""

from __future__ import annotations

import logging
from typing import Sequence

from src.rag.guardrails.models import GuardrailDecision, GuardrailMetadata, GuardrailReport

logger = logging.getLogger(__name__)


class GuardrailReportBuilder:
    """Assembles detailed GuardrailReport objects detailing rule evaluation steps and timings."""

    def build_report(
        self,
        question: str,
        decision: GuardrailDecision,
        evaluated_rules: Sequence[str],
        decision_path: Sequence[str],
        strict_mode: bool = False,
        execution_time_ms: float = 0.0,
    ) -> GuardrailReport:
        """Construct GuardrailReport container.

        Args:
            question: User research question string.
            decision: Evaluated GuardrailDecision.
            evaluated_rules: Sequence of evaluated rule names.
            decision_path: Sequence of decision path log strings.
            strict_mode: Boolean indicating if strict mode was active.
            execution_time_ms: Evaluation duration in milliseconds.

        Returns:
            GuardrailReport instance.
        """
        metadata = GuardrailMetadata(
            evaluation_time_ms=execution_time_ms,
            strict_mode=strict_mode,
            rules_evaluated_count=len(evaluated_rules),
        )

        return GuardrailReport(
            question=question,
            decision=decision,
            evaluated_rules=list(evaluated_rules),
            decision_path=list(decision_path),
            metadata=metadata,
        )
