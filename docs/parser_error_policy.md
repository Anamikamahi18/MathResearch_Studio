# Parser Error Policy (Day 2 Reliability Guide)

## Purpose

This document defines the fail-soft reliability policy for the scientific PDF
parsing pipeline in MathResearch Studio v1.

Goal:
- Export useful structured JSON whenever recovery is possible.
- Attach machine-readable diagnostics so downstream NLP and RAG can decide what
  to trust.

## Final Parse States

Every paper parse must end in one of these states:

1. success
- Clean extraction.
- High confidence.
- No critical warnings.

2. degraded_success
- JSON exported with recoverable warnings.
- Reduced confidence and explicit stage diagnostics.

3. hard_failure
- Parse cannot continue (for example file unreadable or output write failure).
- Emit failure artifact with status and diagnostics.

## Error and Warning Taxonomy

Use stable codes so errors are testable and automatable.

### IO and format errors

| Code | Severity | Stage | Meaning | Default action |
|---|---|---|---|---|
| IO_FILE_NOT_FOUND | error | load_pdf | Input file path does not exist | hard_failure |
| IO_PERMISSION_DENIED | error | load_pdf | File cannot be read due to permissions | hard_failure |
| FORMAT_NOT_PDF | error | load_pdf | File extension or header is not PDF | hard_failure |
| FORMAT_CORRUPT_PDF | error | load_pdf | PDF structure cannot be parsed reliably | degraded_success if any page is recoverable; otherwise hard_failure |
| FORMAT_ENCRYPTED_PDF | error | load_pdf | PDF is encrypted and cannot be opened | hard_failure unless decryption is configured |

### extraction and quality warnings

| Code | Severity | Stage | Meaning | Default action |
|---|---|---|---|---|
| EXTRACT_EMPTY_PAGE | warning | extract_text | Page has no extracted text | keep page, lower confidence, mark OCR recommended |
| EXTRACT_PAGE_FAILED | warning | extract_text | Specific page text extraction failed | continue with remaining pages |
| EXTRACT_MALFORMED_TEXT | warning | extract_text | Garbled characters or malformed text stream | keep cleaned text, mark low quality |
| LAYOUT_MULTICOLUMN_SUSPECTED | warning | detect_sections | Multi-column reading order may be incorrect | keep text, lower section confidence |
| LAYOUT_READING_ORDER_UNCERTAIN | warning | detect_sections | Reading order ambiguity remains after heuristic pass | preserve provenance and reduce confidence |
| SECTION_DETECTOR_FAILED | warning | detect_sections | Section stage raised exception | fallback to single Document section |
| ENTITY_EXTRACTOR_FAILED | warning | extract_entities | Entity extraction failed | return empty entity arrays |
| REFERENCES_PARSE_UNSTABLE | warning | parse_references | Abnormal reference volume or split quality | clamp output size and keep raw text |

### metadata warnings

| Code | Severity | Stage | Meaning | Default action |
|---|---|---|---|---|
| META_TITLE_MISSING | warning | metadata | Title unavailable from metadata and heuristics | fallback to filename |
| META_AUTHORS_MISSING | warning | metadata | Authors unavailable | keep empty authors array |
| META_YEAR_MISSING | warning | metadata | Year unavailable | keep null year |
| META_DOI_MISSING | warning | metadata | DOI unavailable | keep null doi |
| META_FIELD_CONFLICT | warning | metadata | Embedded metadata conflicts with first-page heuristic | prefer embedded metadata and record conflict |

### export and contract errors

| Code | Severity | Stage | Meaning | Default action |
|---|---|---|---|---|
| EXPORT_SCHEMA_INVALID | error | export_json | Required schema keys/types invalid | hard_failure with failure artifact |
| EXPORT_WRITE_FAILED | error | export_json | Output JSON cannot be written | hard_failure |

## Stage-Level Continuation Policy

Use isolated try/except per stage and continue with defaults where possible.

1. load_pdf
- If no pages are recoverable, stop with hard_failure.
- If some pages are recoverable, continue as degraded_success candidate.

2. metadata
- Always continue on failure.
- Fill defaults and add metadata warning codes.

3. extract_text
- Continue page-wise even when individual pages fail.
- Track failed page numbers and text quality metrics.

4. detect_sections
- On failure, create one fallback section:
  - heading: Document
  - level: 1
  - full available text

5. extract_entities
- On failure, set definitions/theorems/lemmas/corollaries/proofs to empty arrays.

6. export_json
- Normalize and validate before write.
- On write failure, emit hard_failure diagnostics.

## Confidence Impact Rules

Start with a base confidence score and apply additive deltas.

Base score:
- 0.70

Positive deltas:
- +0.05 if title extracted from embedded metadata
- +0.05 if authors extracted
- +0.05 if section detection succeeds without fallback

Negative deltas:
- -0.10 for each EXTRACT_PAGE_FAILED (cap -0.25)
- -0.08 for LAYOUT_MULTICOLUMN_SUSPECTED
- -0.08 for LAYOUT_READING_ORDER_UNCERTAIN
- -0.10 for SECTION_DETECTOR_FAILED
- -0.08 for ENTITY_EXTRACTOR_FAILED
- -0.05 for META_TITLE_MISSING
- -0.03 for META_AUTHORS_MISSING
- -0.05 for EXTRACT_MALFORMED_TEXT

Clamp:
- final_confidence = min(1.0, max(0.0, adjusted_score))

State thresholds:
- success: final_confidence >= 0.75 and no error severity diagnostics
- degraded_success: 0.30 <= final_confidence < 0.75 or has warnings
- hard_failure: unrecoverable IO/format/export error

## Diagnostic Payload Shape

Store diagnostics as structured objects in metadata.warnings (or a dedicated
metadata.diagnostics list in v1.1+).

Suggested object shape:
- code: stable string code
- severity: info or warning or error
- stage: load_pdf or metadata or extract_text or detect_sections or
  extract_entities or parse_references or export_json
- message: human-readable message
- page: optional page number
- details: optional object for extra context

## Defensive Thresholds

Apply safety thresholds to protect downstream RAG quality.

- low-content threshold:
  - if extracted text tokens < 150, emit EXTRACT_LOW_CONTENT
- section over-detection threshold:
  - if sections > 200, emit SECTION_OVERSEGMENTED and cap section count
- reference overflow threshold:
  - if references > 300, emit REFERENCES_PARSE_UNSTABLE and clamp output

## Retry Policy

Use bounded retries only for likely transient failures.

- IO and output writes:
  - retry up to 2 times with short backoff
- deterministic parse errors:
  - no repeated retries

## Observability and Run Summary

Per-paper log fields:
- paper_id
- stage_start and stage_end timestamps
- stage_status: ok, warning, failed
- warning/error codes
- processing_time_ms

Batch summary fields:
- total_files
- success_count
- degraded_success_count
- hard_failure_count
- most_common_warning_codes

## Test Requirements

Failure-oriented tests should validate:
- corrupted PDF input
- encrypted PDF without key
- missing metadata fallback behavior
- synthetic multi-column disorder warning
- malformed text quality warning

Assertions:
- parser does not crash for recoverable cases
- JSON is exported for degraded_success
- warning codes are stable and expected
- confidence is reduced according to policy
