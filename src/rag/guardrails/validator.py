"""GuardrailValidator for checking input payload structural integrity."""

from __future__ import annotations

import logging
from typing import Any

from src.rag.answer_generator.models import AnswerResponse
from src.rag.citation_engine.models import CitationBundle
from src.rag.evidence.models import EvidenceBundle
from src.rag.grounding.models import GroundingReport

logger = logging.getLogger(__name__)


class GuardrailValidator:
    """Validates structural types of input payloads before evaluating guardrail rules."""

    def validate_inputs(
        self,
        answer_response: Any,
        evidence_bundle: Any = None,
        citation_bundle: Any = None,
        grounding_report: Any = None,
    ) -> list[str]:
        """Inspect input payloads and return validation errors if types are invalid.

        Args:
            answer_response: Input AnswerResponse container.
            evidence_bundle: Optional EvidenceBundle container.
            citation_bundle: Optional CitationBundle container.
            grounding_report: Optional GroundingReport container.

        Returns:
            List of validation error strings.
        """
        errors: list[str] = []

        if not isinstance(answer_response, AnswerResponse):
            errors.append(f"Expected AnswerResponse, got {type(answer_response).__name__}")

        if evidence_bundle is not None and not isinstance(evidence_bundle, EvidenceBundle):
            errors.append(f"Expected EvidenceBundle, got {type(evidence_bundle).__name__}")

        if citation_bundle is not None and not isinstance(citation_bundle, CitationBundle):
            errors.append(f"Expected CitationBundle, got {type(citation_bundle).__name__}")

        if grounding_report is not None and not isinstance(grounding_report, GroundingReport):
            errors.append(f"Expected GroundingReport, got {type(grounding_report).__name__}")

        return errors
