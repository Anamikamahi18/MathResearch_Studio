"""EvidenceMapper service implementation for mapping answer sentences to retrieved evidence."""

from __future__ import annotations

import logging
from typing import Sequence

from src.rag.answer_generator.models import AnswerResponse
from src.rag.evidence.alignment import AlignmentEngine
from src.rag.evidence.base import BaseEvidenceMapper
from src.rag.evidence.coverage import CoverageAnalyzer
from src.rag.evidence.models import (
    EvidenceBundle,
    EvidenceMetadata,
    EvidenceReference,
    EvidenceSpan,
)
from src.rag.retrieval.models import RetrievalResponse, RetrievalResult

logger = logging.getLogger(__name__)


class EvidenceMapper(BaseEvidenceMapper):
    """Main evidence mapping service associating generated answer text with retrieved evidence."""

    def __init__(
        self,
        alignment_engine: AlignmentEngine | None = None,
        coverage_analyzer: CoverageAnalyzer | None = None,
    ) -> None:
        """Initialize EvidenceMapper with sub-components.

        Args:
            alignment_engine: Optional AlignmentEngine instance.
            coverage_analyzer: Optional CoverageAnalyzer instance.
        """
        self.alignment_engine = alignment_engine or AlignmentEngine()
        self.coverage_analyzer = coverage_analyzer or CoverageAnalyzer()
        logger.info("Initialized EvidenceMapper service successfully")

    def map_evidence(
        self,
        answer_response: AnswerResponse,
        retrieval_response: RetrievalResponse | list[RetrievalResult],
    ) -> EvidenceBundle:
        """Map answer statements to supporting retrieved evidence chunks.

        Args:
            answer_response: Generated AnswerResponse container.
            retrieval_response: RetrievalResponse or list of candidate RetrievalResult items.

        Returns:
            EvidenceBundle containing references, spans, coverage, and metadata.

        Raises:
            TypeError: If answer_response is invalid.
        """
        if not isinstance(answer_response, AnswerResponse):
            raise TypeError(f"Expected AnswerResponse, got {type(answer_response).__name__}")

        # 1. Unpack candidate chunks
        if isinstance(retrieval_response, RetrievalResponse):
            chunks: Sequence[RetrievalResult] = retrieval_response.results
        elif isinstance(retrieval_response, (list, tuple)):
            chunks = retrieval_response
        else:
            chunks = []

        # 2. Build EvidenceReferences
        references: list[EvidenceReference] = [
            EvidenceReference(
                chunk_id=c.chunk_id,
                paper_id=c.paper_id,
                paper_title=c.paper_title,
                section_title=c.section_title or c.section_type,
                page_start=c.page_start,
                page_end=c.page_end,
                retrieval_rank=c.rank,
                retrieval_score=c.final_score,
            )
            for c in chunks
        ]

        # 3. Extract answer sentences from formatted_answer (or direct_answer)
        answer_text = answer_response.formatted_answer or answer_response.direct_answer or ""
        sentences = self.alignment_engine.extract_sentences(answer_text)

        # 4. Perform sentence alignment
        spans: list[EvidenceSpan] = self.alignment_engine.align_sentences_to_chunks(
            sentences=sentences,
            chunks=chunks,
        )

        # 5. Perform coverage analysis
        coverage_score, supported_count, total_count, unsupported_sents, unused_chunks = (
            self.coverage_analyzer.analyze_coverage(spans=spans, chunks=chunks)
        )

        # 6. Compute metadata counts
        direct_count = sum(1 for s in spans if s.support_level == "DIRECT")
        partial_count = sum(1 for s in spans if s.support_level == "PARTIAL")
        weak_count = sum(1 for s in spans if s.support_level == "WEAK")
        no_count = sum(1 for s in spans if s.support_level == "NONE")

        aligned_scores = [s.alignment_score for s in spans if s.alignment_score > 0]
        avg_alignment = round(sum(aligned_scores) / len(aligned_scores), 4) if aligned_scores else 0.0

        metadata = EvidenceMetadata(
            mapping_version="v1.0",
            average_alignment_score=avg_alignment,
            direct_support_count=direct_count,
            partial_support_count=partial_count,
            weak_support_count=weak_count,
            no_support_count=no_count,
        )

        question_str = answer_response.question or (
            answer_response.metadata.query_text if answer_response.metadata else "Question"
        )

        logger.info(
            "EvidenceMapper mapped %d sentences to %d chunks (Coverage: %.2f%%, Direct: %d, Partial: %d)",
            total_count,
            len(chunks),
            coverage_score * 100,
            direct_count,
            partial_count,
        )

        return EvidenceBundle(
            question=question_str,
            answer_text=answer_text,
            references=references,
            spans=spans,
            coverage_score=coverage_score,
            supported_sentence_count=supported_count,
            total_sentence_count=total_count,
            unsupported_sentences=unsupported_sents,
            unused_chunks=unused_chunks,
            metadata=metadata,
        )
