"""CitationValidator for checking citation completeness and evidence alignment integrity."""

from __future__ import annotations

import logging
from typing import Sequence

from src.rag.citation_engine.models import Citation
from src.rag.evidence.models import EvidenceBundle

logger = logging.getLogger(__name__)


class CitationValidator:
    """Validates citations for missing metadata, duplicate references, invalid pages, and orphan evidence."""

    def validate_citations(
        self,
        citations: Sequence[Citation],
        evidence_bundle: EvidenceBundle,
    ) -> list[str]:
        """Inspect citations and evidence bundle for validation warnings.

        Args:
            citations: Sequence of Citation objects.
            evidence_bundle: EvidenceBundle input.

        Returns:
            List of warning strings.
        """
        warnings: list[str] = []
        seen_ids: set[int] = set()
        citation_chunk_ids: set[str] = {c.chunk_id for c in citations}

        for c in citations:
            # 1. Duplicate citation IDs
            if c.citation_id in seen_ids:
                warnings.append(f"Duplicate citation ID detected: {c.citation_id}")
            seen_ids.add(c.citation_id)

            # 2. Missing metadata checks
            if not c.paper_id or c.paper_id.startswith("paper_0"):
                warnings.append(f"Missing or generic paper ID for chunk '{c.chunk_id}'")

            if not c.paper_title or c.paper_title == "Untitled Paper":
                warnings.append(f"Missing paper title for chunk '{c.chunk_id}'")

            # 3. Invalid page numbers
            if c.page_start < 1:
                warnings.append(f"Invalid page_start ({c.page_start}) for chunk '{c.chunk_id}'")

            if c.page_end < c.page_start:
                warnings.append(
                    f"Invalid page range ({c.page_start}-{c.page_end}) for chunk '{c.chunk_id}'"
                )

        # 4. Orphan evidence checks
        for span in evidence_bundle.spans:
            for cid in span.supported_by_chunks:
                if cid not in citation_chunk_ids:
                    warnings.append(
                        f"Orphan evidence: Sentence '{span.sentence_index}' references chunk '{cid}' which has no Citation object"
                    )

        if warnings:
            logger.warning("CitationValidator found %d validation warnings", len(warnings))
        else:
            logger.info("CitationValidator found zero warnings - citation integrity verified")

        return warnings
