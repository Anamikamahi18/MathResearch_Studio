"""Unit tests for Day 5 Step 5.5 Grounding Verification Layer."""

from __future__ import annotations

import pytest

from src.rag.answer_generator.models import AnswerMetadata, AnswerResponse, AnswerSection
from src.rag.citation_engine.models import Citation, CitationBundle, CitationMetadata
from src.rag.evidence.models import EvidenceBundle, EvidenceMetadata, EvidenceReference, EvidenceSpan
from src.rag.grounding import (
    Claim,
    ClaimExtractor,
    ClaimVerifier,
    GroundingConfig,
    GroundingCoverageAnalyzer,
    GroundingMetadata,
    GroundingReport,
    GroundingReportBuilder,
    GroundingVerifier,
)


@pytest.fixture
def sample_evidence_bundle() -> EvidenceBundle:
    """Fixture providing sample EvidenceBundle."""
    refs = [
        EvidenceReference(
            chunk_id="chunk_def_1",
            paper_id="paper_1",
            paper_title="Hilbert Spaces and Operators",
            section_title="1. Definitions",
            retrieval_rank=1,
            retrieval_score=0.95,
        ),
    ]
    spans = [
        EvidenceSpan(
            sentence_index=1,
            sentence_text="Definition 1 states a Hilbert space is a complete inner product space.",
            supported_by_chunks=["chunk_def_1"],
            support_level="DIRECT",
            alignment_score=0.85,
        ),
        EvidenceSpan(
            sentence_index=2,
            sentence_text="This is an ungrounded claim statement.",
            supported_by_chunks=[],
            support_level="NONE",
            alignment_score=0.0,
        ),
    ]
    return EvidenceBundle(
        question="What is a Hilbert space?",
        answer_text="Definition 1 states a Hilbert space is a complete inner product space.\nThis is an ungrounded claim statement.",
        references=refs,
        spans=spans,
        coverage_score=0.5,
        supported_sentence_count=1,
        total_sentence_count=2,
        metadata=EvidenceMetadata(),
    )


@pytest.fixture
def sample_citation_bundle() -> CitationBundle:
    """Fixture providing sample CitationBundle."""
    citations = [
        Citation(
            citation_id=1,
            chunk_id="chunk_def_1",
            paper_id="paper_1",
            paper_title="Hilbert Spaces and Operators",
            display_text="[1]",
        )
    ]
    return CitationBundle(
        question="What is a Hilbert space?",
        answer_text="Ans",
        answer_text_with_citations="Definition 1 states a Hilbert space is a complete inner product space. [1]\nThis is an ungrounded claim statement.",
        citations=citations,
        bibliography=["[1] Ref"],
        metadata=CitationMetadata(total_citations=1, unique_papers_cited=1),
    )


@pytest.fixture
def sample_answer_response() -> AnswerResponse:
    """Fixture providing sample AnswerResponse."""
    meta = AnswerMetadata(query_text="What is a Hilbert space?", intent="definition", provider="mock", model="mock-model")
    sections = [
        AnswerSection(title="Direct Answer", content="Definition 1 states a Hilbert space is a complete inner product space."),
    ]
    return AnswerResponse(
        question="What is a Hilbert space?",
        direct_answer="Definition 1 states a Hilbert space is a complete inner product space.",
        formatted_answer="Definition 1 states a Hilbert space is a complete inner product space.",
        sections=sections,
        metadata=meta,
    )


class TestGroundingModels:
    """Test grounding data models and serialization."""

    def test_claim_to_dict(self) -> None:
        c = Claim(
            claim_id=1,
            claim_text="A Hilbert space is complete.",
            sentence_index=1,
            support_level="SUPPORTED",
            evidence_chunk_ids=["chunk_1"],
            citation_ids=[1],
            verification_score=0.90,
        )
        data = c.to_dict()
        assert data["claim_id"] == 1
        assert data["support_level"] == "SUPPORTED"
        assert data["verification_score"] == 0.90

    def test_grounding_report_to_dict(self) -> None:
        report = GroundingReport(
            question="Q?",
            answer_text="Ans",
            grounding_score=0.85,
            supported_claim_ratio=0.80,
            evidence_coverage=0.90,
            citation_coverage=0.90,
        )
        data = report.to_dict()
        assert data["question"] == "Q?"
        assert data["grounding_score"] == 0.85
        assert data["metadata"]["verification_version"] == "v1.0"


