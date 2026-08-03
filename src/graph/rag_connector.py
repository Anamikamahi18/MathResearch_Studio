"""Graph-augmented retriever module for RAG integration."""

from __future__ import annotations

import logging
from typing import Any

from src.rag.retriever import SemanticRetriever
from .service import GraphService

logger = logging.getLogger(__name__)


class GraphAugmentedRetriever:
    """Combines vector similarity search with mathematical dependency graph expansion."""

    def __init__(
        self,
        retriever: SemanticRetriever,
        graph_service: GraphService,
    ) -> None:
        """Initialize graph-augmented retriever.

        Args:
            retriever: Active SemanticRetriever instance.
            graph_service: Active GraphService instance.
        """
        self.retriever = retriever
        self.graph_service = graph_service

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        include_antecedents: bool = True,
        include_proof_chains: bool = True,
    ) -> list[dict[str, Any]]:
        """Perform semantic retrieval and expand results with graph topological context.

        Args:
            query: Natural language search query string.
            top_k: Target number of vector search hits.
            include_antecedents: Whether to fetch prerequisite definitions/lemmas.
            include_proof_chains: Whether to include proof blocks and target theorems.

        Returns:
            List of augmented result dictionaries enriched with graph dependency metadata.
        """
        base_results = self.retriever.retrieve(query=query, top_k=top_k)
        if not base_results:
            return []

        augmented_results: list[dict[str, Any]] = []

        for res in base_results:
            augmented_entry = dict(res)
            chunk_id = res.get("chunk_id", "")
            paper_id = res.get("paper_id", "")
            entity_type = res.get("entity_type")

            # Try to resolve graph node corresponding to chunk
            graph_node_id: str | None = None
            if entity_type and entity_type in ("definition", "theorem", "lemma", "corollary", "proof"):
                # Chunk IDs are formatted: {paper_id}_{entity_type}_{entity_id}
                # Node IDs are formatted: {paper_id}_{node_type}_{entity_id}
                graph_node_id = chunk_id

            node_data = self.graph_service.get_node(graph_node_id) if graph_node_id else None

            # Fallback: search graph nodes matching paper_id and entity_type in text
            if not node_data and paper_id and entity_type:
                for node in self.graph_service.graph.nodes.values():
                    if node.paper_id == paper_id and (
                        node.node_type.value if hasattr(node.node_type, "value") else str(node.node_type)
                    ) == entity_type:
                        if res.get("text") and res["text"] in node.text:
                            node_data = node.to_dict()
                            graph_node_id = node.node_id
                            break

            antecedents: list[dict[str, Any]] = []
            proof_chain: dict[str, Any] | None = None

            if graph_node_id:
                if include_antecedents:
                    antecedents = self.graph_service.get_antecedents(graph_node_id)
                if include_proof_chains and entity_type in ("theorem", "lemma", "corollary"):
                    proof_chain = self.graph_service.get_proof_chain(graph_node_id)

            augmented_entry["graph_context"] = {
                "graph_node_id": graph_node_id,
                "antecedents": antecedents,
                "proof_chain": proof_chain,
            }
            augmented_results.append(augmented_entry)

        logger.info(
            "GraphAugmentedRetriever expanded %d chunk(s) for query: '%s'",
            len(augmented_results),
            query,
        )
        return augmented_results
