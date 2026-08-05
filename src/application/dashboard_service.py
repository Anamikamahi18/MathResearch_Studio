"""DashboardService application service for aggregated metrics, paper counts, entity breakdowns, and graph statistics."""

from __future__ import annotations

import logging
from typing import Any

from src.application.document_service import DocumentService
from src.application.graph_service import GraphService as ApplicationGraphService
from src.rag.vector_store import FAISSVectorStore

logger = logging.getLogger(__name__)


class DashboardService:
    """Application service providing aggregated dashboard statistics, statement breakdowns, and graph metrics."""

    def __init__(
        self,
        document_service: DocumentService | None = None,
        graph_service: ApplicationGraphService | None = None,
        vector_store: FAISSVectorStore | None = None,
    ) -> None:
        """Initialize DashboardService with service dependencies.

        Args:
            document_service: Optional DocumentService instance.
            graph_service: Optional ApplicationGraphService instance.
            vector_store: Optional FAISSVectorStore instance.
        """
        self.document_service = document_service or DocumentService()
        self.graph_service = graph_service or ApplicationGraphService()
        self.vector_store = vector_store or getattr(self.document_service, "vector_store", FAISSVectorStore())

    def get_statistics(self) -> dict[str, Any]:
        """Aggregate high-level system overview statistics.

        Returns:
            Dictionary containing paper_count, definition_count, theorem_count, lemma_count,
            total_vector_chunks, graph_nodes, and graph_edges.
        """
        paper_count = self.get_paper_counts()
        definitions = self.get_definitions()
        theorems = self.get_theorems()
        lemmas = self.get_lemmas()
        graph_metrics = self.get_graph_metrics()
        vector_chunks = (
            self.vector_store.number_of_vectors()
            if hasattr(self.vector_store, "number_of_vectors")
            else 0
        )

        stats = {
            "paper_count": paper_count,
            "definition_count": len(definitions),
            "theorem_count": len(theorems),
            "lemma_count": len(lemmas),
            "total_vector_chunks": vector_chunks,
            "graph_nodes": graph_metrics.get("total_nodes", 0),
            "graph_edges": graph_metrics.get("total_edges", 0),
            "graph_density": graph_metrics.get("density", 0.0),
        }

        logger.info(
            "Dashboard statistics: %d papers, %d defs, %d thms, %d lemmas, %d vector chunks",
            paper_count,
            len(definitions),
            len(theorems),
            len(lemmas),
            vector_chunks,
        )

        return stats

    def get_paper_counts(self) -> int:
        """Return total count of papers stored/ingested in the library catalog."""
        papers = self.document_service.list_papers()
        return len(papers)

    def get_definitions(self) -> list[dict[str, Any]]:
        """Retrieve all mathematical definition entities across papers and Knowledge Graph.

        Returns:
            List of definition node dictionaries.
        """
        # Try graph node lookup first
        def_nodes = self.graph_service.node_lookup(node_type="definition")
        if def_nodes:
            return def_nodes

        # Fallback to extracting from raw documents in paper library
        extracted_defs: list[dict[str, Any]] = []
        for paper in self.document_service.list_papers():
            raw_doc = paper.get("raw_document") or {}
            entities = raw_doc.get("math_entities") or raw_doc.get("entities") or {}
            for item in entities.get("definitions", []):
                if isinstance(item, dict):
                    extracted_defs.append(item)
                elif isinstance(item, str):
                    extracted_defs.append({"title": item, "paper_id": paper.get("paper_id")})
        return extracted_defs

    def get_theorems(self) -> list[dict[str, Any]]:
        """Retrieve all mathematical theorem entities across papers and Knowledge Graph.

        Returns:
            List of theorem node dictionaries.
        """
        thm_nodes = self.graph_service.node_lookup(node_type="theorem")
        if thm_nodes:
            return thm_nodes

        extracted_thms: list[dict[str, Any]] = []
        for paper in self.document_service.list_papers():
            raw_doc = paper.get("raw_document") or {}
            entities = raw_doc.get("math_entities") or raw_doc.get("entities") or {}
            for item in entities.get("theorems", []):
                if isinstance(item, dict):
                    extracted_thms.append(item)
                elif isinstance(item, str):
                    extracted_thms.append({"title": item, "paper_id": paper.get("paper_id")})
        return extracted_thms

    def get_lemmas(self) -> list[dict[str, Any]]:
        """Retrieve all mathematical lemma entities across papers and Knowledge Graph.

        Returns:
            List of lemma node dictionaries.
        """
        lemma_nodes = self.graph_service.node_lookup(node_type="lemma")
        if lemma_nodes:
            return lemma_nodes

        extracted_lemmas: list[dict[str, Any]] = []
        for paper in self.document_service.list_papers():
            raw_doc = paper.get("raw_document") or {}
            entities = raw_doc.get("math_entities") or raw_doc.get("entities") or {}
            for item in entities.get("lemmas", []):
                if isinstance(item, dict):
                    extracted_lemmas.append(item)
                elif isinstance(item, str):
                    extracted_lemmas.append({"title": item, "paper_id": paper.get("paper_id")})
        return extracted_lemmas

    def get_graph_metrics(self) -> dict[str, Any]:
        """Retrieve topological metrics and statement type breakdowns from the Knowledge Graph.

        Returns:
            Dictionary containing node count, edge count, density, node type breakdown, and relation breakdown.
        """
        return self.graph_service.get_graph_metrics()
