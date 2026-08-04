"""Data models for Answer Generator layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.rag.llm.base import BaseLLMAdapter
from src.rag.prompt_builder.models import PromptResponse


@dataclass
class AnswerSection:
    """Structured research output section."""

    title: str
    content: str
    section_type: str = "text"

    def to_dict(self) -> dict[str, Any]:
        """Convert AnswerSection to dictionary representation."""
        return {
            "title": self.title,
            "content": self.content,
            "section_type": self.section_type,
        }


@dataclass
class AnswerRequest:
    """Input request container for constructing an AnswerResponse."""

    prompt_response: PromptResponse
    llm_adapter: BaseLLMAdapter | None = None
    max_tokens: int = 2048
    temperature: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AnswerMetadata:
    """Metadata container describing answer generation execution details."""

    query_text: str
    intent: str
    provider: str
    model: str
    latency_ms: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    context_coverage: float = 1.0
    confidence_score: float = 1.0
    warnings: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    extra_info: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert AnswerMetadata to dictionary representation."""
        return {
            "query_text": self.query_text,
            "intent": self.intent,
            "provider": self.provider,
            "model": self.model,
            "latency_ms": self.latency_ms,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "context_coverage": self.context_coverage,
            "confidence_score": self.confidence_score,
            "warnings": self.warnings,
            "limitations": self.limitations,
            "extra_info": self.extra_info,
        }


@dataclass
class AnswerResponse:
    """Assembled structured response returned by AnswerGenerator."""

    question: str
    direct_answer: str
    formatted_answer: str
    sections: list[AnswerSection] = field(default_factory=list)
    metadata: AnswerMetadata | None = None
    warnings: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert AnswerResponse to dictionary representation."""
        return {
            "question": self.question,
            "direct_answer": self.direct_answer,
            "formatted_answer": self.formatted_answer,
            "sections": [s.to_dict() for s in self.sections],
            "metadata": self.metadata.to_dict() if self.metadata else {},
            "warnings": self.warnings,
            "limitations": self.limitations,
        }
