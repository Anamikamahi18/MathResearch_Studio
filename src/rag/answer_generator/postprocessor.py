"""Post-processor for normalizing raw LLM generated text and removing duplicate blocks."""

from __future__ import annotations

import re


class AnswerPostProcessor:
    """Normalizes spacing, bullet list formatting, and removes duplicate paragraphs while preserving math equations."""

    def clean_and_normalize(self, raw_text: str) -> str:
        """Clean and normalize raw LLM text.

        Args:
            raw_text: Raw string returned by LLM adapter.

        Returns:
            Normalized markdown string.
        """
        if not raw_text:
            return ""

        # 1. Normalize carriage returns
        text = raw_text.replace("\r\n", "\n").replace("\r", "\n")

        # 2. Normalize bullet points (* -> -)
        text = re.sub(r"^[ \t]*[*•][ \t]+", "- ", text, flags=re.MULTILINE)

        # 3. Deduplicate consecutive identical lines/paragraphs
        lines = text.split("\n")
        cleaned_lines: list[str] = []
        for line in lines:
            stripped = line.strip()
            if cleaned_lines and stripped and cleaned_lines[-1].strip() == stripped:
                continue
            cleaned_lines.append(line)

        normalized = "\n".join(cleaned_lines)

        # 4. Normalize excessive newlines (max 2 consecutive newlines)
        normalized = re.sub(r"\n{3,}", "\n\n", normalized)

        return normalized.strip()
