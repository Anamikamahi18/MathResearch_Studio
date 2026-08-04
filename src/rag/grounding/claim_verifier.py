"""ClaimVerifier for determining support levels (SUPPORTED, PARTIAL, UNSUPPORTED) for extracted claims."""

from __future__ import annotations

import logging
import re
from typing import Sequence

from src.rag.citation_engine.models import CitationBundle
from src.rag.evidence.models import EvidenceBundle
from src.rag.grounding.models import Claim

logger = logging.getLogger(__name__)


class ClaimVerifier:
    """Verifies extracted claims against EvidenceBundle spans and CitationBundle citations."""

    def verify_claims(
        self,
        extracted_claim_texts: Sequence[str],
        evidence_bundle: EvidenceBundle | None = None,
        citation_bundle: CitationBundle | None = None,
    ) -> list[Claim]:
        """Verify each claim against evidence spans and citation objects.

        Args:
            extracted_claim_texts: Sequence of extracted sentence claim strings.
            evidence_bundle: Optional EvidenceBundle container.
            citation_bundle: Optional CitationBundle container.

        Returns:
            List of verified Claim instances.
        """
        verified_claims: list[Claim] = []

        spans = evidence_bundle.spans if evidence_bundle else []
        citations = citation_bundle.citations if citation_bundle else []
        citations_by_chunk = {c.chunk_id: c.citation_id for c in citations}

        for idx, claim_text in enumerate(extracted_claim_texts, start=1):
            # Clean claim text for string comparison
            norm_claim = re.sub(r"\s+", " ", claim_text).strip().lower()

            matching_span = None
            # 1. Primary match by text overlap
            for span in spans:
                norm_span = re.sub(r"\s+", " ", span.sentence_text).strip().lower()
                if norm_claim in norm_span or norm_span in norm_claim:
                    matching_span = span
                    break

            # 2. Fallback match by index if spans list aligns
            if matching_span is None and idx <= len(spans):
                matching_span = spans[idx - 1]

            evidence_chunks: list[str] = matching_span.supported_by_chunks if matching_span else []
            align_score = matching_span.alignment_score if matching_span else 0.0
            span_level = matching_span.support_level if matching_span else "NONE"

            # Find matching Citation IDs
            matched_citation_ids: list[int] = []
            for cid in evidence_chunks:
                if cid in citations_by_chunk:
                    matched_citation_ids.append(citations_by_chunk[cid])

            for c in citations:
                if c.display_text and c.display_text in claim_text:
                    if c.citation_id not in matched_citation_ids:
                        matched_citation_ids.append(c.citation_id)

            # Classify support level
            if (span_level in ("DIRECT", "PARTIAL") or align_score >= 0.25) and (len(evidence_chunks) > 0 or len(matched_citation_ids) > 0):
                support_level = "SUPPORTED"
                ver_score = min(1.0, round(align_score + 0.30, 4))
            elif span_level in ("DIRECT", "PARTIAL", "WEAK") or align_score >= 0.10 or len(evidence_chunks) > 0 or len(matched_citation_ids) > 0:
                support_level = "PARTIAL"
                ver_score = round(max(align_score, 0.50), 4)
            else:
                support_level = "UNSUPPORTED"
                ver_score = 0.0

            claim_obj = Claim(
                claim_id=idx,
                claim_text=claim_text,
                sentence_index=matching_span.sentence_index if matching_span else idx,
                support_level=support_level,
                evidence_chunk_ids=evidence_chunks,
                citation_ids=matched_citation_ids,
                verification_score=ver_score,
            )
            verified_claims.append(claim_obj)

        logger.info("ClaimVerifier verified %d claims", len(verified_claims))
        return verified_claims
