"""Abstract base class interface for guardrail decision engines."""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.rag.answer_generator.models import AnswerResponse
from src.rag.citation_engine.models import CitationBundle
from src.rag.evidence.models import EvidenceBundle
from src.rag.grounding.models import GroundingReport
from src.rag.guardrails.models import GuardrailDecision, GuardrailReport as FullGuardrailReport


class BaseGuardrailEngine(ABC):
    """Abstract Base Class defining the guardrail decision engine service contract."""

    @abstractmethod
    def evaluate_guardrails(
        self,
        answer_response: AnswerResponse,
        evidence_bundle: EvidenceBundle | None = None,
        citation_bundle: CitationBundle | None = None,
        grounding_report: GroundingReport | None = None,
    ) -> tuple[GuardrailDecision, FullGuardrailReport]:
        """Evaluate guardrail rules over upstream outputs and produce a policy decision.

        Args:
            answer_response: AnswerResponse container.
            evidence_bundle: Optional EvidenceBundle container.
            citation_bundle: Optional CitationBundle container.
            grounding_report: Optional GroundingReport container.

        Returns:
            Tuple of (GuardrailDecision, FullGuardrailReport).
        """
        pass
