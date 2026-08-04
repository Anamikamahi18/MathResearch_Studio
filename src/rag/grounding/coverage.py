"""GroundingCoverageAnalyzer for computing grounding metrics and coverage ratios."""

from __future__ import annotations

import logging
from typing import Sequence

from src.rag.citation_engine.models import CitationBundle
from src.rag.evidence.models import EvidenceBundle
from src.rag.grounding.models import Claim

logger = logging.getLogger(__name__)


class GroundingCoverageAnalyzer:
    """Computes grounding score, supported/unsupported claim ratios, and evidence/citation coverage."""

    def compute_coverage(
        self,
        claims: Sequence[Claim],
        evidence_bundle: EvidenceBundle | None = None,
        citation_bundle: CitationBundle | None = None,
    ) -> tuple[float, float, float, float, float]:
        """Calculate grounding metrics and coverage ratios across verified claims.

        Args:
            claims: Sequence of verified Claim objects.
            evidence_bundle: Optional EvidenceBundle container.
            citation_bundle: Optional CitationBundle container.

        Returns:
            Tuple of (grounding_score, supported_claim_ratio, unsupported_claim_ratio, evidence_coverage, citation_coverage).
        """
        total_claims = len(claims)
        if total_claims == 0:
            return 0.0, 0.0, 0.0, 0.0, 0.0

        supported_count = sum(1 for c in claims if c.support_level == "SUPPORTED")
        partial_count = sum(1 for c in claims if c.support_level == "PARTIAL")
        unsupported_count = sum(1 for c in claims if c.support_level == "UNSUPPORTED")

        claims_with_evidence = sum(1 for c in claims if len(c.evidence_chunk_ids) > 0)
        claims_with_citations = sum(1 for c in claims if len(c.citation_ids) > 0)

        supported_claim_ratio = round(supported_count / total_claims, 4)
        unsupported_claim_ratio = round(unsupported_count / total_claims, 4)
        evidence_coverage = round(claims_with_evidence / total_claims, 4)
        citation_coverage = round(claims_with_citations / total_claims, 4)

        # Grounding score gives full credit to SUPPORTED and half credit to PARTIAL
        raw_score = (supported_count * 1.0 + partial_count * 0.5) / total_claims
        grounding_score = round(raw_score, 4)

        logger.info(
            "GroundingCoverageAnalyzer: Score=%.4f, Supported=%.2f%%, EvidenceCov=%.2f%%",
            grounding_score,
            supported_claim_ratio * 100,
            evidence_coverage * 100,
        )

        return (
            grounding_score,
            supported_claim_ratio,
            unsupported_claim_ratio,
            evidence_coverage,
            citation_coverage,
        )
