"""Extraction engine for mathematical symbols and LaTeX equations in user queries."""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)


class MathematicalSymbolExtractor:
    """Extracts mathematical symbols, variables, Unicode math operators, and LaTeX equations."""

    # Unicode math symbols & Greek letters
    _UNICODE_GREEK = r"[\u0370-\u03FF\u1F00-\u1FFF]"
    _UNICODE_MATH_OPS = r"[\u2200-\u22FF\u2100-\u214F\u2A00-\u2AFF]"
    _BLACKBOARD_BOLD = r"[ℝℤℕℂℚ]"

    def __init__(self) -> None:
        """Initialize symbol extractor."""
        # LaTeX math blocks: $...$, \(...\), \[...\]
        self._latex_block_pattern = re.compile(
            r"(\$[^$]+\$|\\\([^)]+\\\)|\\\[[^\]]+\\\])"
        )

        # LaTeX command symbols: \lambda, \sigma, \nabla, \mathbb{R}, etc.
        self._latex_cmd_pattern = re.compile(
            r"\\[a-zA-Z]+(?:\{[a-zA-Z0-9]+\})?"
        )

        # Function calls like f(x), g(x, y)
        self._func_pattern = re.compile(
            r"\b[a-zA-Z]\([a-zA-Z0-9,\s_]+\)"
        )

        # Subscripted variables like x_i, y_1, a_{ij}
        self._subscript_pattern = re.compile(
            r"\b[a-zA-Z]_(?:[a-zA-Z0-9]+|\{[a-zA-Z0-9]+\})"
        )

        # Single Greek, Blackboard bold, or Math operators: λ, σ, ∇, ℝ, etc.
        self._single_symbol_pattern = re.compile(
            f"({self._UNICODE_GREEK}|{self._UNICODE_MATH_OPS}|{self._BLACKBOARD_BOLD})"
        )

    def extract(self, query: str) -> list[str]:
        """Extract all unique mathematical symbols and equations from a query.

        Args:
            query: User query string.

        Returns:
            List of unique symbol strings in extraction order.
        """
        if not isinstance(query, str) or not query.strip():
            return []

        symbols: list[str] = []
        seen: set[str] = set()

        def _add_symbol(sym: str) -> None:
            clean = sym.strip()
            if clean and clean not in seen:
                seen.add(clean)
                symbols.append(clean)

        # 1. LaTeX math blocks ($...$, \(...\), \[...\])
        for match in self._latex_block_pattern.finditer(query):
            _add_symbol(match.group(1))

        # 2. Function notations like f(x), g(x, y)
        for match in self._func_pattern.finditer(query):
            _add_symbol(match.group(0))

        # 3. Subscripted variables like x_i
        for match in self._subscript_pattern.finditer(query):
            _add_symbol(match.group(0))

        # 4. LaTeX command symbols (\lambda, \nabla)
        for match in self._latex_cmd_pattern.finditer(query):
            # Only add if it's a known math command or macro
            cmd = match.group(0)
            if cmd in ("\\lambda", "\\sigma", "\\nabla", "\\alpha", "\\beta", "\\gamma", "\\delta", "\\theta", "\\mu", "\\pi", "\\mathbb{R}", "\\mathbb{Z}", "\\mathbb{N}", "\\mathbb{C}"):
                _add_symbol(cmd)

        # 5. Unicode symbols (λ, σ, ∇, ℝ)
        for match in self._single_symbol_pattern.finditer(query):
            _add_symbol(match.group(1))

        logger.debug("Extracted %d unique mathematical symbol(s) from query", len(symbols))
        return symbols
