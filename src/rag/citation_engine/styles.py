"""Citation style definitions and configuration settings."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class CitationStyleType(str, Enum):
    """Supported citation formatting styles."""

    INLINE = "inline"  # [1], [2]
    AUTHOR_YEAR = "author_year"  # (Smith, 2024)
    ACADEMIC = "academic"  # [Paper Title, Section 2, p. 1]


@dataclass
class CitationStyle:
    """Configuration container for a citation formatting style."""

    style_type: CitationStyleType
    marker_format: str
    include_section: bool = True
    include_page: bool = True
    group_by_paper: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Convert CitationStyle to dictionary representation."""
        return {
            "style_type": self.style_type.value,
            "marker_format": self.marker_format,
            "include_section": self.include_section,
            "include_page": self.include_page,
            "group_by_paper": self.group_by_paper,
        }


STYLE_INLINE = CitationStyle(
    style_type=CitationStyleType.INLINE,
    marker_format="[{id}]",
    include_section=False,
    include_page=False,
)

STYLE_AUTHOR_YEAR = CitationStyle(
    style_type=CitationStyleType.AUTHOR_YEAR,
    marker_format="({author}, {year})",
    include_section=True,
    include_page=False,
)

STYLE_ACADEMIC = CitationStyle(
    style_type=CitationStyleType.ACADEMIC,
    marker_format="[{paper}, {section}]",
    include_section=True,
    include_page=True,
)

BUILTIN_STYLES: dict[str, CitationStyle] = {
    CitationStyleType.INLINE.value: STYLE_INLINE,
    CitationStyleType.AUTHOR_YEAR.value: STYLE_AUTHOR_YEAR,
    CitationStyleType.ACADEMIC.value: STYLE_ACADEMIC,
}
