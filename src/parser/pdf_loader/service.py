"""PDF loading and text extraction service."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..helpers import compute_sha256


def _import_pypdf() -> Any:
    try:
        from pypdf import PdfReader
    except Exception as exc:  # pragma: no cover - import guard
        raise RuntimeError(
            "pypdf is required for PDF extraction. "
            "Install with: pip install pypdf"
        ) from exc
    return PdfReader


def load_pdf(file_path: Path) -> dict[str, Any]:
    """Load PDF content as page-wise text and basic metadata."""
    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    PdfReader = _import_pypdf()
    reader = PdfReader(str(file_path))

    pages: list[dict[str, Any]] = []
    empty_pages = 0
    for index, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if not text:
            empty_pages += 1
        pages.append({"page": index, "text": text})

    return {
        "file_name": file_path.name,
        "file_path": str(file_path.resolve()),
        "file_hash": compute_sha256(file_path),
        "page_count": len(pages),
        "empty_pages": empty_pages,
        "metadata_raw": dict(reader.metadata or {}),
        "pages": pages,
    }
