"""Unit tests for Day 5 Step 6 Guardrails Layer."""

from __future__ import annotations

import pytest

from src.rag.answer_generator.models import AnswerMetadata, AnswerResponse, AnswerSection
from src.rag.citation_engine.models import Citation, CitationBundle, CitationMetadata
from src.rag.evidence.models import EvidenceBundle, EvidenceMetadata, EvidenceReference
from src.rag.grounding.models import GroundingReport
from src.rag.guardrails import (
    DecisionType,
    FinalResearchResponse,
    GuardrailConfig,
    GuardrailDecision,
    GuardrailDecisionEngine,
    GuardrailMetadata,
    GuardrailReport,
    GuardrailRules,
    GuardrailStatus,
    GuardrailValidator,
    ResponseBuilder,
)


@pytest.fixture
def sample_answer_response() -> AnswerResponse:
    """Fixture providing sample AnswerResponse."""
    meta = AnswerMetadata(query_text="What is Definition 2.1?", intent="definition", provider="mock", model="mock-model")
    sections = [
        AnswerSection(title="Direct Answer", content="Definition 2.1 states an operator is Hilbert-Schmidt."),
    ]
    return AnswerResponse(
        question="What is Definition 2.1?",
        direct_answer="Definition 2.1 states an operator is Hilbert-Schmidt.",
        formatted_answer="Definition 2.1 states an operator is Hilbert-Schmidt.",
        sections=sections,
        metadata=meta,
    )


@pytest.fixture
def sample_evidence_bundle() -> EvidenceBundle:
    """Fixture providing sample EvidenceBundle."""
    refs = [
        EvidenceReference(
            chunk_id="chunk_def_1",
            paper_id="paper_1",
            paper_title="Spectral Theory",
            section_title="2. Definitions",
            retrieval_rank=1,
            retrieval_score=0.95,
        ),
    ]
    return EvidenceBundle(
        question="What is Definition 2.1?",
        answer_text="Definition 2.1 states an operator is Hilbert-Schmidt.",
        references=refs,
    )


@pytest.fixture
def sample_citation_bundle() -> CitationBundle:
    """Fixture providing sample CitationBundle."""
    citations = [
        Citation(
            citation_id=1,
            chunk_id="chunk_def_1",
            paper_id="paper_1",
            paper_title="Spectral Theory",
            display_text="[1]",
        )
    ]
    return CitationBundle(
        question="What is Definition 2.1?",
        answer_text="Ans",
        answer_text_with_citations="Definition 2.1 states an operator is Hilbert-Schmidt [1].",
        citations=citations,
        bibliography=["[1] Ref"],
        metadata=CitationMetadata(total_citations=1, unique_papers_cited=1),
    )


@pytest.fixture
def sample_grounding_report() -> GroundingReport:
    """Fixture providing clean GroundingReport."""
    return GroundingReport(
        question="What is Definition 2.1?",
        answer_text="Ans",
        grounding_score=0.85,
        supported_claim_ratio=0.80,
        evidence_coverage=0.90,
        citation_coverage=0.90,
    )


class TestGuardrailModels:
    """Test guardrail data models and serialization."""

    def test_decision_to_dict(self) -> None:
        d = GuardrailDecision(
            decision_type=DecisionType.RETURN,
            status=GuardrailStatus.PASS,
            reason="Clean pass",
            grounding_score=0.90,
        )
        data = d.to_dict()
        assert data["decision_type"] == "RETURN"
        assert data["status"] == "PASS"
        assert data["grounding_score"] == 0.90

    def test_final_response_to_dict(self) -> None:
        resp = FinalResearchResponse(
            question="Q?",
            answer_text="Ans [1]",
            decision=DecisionType.RETURN,
            status=GuardrailStatus.PASS,
            reason="OK",
            citations=["[1]"],
            bibliography=["[1] Ref"],
        )
        data = resp.to_dict()
        assert data["question"] == "Q?"
        assert data["decision"] == "RETURN"
        assert len(data["citations"]) == 1


