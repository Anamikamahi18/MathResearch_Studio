"""Central reliability helpers for parser diagnostics and confidence."""

from __future__ import annotations

from typing import Any

BASE_CONFIDENCE_SCORE = 0.70
SUCCESS_CONFIDENCE_THRESHOLD = 0.75
DEGRADED_CONFIDENCE_THRESHOLD = 0.30

LOW_CONTENT_TOKEN_THRESHOLD = 150
SECTION_OVERSEGMENTED_THRESHOLD = 200
REFERENCE_OVERFLOW_THRESHOLD = 300

EXTRACT_PAGE_FAILED_MAX_PENALTY = -0.25


class ParseState:
    """Stable parse states for parser outputs."""

    SUCCESS = "success"
    DEGRADED_SUCCESS = "degraded_success"
    HARD_FAILURE = "hard_failure"


class WarningCode:
    """Stable warning and error codes for parser stages."""

    IO_FILE_NOT_FOUND = "IO_FILE_NOT_FOUND"
    IO_PERMISSION_DENIED = "IO_PERMISSION_DENIED"
    FORMAT_NOT_PDF = "FORMAT_NOT_PDF"
    FORMAT_CORRUPT_PDF = "FORMAT_CORRUPT_PDF"
    FORMAT_ENCRYPTED_PDF = "FORMAT_ENCRYPTED_PDF"
    EXTRACT_EMPTY_PAGE = "EXTRACT_EMPTY_PAGE"
    EXTRACT_PAGE_FAILED = "EXTRACT_PAGE_FAILED"
    EXTRACT_MALFORMED_TEXT = "EXTRACT_MALFORMED_TEXT"
    LAYOUT_MULTICOLUMN_SUSPECTED = "LAYOUT_MULTICOLUMN_SUSPECTED"
    LAYOUT_READING_ORDER_UNCERTAIN = "LAYOUT_READING_ORDER_UNCERTAIN"
    META_TITLE_MISSING = "META_TITLE_MISSING"
    META_AUTHORS_MISSING = "META_AUTHORS_MISSING"
    META_YEAR_MISSING = "META_YEAR_MISSING"
    META_DOI_MISSING = "META_DOI_MISSING"
    META_FIELD_CONFLICT = "META_FIELD_CONFLICT"
    SECTION_DETECTOR_FAILED = "SECTION_DETECTOR_FAILED"
    ENTITY_EXTRACTOR_FAILED = "ENTITY_EXTRACTOR_FAILED"
    REFERENCES_PARSE_UNSTABLE = "REFERENCES_PARSE_UNSTABLE"
    EXTRACT_LOW_CONTENT = "EXTRACT_LOW_CONTENT"
    SECTION_OVERSEGMENTED = "SECTION_OVERSEGMENTED"
    EXPORT_SCHEMA_INVALID = "EXPORT_SCHEMA_INVALID"
    EXPORT_WRITE_FAILED = "EXPORT_WRITE_FAILED"


KNOWN_WARNING_CODES: set[str] = {
    WarningCode.IO_FILE_NOT_FOUND,
    WarningCode.IO_PERMISSION_DENIED,
    WarningCode.FORMAT_NOT_PDF,
    WarningCode.FORMAT_CORRUPT_PDF,
    WarningCode.FORMAT_ENCRYPTED_PDF,
    WarningCode.EXTRACT_EMPTY_PAGE,
    WarningCode.EXTRACT_PAGE_FAILED,
    WarningCode.EXTRACT_MALFORMED_TEXT,
    WarningCode.LAYOUT_MULTICOLUMN_SUSPECTED,
    WarningCode.LAYOUT_READING_ORDER_UNCERTAIN,
    WarningCode.META_TITLE_MISSING,
    WarningCode.META_AUTHORS_MISSING,
    WarningCode.META_YEAR_MISSING,
    WarningCode.META_DOI_MISSING,
    WarningCode.META_FIELD_CONFLICT,
    WarningCode.SECTION_DETECTOR_FAILED,
    WarningCode.ENTITY_EXTRACTOR_FAILED,
    WarningCode.REFERENCES_PARSE_UNSTABLE,
    WarningCode.EXTRACT_LOW_CONTENT,
    WarningCode.SECTION_OVERSEGMENTED,
    WarningCode.EXPORT_SCHEMA_INVALID,
    WarningCode.EXPORT_WRITE_FAILED,
}


