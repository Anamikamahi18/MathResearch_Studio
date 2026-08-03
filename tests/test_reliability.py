"""Unit tests for parser reliability helpers."""

from __future__ import annotations

import unittest

from src.parser.reliability import (
    WarningCode,
    clamp_references,
    compute_extraction_confidence,
    diagnostics_to_warning_strings,
    evaluate_quality_thresholds,
    make_diagnostic,
    resolve_parse_state,
)


class TestReliability(unittest.TestCase):
    """Validate diagnostics and confidence policy behavior."""

    def test_make_diagnostic_structure(self) -> None:
        """Diagnostic payloads should include stable policy fields."""
        item = make_diagnostic(
            code=WarningCode.META_TITLE_MISSING,
            stage="metadata",
            message="Title missing",
            severity="warning",
            page=1,
            details={"source": "heuristic"},
        )
        self.assertEqual(item["code"], WarningCode.META_TITLE_MISSING)
        self.assertEqual(item["stage"], "metadata")
        self.assertEqual(item["severity"], "warning")
        self.assertEqual(item["page"], 1)
        self.assertEqual(item["details"]["source"], "heuristic")

    def test_confidence_decreases_with_warnings(self) -> None:
        """Confidence should decrease when policy warnings are present."""
        diagnostics = [
            make_diagnostic(
                code=WarningCode.META_TITLE_MISSING,
                stage="metadata",
                message="Title missing",
            ),
            make_diagnostic(
                code=WarningCode.EXTRACT_LOW_CONTENT,
                stage="extract_text",
                message="Low content",
            ),
        ]

        score = compute_extraction_confidence(
            page_count=3,
            has_title=False,
            has_authors=False,
            section_count=1,
            diagnostics=diagnostics,
        )
        self.assertLess(score, 0.75)
        self.assertGreaterEqual(score, 0.0)

    def test_parse_state_resolution(self) -> None:
        """Parse state should follow diagnostics severity and confidence."""
        clean_state = resolve_parse_state(diagnostics=[],
                                          extraction_confidence=0.82)
        self.assertEqual(clean_state, "success")

        warning_state = resolve_parse_state(
            diagnostics=[
                make_diagnostic(
                    code=WarningCode.META_DOI_MISSING,
                    stage="metadata",
                    message="DOI missing",
                )
            ],
            extraction_confidence=0.70,
        )
        self.assertEqual(warning_state, "degraded_success")

        error_state = resolve_parse_state(
            diagnostics=[
                make_diagnostic(
                    code="EXPORT_WRITE_FAILED",
                    stage="export_json",
                    message="Failed",
                    severity="error",
                )
            ],
            extraction_confidence=0.92,
        )
        self.assertEqual(error_state, "hard_failure")

    def test_warning_string_flattening(self) -> None:
        """Diagnostic strings should preserve code and stage context."""
        warnings = diagnostics_to_warning_strings(
            [
                make_diagnostic(
                    code=WarningCode.EXTRACT_EMPTY_PAGE,
                    stage="extract_text",
                    message="2 empty pages",
                )
            ]
        )
        self.assertEqual(len(warnings), 1)
        self.assertIn(WarningCode.EXTRACT_EMPTY_PAGE, warnings[0])
        self.assertIn("extract_text", warnings[0])

    def test_unknown_code_rejected(self) -> None:
        """Diagnostics should enforce centralized code contracts by default."""
        with self.assertRaises(ValueError):
            make_diagnostic(
                code="UNKNOWN_POLICY_CODE",
                stage="metadata",
                message="Unknown",
            )

    def test_extract_page_failed_penalty_is_capped(self) -> None:
        """Page failure confidence penalty should honor policy cap."""
        diagnostics = [
            make_diagnostic(
                code=WarningCode.EXTRACT_PAGE_FAILED,
                stage="extract_text",
                message="page failed",
            )
            for _ in range(5)
        ]
        score = compute_extraction_confidence(
            page_count=5,
            has_title=False,
            has_authors=False,
            section_count=1,
            diagnostics=diagnostics,
        )
        self.assertEqual(score, 0.45)

    def test_quality_threshold_helpers_emit_expected_codes(self) -> None:
        """Quality threshold helper should emit policy diagnostics."""
        diagnostics = evaluate_quality_thresholds(
            token_count=10,
            section_count=999,
            reference_count=500,
        )
        codes = {item["code"] for item in diagnostics}
        self.assertIn(WarningCode.EXTRACT_LOW_CONTENT, codes)
        self.assertIn(WarningCode.SECTION_OVERSEGMENTED, codes)
        self.assertIn(WarningCode.REFERENCES_PARSE_UNSTABLE, codes)

    def test_reference_clamp_respects_policy_limit(self) -> None:
        """Reference clamp should enforce policy maximum."""
        references = [{"reference_id": f"r{i}"} for i in range(350)]
        clamped, was_clamped = clamp_references(references)
        self.assertTrue(was_clamped)
        self.assertEqual(len(clamped), 300)


if __name__ == "__main__":
    unittest.main()
