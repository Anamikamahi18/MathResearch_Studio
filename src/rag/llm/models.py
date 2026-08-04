"""Data models for provider-agnostic LLM adapter layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.rag.prompt_builder.models import PromptResponse


@dataclass
class ProviderConfig:
    """Configuration container for a specific LLM provider backend."""

    provider_name: str
    model_name: str
    temperature: float = 0.0
    max_tokens: int = 2048
    timeout: float = 30.0
    retry_count: int = 3
    extra_params: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert ProviderConfig to dictionary representation."""
        return {
            "provider_name": self.provider_name,
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "timeout": self.timeout,
            "retry_count": self.retry_count,
            "extra_params": self.extra_params,
        }


@dataclass
class LLMRequest:
    """Input request container for LLM text generation."""

    prompt_text: str = ""
    system_prompt: str = ""
    user_prompt: str = ""
    prompt_response: PromptResponse | None = None
    temperature: float = 0.0
    max_tokens: int = 2048
    provider: str = "mock"
    model: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_prompt_response(
        cls,
        prompt_response: PromptResponse,
        provider: str = "mock",
        model: str = "mock-math-v1",
        temperature: float = 0.0,
        max_tokens: int = 2048,
    ) -> LLMRequest:
        """Construct LLMRequest directly from a PromptResponse artifact."""
        return cls(
            prompt_text=prompt_response.full_prompt,
            system_prompt=prompt_response.system_prompt,
            user_prompt=prompt_response.user_prompt,
            prompt_response=prompt_response,
            temperature=temperature,
            max_tokens=max_tokens,
            provider=provider,
            model=model,
            metadata={
                "estimated_prompt_tokens": prompt_response.estimated_tokens,
                "included_chunks": len(prompt_response.included_chunks),
                "excluded_chunks": len(prompt_response.excluded_chunks),
                "context_coverage": prompt_response.context_coverage,
                "prompt_version": prompt_response.prompt_version,
            },
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert LLMRequest to dictionary representation."""
        return {
            "prompt_text": self.prompt_text,
            "system_prompt": self.system_prompt,
            "user_prompt": self.user_prompt,
            "has_prompt_response": self.prompt_response is not None,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "provider": self.provider,
            "model": self.model,
            "metadata": self.metadata,
        }


@dataclass
class LLMMetadata:
    """Response metadata returned by LLM adapter."""

    provider: str
    model: str
    latency_ms: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    finish_reason: str = "stop"
    extra_info: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert LLMMetadata to dictionary representation."""
        return {
            "provider": self.provider,
            "model": self.model,
            "latency_ms": self.latency_ms,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "finish_reason": self.finish_reason,
            "extra_info": self.extra_info,
        }


@dataclass
class LLMResponse:
    """Container holding generated text output and metadata from LLM adapter."""

    raw_text: str
    request: LLMRequest
    metadata: LLMMetadata

    def to_dict(self) -> dict[str, Any]:
        """Convert LLMResponse to dictionary representation."""
        return {
            "raw_text": self.raw_text,
            "request": self.request.to_dict(),
            "metadata": self.metadata.to_dict(),
        }