DEFAULT_CODE_SEVERITY: dict[str, str] = {
    WarningCode.IO_FILE_NOT_FOUND: "error",
    WarningCode.IO_PERMISSION_DENIED: "error",
    WarningCode.FORMAT_NOT_PDF: "error",
    WarningCode.FORMAT_CORRUPT_PDF: "error",
    WarningCode.FORMAT_ENCRYPTED_PDF: "error",
    WarningCode.EXPORT_SCHEMA_INVALID: "error",
    WarningCode.EXPORT_WRITE_FAILED: "error",
}


POSITIVE_CONFIDENCE_DELTAS: dict[str, float] = {
    "title_extracted": 0.05,
    "authors_extracted": 0.05,
    "section_detection_succeeded": 0.05,
}


NEGATIVE_CONFIDENCE_DELTAS: dict[str, float] = {
    WarningCode.EXTRACT_PAGE_FAILED: -0.10,
    WarningCode.LAYOUT_MULTICOLUMN_SUSPECTED: -0.08,
    WarningCode.LAYOUT_READING_ORDER_UNCERTAIN: -0.08,
    WarningCode.SECTION_DETECTOR_FAILED: -0.10,
    WarningCode.ENTITY_EXTRACTOR_FAILED: -0.08,
    WarningCode.META_TITLE_MISSING: -0.05,
    WarningCode.META_AUTHORS_MISSING: -0.03,
    WarningCode.EXTRACT_MALFORMED_TEXT: -0.05,
    WarningCode.EXTRACT_LOW_CONTENT: -0.10,
    WarningCode.SECTION_OVERSEGMENTED: -0.08,
}


# Backward-compatible alias for older call sites.
CONFIDENCE_DELTAS = NEGATIVE_CONFIDENCE_DELTAS


def is_known_warning_code(code: str) -> bool:
    """Return True when code belongs to the centralized policy set."""
    return code in KNOWN_WARNING_CODES


def default_severity_for_code(code: str) -> str:
    """Return policy default severity for a diagnostic code."""
    return DEFAULT_CODE_SEVERITY.get(code, "warning")


def _clamp_confidence(value: float) -> float:
    return max(0.0, min(1.0, value))


def _extract_page_failed_penalty(diagnostics: list[dict[str, Any]]) -> float:
    failed_page_count = sum(
        1
        for item in diagnostics
        if (item.get("code") == WarningCode.EXTRACT_PAGE_FAILED)
    )
    if failed_page_count <= 0:
        return 0.0
    return max(
        EXTRACT_PAGE_FAILED_MAX_PENALTY,
        failed_page_count * NEGATIVE_CONFIDENCE_DELTAS[
            WarningCode.EXTRACT_PAGE_FAILED
            ],
    )


def evaluate_quality_thresholds(
    *,
    token_count: int,
    section_count: int,
    reference_count: int,
) -> list[dict[str, Any]]:
    """Return policy diagnostics for low content and overflow thresholds."""
    diagnostics: list[dict[str, Any]] = []

    if token_count < LOW_CONTENT_TOKEN_THRESHOLD:
        diagnostics.append(
            make_diagnostic(
                code=WarningCode.EXTRACT_LOW_CONTENT,
                stage="extract_text",
                message="Low extracted text volume may reduce "
                "retrieval quality.",
                details={"token_count": token_count},
            )
        )

    if section_count > SECTION_OVERSEGMENTED_THRESHOLD:
        diagnostics.append(
            make_diagnostic(
                code=WarningCode.SECTION_OVERSEGMENTED,
                stage="detect_sections",
                message="Section count exceeded threshold; "
                "review heading rules.",
                details={"section_count": section_count},
            )
        )

    if reference_count > REFERENCE_OVERFLOW_THRESHOLD:
        diagnostics.append(
            make_diagnostic(
                code=WarningCode.REFERENCES_PARSE_UNSTABLE,
                stage="parse_references",
                message="Reference count exceeded threshold; "
                "output was clamped.",
                details={
                    "reference_count": reference_count,
                    "max_references": REFERENCE_OVERFLOW_THRESHOLD,
                },
            )
        )

    return diagnostics


