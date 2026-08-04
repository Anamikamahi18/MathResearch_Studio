"""Data models for prompt builder layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.rag.query_processing.models import QueryAnalysis
from src.rag.retrieval.models import RetrievalResponse, RetrievalResult


@dataclass
class PromptContext:
    """Context selection output containing included and excluded retrieved document chunks."""

    query_text: str
    included_chunks: list[RetrievalResult] = field(default_factory=list)
    excluded_chunks: list[RetrievalResult] = field(default_factory=list)
    total_context_tokens: int = 0
    coverage_score: float = 1.0


@dataclass
class PromptTemplate:
    """Template container holding system instructions, research rules, and prompt structure."""

    template_name: str
    system_prompt: str
    research_rules: list[str] = field(default_factory=list)
    user_prompt_template: str = "{query}"
    context_separator: str = "---"
    version: str = "v1.0"

    def to_dict(self) -> dict[str, Any]:
        """Convert PromptTemplate to dictionary representation."""
        return {
            "template_name": self.template_name,
            "system_prompt": self.system_prompt,
            "research_rules": self.research_rules,
            "user_prompt_template": self.user_prompt_template,
            "context_separator": self.context_separator,
            "version": self.version,
        }


@dataclass
class PromptRequest:
    """Input request container for constructing an LLM prompt."""

    query: str | QueryAnalysis
    retrieval_response: RetrievalResponse | list[RetrievalResult]
    max_prompt_tokens: int = 4096
    max_context_tokens: int = 3000
    template_name: str = "default"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PromptMetadata:
    """Metadata container describing prompt construction details."""

    query_text: str
    intent: str
    included_chunk_ids: list[str] = field(default_factory=list)
    excluded_chunk_ids: list[str] = field(default_factory=list)
    estimated_system_tokens: int = 0
    estimated_context_tokens: int = 0
    estimated_user_tokens: int = 0
    estimated_total_tokens: int = 0
    context_coverage: float = 1.0
    prompt_version: str = "v1.0"
    template_name: str = "default"

    def to_dict(self) -> dict[str, Any]:
        """Convert PromptMetadata to dictionary representation."""
        return {
            "query_text": self.query_text,
            "intent": self.intent,
            "included_chunk_ids": self.included_chunk_ids,
            "excluded_chunk_ids": self.excluded_chunk_ids,
            "estimated_system_tokens": self.estimated_system_tokens,
            "estimated_context_tokens": self.estimated_context_tokens,
            "estimated_user_tokens": self.estimated_user_tokens,
            "estimated_total_tokens": self.estimated_total_tokens,
            "context_coverage": self.context_coverage,
            "prompt_version": self.prompt_version,
            "template_name": self.template_name,
        }


@dataclass
class PromptResponse:
    """Assembled output prompt container returned by PromptBuilder."""

    system_prompt: str
    user_prompt: str
    full_prompt: str
    estimated_tokens: int
    included_chunks: list[RetrievalResult] = field(default_factory=list)
    excluded_chunks: list[RetrievalResult] = field(default_factory=list)
    context_coverage: float = 1.0
    prompt_version: str = "v1.0"
    metadata: PromptMetadata | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert PromptResponse to dictionary representation."""
        return {
            "system_prompt": self.system_prompt,
            "user_prompt": self.user_prompt,
            "full_prompt": self.full_prompt,
            "estimated_tokens": self.estimated_tokens,
            "included_chunks": [c.to_dict() for c in self.included_chunks],
            "excluded_chunks": [c.to_dict() for c in self.excluded_chunks],
            "context_coverage": self.context_coverage,
            "prompt_version": self.prompt_version,
            "metadata": self.metadata.to_dict() if self.metadata else {},
        }
