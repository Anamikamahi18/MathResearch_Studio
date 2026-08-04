"""Retrieval engine subpackage for the AI Research Assistant RAG layer."""

from config.retrieval_config import DEFAULT_RETRIEVAL_CONFIG, RetrievalConfig
from src.rag.retrieval.base import BaseRetriever
from src.rag.retrieval.engine import RetrievalEngine
from src.rag.retrieval.explanation import RankingReasonGenerator
from src.rag.retrieval.hybrid_retriever import HybridRetriever
from src.rag.retrieval.models import (
    HybridScoringWeights,
    RetrievalExplanation,
    RetrievalResponse,
    RetrievalResult,
    RetrievalStatistics,
)
from src.rag.retrieval.scoring import BaseScoringEngine, WeightedScoringEngine
from src.rag.retrieval.statistics import RetrievalStatisticsCalculator

__all__ = [
    "BaseRetriever",
    "BaseScoringEngine",
    "WeightedScoringEngine",
    "HybridRetriever",
    "RetrievalEngine",
    "RetrievalResult",
    "HybridScoringWeights",
    "RetrievalExplanation",
    "RetrievalStatistics",
    "RetrievalResponse",
    "RankingReasonGenerator",
    "RetrievalStatisticsCalculator",
    "RetrievalConfig",
    "DEFAULT_RETRIEVAL_CONFIG",
]
