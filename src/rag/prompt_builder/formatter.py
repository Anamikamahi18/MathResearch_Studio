"""Prompt formatter for constructing structured section-based LLM prompts."""

from __future__ import annotations

from typing import Sequence

from src.rag.prompt_builder.models import PromptContext, PromptTemplate
from src.rag.retrieval.models import RetrievalResult


class PromptFormatter:
    """Formats system instructions, retrieved context, question, and expected output sections into a clean prompt string."""

    @staticmethod
    def format_context_block(included_chunks: Sequence[RetrievalResult], separator: str = "---") -> str:
        """Format included retrieved chunks into a structured context block.

        Args:
            included_chunks: Sequence of selected RetrievalResult items.
            separator: Section separator string.

        Returns:
            Formatted context string.
        """
        if not included_chunks:
            return "No relevant mathematical context found."

        blocks: list[str] = []
        for idx, chunk in enumerate(included_chunks, start=1):
            paper_info = chunk.paper_title or chunk.paper_id or "Unknown Paper"
            section_info = chunk.section_title or chunk.section_type
            header = f"[Passage {idx} | Paper: {paper_info} | Section: {section_info} | Chunk ID: {chunk.chunk_id} | Final Score: {chunk.final_score:.4f}]"
            blocks.append(f"{header}\n{chunk.text.strip()}")

        return f"\n\n{separator}\n\n".join(blocks)

    @classmethod
    def format_full_prompt(
        self,
        query_text: str,
        context: PromptContext,
        template: PromptTemplate,
    ) -> tuple[str, str, str]:
        """Build structured system prompt, user prompt, and full combined prompt string.

        Args:
            query_text: User question string.
            context: PromptContext container with selected chunks.
            template: PromptTemplate instance.

        Returns:
            Tuple of (system_prompt_str, user_prompt_str, full_prompt_str).
        """
        # Section 1: System Instructions & Research Rules
        system_prompt_str = template.system_prompt.strip()

        # Section 2: Formatted Retrieved Context Block
        context_block = self.format_context_block(
            included_chunks=context.included_chunks,
            separator=template.context_separator,
        )

        # Section 3 & 4: User Question & Expected Output Format
        user_body = template.user_prompt_template.format(query=query_text.strip())

        output_format_instructions = (
            "Expected Output Format:\n"
            "1. State the direct answer clearly.\n"
            "2. Provide step-by-step mathematical reasoning using ONLY the supplied context.\n"
            "3. If context is missing critical steps or definitions, explicitly state the limitation."
        )

        user_prompt_str = (
            f"RETRIEVED MATHEMATICAL CONTEXT:\n"
            f"{template.context_separator}\n"
            f"{context_block}\n"
            f"{template.context_separator}\n\n"
            f"{user_body}\n\n"
            f"{output_format_instructions}"
        )

        full_prompt_str = f"=== SYSTEM INSTRUCTIONS ===\n{system_prompt_str}\n\n=== USER REQUEST & CONTEXT ===\n{user_prompt_str}"

        return system_prompt_str, user_prompt_str, full_prompt_str
