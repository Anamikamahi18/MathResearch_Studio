"""CitationEngine service implementation for generating structured citations and bibliographies."""

from __future__ import annotations

import logging

from src.rag.answer_generator.models import AnswerResponse
from src.rag.citation_engine.base import BaseCitationEngine
from src.rag.citation_engine.formatter import CitationFormatter
from src.rag.citation_engine.models import CitationBundle, CitationMetadata
from src.rag.citation_engine.renderer import CitationRenderer
from src.rag.citation_engine.styles import BUILTIN_STYLES, STYLE_INLINE, CitationStyle
from src.rag.citation_engine.validator import CitationValidator
from src.rag.evidence.models import EvidenceBundle

logger = logging.getLogger(__name__)


class CitationEngine(BaseCitationEngine):
    """Main citation service converting evidence mappings into researcher-friendly citations and bibliographies."""

    def __init__(
        self,
        formatter: CitationFormatter | None = None,
        validator: CitationValidator | None = None,
        renderer: CitationRenderer | None = None,
        default_style: CitationStyle | None = None,
    ) -> None:
        """Initialize CitationEngine with sub-components.

        Args:
            formatter: Optional CitationFormatter instance.
            validator: Optional CitationValidator instance.
            renderer: Optional CitationRenderer instance.
            default_style: Optional default CitationStyle.
        """
        self.default_style = default_style or STYLE_INLINE
        self.formatter = formatter or CitationFormatter(style=self.default_style)
        self.validator = validator or CitationValidator()
        self.renderer = renderer or CitationRenderer()
        logger.info("Initialized CitationEngine service successfully")

    def generate_citations(
        self,
        answer_response: AnswerResponse,
        evidence_bundle: EvidenceBundle,
        style: str = "inline",
    ) -> CitationBundle:
        """Generate citations and bibliography from answer text and evidence mappings.

        Args:
            answer_response: Generated AnswerResponse container.
            evidence_bundle: Mapped EvidenceBundle container.
            style: Citation style name ('inline', 'author_year', 'academic').

        Returns:
            CitationBundle containing annotated answer text, citations, and bibliography.

        Raises:
            TypeError: If inputs are invalid.
        """
        if not isinstance(answer_response, AnswerResponse):
            raise TypeError(f"Expected AnswerResponse, got {type(answer_response).__name__}")
        if not isinstance(evidence_bundle, EvidenceBundle):
            raise TypeError(f"Expected EvidenceBundle, got {type(evidence_bundle).__name__}")

        # 1. Resolve citation style
        selected_style = BUILTIN_STYLES.get(style.lower(), self.default_style)
        self.formatter.style = selected_style

        # 2. Build citations map from evidence references
        citations_map = self.formatter.build_citations(evidence_bundle.references)
        citations_list = list(citations_map.values())

        # 3. Format annotated answer text with inline markers
        annotated_answer = self.formatter.format_annotated_answer(
            spans=evidence_bundle.spans,
            citations_map=citations_map,
        )

        # 4. Generate bibliography
        bibliography = self.formatter.generate_bibliography(citations_map)

        # 5. Perform citation validation
        warnings = self.validator.validate_citations(
            citations=citations_list,
            evidence_bundle=evidence_bundle,
        )

        # 6. Compute metadata
        unique_papers = len({c.paper_id for c in citations_list if c.paper_id})
        metadata = CitationMetadata(
            citation_style=selected_style.style_type.value,
            total_citations=len(citations_list),
            unique_papers_cited=unique_papers,
            warnings=warnings,
        )

        question_str = evidence_bundle.question or answer_response.question

        logger.info(
            "CitationEngine generated %d citations across %d papers (Style: %s, Warnings: %d)",
            len(citations_list),
            unique_papers,
            selected_style.style_type.value,
            len(warnings),
        )

        return CitationBundle(
            question=question_str,
            answer_text=evidence_bundle.answer_text,
            answer_text_with_citations=annotated_answer,
            citations=citations_list,
            bibliography=bibliography,
            metadata=metadata,
        )
