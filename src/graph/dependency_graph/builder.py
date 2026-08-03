"""NetworkX-backed mathematical dependency graph builder."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from collections import Counter
from typing import Any, Sequence

import networkx as nx

from src.graph.entity_extraction import EntityType, ExtractedEntity
from src.graph.relation_extraction import ExtractedRelation, RelationType

logger = logging.getLogger(__name__)


class BaseGraphBuilder(ABC):
    """Abstract interface for mathematical dependency graph builders."""

    @abstractmethod
    def build_graph(
        self,
        entities: Sequence[ExtractedEntity],
        relations: Sequence[ExtractedRelation],
    ) -> Any:
        """Build and populate graph from entities and relations."""
        pass

    @abstractmethod
    def add_entities(self, entities: Sequence[ExtractedEntity]) -> None:
        """Add or update entity nodes in the graph."""
        pass

    @abstractmethod
    def add_relations(self, relations: Sequence[ExtractedRelation]) -> None:
        """Add or update relation edges in the graph."""
        pass

    @abstractmethod
    def merge_graph(self, other: BaseGraphBuilder | Any) -> None:
        """Merge another graph instance into this graph."""
        pass

    @abstractmethod
    def export_networkx(self) -> nx.MultiDiGraph:
        """Export the graph as a NetworkX MultiDiGraph instance."""
        pass

    @abstractmethod
    def graph_statistics(self) -> dict[str, Any]:
        """Compute structural statistics of the graph."""
        pass


class NetworkXGraphBuilder(BaseGraphBuilder):
    """NetworkX MultiDiGraph builder for mathematical statement dependency graphs."""

    def __init__(self, graph: nx.MultiDiGraph | None = None) -> None:
        """Initialize builder with an optional existing MultiDiGraph."""
        self._graph: nx.MultiDiGraph = graph if graph is not None else nx.MultiDiGraph()

    @property
    def graph(self) -> nx.MultiDiGraph:
        """Return the underlying MultiDiGraph."""
        return self._graph

    def build_graph(
        self,
        entities: Sequence[ExtractedEntity],
        relations: Sequence[ExtractedRelation],
    ) -> nx.MultiDiGraph:
        """Build a new graph from given entities and relations."""
        self._graph.clear()
        self.add_entities(entities)
        self.add_relations(relations)
        return self._graph

    def add_entities(self, entities: Sequence[ExtractedEntity]) -> None:
        """Add or update entity nodes in the graph preserving all metadata."""
        for entity in entities:
            if not isinstance(entity, ExtractedEntity):
                raise TypeError(f"Expected ExtractedEntity, got {type(entity)}")

            e_type = (
                entity.entity_type.value
                if isinstance(entity.entity_type, EntityType)
                else str(entity.entity_type)
            )

            node_attrs = {
                "entity_id": entity.entity_id,
                "entity_type": e_type,
                "title": entity.title,
                "text": entity.text,
                "source_paper": entity.source_paper,
                "section_id": entity.section_id,
                "section_title": entity.section_title,
                "page_start": entity.page_start,
                "page_end": entity.page_end,
                "symbols": list(entity.symbols),
                "references": list(entity.references),
                "dependencies": list(entity.dependencies),
            }

            self._graph.add_node(entity.entity_id, **node_attrs)

        logger.info("Added/updated %d entity node(s)", len(entities))

    def add_relations(self, relations: Sequence[ExtractedRelation]) -> None:
        """Add or update relation edges in the graph preserving metadata."""
        for rel in relations:
            if not isinstance(rel, ExtractedRelation):
                raise TypeError(f"Expected ExtractedRelation, got {type(rel)}")

            # Ensure source and target nodes exist (create stub if target is reference/external)
            if not self._graph.has_node(rel.source_entity_id):
                self._graph.add_node(
                    rel.source_entity_id,
                    entity_id=rel.source_entity_id,
                    entity_type="stub",
                    title=rel.source_entity_id,
                    text="",
                    source_paper=rel.source_paper,
                    section_id="",
                    section_title="",
                    page_start=1,
                    page_end=1,
                    symbols=[],
                    references=[],
                    dependencies=[],
                )

            if not self._graph.has_node(rel.target_entity_id):
                stub_type = (
                    "reference"
                    if rel.target_entity_id.startswith("[")
                    or "ref_" in rel.target_entity_id
                    else "stub"
                )
                self._graph.add_node(
                    rel.target_entity_id,
                    entity_id=rel.target_entity_id,
                    entity_type=stub_type,
                    title=rel.target_entity_id,
                    text="",
                    source_paper=rel.source_paper,
                    section_id="",
                    section_title="",
                    page_start=1,
                    page_end=1,
                    symbols=[],
                    references=[],
                    dependencies=[],
                )

            r_type = (
                rel.relation_type.value
                if isinstance(rel.relation_type, RelationType)
                else str(rel.relation_type)
            )

            edge_attrs = {
                "relation_id": rel.relation_id,
                "relation_type": r_type,
                "confidence": rel.confidence,
                "evidence_text": rel.evidence_text,
                "source_paper": rel.source_paper,
                "metadata": dict(rel.metadata),
            }

            self._graph.add_edge(
                rel.source_entity_id,
                rel.target_entity_id,
                key=rel.relation_id,
                **edge_attrs,
            )

        logger.info("Added/updated %d relation edge(s)", len(relations))

    def merge_graph(
        self, other: BaseGraphBuilder | nx.MultiDiGraph | Any
    ) -> None:
        """Merge another graph instance into this graph."""
        if isinstance(other, BaseGraphBuilder):
            other_nx = other.export_networkx()
        elif isinstance(other, (nx.MultiDiGraph, nx.DiGraph, nx.Graph)):
            other_nx = other
        else:
            raise TypeError(f"Unsupported graph type for merge: {type(other)}")

        for node_id, node_attrs in other_nx.nodes(data=True):
            if not self._graph.has_node(node_id):
                self._graph.add_node(node_id, **dict(node_attrs))
            else:
                self._graph.nodes[node_id].update(node_attrs)

        for u, v, k, edge_attrs in other_nx.edges(keys=True, data=True):
            self._graph.add_edge(u, v, key=k, **dict(edge_attrs))

        logger.info(
            "Merged graph. Total nodes: %d, edges: %d",
            self._graph.number_of_nodes(),
            self._graph.number_of_edges(),
        )

    def export_networkx(self) -> nx.MultiDiGraph:
        """Export the graph as a NetworkX MultiDiGraph instance."""
        return self._graph.copy()

    def graph_statistics(self) -> dict[str, Any]:
        """Compute comprehensive structural statistics of the graph."""
        total_nodes = self._graph.number_of_nodes()
        total_edges = self._graph.number_of_edges()

        node_counts: Counter[str] = Counter()
        for _, attrs in self._graph.nodes(data=True):
            n_type = str(attrs.get("entity_type", "unknown"))
            node_counts[n_type] += 1

        edge_counts: Counter[str] = Counter()
        for _, _, _, attrs in self._graph.edges(keys=True, data=True):
            r_type = str(attrs.get("relation_type", "unknown"))
            edge_counts[r_type] += 1

        connected_components = (
            nx.number_weakly_connected_components(self._graph)
            if total_nodes > 0
            else 0
        )

        isolated_nodes = (
            sum(1 for node in self._graph.nodes if self._graph.degree(node) == 0)
            if total_nodes > 0
            else 0
        )

        density = float(nx.density(self._graph)) if total_nodes > 1 else 0.0

        return {
            "total_nodes": total_nodes,
            "total_edges": total_edges,
            "node_count_by_type": dict(node_counts),
            "edge_count_by_type": dict(edge_counts),
            "connected_components": connected_components,
            "isolated_nodes": isolated_nodes,
            "density": round(density, 6),
        }


# Alias for backward compatibility and convenience
ResearchGraphBuilder = NetworkXGraphBuilder
