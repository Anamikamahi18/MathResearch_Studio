"""Abstract base class interface for grounding verifiers."""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.rag.answer_generator.models import AnswerResponse
from src.rag.citation_engine.models import CitationBundle
from src.rag.evidence.models import EvidenceBundle
from src.rag.grounding.models import GroundingReport


class BaseGroundingVerifier(ABC):
    """Abstract Base Class defining the grounding verifier service contract."""

    @abstractmethod
    def verify_grounding(
        self,
        answer_response: AnswerResponse,
        evidence_bundle: EvidenceBundle | None = None,
        citation_bundle: CitationBundle | None = None,
    ) -> GroundingReport:
        """Verify grounding of answer response against evidence and citations.

        Args:
            answer_response: AnswerResponse container.
            evidence_bundle: Optional EvidenceBundle container.
            citation_bundle: Optional CitationBundle container.

        Returns:
            GroundingReport containing claim verification results and metrics.
        """
        pass
