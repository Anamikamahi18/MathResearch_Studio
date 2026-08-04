"""GuardrailDecisionEngine service implementation for evaluating guardrail policy decisions."""

from __future__ import annotations

import logging
import time

from src.rag.answer_generator.models import AnswerResponse
from src.rag.citation_engine.models import CitationBundle
from src.rag.evidence.models import EvidenceBundle
from src.rag.grounding.models import GroundingReport
from src.rag.guardrails.base import BaseGuardrailEngine
from src.rag.guardrails.config import GuardrailConfig
from src.rag.guardrails.models import GuardrailDecision, GuardrailReport as FullGuardrailReport
from src.rag.guardrails.report import GuardrailReportBuilder
from src.rag.guardrails.responses import FinalResearchResponse, ResponseBuilder
from src.rag.guardrails.rules import GuardrailRules
from src.rag.guardrails.validator import GuardrailValidator

logger = logging.getLogger(__name__)


class GuardrailDecisionEngine(BaseGuardrailEngine):
    """Main guardrail decision service evaluating policy constraints over upstream RAG layer outputs."""

    def __init__(
        self,
        rules: GuardrailRules | None = None,
        validator: GuardrailValidator | None = None,
        response_builder: ResponseBuilder | None = None,
        report_builder: GuardrailReportBuilder | None = None,
        config: GuardrailConfig | None = None,
    ) -> None:
        """Initialize GuardrailDecisionEngine with sub-components.

        Args:
            rules: Optional GuardrailRules instance.
            validator: Optional GuardrailValidator instance.
            response_builder: Optional ResponseBuilder instance.
            report_builder: Optional GuardrailReportBuilder instance.
            config: Optional GuardrailConfig instance.
        """
        self.config = config or GuardrailConfig()
        self.rules = rules or GuardrailRules(config=self.config)
        self.validator = validator or GuardrailValidator()
        self.response_builder = response_builder or ResponseBuilder()
        self.report_builder = report_builder or GuardrailReportBuilder()
        logger.info("Initialized GuardrailDecisionEngine service successfully")

    def evaluate_guardrails(
        self,
        answer_response: AnswerResponse,
        evidence_bundle: EvidenceBundle | None = None,
        citation_bundle: CitationBundle | None = None,
        grounding_report: GroundingReport | None = None,
    ) -> tuple[GuardrailDecision, FullGuardrailReport]:
        """Evaluate guardrail rules over upstream outputs and produce a policy decision.

        Args:
            answer_response: AnswerResponse container.
            evidence_bundle: Optional EvidenceBundle container.
            citation_bundle: Optional CitationBundle container.
            grounding_report: Optional GroundingReport container.

        Returns:
            Tuple of (GuardrailDecision, FullGuardrailReport).

        Raises:
            TypeError: If input payload types are invalid.
        """
        errors = self.validator.validate_inputs(
            answer_response=answer_response,
            evidence_bundle=evidence_bundle,
            citation_bundle=citation_bundle,
            grounding_report=grounding_report,
        )
        if errors:
            raise TypeError(f"Guardrail input validation failed: {'; '.join(errors)}")

        start_time = time.perf_counter()

        # 1. Evaluate rules
        decision, eval_rules, decision_path = self.rules.evaluate_rules(
            answer_response=answer_response,
            evidence_bundle=evidence_bundle,
            citation_bundle=citation_bundle,
            grounding_report=grounding_report,
        )

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

        # 2. Build report
        question_str = (
            citation_bundle.question
            if citation_bundle
            else (answer_response.question or "Question")
        )

        report = self.report_builder.build_report(
            question=question_str,
            decision=decision,
            evaluated_rules=eval_rules,
            decision_path=decision_path,
            strict_mode=self.config.strict_mode,
            execution_time_ms=elapsed_ms,
        )

        logger.info(
            "GuardrailDecisionEngine evaluated '%s' -> Decision: %s (Status: %s, Violations: %d)",
            question_str,
            decision.decision_type.value,
            decision.status.value,
            len(decision.violated_rules),
        )

        return decision, report

    def process_and_build_response(
        self,
        answer_response: AnswerResponse,
        evidence_bundle: EvidenceBundle | None = None,
        citation_bundle: CitationBundle | None = None,
        grounding_report: GroundingReport | None = None,
    ) -> FinalResearchResponse:
        """Convenience method to evaluate guardrails and return a FinalResearchResponse.

        Args:
            answer_response: AnswerResponse container.
            evidence_bundle: Optional EvidenceBundle container.
            citation_bundle: Optional CitationBundle container.
            grounding_report: Optional GroundingReport container.

        Returns:
            FinalResearchResponse object.
        """
        decision, _ = self.evaluate_guardrails(
            answer_response=answer_response,
            evidence_bundle=evidence_bundle,
            citation_bundle=citation_bundle,
            grounding_report=grounding_report,
        )

        return self.response_builder.build_response(
            decision=decision,
            answer_response=answer_response,
            citation_bundle=citation_bundle,
            grounding_report=grounding_report,
        )
