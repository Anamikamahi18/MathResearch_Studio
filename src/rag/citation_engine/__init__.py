"""Citation Engine subpackage for the AI Research Assistant RAG layer."""

from src.rag.citation_engine.base import BaseCitationEngine
from src.rag.citation_engine.engine import CitationEngine
from src.rag.citation_engine.formatter import CitationFormatter
from src.rag.citation_engine.models import (
    Citation,
    CitationBundle,
    CitationMetadata,
    CitationReference,
)
from src.rag.citation_engine.renderer import CitationRenderer
from src.rag.citation_engine.styles import (
    BUILTIN_STYLES,
    STYLE_ACADEMIC,
    STYLE_AUTHOR_YEAR,
    STYLE_INLINE,
    CitationStyle,
    CitationStyleType,
)
from src.rag.citation_engine.validator import CitationValidator

__all__ = [
    "BaseCitationEngine",
    "CitationEngine",
    "CitationFormatter",
    "CitationValidator",
    "CitationRenderer",
    "CitationStyle",
    "CitationStyleType",
    "Citation",
    "CitationReference",
    "CitationBundle",
    "CitationMetadata",
    "STYLE_INLINE",
    "STYLE_AUTHOR_YEAR",
    "STYLE_ACADEMIC",
    "BUILTIN_STYLES",
]
