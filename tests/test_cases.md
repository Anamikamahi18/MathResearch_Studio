# Parser Test Cases (Day 2 Session 3)

This file tracks sample paper inputs and baseline parser test status.

## Test Inputs Location

- `tests/sample_papers/`

## Test Case Records

| Paper title | Successfully loaded (Yes/No) | Metadata extracted (Yes/No) | Sections detected (Yes/No) | Parsing issues | Notes |
|---|---|---|---|---|---|
| Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | Yes | Yes | Yes | Heuristic metadata and section extraction may include noisy lines in complex layouts | Parsed JSON saved as `paper_23e3249e9a1e.json` |
| SciBERT: A Pretrained Language Model for Scientific Text | Yes | Yes | Yes | Author metadata quality is heuristic and can include affiliation-like tokens | Parsed JSON saved as `paper_6cd768c13674.json` |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | Yes | Yes | Yes | Section boundaries may require refinement on dense pages | Parsed JSON saved as `paper_6336d5787f65.json` |
| LayoutLM: Pre-training of Text and Layout for Document Image Understanding | Yes | Yes | Yes | Equation and reference extraction remain baseline pattern-based | Parsed JSON saved as `paper_5bec7f495a9e.json` |
| Nougat: Neural Optical Understanding for Academic Documents | Yes | Yes | Yes | OCR fallback is not fully implemented; empty pages trigger warnings only | Parsed JSON saved as `paper_679be336ce80.json` |

## Notes

- These files are openly available research PDFs and can be used to validate loading, metadata parsing, section detection, and JSON export as each parser module is implemented.
- Current status reflects Day 2 baseline parser implementation with modular extraction components.

## Section Taxonomy Coverage (Day 2 Update)

Target section types for the section detector module:

- Abstract
- Introduction
- Preliminaries
- Definitions
- Lemmas
- Theorems
- Proofs
- Results
- Conclusion
- References

Automated validation is now covered by `tests/test_section_detector.py`.

| Validation scope | Result | Notes |
|---|---|---|
| Synthetic heading classification for all 10 target section types | Pass | Uses direct heading tests such as `1 Introduction`, `3 Definitions`, and `References` |
| Noise-line rejection (author-like lines, prose lines, URL lines) | Pass | Reduces false heading detections |
| Hierarchy assignment from numbered headings | Pass | Confirms parent-child mapping for subsection levels |
| Real sample PDF check (`paper_01_rag.pdf`) | Pass | Confirms presence of abstract, introduction, and references with bounded section count |

## Sample PDF Section Coverage Snapshot

This compact table can be reused in the root README to summarize Day 2
section detection behavior on the sample corpus.

| Sample PDF | Sections detected | Section types observed |
|---|---:|---|
| paper_01_rag.pdf | 18 | abstract, introduction, results, references, other |
| paper_02_scibert.pdf | 13 | abstract, introduction, results, references, other |
| paper_03_specter.pdf | 20 | abstract, introduction, results, references, other |
| paper_04_layoutlm.pdf | 11 | abstract, introduction, results, references, other |
| paper_05_nougat.pdf | 13 | abstract, introduction, conclusion, references, other |

Core coverage result:

- Every sample paper contains abstract, introduction, and references.
- The corpus includes both results and conclusion section types.
