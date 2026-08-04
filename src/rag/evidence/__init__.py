"""Evidence Mapping subpackage for the AI Research Assistant RAG layer."""

from src.rag.evidence.alignment import AlignmentEngine
from src.rag.evidence.base import BaseEvidenceMapper
from src.rag.evidence.coverage import CoverageAnalyzer
from src.rag.evidence.mapper import EvidenceMapper
from src.rag.evidence.models import (
    EvidenceBundle,
    EvidenceMetadata,
    EvidenceReference,
    EvidenceSpan,
)

__all__ = [
    "BaseEvidenceMapper",
    "EvidenceMapper",
    "AlignmentEngine",
    "CoverageAnalyzer",
    "EvidenceBundle",
    "EvidenceMetadata",
    "EvidenceReference",
    "EvidenceSpan",
]
