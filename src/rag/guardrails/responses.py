"""ResponseBuilder for constructing FinalResearchResponse objects."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from src.rag.answer_generator.models import AnswerResponse
from src.rag.citation_engine.models import CitationBundle
from src.rag.grounding.models import GroundingReport
from src.rag.guardrails.models import DecisionType, GuardrailDecision, GuardrailStatus

logger = logging.getLogger(__name__)


@dataclass
class FinalResearchResponse:
    """Final output response returned to the researcher after passing through Guardrails."""

    question: str
    answer_text: str
    decision: DecisionType
    status: GuardrailStatus
    reason: str
    citations: list[str] = field(default_factory=list)
    bibliography: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    grounding_summary: dict[str, float] = field(default_factory=dict)
    confidence: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert FinalResearchResponse to dictionary representation."""
        return {
            "question": self.question,
            "answer_text": self.answer_text,
            "decision": self.decision.value,
            "status": self.status.value,
            "reason": self.reason,
            "citations": self.citations,
            "bibliography": self.bibliography,
            "warnings": self.warnings,
            "grounding_summary": self.grounding_summary,
            "confidence": self.confidence,
            "metadata": self.metadata,
        }


class ResponseBuilder:
    """Assembles FinalResearchResponse combining decision, answer text, citations, and grounding summary."""

    def build_response(
        self,
        decision: GuardrailDecision,
        answer_response: AnswerResponse,
        citation_bundle: CitationBundle | None = None,
        grounding_report: GroundingReport | None = None,
    ) -> FinalResearchResponse:
        """Construct FinalResearchResponse based on guardrail decision outcome.

        Args:
            decision: Evaluated GuardrailDecision.
            answer_response: Raw AnswerResponse container.
            citation_bundle: Optional CitationBundle container.
            grounding_report: Optional GroundingReport container.

        Returns:
            FinalResearchResponse instance.
        """
        question_str = (
            citation_bundle.question
            if citation_bundle
            else (answer_response.question or "Question")
        )

        # Determine output answer text based on decision policy
        if decision.decision_type == DecisionType.REFUSE:
            output_text = f"🛑 **Request Refused**: {decision.reason}"
        elif decision.decision_type == DecisionType.INSUFFICIENT_EVIDENCE:
            output_text = f"⚠️ **Insufficient Evidence**: {decision.reason}"
        elif decision.decision_type == DecisionType.ASK_FOR_CLARIFICATION:
            output_text = f"❓ **Clarification Required**: {decision.reason}"
        elif citation_bundle and citation_bundle.answer_text_with_citations:
            output_text = citation_bundle.answer_text_with_citations
        else:
            output_text = answer_response.formatted_answer or answer_response.direct_answer or ""

        # Extract bibliography and citations
        bib_entries = citation_bundle.bibliography if citation_bundle else []
        cit_markers = [c.display_text for c in citation_bundle.citations] if citation_bundle else []

        grounding_summary = {
            "grounding_score": grounding_report.grounding_score if grounding_report else 0.0,
            "supported_claim_ratio": grounding_report.supported_claim_ratio if grounding_report else 0.0,
            "evidence_coverage": grounding_report.evidence_coverage if grounding_report else 0.0,
            "citation_coverage": grounding_report.citation_coverage if grounding_report else 0.0,
        }

        metadata = {
            "query_text": answer_response.metadata.query_text if answer_response.metadata else "",
            "intent": str(answer_response.metadata.intent if answer_response.metadata else ""),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

        return FinalResearchResponse(
            question=question_str,
            answer_text=output_text,
            decision=decision.decision_type,
            status=decision.status,
            reason=decision.reason,
            citations=cit_markers,
            bibliography=bib_entries,
            warnings=decision.warnings,
            grounding_summary=grounding_summary,
            confidence=answer_response.metadata.confidence_score if answer_response.metadata else 0.90,
            metadata=metadata,
        )
