"""Utility helpers used across parser modules."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


def compute_sha256(file_path: Path) -> str:
    """Compute a SHA-256 hash of a file."""
    digest = hashlib.sha256()
    with file_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_paper_id(file_hash: str) -> str:
    """Build a stable paper ID from file content hash."""
    return f"paper_{file_hash[:12]}"


def clean_line(value: str) -> str:
    """Normalize whitespace in a line."""
    return re.sub(r"\s+", " ", (value or "")).strip()


def non_empty_lines(text: str) -> list[str]:
    """Return normalized non-empty lines."""
    return [clean_line(line) for line in text.splitlines() if clean_line(line)]
