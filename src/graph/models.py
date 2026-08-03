"""Data models for mathematical knowledge graphs."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class NodeType(str, Enum):
    """Enumeration of graph node types."""

    PAPER = "paper"
    SECTION = "section"
    DEFINITION = "definition"
    THEOREM = "theorem"
    LEMMA = "lemma"
    COROLLARY = "corollary"
    PROOF = "proof"
    EQUATION = "equation"
    REFERENCE = "reference"
    OTHER = "other"


class RelationType(str, Enum):
    """Enumeration of graph edge relationship types."""

    DEPENDS_ON = "DEPENDS_ON"
    PROVES = "PROVES"
    USES_DEFINITION = "USES_DEFINITION"
    USES_LEMMA = "USES_LEMMA"
    USES_THEOREM = "USES_THEOREM"
    CONTAINED_IN = "CONTAINED_IN"
    CITES = "CITES"
    RELATED_TO = "RELATED_TO"


@dataclass
class GraphNode:
    """Represents a node in the mathematical research graph."""

    node_id: str
    node_type: NodeType | str
    label: str
    text: str = ""
    paper_id: str = ""
    section_id: str = ""
    page_start: int = 1
    page_end: int = 1
    attributes: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate graph node properties."""
        if not self.node_id:
            raise ValueError("node_id cannot be empty")
        if isinstance(self.node_type, str) and self.node_type in [
            e.value for e in NodeType
        ]:
            self.node_type = NodeType(self.node_type)

    def to_dict(self) -> dict[str, Any]:
        """Convert node instance to a plain dictionary."""
        return {
            "node_id": self.node_id,
            "node_type": (
                self.node_type.value
                if isinstance(self.node_type, Enum)
                else str(self.node_type)
            ),
            "label": self.label,
            "text": self.text,
            "paper_id": self.paper_id,
            "section_id": self.section_id,
            "page_start": self.page_start,
            "page_end": self.page_end,
            "attributes": self.attributes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GraphNode:
        """Create a GraphNode instance from a dictionary."""
        return cls(
            node_id=data.get("node_id", ""),
            node_type=data.get("node_type", NodeType.OTHER.value),
            label=data.get("label", ""),
            text=data.get("text", ""),
            paper_id=data.get("paper_id", ""),
            section_id=data.get("section_id", ""),
            page_start=int(data.get("page_start", 1)),
            page_end=int(data.get("page_end", 1)),
            attributes=dict(data.get("attributes") or {}),
        )


@dataclass
class GraphEdge:
    """Represents a directional relationship edge in the research graph."""

    edge_id: str
    source_id: str
    target_id: str
    relation_type: RelationType | str
    confidence: float = 1.0
    attributes: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate edge properties."""
        if not self.edge_id:
            raise ValueError("edge_id cannot be empty")
        if not self.source_id or not self.target_id:
            raise ValueError("source_id and target_id cannot be empty")
        if isinstance(self.relation_type, str) and self.relation_type in [
            e.value for e in RelationType
        ]:
            self.relation_type = RelationType(self.relation_type)

    def to_dict(self) -> dict[str, Any]:
        """Convert edge instance to a plain dictionary."""
        return {
            "edge_id": self.edge_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relation_type": (
                self.relation_type.value
                if isinstance(self.relation_type, Enum)
                else str(self.relation_type)
            ),
            "confidence": self.confidence,
            "attributes": self.attributes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GraphEdge:
        """Create a GraphEdge instance from a dictionary."""
        return cls(
            edge_id=data.get("edge_id", ""),
            source_id=data.get("source_id", ""),
            target_id=data.get("target_id", ""),
            relation_type=data.get("relation_type", RelationType.RELATED_TO.value),
            confidence=float(data.get("confidence", 1.0)),
            attributes=dict(data.get("attributes") or {}),
        )


class ResearchGraph:
    """Container representing a network of mathematical statements and dependencies."""

    def __init__(self) -> None:
        """Initialize an empty research graph."""
        self.nodes: dict[str, GraphNode] = {}
        self.edges: dict[str, GraphEdge] = {}
        self._out_adjacency: dict[str, list[str]] = {}
        self._in_adjacency: dict[str, list[str]] = {}

    def add_node(self, node: GraphNode) -> None:
        """Add or update a node in the graph."""
        if not isinstance(node, GraphNode):
            raise TypeError(f"Expected GraphNode, got {type(node)}")

        self.nodes[node.node_id] = node
        if node.node_id not in self._out_adjacency:
            self._out_adjacency[node.node_id] = []
        if node.node_id not in self._in_adjacency:
            self._in_adjacency[node.node_id] = []

    def add_edge(self, edge: GraphEdge) -> None:
        """Add an edge connecting two nodes in the graph."""
        if not isinstance(edge, GraphEdge):
            raise TypeError(f"Expected GraphEdge, got {type(edge)}")

        if edge.source_id not in self.nodes:
            raise KeyError(f"Source node '{edge.source_id}' not found in graph")
        if edge.target_id not in self.nodes:
            raise KeyError(f"Target node '{edge.target_id}' not found in graph")

        self.edges[edge.edge_id] = edge
        if edge.edge_id not in self._out_adjacency[edge.source_id]:
            self._out_adjacency[edge.source_id].append(edge.edge_id)
        if edge.edge_id not in self._in_adjacency[edge.target_id]:
            self._in_adjacency[edge.target_id].append(edge.edge_id)

    def get_node(self, node_id: str) -> GraphNode | None:
        """Retrieve a graph node by its ID."""
        return self.nodes.get(node_id)

    def get_out_edges(self, node_id: str) -> list[GraphEdge]:
        """Retrieve outgoing edges from a given node."""
        edge_ids = self._out_adjacency.get(node_id, [])
        return [self.edges[eid] for eid in edge_ids if eid in self.edges]

    def get_in_edges(self, node_id: str) -> list[GraphEdge]:
        """Retrieve incoming edges to a given node."""
        edge_ids = self._in_adjacency.get(node_id, [])
        return [self.edges[eid] for eid in edge_ids if eid in self.edges]

    def get_antecedents(self, node_id: str) -> list[GraphNode]:
        """Get nodes that the given node depends on (target nodes of outgoing edges)."""
        out_edges = self.get_out_edges(node_id)
        antecedent_ids = [edge.target_id for edge in out_edges]
        return [self.nodes[target_id] for target_id in antecedent_ids if target_id in self.nodes]

    def get_consequents(self, node_id: str) -> list[GraphNode]:
        """Get nodes that depend on the given node (source nodes of incoming edges)."""
        in_edges = self.get_in_edges(node_id)
        consequent_ids = [edge.source_id for edge in in_edges]
        return [self.nodes[source_id] for source_id in consequent_ids if source_id in self.nodes]

    def get_all_antecedents(self, node_id: str, max_depth: int = 5) -> list[GraphNode]:
        """Recursively retrieve all prerequisite nodes up to max_depth."""
        visited: set[str] = set()
        queue: list[tuple[str, int]] = [(node_id, 0)]
        result: list[GraphNode] = []

        while queue:
            curr_id, depth = queue.pop(0)
            if depth >= max_depth:
                continue

            for edge in self.get_out_edges(curr_id):
                target_id = edge.target_id
                if target_id not in visited and target_id in self.nodes:
                    visited.add(target_id)
                    result.append(self.nodes[target_id])
                    queue.append((target_id, depth + 1))

        return result

    def get_all_consequents(self, node_id: str, max_depth: int = 5) -> list[GraphNode]:
        """Recursively retrieve all downstream dependent nodes up to max_depth."""
        visited: set[str] = set()
        queue: list[tuple[str, int]] = [(node_id, 0)]
        result: list[GraphNode] = []

        while queue:
            curr_id, depth = queue.pop(0)
            if depth >= max_depth:
                continue

            for edge in self.get_in_edges(curr_id):
                source_id = edge.source_id
                if source_id not in visited and source_id in self.nodes:
                    visited.add(source_id)
                    result.append(self.nodes[source_id])
                    queue.append((source_id, depth + 1))

        return result

    def to_dict(self) -> dict[str, Any]:
        """Serialize the complete research graph to a plain dictionary."""
        return {
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "nodes": [node.to_dict() for node in self.nodes.values()],
            "edges": [edge.to_dict() for edge in self.edges.values()],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ResearchGraph:
        """Deserialize a research graph from a dictionary."""
        graph = cls()
        for node_data in data.get("nodes") or []:
            graph.add_node(GraphNode.from_dict(node_data))
        for edge_data in data.get("edges") or []:
            graph.add_edge(GraphEdge.from_dict(edge_data))
        return graph

    def to_networkx(self) -> Any:
        """Convert graph to a NetworkX DiGraph if networkx is installed."""
        try:
            import networkx as nx

            dg = nx.DiGraph()
            for node in self.nodes.values():
                dg.add_node(node.node_id, **node.to_dict())
            for edge in self.edges.values():
                dg.add_edge(edge.source_id, edge.target_id, **edge.to_dict())
            return dg
        except ImportError:
            raise RuntimeError("networkx library is required for to_networkx()")
