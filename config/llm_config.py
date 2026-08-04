"""LLM adapter layer configuration settings."""

from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Any


@dataclass
class LLMConfig:
    """Configuration settings for LLM adapter generation and provider selection."""

    default_provider: str = "mock"
    default_model: str = "mock-math-v1"
    temperature: float = 0.0
    max_tokens: int = 2048
    timeout: float = 30.0
    retry_count: int = 3

    @classmethod
    def from_env(cls) -> LLMConfig:
        """Construct LLMConfig from environment variables if present."""
        return cls(
            default_provider=os.getenv("LLM_DEFAULT_PROVIDER", "mock"),
            default_model=os.getenv("LLM_DEFAULT_MODEL", "mock-math-v1"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.0")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2048")),
            timeout=float(os.getenv("LLM_TIMEOUT", "30.0")),
            retry_count=int(os.getenv("LLM_RETRY_COUNT", "3")),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert LLMConfig to dictionary representation."""
        return {
            "default_provider": self.default_provider,
            "default_model": self.default_model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "timeout": self.timeout,
            "retry_count": self.retry_count,
        }


DEFAULT_LLM_CONFIG = LLMConfig()
