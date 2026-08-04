"""GroundingVerifier service implementation for evaluating claim grounding quality."""

from __future__ import annotations

import logging
import time

from src.rag.answer_generator.models import AnswerResponse
from src.rag.citation_engine.models import CitationBundle
from src.rag.evidence.models import EvidenceBundle
from src.rag.grounding.base import BaseGroundingVerifier
from src.rag.grounding.claim_extractor import ClaimExtractor
from src.rag.grounding.claim_verifier import ClaimVerifier
from src.rag.grounding.config import GroundingConfig
from src.rag.grounding.coverage import GroundingCoverageAnalyzer
from src.rag.grounding.models import GroundingReport
from src.rag.grounding.report import GroundingReportBuilder

logger = logging.getLogger(__name__)


class GroundingVerifier(BaseGroundingVerifier):
    """Main grounding verifier service evaluating whether generated claims are supported by evidence and citations."""

    def __init__(
        self,
        claim_extractor: ClaimExtractor | None = None,
        claim_verifier: ClaimVerifier | None = None,
        coverage_analyzer: GroundingCoverageAnalyzer | None = None,
        report_builder: GroundingReportBuilder | None = None,
        config: GroundingConfig | None = None,
    ) -> None:
        """Initialize GroundingVerifier with sub-components.

        Args:
            claim_extractor: Optional ClaimExtractor instance.
            claim_verifier: Optional ClaimVerifier instance.
            coverage_analyzer: Optional GroundingCoverageAnalyzer instance.
            report_builder: Optional GroundingReportBuilder instance.
            config: Optional GroundingConfig settings.
        """
        self.config = config or GroundingConfig()
        self.claim_extractor = claim_extractor or ClaimExtractor()
        self.claim_verifier = claim_verifier or ClaimVerifier()
        self.coverage_analyzer = coverage_analyzer or GroundingCoverageAnalyzer()
        self.report_builder = report_builder or GroundingReportBuilder()
        logger.info("Initialized GroundingVerifier service successfully")

    def verify_grounding(
        self,
        answer_response: AnswerResponse,
        evidence_bundle: EvidenceBundle | None = None,
        citation_bundle: CitationBundle | None = None,
    ) -> GroundingReport:
        """Verify grounding of answer response against evidence and citations.

        Args:
            answer_response: AnswerResponse container.
            evidence_bundle: Optional EvidenceBundle container.
            citation_bundle: Optional CitationBundle container.

        Returns:
            GroundingReport containing claim verification results and metrics.

        Raises:
            TypeError: If answer_response is invalid.
        """
        if not isinstance(answer_response, AnswerResponse):
            raise TypeError(f"Expected AnswerResponse, got {type(answer_response).__name__}")

        start_time = time.perf_counter()

        answer_text = (
            citation_bundle.answer_text_with_citations
            if citation_bundle
            else (answer_response.formatted_answer or answer_response.direct_answer or "")
        )

        # 1. Extract sentence claims
        claim_texts = self.claim_extractor.extract_claims(answer_text)

        # 2. Verify claims against evidence and citations
        verified_claims = self.claim_verifier.verify_claims(
            extracted_claim_texts=claim_texts,
            evidence_bundle=evidence_bundle,
            citation_bundle=citation_bundle,
        )

        # 3. Compute coverage metrics
        g_score, supp_ratio, unsupp_ratio, ev_cov, cit_cov = self.coverage_analyzer.compute_coverage(
            claims=verified_claims,
            evidence_bundle=evidence_bundle,
            citation_bundle=citation_bundle,
        )

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

        # 4. Build grounding report
        question_str = (
            evidence_bundle.question
            if evidence_bundle
            else (answer_response.question or "Question")
        )

        report = self.report_builder.build_report(
            question=question_str,
            answer_text=answer_text,
            claims=verified_claims,
            grounding_score=g_score,
            supported_claim_ratio=supp_ratio,
            unsupported_claim_ratio=unsupp_ratio,
            evidence_coverage=ev_cov,
            citation_coverage=cit_cov,
            config=self.config,
            execution_time_ms=elapsed_ms,
        )

        logger.info(
            "GroundingVerifier completed verification for '%s' (Score: %.4f, Supported Ratio: %.2f%%)",
            question_str,
            g_score,
            supp_ratio * 100,
        )

        return report
