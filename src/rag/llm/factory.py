"""LLM Adapter Factory for instantiating and managing provider backends."""

from __future__ import annotations

import logging
from typing import Type

from src.rag.llm.adapter import MockLLMAdapter
from src.rag.llm.base import BaseLLMAdapter

logger = logging.getLogger(__name__)


class LLMAdapterFactory:
    """Factory for creating and registering LLM provider adapters."""

    _registry: dict[str, Type[BaseLLMAdapter]] = {
        "mock": MockLLMAdapter,
    }

    # Registered provider string constants for future provider implementations
    PROVIDER_MOCK = "mock"
    PROVIDER_OPENAI = "openai"
    PROVIDER_GEMINI = "gemini"
    PROVIDER_ANTHROPIC = "anthropic"
    PROVIDER_OLLAMA = "ollama"
    PROVIDER_AZURE_OPENAI = "azure_openai"
    PROVIDER_VLLM = "vllm"
    PROVIDER_HUGGINGFACE = "huggingface"

    @classmethod
    def register_adapter(cls, provider_name: str, adapter_class: Type[BaseLLMAdapter]) -> None:
        """Register a new LLM provider adapter class.

        Args:
            provider_name: Provider key identifier (e.g. 'openai', 'gemini').
            adapter_class: Class inheriting from BaseLLMAdapter.

        Raises:
            TypeError: If adapter_class does not inherit from BaseLLMAdapter.
        """
        if not issubclass(adapter_class, BaseLLMAdapter):
            raise TypeError(f"Adapter class must inherit from BaseLLMAdapter, got {adapter_class.__name__}")
        key = provider_name.lower().strip()
        cls._registry[key] = adapter_class
        logger.info("Registered LLM adapter '%s' -> %s", key, adapter_class.__name__)

    @classmethod
    def get_adapter(
        cls,
        provider_name: str = "mock",
        model_name: str = "mock-math-v1",
        **kwargs,
    ) -> BaseLLMAdapter:
        """Instantiate and return an LLM adapter for the specified provider.

        Args:
            provider_name: Provider name string (default: 'mock').
            model_name: Model identifier string.
            **kwargs: Extra parameters passed to the adapter constructor.

        Returns:
            Instance of BaseLLMAdapter.

        Raises:
            ValueError: If provider_name is not registered.
        """
        key = provider_name.lower().strip()
        if key not in cls._registry:
            supported = ", ".join(cls.list_supported_providers())
            raise ValueError(f"Unsupported LLM provider '{provider_name}'. Supported providers: {supported}")

        adapter_cls = cls._registry[key]
        logger.info("Instantiating LLM adapter '%s' (%s)", key, adapter_cls.__name__)
        return adapter_cls(model_name=model_name, **kwargs)

    @classmethod
    def list_supported_providers(cls) -> list[str]:
        """Return list of currently registered provider names.

        Returns:
            List of registered provider key strings.
        """
        return sorted(list(cls._registry.keys()))
