"""Abstract base class interface for answer generators."""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.rag.answer_generator.models import AnswerRequest, AnswerResponse
from src.rag.prompt_builder.models import PromptResponse


class BaseAnswerGenerator(ABC):
    """Abstract Base Class defining the answer generator service contract."""

    @abstractmethod
    def generate_answer(self, request: AnswerRequest | PromptResponse) -> AnswerResponse:
        """Transform a PromptResponse or AnswerRequest into a structured AnswerResponse.

        Args:
            request: Input AnswerRequest or PromptResponse artifact.

        Returns:
            AnswerResponse containing structured markdown, sections, metadata, and validation warnings.
        """
        pass
