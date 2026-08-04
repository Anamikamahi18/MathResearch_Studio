"""Alignment engine for deterministically mapping answer sentences to retrieved chunks."""

from __future__ import annotations

import re
from typing import Sequence

from src.rag.evidence.models import EvidenceSpan
from src.rag.retrieval.models import RetrievalResult


class AlignmentEngine:
    """Deterministic rule-based alignment engine matching answer sentences against retrieved chunks."""

    @staticmethod
    def extract_sentences(text: str) -> list[str]:
        """Split text into distinct non-empty sentences, filtering out markdown headers.

        Args:
            text: Input string.

        Returns:
            List of sentence strings.
        """
        if not text:
            return []

        # Remove markdown section headers (e.g. ### Direct Answer)
        cleaned_text = re.sub(r"^#{1,6}\s+.*$", "", text, flags=re.MULTILINE)

        # Split on sentence boundary punctuation (. ! ?)
        raw_sentences = re.split(r"(?<=[.!?])\s+", cleaned_text)
        sentences: list[str] = []

        for s in raw_sentences:
            s_clean = s.strip()
            # Ignore empty lines or short list markers
            if s_clean and len(s_clean.split()) >= 3:
                sentences.append(s_clean)

        return sentences

    def _compute_overlap_score(self, sentence: str, chunk_text: str) -> float:
        """Compute term overlap score between a sentence and chunk text."""
        sent_words = set(re.findall(r"\w+", sentence.lower()))
        chunk_words = set(re.findall(r"\w+", chunk_text.lower()))

        # Filter out common stop words
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been", "being", "in", "on", "at", "to", "for", "of", "and", "or", "that", "this", "it", "with", "by", "as"}
        sent_terms = sent_words - stop_words
        chunk_terms = chunk_words - stop_words

        if not sent_terms:
            return 0.0

        intersection = sent_terms.intersection(chunk_terms)
        return len(intersection) / len(sent_terms)

    def align_sentence_to_chunks(
        self,
        sentence_index: int,
        sentence_text: str,
        chunks: Sequence[RetrievalResult],
    ) -> EvidenceSpan:
        """Find supporting chunks for a single sentence and classify support level.

        Args:
            sentence_index: Index of the sentence (1-based).
            sentence_text: Text of the sentence.
            chunks: Sequence of candidate RetrievalResult items.

        Returns:
            EvidenceSpan container.
        """
        if not chunks:
            return EvidenceSpan(
                sentence_index=sentence_index,
                sentence_text=sentence_text,
                supported_by_chunks=[],
                support_level="NONE",
                support_type="none",
                alignment_score=0.0,
            )

        best_score = 0.0
        best_chunk_id: str | None = None
        support_type = "none"
        supported_chunks: list[str] = []

        sent_lower = sentence_text.lower()

        for chunk in chunks:
            # 1. Compute term overlap score
            overlap_score = self._compute_overlap_score(sentence_text, chunk.text)
            curr_score = overlap_score
            curr_type = "token_overlap"

            # 2. Boost if matched entities are present in sentence
            for entity in chunk.matched_entities:
                if entity.lower() in sent_lower:
                    curr_score += 0.25
                    curr_type = "entity_match"
                    break

            # 3. Boost if section/statement match (e.g. "Definition 2.1" in sentence)
            if chunk.section_title and chunk.section_title.lower() in sent_lower:
                curr_score += 0.30
                curr_type = "statement_match"

            if curr_score > 0.08:
                supported_chunks.append(chunk.chunk_id)

            if curr_score > best_score:
                best_score = curr_score
                best_chunk_id = chunk.chunk_id
                support_type = curr_type

        best_score = round(min(1.0, best_score), 4)

        # 4. Classify support level
        if best_score >= 0.35:
            support_level = "DIRECT"
        elif best_score >= 0.20:
            support_level = "PARTIAL"
        elif best_score >= 0.08:
            support_level = "WEAK"
        else:
            support_level = "NONE"
            supported_chunks = []

        return EvidenceSpan(
            sentence_index=sentence_index,
            sentence_text=sentence_text,
            supported_by_chunks=supported_chunks,
            support_level=support_level,
            support_type=support_type if support_level != "NONE" else "none",
            alignment_score=best_score if support_level != "NONE" else 0.0,
        )

    def align_sentences_to_chunks(
        self,
        sentences: Sequence[str],
        chunks: Sequence[RetrievalResult],
    ) -> list[EvidenceSpan]:
        """Align all sentences against candidate chunks.

        Args:
            sentences: Sequence of sentence strings.
            chunks: Sequence of candidate RetrievalResult items.

        Returns:
            List of EvidenceSpan containers.
        """
        return [
            self.align_sentence_to_chunks(
                sentence_index=idx,
                sentence_text=sent,
                chunks=chunks,
            )
            for idx, sent in enumerate(sentences, start=1)
        ]
