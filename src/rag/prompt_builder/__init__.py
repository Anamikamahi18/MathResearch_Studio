"""Prompt builder subpackage for the AI Research Assistant RAG layer."""

from src.rag.prompt_builder.base import BasePromptBuilder
from src.rag.prompt_builder.builder import PromptBuilder
from src.rag.prompt_builder.context_selector import ContextSelector
from src.rag.prompt_builder.formatter import PromptFormatter
from src.rag.prompt_builder.models import (
    PromptContext,
    PromptMetadata,
    PromptRequest,
    PromptResponse,
    PromptTemplate,
)
from src.rag.prompt_builder.templates import DEFAULT_RESEARCH_RULES, DEFAULT_SYSTEM_PROMPT, TemplateRegistry
from src.rag.prompt_builder.token_manager import TokenManager

__all__ = [
    "BasePromptBuilder",
    "PromptBuilder",
    "ContextSelector",
    "PromptFormatter",
    "PromptContext",
    "PromptMetadata",
    "PromptRequest",
    "PromptResponse",
    "PromptTemplate",
    "DEFAULT_RESEARCH_RULES",
    "DEFAULT_SYSTEM_PROMPT",
    "TemplateRegistry",
    "TokenManager",
]
