"""Abstract base class interface for citation engines."""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.rag.answer_generator.models import AnswerResponse
from src.rag.citation_engine.models import CitationBundle
from src.rag.evidence.models import EvidenceBundle


class BaseCitationEngine(ABC):
    """Abstract Base Class defining the citation engine service contract."""

    @abstractmethod
    def generate_citations(
        self,
        answer_response: AnswerResponse,
        evidence_bundle: EvidenceBundle,
        style: str = "inline",
    ) -> CitationBundle:
        """Generate citations and bibliography from answer text and evidence mappings.

        Args:
            answer_response: Generated AnswerResponse container.
            evidence_bundle: Mapped EvidenceBundle container.
            style: Name of citation style ('inline', 'author_year', 'academic').

        Returns:
            CitationBundle containing annotated answer text, citations, and bibliography.
        """
        pass
