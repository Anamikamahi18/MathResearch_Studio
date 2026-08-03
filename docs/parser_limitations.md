# Parser Limitations (Day 2 Session 4)

## Purpose

This document lists expected limitations in the scientific document parsing pipeline for MathResearch Studio v1.

Being explicit about limitations is good engineering practice and helps users interpret outputs responsibly.

## Expected Limitations

### 1) Multi-column Layouts

Issue:
- Two-column or mixed-column papers may produce incorrect reading order.

Impact:
- Definitions and theorem statements can be interleaved with unrelated text.

Mitigation:
- Add layout-aware ordering heuristics and page-level confidence flags.

### 2) Scanned PDFs

Issue:
- Image-only PDFs rely on OCR and may lose symbols, punctuation, and structure.

Impact:
- Metadata and equation extraction quality can drop significantly.

Mitigation:
- Use OCR fallback only when needed and record `ocr_used` in metadata.

### 3) Complex Equations

Issue:
- Nested math expressions, matrices, and alignment environments are hard to reconstruct reliably.

Impact:
- Extracted equations may be incomplete or semantically incorrect.

Mitigation:
- Preserve raw equation blocks and confidence scores; defer strict normalization to later versions.

### 4) Handwritten Annotations

Issue:
- Marginal notes, highlights, and handwritten marks are difficult to parse consistently.

Impact:
- Noise can contaminate extracted text and section boundaries.

Mitigation:
- Filter annotation-like regions where possible and flag uncertain pages.

### 5) Non-standard Theorem Environments

Issue:
- Papers use inconsistent naming conventions (Proposition, Claim, Fact, Result, etc.).

Impact:
- Entity extractor can miss or misclassify mathematical statements.

Mitigation:
- Keep rule sets configurable and extendable; log missed patterns for iterative updates.

### 6) Reference Parsing Variability

Issue:
- Citation formats vary significantly across venues and author styles.

Impact:
- Partial or incorrect reference field extraction.

Mitigation:
- Store raw citation text in addition to structured fields.

### 7) Metadata Inconsistency

Issue:
- Titles, authors, and years can appear in multiple layouts and may not be present in embedded PDF metadata.

Impact:
- Incomplete or low-confidence metadata objects.

Mitigation:
- Use layered extraction (embedded metadata + first-page heuristics) and confidence scores.

## What This Means for Version 1

- Version 1 focuses on robust baseline extraction, not perfect semantic parsing.
- Some outputs will require user review, especially around equations and theorem boundaries.
- Reliability should be measured and improved iteratively with tracked test cases.

## Transparency Commitments

- Expose parser warnings and confidence in downstream views.
- Preserve source provenance for traceability.
- Keep known limitations documented and updated as parser quality improves.
