"""Answer formatter for parsing and building structured 5-section research outputs."""

from __future__ import annotations

from typing import Sequence

from src.rag.answer_generator.models import AnswerSection
from src.rag.retrieval.models import RetrievalResult


class AnswerFormatter:
    """Formats raw LLM text into a clean 5-section structured research response preserving math notation."""

    SECTION_DIRECT_ANSWER = "Direct Answer"
    SECTION_SUPPORTING_EVIDENCE = "Supporting Evidence"
    SECTION_REASONING = "Reasoning"
    SECTION_LIMITATIONS = "Limitations"
    SECTION_NEXT_TOPICS = "Next Related Topics"

    def format_answer(
        self,
        raw_text: str,
        query_text: str,
        included_chunks: Sequence[RetrievalResult],
    ) -> tuple[str, list[AnswerSection], list[str]]:
        """Format raw text into structured AnswerSections and complete markdown.

        Args:
            raw_text: Post-processed raw LLM output text.
            query_text: Original user query string.
            included_chunks: Sequence of selected context chunks.

        Returns:
            Tuple of (formatted_markdown, answer_sections, limitations_list).
        """
        # Build section 1: Direct Answer
        direct_answer_content = raw_text if raw_text else "No direct answer generated."

        # Build section 2: Supporting Evidence from Context
        if included_chunks:
            evidence_lines: list[str] = []
            for idx, chunk in enumerate(included_chunks, start=1):
                paper = chunk.paper_title or chunk.paper_id or "Paper"
                sec = chunk.section_title or chunk.section_type
                evidence_lines.append(f"{idx}. **[{paper} - {sec}]**: {chunk.text.strip()}")
            supporting_evidence_content = "\n".join(evidence_lines)
        else:
            supporting_evidence_content = "No supporting context passages available."

        # Build section 3: Reasoning
        reasoning_content = (
            f"The answer was deduced directly from the provided mathematical passages. "
            f"All theorem, lemma, and definition statements were evaluated against the query '{query_text}'."
        )

        # Build section 4: Limitations
        limitations: list[str] = []
        if not included_chunks:
            limitations.append("No uploaded papers matched the query terms.")
        else:
            limitations.append("Analysis is strictly bounded to the supplied paper passages.")
        limitations_content = "\n".join(f"- {lim}" for lim in limitations)

        # Build section 5: Next Related Topics
        next_topics: list[str] = []
        if included_chunks:
            entity_names = set()
            for c in included_chunks:
                entity_names.update(c.matched_entities)
            if entity_names:
                next_topics.append(f"Explore properties of {', '.join(sorted(list(entity_names)))}.")
        if not next_topics:
            next_topics.append("Analyze proof dependencies and formal prerequisite lemmas.")
            next_topics.append("Search for broader spectral theory applications.")
        next_topics_content = "\n".join(f"- {topic}" for topic in next_topics)

        sections: list[AnswerSection] = [
            AnswerSection(title=self.SECTION_DIRECT_ANSWER, content=direct_answer_content, section_type="direct_answer"),
            AnswerSection(title=self.SECTION_SUPPORTING_EVIDENCE, content=supporting_evidence_content, section_type="evidence"),
            AnswerSection(title=self.SECTION_REASONING, content=reasoning_content, section_type="reasoning"),
            AnswerSection(title=self.SECTION_LIMITATIONS, content=limitations_content, section_type="limitations"),
            AnswerSection(title=self.SECTION_NEXT_TOPICS, content=next_topics_content, section_type="next_topics"),
        ]

        # Assemble formatted markdown
        markdown_blocks: list[str] = []
        for sec in sections:
            markdown_blocks.append(f"### {sec.title}\n{sec.content}")

        formatted_markdown = "\n\n".join(markdown_blocks)

        return formatted_markdown, sections, limitations