class TestGuardrailRules:
    """Test policy rule evaluations for different response decision outcomes."""

    def test_clean_pass_rule(
        self,
        sample_answer_response: AnswerResponse,
        sample_evidence_bundle: EvidenceBundle,
        sample_citation_bundle: CitationBundle,
        sample_grounding_report: GroundingReport,
    ) -> None:
        rules = GuardrailRules()
        decision, eval_rules, path = rules.evaluate_rules(
            answer_response=sample_answer_response,
            evidence_bundle=sample_evidence_bundle,
            citation_bundle=sample_citation_bundle,
            grounding_report=sample_grounding_report,
        )
        assert decision.decision_type == DecisionType.RETURN
        assert decision.status == GuardrailStatus.PASS
        assert "Rule_CleanPass" in eval_rules

    def test_zero_evidence_rule(self, sample_answer_response: AnswerResponse) -> None:
        rules = GuardrailRules()
        empty_bundle = EvidenceBundle(question="Q?", answer_text="", references=[])
        decision, _, _ = rules.evaluate_rules(
            answer_response=sample_answer_response,
            evidence_bundle=empty_bundle,
        )
        assert decision.decision_type == DecisionType.INSUFFICIENT_EVIDENCE
        assert decision.status == GuardrailStatus.FAIL

    def test_unknown_intent_rule(
        self,
        sample_evidence_bundle: EvidenceBundle,
    ) -> None:
        rules = GuardrailRules()
        meta = AnswerMetadata(query_text="???", intent="unknown", provider="mock", model="mock-model")
        ans_resp = AnswerResponse(
            question="???",
            direct_answer="Ans",
            formatted_answer="Ans",
            metadata=meta,
        )
        decision, _, _ = rules.evaluate_rules(
            answer_response=ans_resp,
            evidence_bundle=sample_evidence_bundle,
        )
        assert decision.decision_type == DecisionType.ASK_FOR_CLARIFICATION

    def test_severe_hallucination_rule(
        self,
        sample_answer_response: AnswerResponse,
        sample_evidence_bundle: EvidenceBundle,
    ) -> None:
        rules = GuardrailRules()
        bad_report = GroundingReport(
            question="Q?",
            answer_text="Fabricated text",
            grounding_score=0.05,
            supported_claim_ratio=0.05,
        )
        decision, _, _ = rules.evaluate_rules(
            answer_response=sample_answer_response,
            evidence_bundle=sample_evidence_bundle,
            grounding_report=bad_report,
        )
        assert decision.decision_type == DecisionType.REFUSE
        assert decision.status == GuardrailStatus.FAIL


class TestGuardrailValidator:
    """Test input type validation."""

    def test_validate_inputs_invalid_type(self) -> None:
        validator = GuardrailValidator()
        errors = validator.validate_inputs("invalid_answer")
        assert len(errors) > 0
        assert "Expected AnswerResponse" in errors[0]


class TestResponseBuilder:
    """Test response wrapping and exact text preservation."""

    def test_build_response_refuse(self, sample_answer_response: AnswerResponse) -> None:
        builder = ResponseBuilder()
        decision = GuardrailDecision(
            decision_type=DecisionType.REFUSE,
            status=GuardrailStatus.FAIL,
            reason="Grounding failed",
        )
        final_resp = builder.build_response(decision=decision, answer_response=sample_answer_response)
        assert "Request Refused" in final_resp.answer_text

    def test_build_response_clean(
        self,
        sample_answer_response: AnswerResponse,
        sample_citation_bundle: CitationBundle,
        sample_grounding_report: GroundingReport,
    ) -> None:
        builder = ResponseBuilder()
        decision = GuardrailDecision(
            decision_type=DecisionType.RETURN,
            status=GuardrailStatus.PASS,
            reason="Clean pass",
        )
        final_resp = builder.build_response(
            decision=decision,
            answer_response=sample_answer_response,
            citation_bundle=sample_citation_bundle,
            grounding_report=sample_grounding_report,
        )
        assert final_resp.decision == DecisionType.RETURN
        assert "Hilbert-Schmidt [1]" in final_resp.answer_text


class TestGuardrailDecisionEngine:
    """Test end-to-end GuardrailDecisionEngine integration."""

    def test_evaluate_guardrails_integration(
        self,
        sample_answer_response: AnswerResponse,
        sample_evidence_bundle: EvidenceBundle,
        sample_citation_bundle: CitationBundle,
        sample_grounding_report: GroundingReport,
    ) -> None:
        engine = GuardrailDecisionEngine()
        decision, report = engine.evaluate_guardrails(
            answer_response=sample_answer_response,
            evidence_bundle=sample_evidence_bundle,
            citation_bundle=sample_citation_bundle,
            grounding_report=sample_grounding_report,
        )
        assert decision.decision_type == DecisionType.RETURN
        assert report.metadata.rules_evaluated_count > 0

    def test_process_and_build_response(
        self,
        sample_answer_response: AnswerResponse,
        sample_evidence_bundle: EvidenceBundle,
        sample_citation_bundle: CitationBundle,
        sample_grounding_report: GroundingReport,
    ) -> None:
        engine = GuardrailDecisionEngine()
        final_resp = engine.process_and_build_response(
            answer_response=sample_answer_response,
            evidence_bundle=sample_evidence_bundle,
            citation_bundle=sample_citation_bundle,
            grounding_report=sample_grounding_report,
        )
        assert isinstance(final_resp, FinalResearchResponse)
        assert final_resp.decision == DecisionType.RETURN
