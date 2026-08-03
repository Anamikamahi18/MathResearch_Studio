"""Mathematical dependency extractor module."""

from __future__ import annotations

import logging
import re
from typing import Any

from .models import GraphEdge, GraphNode, NodeType, RelationType

logger = logging.getLogger(__name__)

# Regex patterns for cross-reference extraction
REF_PATTERNS = {
    "definition": re.compile(
        r"\b(?:Definition|Def\.)\s+(?P<num>\d+(?:\.\d+)*)\b", re.IGNORECASE
    ),
    "theorem": re.compile(
        r"\b(?:Theorem|Thm\.)\s+(?P<num>\d+(?:\.\d+)*)\b", re.IGNORECASE
    ),
    "lemma": re.compile(
        r"\b(?:Lemma|Lem\.)\s+(?P<num>\d+(?:\.\d+)*)\b", re.IGNORECASE
    ),
    "corollary": re.compile(
        r"\b(?:Corollary|Cor\.)\s+(?P<num>\d+(?:\.\d+)*)\b", re.IGNORECASE
    ),
}


class DependencyExtractor:
    """Extracts nodes and dependency relationships from parsed document JSONs."""

    def extract(
        self, document: dict[str, Any]
    ) -> tuple[list[GraphNode], list[GraphEdge]]:
        """Extract graph nodes and dependency edges from a parsed document dictionary.

        Args:
            document: Parsed document dictionary adhering to Schema v1.0.

        Returns:
            Tuple of (list of GraphNode, list of GraphEdge).
        """
        if not isinstance(document, dict):
            raise TypeError(f"Document must be a dictionary, got {type(document)}")

        paper_id = document.get("paper_id") or "unknown_paper"
        paper_title = document.get("title") or "Untitled Paper"

        nodes: list[GraphNode] = []
        edges: list[GraphEdge] = []
        node_map_by_label: dict[str, str] = {}
        edge_counter = 1

        # 1. Create Paper Node
        paper_node_id = f"paper_{paper_id}"
        nodes.append(
            GraphNode(
                node_id=paper_node_id,
                node_type=NodeType.PAPER,
                label=paper_title,
                text=document.get("abstract") or "",
                paper_id=paper_id,
            )
        )

        # 2. Create Section Nodes and CONTAINED_IN Edges
        section_lookup: dict[str, str] = {}
        sections = document.get("sections") or []
        for sec in sections:
            if not isinstance(sec, dict):
                continue

            sec_id = sec.get("section_id") or f"s_{len(section_lookup)+1}"
            sec_node_id = f"{paper_id}_{sec_id}"
            sec_title = sec.get("heading") or "Untitled Section"
            section_lookup[sec_id] = sec_node_id

            nodes.append(
                GraphNode(
                    node_id=sec_node_id,
                    node_type=NodeType.SECTION,
                    label=sec_title,
                    text=(sec.get("text") or "")[:500],
                    paper_id=paper_id,
                    section_id=sec_id,
                    page_start=int(sec.get("page_start") or 1),
                    page_end=int(sec.get("page_end") or 1),
                    attributes={"section_type": sec.get("section_type", "other")},
                )
            )

            # Edge: Section CONTAINED_IN Paper
            edge_id = f"edge_{edge_counter:04d}"
            edge_counter += 1
            edges.append(
                GraphEdge(
                    edge_id=edge_id,
                    source_id=sec_node_id,
                    target_id=paper_node_id,
                    relation_type=RelationType.CONTAINED_IN,
                )
            )

        # 3. Create Statement Entity Nodes
        statement_categories = [
            ("definitions", NodeType.DEFINITION, "def"),
            ("theorems", NodeType.THEOREM, "thm"),
            ("lemmas", NodeType.LEMMA, "lem"),
            ("corollaries", NodeType.COROLLARY, "cor"),
            ("proofs", NodeType.PROOF, "prf"),
        ]

        for cat_key, node_type, prefix in statement_categories:
            entities = document.get(cat_key) or []
            for idx, entity in enumerate(entities):
                if not isinstance(entity, dict):
                    continue

                entity_id = (
                    entity.get(f"{prefix}_id")
                    or entity.get("entity_id")
                    or f"{prefix}_{idx + 1:03d}"
                )
                node_id = f"{paper_id}_{node_type.value}_{entity_id}"
                label = (
                    entity.get("label")
                    or f"{node_type.value.capitalize()} {idx + 1}"
                )
                text = entity.get("text") or ""
                sec_id = entity.get("section_id") or ""
                sec_node_id = section_lookup.get(sec_id, paper_node_id)
                page_start = int(
                    entity.get("page_start")
                    or entity.get("page")
                    or 1
                )
                page_end = int(
                    entity.get("page_end") or page_start
                )

                node = GraphNode(
                    node_id=node_id,
                    node_type=node_type,
                    label=label,
                    text=text,
                    paper_id=paper_id,
                    section_id=sec_id,
                    page_start=page_start,
                    page_end=page_end,
                )
                nodes.append(node)

                if label:
                    node_map_by_label[label.lower()] = node_id
                    # Also map stripped label (e.g. "theorem 3.1" -> "thm 3.1")
                    norm_label = label.lower().replace("theorem", "thm").replace("definition", "def").replace("lemma", "lem").replace("corollary", "cor")
                    node_map_by_label[norm_label] = node_id

                # Edge: Statement CONTAINED_IN Section
                edge_id = f"edge_{edge_counter:04d}"
                edge_counter += 1
                edges.append(
                    GraphEdge(
                        edge_id=edge_id,
                        source_id=node_id,
                        target_id=sec_node_id,
                        relation_type=RelationType.CONTAINED_IN,
                    )
                )

                # Explicit Proof -> Theorem/Lemma/Corollary Link
                if node_type == NodeType.PROOF:
                    related = entity.get("related_to") or {}
                    for target_key, rel_type in [
                        ("theorem_id", RelationType.PROVES),
                        ("lemma_id", RelationType.PROVES),
                        ("corollary_id", RelationType.PROVES),
                    ]:
                        target_entity_id = related.get(target_key)
                        if target_entity_id:
                            target_type = target_key.replace("_id", "")
                            target_node_id = f"{paper_id}_{target_type}_{target_entity_id}"
                            edge_id = f"edge_{edge_counter:04d}"
                            edge_counter += 1
                            edges.append(
                                GraphEdge(
                                    edge_id=edge_id,
                                    source_id=node_id,
                                    target_id=target_node_id,
                                    relation_type=rel_type,
                                    confidence=0.9,
                                )
                            )

        # 4. Create Reference Nodes and CITES Edges
        references = document.get("references") or []
        for idx, ref in enumerate(references):
            if not isinstance(ref, dict):
                continue
            ref_id = ref.get("reference_id") or f"ref_{idx + 1:03d}"
            ref_node_id = f"{paper_id}_{ref_id}"
            ref_title = ref.get("title") or f"Reference {idx + 1}"
            ref_text = ref.get("raw_text") or ref_title

            ref_node = GraphNode(
                node_id=ref_node_id,
                node_type=NodeType.REFERENCE,
                label=ref_title[:100],
                text=ref_text,
                paper_id=paper_id,
                attributes={
                    "authors": ref.get("authors") or [],
                    "year": ref.get("year"),
                    "venue": ref.get("venue"),
                    "doi": ref.get("doi"),
                    "url": ref.get("url"),
                },
            )
            nodes.append(ref_node)

            edge_id = f"edge_{edge_counter:04d}"
            edge_counter += 1
            edges.append(
                GraphEdge(
                    edge_id=edge_id,
                    source_id=paper_node_id,
                    target_id=ref_node_id,
                    relation_type=RelationType.CITES,
                )
            )

        # 5. Create Equation Nodes and CONTAINED_IN Edges
        equations = document.get("equations") or []
        for idx, eq in enumerate(equations):
            if not isinstance(eq, dict):
                continue
            eq_id = eq.get("equation_id") or f"eq_{idx + 1:03d}"
            eq_node_id = f"{paper_id}_{eq_id}"
            eq_label = f"Eq ({eq.get('eq_number')})" if eq.get("eq_number") else f"Equation {idx + 1}"
            sec_id = eq.get("section_id") or ""
            sec_node_id = section_lookup.get(sec_id, paper_node_id)
            page = int(eq.get("page") or 1)

            eq_node = GraphNode(
                node_id=eq_node_id,
                node_type=NodeType.EQUATION,
                label=eq_label,
                text=eq.get("latex_text") or eq.get("raw_text") or "",
                paper_id=paper_id,
                section_id=sec_id,
                page_start=page,
                page_end=page,
                attributes={
                    "is_numbered": bool(eq.get("is_numbered")),
                    "eq_number": eq.get("eq_number"),
                },
            )
            nodes.append(eq_node)

            edge_id = f"edge_{edge_counter:04d}"
            edge_counter += 1
            edges.append(
                GraphEdge(
                    edge_id=edge_id,
                    source_id=eq_node_id,
                    target_id=sec_node_id,
                    relation_type=RelationType.CONTAINED_IN,
                )
            )

        # 6. In-Text Cross-Reference Dependency Extraction (Implicit Links)
        for node in nodes:
            if node.node_type in (NodeType.PAPER, NodeType.SECTION, NodeType.REFERENCE, NodeType.EQUATION) or not node.text:
                continue

            for cat, pattern in REF_PATTERNS.items():
                for match in pattern.finditer(node.text):
                    num = match.group("num")
                    target_label = f"{cat} {num}".lower()
                    target_node_id = node_map_by_label.get(target_label)

                    if target_node_id and target_node_id != node.node_id:
                        relation = (
                            RelationType.USES_DEFINITION
                            if cat == "definition"
                            else RelationType.USES_LEMMA
                            if cat == "lemma"
                            else RelationType.USES_THEOREM
                        )
                        edge_id = f"edge_{edge_counter:04d}"
                        edge_counter += 1
                        edges.append(
                            GraphEdge(
                                edge_id=edge_id,
                                source_id=node.node_id,
                                target_id=target_node_id,
                                relation_type=relation,
                                confidence=0.8,
                            )
                        )

        logger.info(
            "Extracted %d nodes and %d edges for paper '%s'",
            len(nodes),
            len(edges),
            paper_id,
        )
        return nodes, edges
