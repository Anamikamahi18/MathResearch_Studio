"""Unit tests for Day 5 Step 4.5 Evidence Mapping Layer."""

from __future__ import annotations

import pytest

from src.rag.answer_generator.models import AnswerMetadata, AnswerResponse, AnswerSection
from src.rag.evidence import (
    AlignmentEngine,
    CoverageAnalyzer,
    EvidenceBundle,
    EvidenceMapper,
    EvidenceMetadata,
    EvidenceReference,
    EvidenceSpan,
)
from src.rag.retrieval.models import RetrievalResult


@pytest.fixture
def sample_retrieval_chunks() -> list[RetrievalResult]:
    """Fixture providing sample retrieved mathematical document chunks."""
    return [
        RetrievalResult(
            chunk_id="chunk_def_1",
            text="Definition 1. A Hilbert space is a complete inner product space.",
            paper_id="paper_1",
            paper_title="Hilbert Spaces",
            section_title="1. Definitions",
            section_type="definition",
            final_score=0.95,
            matched_entities=["Hilbert space", "Definition 1"],
        ),
        RetrievalResult(
            chunk_id="chunk_thm_1",
            text="Theorem 1. Every Hilbert space has an orthonormal basis.",
            paper_id="paper_1",
            paper_title="Hilbert Spaces",
            section_title="2. Bases",
            section_type="theorem",
            final_score=0.90,
            matched_entities=["Theorem 1"],
        ),
    ]


@pytest.fixture
def sample_answer_response() -> AnswerResponse:
    """Fixture providing sample generated AnswerResponse container."""
    meta = AnswerMetadata(query_text="What is a Hilbert space?", intent="definition", provider="mock", model="mock-model")
    sections = [
        AnswerSection(title="Direct Answer", content="Definition 1. A Hilbert space is a complete inner product space."),
        AnswerSection(title="Supporting Evidence", content="Theorem 1 proves every Hilbert space contains an orthonormal basis."),
    ]
    return AnswerResponse(
        question="What is a Hilbert space?",
        direct_answer="Definition 1. A Hilbert space is a complete inner product space.",
        formatted_answer="### Direct Answer\nDefinition 1. A Hilbert space is a complete inner product space.\n\n### Supporting Evidence\nTheorem 1 proves every Hilbert space contains an orthonormal basis.",
        sections=sections,
        metadata=meta,
    )


class TestEvidenceModels:
    """Test evidence data models and serialization."""

    def test_evidence_reference_to_dict(self) -> None:
        ref = EvidenceReference(
            chunk_id="c1",
            paper_id="p1",
            paper_title="Title",
            section_title="Sec 1",
            retrieval_rank=1,
            retrieval_score=0.95,
        )
        data = ref.to_dict()
        assert data["chunk_id"] == "c1"
        assert data["retrieval_score"] == 0.95

    def test_evidence_span_to_dict(self) -> None:
        span = EvidenceSpan(
            sentence_index=1,
            sentence_text="A Hilbert space is complete.",
            supported_by_chunks=["c1"],
            support_level="DIRECT",
            support_type="entity_match",
            alignment_score=0.85,
        )
        data = span.to_dict()
        assert data["support_level"] == "DIRECT"
        assert data["alignment_score"] == 0.85

    def test_evidence_bundle_to_dict(self) -> None:
        meta = EvidenceMetadata(average_alignment_score=0.8)
        bundle = EvidenceBundle(
            question="Query",
            answer_text="Answer",
            coverage_score=0.9,
            metadata=meta,
        )
        data = bundle.to_dict()
        assert data["question"] == "Query"
        assert data["coverage_score"] == 0.9
        assert data["metadata"]["average_alignment_score"] == 0.8


class TestAlignmentEngine:
    """Test sentence segmentation and support level classification."""

    def test_extract_sentences(self) -> None:
        engine = AlignmentEngine()
        text = "### Section\nDefinition 1 states H is complete. Theorem 1 proves existence of bases."
        sentences = engine.extract_sentences(text)

        assert len(sentences) == 2
        assert "Definition 1 states H is complete." in sentences[0]
        assert "Theorem 1 proves existence of bases." in sentences[1]

    def test_align_sentence_direct_support(self, sample_retrieval_chunks: list[RetrievalResult]) -> None:
        engine = AlignmentEngine()
        sentence = "Definition 1 states that a Hilbert space is a complete inner product space."
        span = engine.align_sentence_to_chunks(sentence_index=1, sentence_text=sentence, chunks=sample_retrieval_chunks)

        assert span.support_level == "DIRECT"
        assert "chunk_def_1" in span.supported_by_chunks
        assert span.alignment_score > 0.35

    def test_align_sentence_no_support(self, sample_retrieval_chunks: list[RetrievalResult]) -> None:
        engine = AlignmentEngine()
        sentence = "Unrelated sentence about quantum mechanics velocity parameters."
        span = engine.align_sentence_to_chunks(sentence_index=1, sentence_text=sentence, chunks=sample_retrieval_chunks)

        assert span.support_level == "NONE"
        assert len(span.supported_by_chunks) == 0


class TestCoverageAnalyzer:
    """Test coverage score and unused chunks analysis."""

    def test_analyze_coverage(self, sample_retrieval_chunks: list[RetrievalResult]) -> None:
        analyzer = CoverageAnalyzer()
        spans = [
            EvidenceSpan(sentence_index=1, sentence_text="Sent 1", supported_by_chunks=["chunk_def_1"], support_level="DIRECT"),
            EvidenceSpan(sentence_index=2, sentence_text="Sent 2", supported_by_chunks=[], support_level="NONE"),
        ]
        score, supp, total, unsup, unused = analyzer.analyze_coverage(spans=spans, chunks=sample_retrieval_chunks)

        assert score == 0.5
        assert supp == 1
        assert total == 2
        assert len(unsup) == 1
        assert "chunk_thm_1" in unused  # chunk_thm_1 was not mapped to any sentence


class TestEvidenceMapper:
    """Test EvidenceMapper service orchestration."""

    def test_map_evidence(
        self,
        sample_answer_response: AnswerResponse,
        sample_retrieval_chunks: list[RetrievalResult],
    ) -> None:
        mapper = EvidenceMapper()
        bundle = mapper.map_evidence(
            answer_response=sample_answer_response,
            retrieval_response=sample_retrieval_chunks,
        )

        assert isinstance(bundle, EvidenceBundle)
        assert bundle.question == "What is a Hilbert space?"
        assert len(bundle.references) == 2
        assert len(bundle.spans) > 0
        assert bundle.coverage_score > 0.0
        assert bundle.metadata.mapping_version == "v1.0"
        assert bundle.to_dict()["coverage_score"] > 0.0

    def test_invalid_answer_response_type(self) -> None:
        mapper = EvidenceMapper()
        with pytest.raises(TypeError):
            mapper.map_evidence("invalid_answer", [])  # type: ignore
