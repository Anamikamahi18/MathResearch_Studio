"""CitationFormatter for formatting inline markers and generating bibliographies."""

from __future__ import annotations

import logging
from typing import Sequence

from src.rag.citation_engine.models import Citation, CitationReference
from src.rag.citation_engine.styles import (
    STYLE_INLINE,
    CitationStyle,
    CitationStyleType,
)
from src.rag.evidence.models import EvidenceBundle, EvidenceReference, EvidenceSpan

logger = logging.getLogger(__name__)


class CitationFormatter:
    """Formats inline citations and bibliography entries based on CitationStyle configuration."""

    def __init__(self, style: CitationStyle | None = None) -> None:
        """Initialize CitationFormatter with a CitationStyle.

        Args:
            style: Optional CitationStyle configuration. Defaults to STYLE_INLINE.
        """
        self.style = style or STYLE_INLINE

    def build_citations(self, references: Sequence[EvidenceReference]) -> dict[str, Citation]:
        """Build Citation objects from EvidenceReference objects, assigning unique IDs.

        Args:
            references: Sequence of EvidenceReference objects from EvidenceBundle.

        Returns:
            Dictionary mapping chunk_id to Citation instance.
        """
        citations_map: dict[str, Citation] = {}
        for idx, ref in enumerate(references, start=1):
            if ref.chunk_id in citations_map:
                continue

            disp_author = ref.paper_title.split()[0] if ref.paper_title else "Anonymous"
            disp_year = "2024"

            display_text = self._format_citation_marker(
                citation_id=idx,
                paper_title=ref.paper_title or ref.paper_id or "Reference",
                author=disp_author,
                year=disp_year,
                section=ref.section_title or "Section",
                page=ref.page_start,
            )

            citations_map[ref.chunk_id] = Citation(
                citation_id=idx,
                chunk_id=ref.chunk_id,
                paper_id=ref.paper_id or f"paper_{idx}",
                paper_title=ref.paper_title or "Untitled Paper",
                authors=[disp_author],
                year=disp_year,
                section_title=ref.section_title or "General",
                page_start=ref.page_start,
                page_end=ref.page_end,
                retrieval_rank=ref.retrieval_rank,
                retrieval_score=ref.retrieval_score,
                display_text=display_text,
            )
        return citations_map

    def format_annotated_answer(
        self,
        spans: Sequence[EvidenceSpan],
        citations_map: dict[str, Citation],
    ) -> str:
        """Attach inline citation markers to answer sentences based on evidence spans.

        Args:
            spans: Sequence of EvidenceSpan items from EvidenceBundle.
            citations_map: Mapping of chunk_id to Citation instances.

        Returns:
            Answer text string with inline citation markers attached.
        """
        annotated_sentences: list[str] = []

        for span in spans:
            sent = span.sentence_text.rstrip()
            if not span.supported_by_chunks:
                annotated_sentences.append(sent)
                continue

            # Gather citations for supported chunks
            span_citations = [citations_map[cid] for cid in span.supported_by_chunks if cid in citations_map]
            if not span_citations:
                annotated_sentences.append(sent)
                continue

            markers = [c.display_text for c in span_citations]
            markers_str = " ".join(markers)

            if sent.endswith("."):
                annotated_sent = f"{sent[:-1]} {markers_str}."
            else:
                annotated_sent = f"{sent} {markers_str}"

            annotated_sentences.append(annotated_sent)

        return "\n\n".join(annotated_sentences)

    def generate_bibliography(self, citations_map: dict[str, Citation]) -> list[str]:
        """Generate structured bibliography items sorted by citation ID.

        Args:
            citations_map: Mapping of chunk_id to Citation instances.

        Returns:
            List of bibliography entry strings.
        """
        citations = sorted(citations_map.values(), key=lambda c: c.citation_id)
        bib_entries: list[str] = []

        for c in citations:
            author_str = ", ".join(c.authors) if c.authors else "Unknown Author"
            sec_str = f", {c.section_title}" if c.section_title else ""
            page_str = f", pp. {c.page_start}-{c.page_end}" if c.page_start else ""

            entry = f"[{c.citation_id}] {author_str} ({c.year}). *{c.paper_title}*{sec_str}{page_str}. [Chunk ID: {c.chunk_id}]"
            bib_entries.append(entry)

        return bib_entries

    def _format_citation_marker(
        self,
        citation_id: int,
        paper_title: str,
        author: str,
        year: str,
        section: str,
        page: int,
    ) -> str:
        """Internal helper for rendering citation marker string according to style."""
        if self.style.style_type == CitationStyleType.INLINE:
            return f"[{citation_id}]"
        elif self.style.style_type == CitationStyleType.AUTHOR_YEAR:
            return f"({author}, {year})"
        elif self.style.style_type == CitationStyleType.ACADEMIC:
            short_title = paper_title[:25] + "..." if len(paper_title) > 25 else paper_title
            return f"[{short_title}, {section}, p.{page}]"
        else:
            return f"[{citation_id}]"
