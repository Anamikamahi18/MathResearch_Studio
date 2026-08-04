"""GuardrailRules for evaluating policy constraints and refusal conditions."""

from __future__ import annotations

import logging
from typing import Sequence

from src.rag.answer_generator.models import AnswerResponse
from src.rag.citation_engine.models import CitationBundle
from src.rag.evidence.models import EvidenceBundle
from src.rag.grounding.models import GroundingReport
from src.rag.guardrails.config import GuardrailConfig
from src.rag.guardrails.models import DecisionType, GuardrailDecision, GuardrailStatus

logger = logging.getLogger(__name__)


class GuardrailRules:
    """Evaluates policy rules to determine the appropriate decision for an answer response."""

    def __init__(self, config: GuardrailConfig | None = None) -> None:
        """Initialize GuardrailRules with configuration.

        Args:
            config: Optional GuardrailConfig instance.
        """
        self.config = config or GuardrailConfig()

    def evaluate_rules(
        self,
        answer_response: AnswerResponse,
        evidence_bundle: EvidenceBundle | None = None,
        citation_bundle: CitationBundle | None = None,
        grounding_report: GroundingReport | None = None,
    ) -> tuple[GuardrailDecision, list[str], list[str]]:
        """Evaluate guardrail rules and return a decision, evaluated rules list, and decision trace.

        Args:
            answer_response: AnswerResponse container.
            evidence_bundle: Optional EvidenceBundle container.
            citation_bundle: Optional CitationBundle container.
            grounding_report: Optional GroundingReport container.

        Returns:
            Tuple of (GuardrailDecision, evaluated_rules, decision_path).
        """
        evaluated_rules: list[str] = []
        decision_path: list[str] = []
        warnings: list[str] = []
        violated_rules: list[str] = []

        g_score = grounding_report.grounding_score if grounding_report else 0.0
        cit_cov = grounding_report.citation_coverage if grounding_report else 0.0
        supp_ratio = grounding_report.supported_claim_ratio if grounding_report else 0.0

        # Collect warnings from upstream reports
        if grounding_report and grounding_report.warnings:
            warnings.extend(grounding_report.warnings[:5])
        if citation_bundle and citation_bundle.metadata.warnings:
            warnings.extend(citation_bundle.metadata.warnings[:3])

        # --------------------------------------------------
        # Rule 1: Unknown / Ambiguous Intent Check
        # --------------------------------------------------
        evaluated_rules.append("Rule_UnknownIntent")
        intent_str = str(answer_response.metadata.intent if answer_response.metadata else "").lower()
        if self.config.ask_clarification_on_unknown_intent and intent_str in ("unknown", "ambiguous"):
            decision_path.append("Triggered Rule_UnknownIntent -> Decision: ASK_FOR_CLARIFICATION")
            violated_rules.append("Rule_UnknownIntent")
            return (
                GuardrailDecision(
                    decision_type=DecisionType.ASK_FOR_CLARIFICATION,
                    status=GuardrailStatus.FAIL,
                    reason="Query intent is unknown or ambiguous. Please clarify the mathematical question.",
                    warnings=warnings,
                    violated_rules=violated_rules,
                    grounding_score=g_score,
                    citation_coverage=cit_cov,
                    supported_claim_ratio=supp_ratio,
                ),
                evaluated_rules,
                decision_path,
            )

        # --------------------------------------------------
        # Rule 2: Zero Evidence / Empty Context Check
        # --------------------------------------------------
        evaluated_rules.append("Rule_ZeroEvidence")
        no_references = (not evidence_bundle or len(evidence_bundle.references) == 0)
        if self.config.refuse_on_zero_evidence and no_references:
            decision_path.append("Triggered Rule_ZeroEvidence -> Decision: INSUFFICIENT_EVIDENCE")
            violated_rules.append("Rule_ZeroEvidence")
            return (
                GuardrailDecision(
                    decision_type=DecisionType.INSUFFICIENT_EVIDENCE,
                    status=GuardrailStatus.FAIL,
                    reason="No relevant mathematical evidence was retrieved to support an answer.",
                    warnings=warnings,
                    violated_rules=violated_rules,
                    grounding_score=g_score,
                    citation_coverage=cit_cov,
                    supported_claim_ratio=supp_ratio,
                ),
                evaluated_rules,
                decision_path,
            )

        # --------------------------------------------------
        # Rule 3: Severe Hallucination / Zero Grounding Check
        # --------------------------------------------------
        evaluated_rules.append("Rule_SevereHallucination")
        if grounding_report and g_score < 0.15 and supp_ratio < 0.10:
            decision_path.append("Triggered Rule_SevereHallucination -> Decision: REFUSE")
            violated_rules.append("Rule_SevereHallucination")
            return (
                GuardrailDecision(
                    decision_type=DecisionType.REFUSE,
                    status=GuardrailStatus.FAIL,
                    reason="Generated answer statements are unsupported by retrieved mathematical evidence.",
                    warnings=warnings,
                    violated_rules=violated_rules,
                    grounding_score=g_score,
                    citation_coverage=cit_cov,
                    supported_claim_ratio=supp_ratio,
                ),
                evaluated_rules,
                decision_path,
            )

        # --------------------------------------------------
        # Rule 4: Strict Mode Threshold Violation
        # --------------------------------------------------
        evaluated_rules.append("Rule_StrictModeGrounding")
        if self.config.strict_mode and g_score < self.config.minimum_grounding_score:
            decision_path.append("Triggered Rule_StrictModeGrounding -> Decision: REFUSE")
            violated_rules.append("Rule_StrictModeGrounding")
            return (
                GuardrailDecision(
                    decision_type=DecisionType.REFUSE,
                    status=GuardrailStatus.FAIL,
                    reason=f"Grounding score ({g_score:.2f}) violates strict threshold ({self.config.minimum_grounding_score:.2f}).",
                    warnings=warnings,
                    violated_rules=violated_rules,
                    grounding_score=g_score,
                    citation_coverage=cit_cov,
                    supported_claim_ratio=supp_ratio,
                ),
                evaluated_rules,
                decision_path,
            )

        # --------------------------------------------------
        # Rule 5: Partial Support / Warning Threshold Check
        # --------------------------------------------------
        evaluated_rules.append("Rule_WarningThreshold")
        has_low_score = g_score < self.config.warning_threshold
        has_low_cit = cit_cov < self.config.minimum_citation_coverage
        has_low_supp = supp_ratio < self.config.minimum_supported_ratio

        if has_low_score or has_low_cit or has_low_supp or len(warnings) > 0:
            decision_path.append("Triggered Rule_WarningThreshold -> Decision: RETURN_WITH_WARNING")
            if has_low_score:
                violated_rules.append("LowGroundingScore")
            if has_low_cit:
                violated_rules.append("LowCitationCoverage")
            if has_low_supp:
                violated_rules.append("LowSupportedClaimRatio")

            return (
                GuardrailDecision(
                    decision_type=DecisionType.RETURN_WITH_WARNING,
                    status=GuardrailStatus.WARNING,
                    reason="Answer returned with warnings regarding evidence coverage or citation density.",
                    warnings=warnings,
                    violated_rules=violated_rules,
                    grounding_score=g_score,
                    citation_coverage=cit_cov,
                    supported_claim_ratio=supp_ratio,
                ),
                evaluated_rules,
                decision_path,
            )

        # --------------------------------------------------
        # Rule 6: Clean High Confidence Pass
        # --------------------------------------------------
        evaluated_rules.append("Rule_CleanPass")
        decision_path.append("Passed all rule checks -> Decision: RETURN")
        return (
            GuardrailDecision(
                decision_type=DecisionType.RETURN,
                status=GuardrailStatus.PASS,
                reason="Answer is fully grounded, cited, and verified against mathematical evidence.",
                warnings=[],
                violated_rules=[],
                grounding_score=g_score,
                citation_coverage=cit_cov,
                supported_claim_ratio=supp_ratio,
            ),
            evaluated_rules,
            decision_path,
        )
