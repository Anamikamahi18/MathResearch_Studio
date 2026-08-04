"""ClaimExtractor for extracting distinct sentence claims from mathematical answer text."""

from __future__ import annotations

import logging
import re
from typing import Sequence

logger = logging.getLogger(__name__)


class ClaimExtractor:
    """Extracts distinct mathematical sentence claims from answer text without using an LLM."""

    PREAMBLE_PATTERN = re.compile(r"^(\[Mock LLM Response\]|Based on the supplied|Note: Generated via|Context Analysis:)")

    def extract_claims(self, answer_text: str) -> list[str]:
        """Extract valid sentence claim strings from answer text.

        Args:
            answer_text: Raw or formatted answer text string.

        Returns:
            List of sentence claim strings.
        """
        if not answer_text or not answer_text.strip():
            return []

        raw_lines = [line.strip() for line in answer_text.split("\n") if line.strip()]
        candidate_lines: list[str] = []

        for line in raw_lines:
            # Skip markdown headers and preambles
            if line.startswith("### ") or line.startswith("## ") or line.startswith("# "):
                continue

            if self.PREAMBLE_PATTERN.search(line):
                continue

            candidate_lines.append(line)

        sentence_claims: list[str] = []
        for line in candidate_lines:
            # Split into sentences
            parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\u0370-\u03ff\*\\])", line)
            for p in parts:
                clean_p = p.strip()
                if len(clean_p) > 5 and not clean_p.startswith(":") and not self.PREAMBLE_PATTERN.search(clean_p):
                    sentence_claims.append(clean_p)

        logger.info("ClaimExtractor extracted %d sentence claims", len(sentence_claims))
        return sentence_claims
