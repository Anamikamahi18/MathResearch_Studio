# JSON Schema Design (Day 2 Session 2)

## Purpose

This document defines the target structured JSON output for the MathResearch Studio parser pipeline.

The goal is to establish a stable schema contract now, so parser submodules can populate fields incrementally over time.

This is a design specification, not a statement that every field is fully extracted in Version 1.

## Scope for Version 1

Version 1 should prioritize reliable population of core fields:

- Title
- Authors
- Abstract
- Sections
- Definitions (candidate extraction)
- Theorems (candidate extraction)
- Lemmas (candidate extraction)
- Proofs (candidate extraction)
- References (basic extraction)
- Metadata

The remaining fields are included now for forward compatibility.

## High-Level Schema

```json
{
  "schema_version": "1.0",
  "paper_id": "string",
  "source_file": {
    "file_name": "string",
    "file_path": "string",
    "file_hash": "string",
    "ingested_at": "ISO-8601 datetime"
  },
  "title": "string",
  "authors": [
    {
      "name": "string",
      "affiliation": "string|null",
      "email": "string|null"
    }
  ],
  "abstract": "string",
  "keywords": ["string"],
  "sections": [],
  "definitions": [],
  "theorems": [],
  "lemmas": [],
  "corollaries": [],
  "proofs": [],
  "references": [],
  "equations": [],
  "figures": [],
  "tables": [],
  "metadata": {}
}
```

## Detailed Field Plan

### 1) Title

Type: string

Description:
- Full paper title.

Suggested metadata:
- Source confidence score
- Page location

### 2) Authors

Type: array of author objects

Each author object:
- name: string
- affiliation: string or null
- email: string or null

Description:
- Ordered author list from the paper metadata or first page block.

### 3) Abstract

Type: string

Description:
- Abstract text extracted from the abstract section.

Suggested metadata:
- section_id
- page_start
- page_end

### 4) Keywords

Type: array of strings

Description:
- Explicit keyword list if present, otherwise empty.

### 5) Sections

Type: array of section objects

Each section object:
- section_id: string
- heading: string
- level: integer
- page_start: integer
- page_end: integer
- text: string
- parent_section_id: string or null

Description:
- Full document segmented into hierarchical sections.

### 6) Definitions

Type: array of math statement objects

Each object:
- definition_id: string
- label: string or null
- text: string
- section_id: string
- page: integer
- span: object with start and end offsets
- confidence: float

Description:
- Candidate definition statements extracted from paper text.

### 7) Theorems

Type: array of math statement objects

Each object:
- theorem_id: string
- label: string or null
- text: string
- section_id: string
- page: integer
- span: object with start and end offsets
- confidence: float

Description:
- Candidate theorem statements.

### 8) Lemmas

Type: array of math statement objects

Each object:
- lemma_id: string
- label: string or null
- text: string
- section_id: string
- page: integer
- span: object with start and end offsets
- confidence: float

Description:
- Candidate lemma statements.

### 9) Corollaries

Type: array of math statement objects

Each object:
- corollary_id: string
- label: string or null
- text: string
- section_id: string
- page: integer
- span: object with start and end offsets
- confidence: float

Description:
- Candidate corollary statements.

### 10) Proofs

Type: array of proof objects

Each proof object:
- proof_id: string
- related_to: object (theorem_id, lemma_id, corollary_id, or null)
- text: string
- section_id: string
- page_start: integer
- page_end: integer
- confidence: float

Description:
- Extracted or candidate proof blocks, optionally linked to statements.

### 11) References

Type: array of reference objects

Each reference object:
- reference_id: string
- raw_text: string
- title: string or null
- authors: array of strings
- year: integer or null
- venue: string or null
- doi: string or null
- url: string or null

Description:
- Bibliographic entries from reference section.

### 12) Equations

Type: array of equation objects

Each equation object:
- equation_id: string
- label: string or null
- text_repr: string
- latex_repr: string or null
- section_id: string
- page: integer
- confidence: float

Description:
- Equation blocks and normalized representations where possible.

### 13) Figures

Type: array of figure objects

Each figure object:
- figure_id: string
- caption: string or null
- page: integer
- bbox: object or null
- reference_mentions: array of strings

Description:
- Figure metadata and links to mentions in text.

### 14) Tables

Type: array of table objects

Each table object:
- table_id: string
- caption: string or null
- page: integer
- csv_repr: string or null
- reference_mentions: array of strings

Description:
- Table metadata and optional serialized table content.

### 15) Metadata

Type: object

Suggested keys:
- parser_version: string
- extraction_mode: text_pdf or ocr_fallback or hybrid
- extraction_confidence: float
- language: string
- page_count: integer
- ocr_used: boolean
- processing_time_ms: integer
- warnings: array of strings

Description:
- Operational and quality metadata for debugging and trust.

## Normalization and Conventions

- All ids should be deterministic or UUID based and unique per paper.
- Preserve page numbers for traceability.
- Keep raw text and normalized text where relevant.
- Add confidence scores for uncertain extraction outputs.
- Store empty arrays for missing structures instead of null values.

## Minimal Example

```json
{
  "schema_version": "1.0",
  "paper_id": "paper_001",
  "title": "Sample Mathematical Paper",
  "authors": [
    {"name": "A. Researcher", "affiliation": null, "email": null}
  ],
  "abstract": "This paper studies...",
  "keywords": ["graph theory", "proof mining"],
  "sections": [
    {
      "section_id": "s1",
      "heading": "Introduction",
      "level": 1,
      "page_start": 1,
      "page_end": 2,
      "text": "...",
      "parent_section_id": null
    }
  ],
  "definitions": [],
  "theorems": [],
  "lemmas": [],
  "corollaries": [],
  "proofs": [],
  "references": [],
  "equations": [],
  "figures": [],
  "tables": [],
  "metadata": {
    "parser_version": "0.1.0",
    "extraction_mode": "text_pdf",
    "extraction_confidence": 0.82,
    "language": "en",
    "page_count": 12,
    "ocr_used": false,
    "processing_time_ms": 1834,
    "warnings": []
  }
}
```

## Implementation Notes for Session 2

- Build parser submodules to write into this schema gradually.
- Do not block pipeline execution if advanced fields are empty.
- Validate output against this contract before saving JSON files.
- Keep schema updates versioned to avoid breaking downstream RAG and graph modules.
