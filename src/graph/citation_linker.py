"""Multi-paper citation linker module."""

from __future__ import annotations

import logging
from typing import Any

from .models import GraphEdge, NodeType, RelationType, ResearchGraph

logger = logging.getLogger(__name__)


class CitationLinker:
    """Resolves cross-paper citation links in multi-paper ResearchGraph instances."""

    def resolve_cross_paper_citations(self, graph: ResearchGraph) -> int:
        """Scan reference nodes in the graph and connect citing papers to target paper nodes.

        Args:
            graph: The ResearchGraph instance to update in-place.

        Returns:
            Number of new cross-paper CITES edges created.
        """
        paper_nodes = [
            node for node in graph.nodes.values() if node.node_type == NodeType.PAPER
        ]
        ref_nodes = [
            node for node in graph.nodes.values() if node.node_type == NodeType.REFERENCE
        ]

        if len(paper_nodes) < 2 or not ref_nodes:
            return 0

        # Build lookup maps for target papers
        paper_doi_map: dict[str, str] = {}
        paper_title_map: dict[str, str] = {}

        for paper in paper_nodes:
            doi = paper.attributes.get("doi")
            if doi:
                paper_doi_map[str(doi).strip().lower()] = paper.node_id

            title = paper.label.strip().lower()
            if title:
                paper_title_map[title] = paper.node_id

        new_edge_count = 0
        edge_counter = len(graph.edges) + 1

        for ref in ref_nodes:
            ref_doi = ref.attributes.get("doi")
            ref_title = (ref.label or "").strip().lower()
            citing_paper_id = ref.paper_id

            target_paper_id: str | None = None

            # 1. Match by DOI
            if ref_doi and str(ref_doi).strip().lower() in paper_doi_map:
                target_paper_id = paper_doi_map[str(ref_doi).strip().lower()]

            # 2. Match by exact title
            elif ref_title and ref_title in paper_title_map:
                target_paper_id = paper_title_map[ref_title]

            # 3. Match by partial title containment
            elif ref_title and len(ref_title) > 15:
                for paper_title, p_node_id in paper_title_map.items():
                    if len(paper_title) > 15 and (
                        ref_title in paper_title or paper_title in ref_title
                    ):
                        target_paper_id = p_node_id
                        break

            if target_paper_id and target_paper_id != f"paper_{citing_paper_id}":
                source_paper_node_id = f"paper_{citing_paper_id}"
                if source_paper_node_id in graph.nodes and target_paper_id in graph.nodes:
                    # Check if edge already exists
                    existing_edges = [
                        e for e in graph.get_out_edges(source_paper_node_id)
                        if e.target_id == target_paper_id and e.relation_type == RelationType.CITES
                    ]

                    if not existing_edges:
                        edge_id = f"edge_cite_{edge_counter:04d}"
                        edge_counter += 1
                        graph.add_edge(
                            GraphEdge(
                                edge_id=edge_id,
                                source_id=source_paper_node_id,
                                target_id=target_paper_id,
                                relation_type=RelationType.CITES,
                                confidence=0.85,
                                attributes={"via_reference_id": ref.node_id},
                            )
                        )
                        new_edge_count += 1

        logger.info("Resolved %d cross-paper CITES edge(s)", new_edge_count)
        return new_edge_count
