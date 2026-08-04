"""Unit tests for Day 5 Step 3 Prompt Builder."""

from __future__ import annotations

import pytest

from src.rag.prompt_builder import (
    ContextSelector,
    PromptBuilder,
    PromptContext,
    PromptFormatter,
    PromptMetadata,
    PromptRequest,
    PromptResponse,
    PromptTemplate,
    TemplateRegistry,
    TokenManager,
)
from src.rag.query_processing.models import QueryAnalysis, QueryIntent
from src.rag.retrieval.models import RetrievalExplanation, RetrievalResponse, RetrievalResult


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
            semantic_score=0.9,
            final_score=0.95,
            explanation=RetrievalExplanation(semantic_score=0.9, final_score=0.95),
        ),
        RetrievalResult(
            chunk_id="chunk_thm_1",
            text="Theorem 1. Every Hilbert space has an orthonormal basis.",
            paper_id="paper_1",
            paper_title="Hilbert Spaces",
            section_title="2. Bases",
            section_type="theorem",
            semantic_score=0.85,
            final_score=0.90,
            explanation=RetrievalExplanation(semantic_score=0.85, final_score=0.90),
        ),
        RetrievalResult(
            chunk_id="chunk_lem_1",
            text="Lemma 1. Bessel's inequality holds for any orthonormal set.",
            paper_id="paper_1",
            paper_title="Hilbert Spaces",
            section_title="2. Bases",
            section_type="lemma",
            semantic_score=0.80,
            final_score=0.85,
            explanation=RetrievalExplanation(semantic_score=0.80, final_score=0.85),
        ),
    ]


class TestTokenManager:
    """Test token length estimation and token budget filtering."""

    def test_token_estimation(self) -> None:
        tm = TokenManager(chars_per_token=4.0)
        assert tm.estimate_tokens("") == 0
        tokens = tm.estimate_tokens("Definition 1. A Hilbert space is a complete inner product space.")
        assert tokens > 0

    def test_chunk_token_filtering(self, sample_retrieval_chunks: list[RetrievalResult]) -> None:
        tm = TokenManager()
        # Generous limit fits all chunks
        included, excluded, used = tm.filter_chunks_by_token_limit(sample_retrieval_chunks, max_tokens=1000)
        assert len(included) == 3
        assert len(excluded) == 0
        assert used > 0

        # Strict limit fits only top chunk
        included_strict, excluded_strict, used_strict = tm.filter_chunks_by_token_limit(
            sample_retrieval_chunks, max_tokens=60
        )
        assert len(included_strict) == 1
        assert included_strict[0].chunk_id == "chunk_def_1"
        assert len(excluded_strict) == 2


class TestContextSelector:
    """Test chunk deduplication, score prioritization, and selection."""

    def test_context_selection_and_deduplication(self, sample_retrieval_chunks: list[RetrievalResult]) -> None:
        selector = ContextSelector()
        # Add duplicate chunk
        duplicate_chunk = RetrievalResult(
            chunk_id="chunk_def_1",  # Same chunk ID
            text="Definition 1. A Hilbert space is a complete inner product space.",
            final_score=0.95,
        )
        candidates = sample_retrieval_chunks + [duplicate_chunk]
        context = selector.select_context("What is a Hilbert space?", candidates, max_context_tokens=1000)

        assert len(context.included_chunks) == 3
        assert context.coverage_score == 1.0
        assert context.query_text == "What is a Hilbert space?"

    def test_empty_candidates(self) -> None:
        selector = ContextSelector()
        context = selector.select_context("Query", [])
        assert len(context.included_chunks) == 0
        assert context.coverage_score == 0.0


class TestTemplateRegistry:
    """Test prompt template retrieval and registration."""

    def test_default_templates(self) -> None:
        registry = TemplateRegistry()
        default_tpl = registry.get_template("default")
        assert default_tpl.template_name == "default"
        assert "ONLY using the supplied" in "".join(default_tpl.research_rules)

        def_tpl = registry.get_template("definition")
        assert def_tpl.template_name == "definition"

    def test_custom_template_registration(self) -> None:
        registry = TemplateRegistry()
        custom_tpl = PromptTemplate(
            template_name="custom_math",
            system_prompt="Custom System Prompt",
            research_rules=["Rule 1"],
            user_prompt_template="{query}",
        )
        registry.register_template(custom_tpl)
        fetched = registry.get_template("custom_math")
        assert fetched.template_name == "custom_math"
        assert fetched.system_prompt == "Custom System Prompt"


class TestPromptFormatter:
    """Test prompt formatting and section construction."""

    def test_format_context_block(self, sample_retrieval_chunks: list[RetrievalResult]) -> None:
        block = PromptFormatter.format_context_block(sample_retrieval_chunks[:1])
        assert "Passage 1" in block
        assert "Hilbert Spaces" in block
        assert "Definition 1" in block

    def test_format_full_prompt(self, sample_retrieval_chunks: list[RetrievalResult]) -> None:
        registry = TemplateRegistry()
        template = registry.get_template("default")
        context = PromptContext(
            query_text="What is Theorem 1?",
            included_chunks=sample_retrieval_chunks,
            excluded_chunks=[],
            total_context_tokens=150,
            coverage_score=1.0,
        )

        sys_str, user_str, full_str = PromptFormatter.format_full_prompt(
            query_text="What is Theorem 1?",
            context=context,
            template=template,
        )

        assert "SYSTEM INSTRUCTIONS" in full_str
        assert "RETRIEVED MATHEMATICAL CONTEXT" in full_str
        assert "What is Theorem 1?" in user_str


class TestPromptBuilder:
    """Test PromptBuilder orchestrator service."""

    def test_build_prompt_with_query_analysis(self, sample_retrieval_chunks: list[RetrievalResult]) -> None:
        builder = PromptBuilder()
        analysis = QueryAnalysis(
            original_query="What is Definition 1?",
            normalized_query="What is Definition 1?",
            intent=QueryIntent.DEFINITION,
        )
        retrieval_response = RetrievalResponse(
            query_analysis=analysis,
            results=sample_retrieval_chunks,
        )
        request = PromptRequest(query=analysis, retrieval_response=retrieval_response)
        response = builder.build_prompt(request)

        assert isinstance(response, PromptResponse)
        assert response.metadata is not None
        assert response.metadata.intent == "definition"
        assert response.metadata.template_name == "definition"
        assert len(response.included_chunks) > 0

    def test_build_prompt_with_raw_query(self, sample_retrieval_chunks: list[RetrievalResult]) -> None:
        builder = PromptBuilder()
        request = PromptRequest(
            query="Summarize paper",
            retrieval_response=sample_retrieval_chunks,
            template_name="summary",
        )
        response = builder.build_prompt(request)

        assert response.metadata.template_name == "summary"
        assert response.metadata.query_text == "Summarize paper"
        assert response.to_dict()["prompt_version"] == "v1.0"

    def test_invalid_request_type(self) -> None:
        builder = PromptBuilder()
        with pytest.raises(TypeError):
            builder.build_prompt("invalid_request")  # type: ignore

    def test_invalid_max_tokens(self, sample_retrieval_chunks: list[RetrievalResult]) -> None:
        builder = PromptBuilder()
        request = PromptRequest(
            query="Query",
            retrieval_response=sample_retrieval_chunks,
            max_prompt_tokens=-10,
        )
        with pytest.raises(ValueError):
            builder.build_prompt(request)
