"""Abstract base class interface for prompt builders."""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.rag.prompt_builder.models import PromptRequest, PromptResponse


class BasePromptBuilder(ABC):
    """Abstract base class defining the prompt builder service contract."""

    @abstractmethod
    def build_prompt(self, request: PromptRequest) -> PromptResponse:
        """Construct a grounded LLM prompt response from a prompt request.

        Args:
            request: PromptRequest container holding query, retrieval candidates, and token limits.

        Returns:
            PromptResponse containing assembled prompts, token estimates, and metadata.
        """
        pass