def clamp_references(
    references: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], bool]:
    """Clamp references to policy limit and report
    whether truncation occurred."""
    if len(references) <= REFERENCE_OVERFLOW_THRESHOLD:
        return references, False
    return references[:REFERENCE_OVERFLOW_THRESHOLD], True


def make_diagnostic(
    *,
    code: str,
    stage: str,
    message: str,
    severity: str | None = None,
    page: int | None = None,
    details: dict[str, Any] | None = None,
    allow_unknown_code: bool = False,
) -> dict[str, Any]:
    """Create a structured parser diagnostic payload."""
    if not allow_unknown_code and not is_known_warning_code(code):
        raise ValueError(f"Unknown diagnostic code: {code}")

    diagnostic = {
        "code": code,
        "severity": severity or default_severity_for_code(code),
        "stage": stage,
        "message": message,
    }
    if page is not None:
        diagnostic["page"] = page
    if details:
        diagnostic["details"] = details
    return diagnostic


def diagnostics_to_warning_strings(
    diagnostics: list[dict[str, Any]],
) -> list[str]:
    """Flatten diagnostic objects into compact warning strings."""
    warnings: list[str] = []
    for item in diagnostics:
        code = str(item.get("code", "UNKNOWN"))
        message = str(item.get("message", ""))
        stage = str(item.get("stage", "unknown"))
        warnings.append(f"[{code}] ({stage}) {message}")
    return warnings


def compute_extraction_confidence(
    *,
    page_count: int,
    has_title: bool,
    has_authors: bool,
    section_count: int,
    diagnostics: list[dict[str, Any]],
    title_extracted: bool | None = None,
    authors_extracted: bool | None = None,
    section_detection_succeeded: bool | None = None,
) -> float:
    """Compute confidence using baseline score and diagnostic deltas."""
    score = BASE_CONFIDENCE_SCORE

    title_available = has_title if title_extracted is None else title_extracted
    authors_available = (
        has_authors if (authors_extracted is None) else authors_extracted
    )
    section_success = (
        section_count >= 2
        if section_detection_succeeded is None
        else section_detection_succeeded
    )

    if title_available:
        score += POSITIVE_CONFIDENCE_DELTAS["title_extracted"]
    if authors_available:
        score += POSITIVE_CONFIDENCE_DELTAS["authors_extracted"]
    if section_success:
        score += POSITIVE_CONFIDENCE_DELTAS["section_detection_succeeded"]

    score += _extract_page_failed_penalty(diagnostics)

    for item in diagnostics:
        code = str(item.get("code", ""))
        if code == WarningCode.EXTRACT_PAGE_FAILED:
            continue
        score += NEGATIVE_CONFIDENCE_DELTAS.get(code, 0.0)

    if page_count == 0:
        score = min(score, 0.10)

    return round(_clamp_confidence(score), 2)


def resolve_parse_state(
    *,
    diagnostics: list[dict[str, Any]],
    extraction_confidence: float,
) -> str:
    """Resolve final parse state from diagnostics and confidence."""
    if any(item.get("severity") == "error" for item in diagnostics):
        return ParseState.HARD_FAILURE
    has_warning = any(
        item.get("severity") == "warning" for item in diagnostics
        )
    if (
        extraction_confidence >= SUCCESS_CONFIDENCE_THRESHOLD
        and not has_warning
    ):
        return ParseState.SUCCESS
    if (
        extraction_confidence >= DEGRADED_CONFIDENCE_THRESHOLD or has_warning
    ):
        return ParseState.DEGRADED_SUCCESS
    return ParseState.HARD_FAILURE
