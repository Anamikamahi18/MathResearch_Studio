"""GroundingReportBuilder for assembling complete GroundingReport metrics and warnings."""

from __future__ import annotations

import logging
from typing import Sequence

from src.rag.grounding.config import GroundingConfig
from src.rag.grounding.models import Claim, GroundingMetadata, GroundingReport

logger = logging.getLogger(__name__)


class GroundingReportBuilder:
    """Assembles GroundingReport container with claim summaries, coverage metrics, and integrity warnings."""

    def build_report(
        self,
        question: str,
        answer_text: str,
        claims: Sequence[Claim],
        grounding_score: float,
        supported_claim_ratio: float,
        unsupported_claim_ratio: float,
        evidence_coverage: float,
        citation_coverage: float,
        config: GroundingConfig,
        execution_time_ms: float = 0.0,
    ) -> GroundingReport:
        """Construct GroundingReport and evaluate integrity warnings.

        Args:
            question: User research question string.
            answer_text: Generated answer text.
            claims: Sequence of verified Claim objects.
            grounding_score: Calculated overall grounding score.
            supported_claim_ratio: Ratio of fully supported claims.
            unsupported_claim_ratio: Ratio of unsupported claims.
            evidence_coverage: Ratio of claims with evidence.
            citation_coverage: Ratio of claims with citations.
            config: GroundingConfig settings.
            execution_time_ms: Evaluation duration in milliseconds.

        Returns:
            GroundingReport instance.
        """
        warnings: list[str] = []

        if grounding_score < config.grounding_threshold:
            warnings.append(
                f"Overall grounding score ({grounding_score:.2f}) is below threshold ({config.grounding_threshold:.2f})"
            )

        if unsupported_claim_ratio > 0.30:
            warnings.append(f"High ratio of unsupported claims ({unsupported_claim_ratio:.2%})")

        if citation_coverage < config.min_citation_coverage:
            warnings.append(
                f"Citation coverage ({citation_coverage:.2%}) is below expected minimum ({config.min_citation_coverage:.2%})"
            )

        for c in claims:
            if c.support_level == "UNSUPPORTED":
                warnings.append(f"Unsupported claim detected (Claim #{c.claim_id}): '{c.claim_text[:60]}...'")

        metadata = GroundingMetadata(
            verification_version="v1.0",
            grounding_threshold=config.grounding_threshold,
            verification_time_ms=execution_time_ms,
        )

        logger.info(
            "GroundingReportBuilder built report for '%s' (%d claims, %d warnings)",
            question,
            len(claims),
            len(warnings),
        )

        return GroundingReport(
            question=question,
            answer_text=answer_text,
            grounding_score=grounding_score,
            supported_claim_ratio=supported_claim_ratio,
            unsupported_claim_ratio=unsupported_claim_ratio,
            evidence_coverage=evidence_coverage,
            citation_coverage=citation_coverage,
            claims=list(claims),
            warnings=warnings,
            metadata=metadata,
        )
