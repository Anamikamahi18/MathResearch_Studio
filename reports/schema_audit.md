# Day 2 Parser Output & Schema Audit Report

## 1. Executive Summary

This report documents the schema audit of the Day 2 Scientific Document Parsing Pipeline output (`exports/parser_outputs/*.json`) and its compatibility with the Day 4 Mathematical Entity and Relation Extraction Pipeline (`src/graph/`).

---

## 2. Schema Specification & Field Audit

The parser output strictly adheres to Schema v1.0. The audit verified the field names, data types, nesting levels, required attributes, and optional attributes across all entity types:

### A. Mathematical Statement Collections (`definitions`, `theorems`, `lemmas`, `corollaries`)
- **Nesting Level**: Top-level array of dictionaries.
- **Key Names**:
  - `definitions`: array of Definition objects.
  - `theorems`: array of Theorem objects.
  - `lemmas`: array of Lemma objects.
  - `corollaries`: array of Corollary objects.
- **Attributes**:
  - `def_id` / `thm_id` / `lem_id` / `cor_id` (str, required): Unique identifier (e.g. `"def_001"`, `"thm_001"`).
  - `entity_id` (str, optional): Canonical entity identifier.
  - `label` (str, required): Statement title/numbering (e.g. `"Definition 1.1"`).
  - `text` (str, required): Complete text body of the statement.
  - `section_id` (str, required): Parent section identifier (e.g. `"s1"`).
  - `page` (int, required): 1-indexed starting page number.
  - `page_start` / `page_end` (int, optional): Page range spanning the statement.
  - `span` (dict, required): Line index span within section (`{"start": int, "end": int}`).
  - `confidence` (float, required): Extraction confidence score (0.0 - 1.0).

### B. Proof Blocks (`proofs`)
- **Nesting Level**: Top-level array of dictionaries.
- **Attributes**:
  - `proof_id` (str, required): Unique identifier (e.g. `"prf_001"`).
  - `label` (str, optional): Canonical label (e.g. `"Proof of Theorem 3.2"`).
  - `related_to` (dict, required): Mapping to target statement IDs (`{"theorem_id": str | None, "lemma_id": str | None, "corollary_id": str | None}`).
  - `text` (str, required): Complete text body of the proof block.
  - `section_id` (str, required): Parent section identifier.
  - `page_start` (int, required): Starting page.
  - `page_end` (int, required): Ending page.
  - `confidence` (float, required): Extraction confidence score.

### C. Displayed & Inline Equations (`equations`)
- **Nesting Level**: Top-level array of dictionaries.
- **Attributes**:
  - `equation_id` (str, required): Unique equation ID (e.g. `"eq_001"`).
  - `latex_text` (str, required): LaTeX representation.
  - `raw_text` (str, optional): Extracted text snippet.
  - `section_id` (str, required): Parent section ID.
  - `page` (int, required): Page number.
  - `is_numbered` (bool, required): Whether equation has an explicit number.
  - `eq_number` (str | None, optional): Equation number string (e.g. `"1"`).
  - `confidence` (float, required): Extraction confidence score.

### D. Bibliographic References (`references`)
- **Nesting Level**: Top-level array of dictionaries.
- **Attributes**:
  - `reference_id` (str, required): Reference ID (e.g. `"ref_001"`).
  - `raw_text` (str, required): Full reference text entry.
  - `title` (str | None, optional): Parsed title string.
  - `authors` (list[str], required): List of author names.
  - `year` (int | None, optional): Publication year.
  - `venue` (str | None, optional): Publication venue or journal.
  - `doi` (str | None, optional): Digital Object Identifier.
  - `url` (str | None, optional): Source URL.

### E. Structural Sections (`sections`)
- **Nesting Level**: Top-level array of dictionaries.
- **Attributes**:
  - `section_id` (str, required): Section ID (e.g. `"s1"`).
  - `heading` (str, required): Section heading label.
  - `level` (int, required): Heading hierarchy level (1, 2, 3).
  - `page_start` (int, required): Starting page.
  - `page_end` (int, required): Ending page.
  - `text` (str, required): Section narrative prose.
  - `parent_section_id` (str | None, required): Parent section ID for tree hierarchy.
  - `section_type` (str, required): Canonical section type (`preliminaries`, `theorems`, etc.).
  - `confidence` (float, required): Detection confidence score.

---

## 3. Identified Mismatches & Applied Fixes

| Audit Item | Pre-Audit Issue | Applied Fix |
| :--- | :--- | :--- |
| **Label Formatting** | Day 2 parser extracted raw regex match numbers (e.g. `"1.1"` or `None`) instead of `"Definition 1.1"`, preventing cross-reference matching. | Updated `src/parser/section_detector/service.py` and `src/graph/entity_extraction/extractor.py` to format canonical labels (`"Definition 1.1"`, `"Theorem 3.2"`). |
| **Multi-line Body Truncation** | Statements and proofs were truncated at single line boundaries. | Implemented multi-line text block lookahead accumulation until double blank line or next entity header. |
| **Proof Target Resolution** | `proofs.related_to` was unpopulated (`None` targets). | Added target statement parsing from `"Proof of Theorem X"` lines and preceding statement tracking in section traversal. |
| **Page Attribute Uniformity** | Statements used `page`, while proofs used `page_start`/`page_end`. | Standardized `EntityExtractor` to read `page_start` / `page_end` with fallback to `page`. |
