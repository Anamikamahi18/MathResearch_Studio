"""CitationRenderer for rendering markdown outputs with inline citations, bibliographies, and hover metadata."""

from __future__ import annotations

import logging
from typing import Sequence

from src.rag.citation_engine.models import Citation, CitationBundle

logger = logging.getLogger(__name__)


class CitationRenderer:
    """Renders final Markdown output including inline markers, bibliography, and hover metadata comments."""

    def render_markdown(self, bundle: CitationBundle) -> str:
        """Render complete formatted markdown string from CitationBundle.

        Args:
            bundle: Input CitationBundle container.

        Returns:
            Formatted markdown text string.
        """
        lines: list[str] = [
            f"# Answer: {bundle.question}\n",
            bundle.answer_text_with_citations,
            "\n---\n",
            "## References\n",
        ]

        if bundle.bibliography:
            for bib_entry in bundle.bibliography:
                lines.append(f"- {bib_entry}")
        else:
            lines.append("*No external references cited.*")

        # Attach hover metadata comment placeholders
        hover_comments = self.render_hover_metadata(bundle.citations)
        if hover_comments:
            lines.append("\n" + hover_comments)

        return "\n".join(lines)

    def render_hover_metadata(self, citations: Sequence[Citation]) -> str:
        """Generate hover metadata comment blocks for future UI tooltip integration.

        Args:
            citations: Sequence of Citation objects.

        Returns:
            HTML / comment string containing hover metadata.
        """
        if not citations:
            return ""

        meta_lines: list[str] = ["<!-- CITATION HOVER METADATA FOR UI INTERACTION -->"]
        for c in citations:
            meta_comment = (
                f"<!-- citation:{c.citation_id} chunk='{c.chunk_id}' paper='{c.paper_title}' "
                f"section='{c.section_title}' page='{c.page_start}' score={c.retrieval_score:.4f} -->"
            )
            meta_lines.append(meta_comment)

        return "\n".join(meta_lines)
