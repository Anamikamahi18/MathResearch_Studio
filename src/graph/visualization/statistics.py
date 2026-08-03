"""Structured graph statistics calculator."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from typing import Any

import networkx as nx


@dataclass
class GraphStatistics:
    """Structured container for graph analytical statistics."""

    total_nodes: int
    total_edges: int
    node_count_by_type: dict[str, int]
    edge_count_by_type: dict[str, int]
    density: float
    connected_components: int
    isolated_nodes: int
    average_degree: float
    largest_connected_component_size: int

    def to_dict(self) -> dict[str, Any]:
        """Convert statistics container to a dictionary."""
        return asdict(self)


def calculate_graph_statistics(graph: nx.MultiDiGraph) -> GraphStatistics:
    """Compute detailed analytical statistics for a NetworkX MultiDiGraph.

    Args:
        graph: NetworkX MultiDiGraph instance.

    Returns:
        Structured GraphStatistics instance.
    """
    total_nodes = graph.number_of_nodes()
    total_edges = graph.number_of_edges()

    if total_nodes == 0:
        return GraphStatistics(
            total_nodes=0,
            total_edges=0,
            node_count_by_type={},
            edge_count_by_type={},
            density=0.0,
            connected_components=0,
            isolated_nodes=0,
            average_degree=0.0,
            largest_connected_component_size=0,
        )

    node_counts: Counter[str] = Counter()
    for _, attrs in graph.nodes(data=True):
        n_type = str(attrs.get("entity_type", "unknown")).lower()
        node_counts[n_type] += 1

    edge_counts: Counter[str] = Counter()
    for _, _, _, attrs in graph.edges(keys=True, data=True):
        r_type = str(attrs.get("relation_type", "unknown")).lower()
        edge_counts[r_type] += 1

    components = list(nx.weakly_connected_components(graph))
    connected_components = len(components)
    largest_cc = max(len(c) for c in components) if components else 0

    isolated_nodes = sum(1 for node in graph.nodes if graph.degree(node) == 0)
    density = float(nx.density(graph)) if total_nodes > 1 else 0.0

    degrees = [deg for _, deg in graph.degree()]
    average_degree = float(sum(degrees) / total_nodes) if total_nodes > 0 else 0.0

    return GraphStatistics(
        total_nodes=total_nodes,
        total_edges=total_edges,
        node_count_by_type=dict(node_counts),
        edge_count_by_type=dict(edge_counts),
        density=round(density, 6),
        connected_components=connected_components,
        isolated_nodes=isolated_nodes,
        average_degree=round(average_degree, 4),
        largest_connected_component_size=largest_cc,
    )
