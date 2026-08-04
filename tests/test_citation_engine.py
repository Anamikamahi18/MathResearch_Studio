"""Unit tests for Day 5 Step 5 Citation Engine Layer."""

from __future__ import annotations

import pytest

from src.rag.answer_generator.models import AnswerMetadata, AnswerResponse, AnswerSection
from src.rag.citation_engine import (
    BUILTIN_STYLES,
    STYLE_ACADEMIC,
    STYLE_AUTHOR_YEAR,
    STYLE_INLINE,
    Citation,
    CitationBundle,
    CitationEngine,
    CitationFormatter,
    CitationMetadata,
    CitationReference,
    CitationRenderer,
    CitationStyle,
    CitationStyleType,
    CitationValidator,
)
from src.rag.evidence.models import EvidenceBundle, EvidenceMetadata, EvidenceReference, EvidenceSpan


@pytest.fixture
def sample_evidence_bundle() -> EvidenceBundle:
    """Fixture providing sample EvidenceBundle."""
    refs = [
        EvidenceReference(
            chunk_id="chunk_def_1",
            paper_id="paper_1",
            paper_title="Hilbert Spaces and Operators",
            section_title="1. Definitions",
            page_start=1,
            page_end=2,
            retrieval_rank=1,
            retrieval_score=0.95,
        ),
        EvidenceReference(
            chunk_id="chunk_thm_1",
            paper_id="paper_1",
            paper_title="Hilbert Spaces and Operators",
            section_title="2. Main Theorems",
            page_start=3,
            page_end=4,
            retrieval_rank=2,
            retrieval_score=0.89,
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
            sentence_text="Theorem 1 proves every Hilbert space has an orthonormal basis.",
            supported_by_chunks=["chunk_thm_1"],
            support_level="DIRECT",
            alignment_score=0.82,
        ),
    ]
    return EvidenceBundle(
        question="What is a Hilbert space?",
        answer_text="Definition 1 states a Hilbert space is a complete inner product space.\n\nTheorem 1 proves every Hilbert space has an orthonormal basis.",
        references=refs,
        spans=spans,
        coverage_score=1.0,
        supported_sentence_count=2,
        total_sentence_count=2,
        metadata=EvidenceMetadata(mapping_version="v1.0", direct_support_count=2),
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


class TestCitationModels:
    """Test citation models and serialization."""

    def test_citation_to_dict(self) -> None:
        c = Citation(
            citation_id=1,
            chunk_id="c1",
            paper_id="p1",
            paper_title="Paper Title",
            display_text="[1]",
        )
        data = c.to_dict()
        assert data["citation_id"] == 1
        assert data["chunk_id"] == "c1"
        assert data["display_text"] == "[1]"

    def test_citation_bundle_to_dict(self) -> None:
        bundle = CitationBundle(
            question="Q?",
            answer_text="Ans",
            answer_text_with_citations="Ans [1]",
            bibliography=["[1] Ref"],
        )
        data = bundle.to_dict()
        assert data["question"] == "Q?"
        assert data["answer_text_with_citations"] == "Ans [1]"
        assert len(data["bibliography"]) == 1


class TestCitationStyles:
    """Test citation style configurations."""

    def test_builtin_styles(self) -> None:
        assert "inline" in BUILTIN_STYLES
        assert "author_year" in BUILTIN_STYLES
        assert "academic" in BUILTIN_STYLES
        assert BUILTIN_STYLES["inline"].style_type == CitationStyleType.INLINE


class TestCitationFormatter:
    """Test inline marker formatting and bibliography generation."""

    def test_build_citations_and_annotated_answer(self, sample_evidence_bundle: EvidenceBundle) -> None:
        formatter = CitationFormatter(style=STYLE_INLINE)
        citations_map = formatter.build_citations(sample_evidence_bundle.references)

        assert len(citations_map) == 2
        assert "chunk_def_1" in citations_map
        assert citations_map["chunk_def_1"].citation_id == 1

        annotated = formatter.format_annotated_answer(
            spans=sample_evidence_bundle.spans,
            citations_map=citations_map,
        )
        assert "[1]" in annotated
        assert "[2]" in annotated

    def test_generate_bibliography(self, sample_evidence_bundle: EvidenceBundle) -> None:
        formatter = CitationFormatter(style=STYLE_INLINE)
        citations_map = formatter.build_citations(sample_evidence_bundle.references)
        bib = formatter.generate_bibliography(citations_map)

        assert len(bib) == 2
        assert "[1]" in bib[0]
        assert "Hilbert Spaces and Operators" in bib[0]


class TestCitationValidator:
    """Test citation integrity and validation warnings."""

    def test_validate_citations_clean(self, sample_evidence_bundle: EvidenceBundle) -> None:
        formatter = CitationFormatter(style=STYLE_INLINE)
        validator = CitationValidator()

        citations_map = formatter.build_citations(sample_evidence_bundle.references)
        citations_list = list(citations_map.values())

        warnings = validator.validate_citations(
            citations=citations_list,
            evidence_bundle=sample_evidence_bundle,
        )
        assert len(warnings) == 0

    def test_validate_citations_warnings(self, sample_evidence_bundle: EvidenceBundle) -> None:
        validator = CitationValidator()
        invalid_citation = Citation(
            citation_id=1,
            chunk_id="chunk_def_1",
            paper_id="",
            paper_title="Untitled Paper",
            page_start=0,
            page_end=-1,
        )
        warnings = validator.validate_citations(
            citations=[invalid_citation],
            evidence_bundle=sample_evidence_bundle,
        )
        assert len(warnings) >= 3  # generic paper id, untitled paper, invalid page_start, invalid page range


class TestCitationRenderer:
    """Test Markdown and hover metadata rendering."""

    def test_render_markdown_and_hover(self, sample_evidence_bundle: EvidenceBundle) -> None:
        formatter = CitationFormatter(style=STYLE_INLINE)
        renderer = CitationRenderer()

        citations_map = formatter.build_citations(sample_evidence_bundle.references)
        citations_list = list(citations_map.values())
        bib = formatter.generate_bibliography(citations_map)

        bundle = CitationBundle(
            question="What is a Hilbert space?",
            answer_text="Ans",
            answer_text_with_citations="Ans [1]",
            citations=citations_list,
            bibliography=bib,
        )

        md = renderer.render_markdown(bundle)
        assert "# Answer: What is a Hilbert space?" in md
        assert "## References" in md
        assert "<!-- citation:1" in md


class TestCitationEngine:
    """Test end-to-end CitationEngine integration service."""

    def test_generate_citations_integration(
        self,
        sample_answer_response: AnswerResponse,
        sample_evidence_bundle: EvidenceBundle,
    ) -> None:
        engine = CitationEngine()
        bundle = engine.generate_citations(
            answer_response=sample_answer_response,
            evidence_bundle=sample_evidence_bundle,
            style="academic",
        )

        assert isinstance(bundle, CitationBundle)
        assert bundle.question == "What is a Hilbert space?"
        assert len(bundle.citations) == 2
        assert bundle.metadata.citation_style == "academic"
        assert bundle.metadata.unique_papers_cited == 1
        assert len(bundle.bibliography) == 2

    def test_invalid_input_types(self) -> None:
        engine = CitationEngine()
        with pytest.raises(TypeError):
            engine.generate_citations("invalid_answer", [])  # type: ignore