class TestClaimExtractor:
    """Test claim extraction and sentence segmentation."""

    def test_extract_claims_clean(self) -> None:
        extractor = ClaimExtractor()
        text = "Definition 1 states H is complete. Theorem 1 proves existence of bases."
        claims = extractor.extract_claims(text)

        assert len(claims) == 2
        assert "Definition 1" in claims[0]
        assert "Theorem 1" in claims[1]

    def test_extract_claims_filters_preambles(self) -> None:
        extractor = ClaimExtractor()
        text = "[Mock LLM Response]\nBased on the supplied mathematical context, the query is resolved as follows:\n1 [1].\nDefinition 1 states H is complete."
        claims = extractor.extract_claims(text)

        assert not any("[Mock LLM Response]" in c for c in claims)
        assert any("Definition 1" in c for c in claims)


class TestClaimVerifier:
    """Test claim support level verification."""

    def test_verify_claims(
        self,
        sample_evidence_bundle: EvidenceBundle,
        sample_citation_bundle: CitationBundle,
    ) -> None:
        verifier = ClaimVerifier()
        claims = ["Definition 1 states a Hilbert space is a complete inner product space.", "This is an ungrounded claim statement."]
        verified = verifier.verify_claims(
            extracted_claim_texts=claims,
            evidence_bundle=sample_evidence_bundle,
            citation_bundle=sample_citation_bundle,
        )

        assert len(verified) == 2
        assert verified[0].support_level in ("SUPPORTED", "PARTIAL")
        assert verified[1].support_level == "UNSUPPORTED"


class TestGroundingCoverageAnalyzer:
    """Test metric and coverage ratio calculations."""

    def test_compute_coverage(self) -> None:
        analyzer = GroundingCoverageAnalyzer()
        claims = [
            Claim(claim_id=1, claim_text="C1", sentence_index=1, support_level="SUPPORTED", evidence_chunk_ids=["chk1"], citation_ids=[1]),
            Claim(claim_id=2, claim_text="C2", sentence_index=2, support_level="UNSUPPORTED", evidence_chunk_ids=[], citation_ids=[]),
        ]
        g_score, supp_ratio, unsupp_ratio, ev_cov, cit_cov = analyzer.compute_coverage(claims)

        assert g_score == 0.5
        assert supp_ratio == 0.5
        assert unsupp_ratio == 0.5
        assert ev_cov == 0.5
        assert cit_cov == 0.5


class TestGroundingReportBuilder:
    """Test warning generation and report building."""

    def test_build_report_warnings(self) -> None:
        builder = GroundingReportBuilder()
        config = GroundingConfig(grounding_threshold=0.80)
        claims = [
            Claim(claim_id=1, claim_text="C1", sentence_index=1, support_level="UNSUPPORTED"),
        ]
        report = builder.build_report(
            question="Q?",
            answer_text="Ans",
            claims=claims,
            grounding_score=0.0,
            supported_claim_ratio=0.0,
            unsupported_claim_ratio=1.0,
            evidence_coverage=0.0,
            citation_coverage=0.0,
            config=config,
        )

        assert report.grounding_score == 0.0
        assert len(report.warnings) >= 3  # low score warning, high unsupported ratio warning, unsupported claim warning


class TestGroundingVerifier:
    """Test end-to-end GroundingVerifier integration service."""

    def test_verify_grounding_integration(
        self,
        sample_answer_response: AnswerResponse,
        sample_evidence_bundle: EvidenceBundle,
        sample_citation_bundle: CitationBundle,
    ) -> None:
        verifier = GroundingVerifier()
        report = verifier.verify_grounding(
            answer_response=sample_answer_response,
            evidence_bundle=sample_evidence_bundle,
            citation_bundle=sample_citation_bundle,
        )

        assert isinstance(report, GroundingReport)
        assert report.question == "What is a Hilbert space?"
        assert len(report.claims) > 0
        assert report.grounding_score >= 0.0

    def test_invalid_answer_response_type(self) -> None:
        verifier = GroundingVerifier()
        with pytest.raises(TypeError):
            verifier.verify_grounding("invalid_answer")  # type: ignore
