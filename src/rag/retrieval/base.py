"""Abstract Base Class for modular retrieval backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from src.rag.query_processing.models import QueryAnalysis
from src.rag.retrieval.models import RetrievalResult


class BaseRetriever(ABC):
    """Abstract Base Class for document retrieval engines.

    Allows FAISS, BM25, Elasticsearch, Vespa, or cloud vector databases to be used
    interchangeably without changing downstream code.
    """

    @abstractmethod
    def retrieve(
        self, query_analysis: QueryAnalysis, top_k: int = 5
    ) -> list[RetrievalResult]:
        """Retrieve and rank candidate document chunks for a processed query analysis.

        Args:
            query_analysis: Structured QueryAnalysis from QueryProcessor.
            top_k: Target number of ranked results to return.

        Returns:
            List of RetrievalResult objects sorted by final score descending.
        """
        pass
