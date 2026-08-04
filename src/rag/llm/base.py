"""Abstract base class for provider-agnostic LLM adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.rag.llm.models import LLMRequest, LLMResponse


class BaseLLMAdapter(ABC):
    """Abstract Base Class interface for all LLM provider backends."""

    @abstractmethod
    def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate text output for a given LLMRequest.

        Args:
            request: LLMRequest container with prompt and generation parameters.

        Returns:
            LLMResponse containing raw_text, request, and execution metadata.
        """
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Verify provider availability and connectivity.

        Returns:
            True if service is accessible, False otherwise.
        """
        pass

    @abstractmethod
    def supports_streaming(self) -> bool:
        """Indicate whether the provider adapter supports token streaming.

        Returns:
            True if streaming is supported, False otherwise.
        """
        pass
