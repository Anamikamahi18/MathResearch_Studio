"""Mathematical document chunking module."""

from __future__ import annotations

import logging
import re
from typing import Any

from .models import ChunkMetadata, TextChunk

logger = logging.getLogger(__name__)


def _normalize_authors(authors_raw: Any) -> list[str]:
    """Extract a list of author name strings from various parser author formats."""
    if not authors_raw:
        return []
    if isinstance(authors_raw, list):
        names: list[str] = []
        for author in authors_raw:
            if isinstance(author, str) and author.strip():
                names.append(author.strip())
            elif isinstance(author, dict):
                name = author.get("name") or author.get("author")
                if name and isinstance(name, str) and name.strip():
                    names.append(name.strip())
        return names
    if isinstance(authors_raw, str) and authors_raw.strip():
        return [authors_raw.strip()]
    return []


class MathDocumentChunker:
    """Section-aware and mathematical entity-preserving document chunker."""

    def __init__(
        self,
        max_chunk_size: int = 800,
        chunk_overlap: int = 150,
        min_chunk_size: int = 50,
    ) -> None:
        """Initialize chunker configuration.

        Args:
            max_chunk_size: Target maximum character length for narrative chunks.
            chunk_overlap: Character overlap between contiguous narrative chunks.
            min_chunk_size: Minimum character length for a valid chunk.
        """
        if max_chunk_size <= 0:
            raise ValueError("max_chunk_size must be positive")
        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")
        if chunk_overlap >= max_chunk_size:
            raise ValueError("chunk_overlap must be less than max_chunk_size")

        self.max_chunk_size = max_chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size

    def chunk_document(self, document: dict[str, Any]) -> list[TextChunk]:
        """Chunk a parsed document into structured TextChunk instances.

        Args:
            document: Parsed document dictionary adhering to Schema v1.0.

        Returns:
            List of TextChunk instances preserving math entities and section context.
        """
        if not isinstance(document, dict):
            logger.error("Invalid document input: expected dict, got %s", type(document))
            raise TypeError(f"Document must be a dictionary, got {type(document)}")

        paper_id = document.get("paper_id") or "unknown_paper"
        paper_title = document.get("title") or "Untitled Paper"
        authors = _normalize_authors(document.get("authors"))

        chunks: list[TextChunk] = []
        section_lookup: dict[str, dict[str, Any]] = {}

        # Pre-build section lookup map for fast context resolution
        for section in document.get("sections") or []:
            sec_id = section.get("section_id")
            if sec_id:
                section_lookup[sec_id] = section

        # 1. Chunk Mathematical Entities (Definitions, Theorems, Lemmas, Corollaries, Proofs)
        entity_categories = [
            ("definitions", "definition"),
            ("theorems", "theorem"),
            ("lemmas", "lemma"),
            ("corollaries", "corollary"),
            ("proofs", "proof"),
        ]

        for cat_key, entity_type in entity_categories:
            entities = document.get(cat_key) or []
            for idx, entity in enumerate(entities):
                if not isinstance(entity, dict):
                    continue

                raw_text = (entity.get("text") or "").strip()
                if not raw_text:
                    continue

                label = entity.get("label")
                if label and not raw_text.startswith(label):
                    text_content = f"{label}: {raw_text}"
                else:
                    text_content = raw_text

                sec_id = entity.get("section_id") or ""
                parent_section = section_lookup.get(sec_id, {})
                sec_title = parent_section.get("heading") or ""
                sec_type = parent_section.get("section_type") or "other"

                page_start = (
                    entity.get("page_start")
                    or entity.get("page")
                    or parent_section.get("page_start")
                    or 1
                )
                page_end = (
                    entity.get("page_end")
                    or entity.get("page")
                    or parent_section.get("page_end")
                    or page_start
                )

                entity_id = (
                    entity.get(f"{entity_type}_id")
                    or entity.get("entity_id")
                    or f"{entity_type}_{idx + 1:03d}"
                )
                chunk_id = f"{paper_id}_{entity_type}_{entity_id}"

                metadata = ChunkMetadata(
                    paper_id=paper_id,
                    paper_title=paper_title,
                    authors=authors,
                    section_id=sec_id,
                    section_title=sec_title,
                    section_type=sec_type,
                    page_start=int(page_start),
                    page_end=int(page_end),
                    entity_type=entity_type,
                )

                chunks.append(
                    TextChunk(
                        chunk_id=chunk_id,
                        text=text_content,
                        metadata=metadata,
                    )
                )

        # 2. Chunk Section Narrative Text
        sections = document.get("sections") or []
        for sec_idx, section in enumerate(sections):
            if not isinstance(section, dict):
                continue

            sec_id = section.get("section_id") or f"s{sec_idx + 1}"
            sec_title = section.get("heading") or "Untitled Section"
            sec_type = section.get("section_type") or "other"
            sec_text = (section.get("text") or "").strip()
            page_start = int(section.get("page_start") or 1)
            page_end = int(section.get("page_end") or page_start)

            if not sec_text:
                continue

            entity_type_label = "abstract" if sec_type == "abstract" else "section_text"

            section_text_chunks = self._split_text(sec_text)
            for c_idx, chunk_str in enumerate(section_text_chunks):
                chunk_id = f"{paper_id}_{sec_id}_c{c_idx + 1:03d}"
                metadata = ChunkMetadata(
                    paper_id=paper_id,
                    paper_title=paper_title,
                    authors=authors,
                    section_id=sec_id,
                    section_title=sec_title,
                    section_type=sec_type,
                    page_start=page_start,
                    page_end=page_end,
                    entity_type=entity_type_label,
                )

                chunks.append(
                    TextChunk(
                        chunk_id=chunk_id,
                        text=chunk_str,
                        metadata=metadata,
                    )
                )

        logger.info(
            "Chunked paper '%s' (%s): generated %d chunk(s)",
            paper_title,
            paper_id,
            len(chunks),
        )
        return chunks

    def _split_text(self, text: str) -> list[str]:
        """Split text string into overlapping chunks respecting sentence boundaries."""
        text = text.strip()
        if not text:
            return []
        if len(text) <= self.max_chunk_size:
            return [text]

        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        if not paragraphs:
            paragraphs = [text]

        result_chunks: list[str] = []
        current_chunk: list[str] = []
        current_length = 0

        for para in paragraphs:
            para_len = len(para)
            if current_length + para_len + 2 > self.max_chunk_size and current_chunk:
                chunk_str = "\n\n".join(current_chunk).strip()
                if len(chunk_str) >= self.min_chunk_size:
                    result_chunks.append(chunk_str)
                overlap_str = (
                    chunk_str[-self.chunk_overlap :]
                    if len(chunk_str) > self.chunk_overlap
                    else chunk_str
                )
                current_chunk = [overlap_str] if overlap_str else []
                current_length = len(overlap_str)

            if para_len > self.max_chunk_size:
                sentences = re.split(r"(?<=[.!?])\s+", para)
                for sentence in sentences:
                    sent_len = len(sentence)
                    if (
                        current_length + sent_len + 1 > self.max_chunk_size
                        and current_chunk
                    ):
                        chunk_str = " ".join(current_chunk).strip()
                        if len(chunk_str) >= self.min_chunk_size:
                            result_chunks.append(chunk_str)
                        overlap_str = (
                            chunk_str[-self.chunk_overlap :]
                            if len(chunk_str) > self.chunk_overlap
                            else chunk_str
                        )
                        current_chunk = [overlap_str] if overlap_str else []
                        current_length = len(overlap_str)

                    current_chunk.append(sentence)
                    current_length += sent_len + 1
            else:
                current_chunk.append(para)
                current_length += para_len + 2

        if current_chunk:
            chunk_str = "\n\n".join(current_chunk).strip()
            if len(chunk_str) >= self.min_chunk_size:
                result_chunks.append(chunk_str)

        return result_chunks


def chunk_document(
    document: dict[str, Any],
    max_chunk_size: int = 800,
    chunk_overlap: int = 150,
    min_chunk_size: int = 50,
) -> list[TextChunk]:
    """Convenience helper function to chunk a parsed document."""
    chunker = MathDocumentChunker(
        max_chunk_size=max_chunk_size,
        chunk_overlap=chunk_overlap,
        min_chunk_size=min_chunk_size,
    )
    return chunker.chunk_document(document)
