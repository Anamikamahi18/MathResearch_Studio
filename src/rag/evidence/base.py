"""Abstract base class interface for evidence mappers."""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.rag.answer_generator.models import AnswerResponse
from src.rag.evidence.models import EvidenceBundle
from src.rag.retrieval.models import RetrievalResponse, RetrievalResult


class BaseEvidenceMapper(ABC):
    """Abstract Base Class defining the evidence mapper service contract."""

    @abstractmethod
    def map_evidence(
        self,
        answer_response: AnswerResponse,
        retrieval_response: RetrievalResponse | list[RetrievalResult],
    ) -> EvidenceBundle:
        """Map answer statements to supporting retrieved evidence chunks.

        Args:
            answer_response: Generated AnswerResponse container.
            retrieval_response: RetrievalResponse or list of candidate RetrievalResult items.

        Returns:
            EvidenceBundle containing references, spans, coverage, and metadata.
        """
        pass
