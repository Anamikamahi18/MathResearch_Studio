# Parser Test Cases (Day 2 Session 3)

This file tracks sample paper inputs and baseline parser test status.

## Test Inputs Location

- `tests/sample_papers/`

## Test Case Records

| Paper title | Successfully loaded (Yes/No) | Metadata extracted (Yes/No) | Sections detected (Yes/No) | Parsing issues | Notes |
|---|---|---|---|---|---|
| Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | Yes | No | No | Parser pipeline not implemented yet for metadata and sections | Local PDF downloaded as `paper_01_rag.pdf` |
| SciBERT: A Pretrained Language Model for Scientific Text | Yes | No | No | Parser pipeline not implemented yet for metadata and sections | Local PDF downloaded as `paper_02_scibert.pdf` |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | Yes | No | No | Parser pipeline not implemented yet for metadata and sections | Local PDF downloaded as `paper_03_specter.pdf` |
| LayoutLM: Pre-training of Text and Layout for Document Image Understanding | Yes | No | No | Parser pipeline not implemented yet for metadata and sections | Local PDF downloaded as `paper_04_layoutlm.pdf` |
| Nougat: Neural Optical Understanding for Academic Documents | Yes | No | No | Parser pipeline not implemented yet for metadata and sections | Local PDF downloaded as `paper_05_nougat.pdf` |

## Notes

- These files are openly available research PDFs and can be used to validate loading, metadata parsing, section detection, and JSON export as each parser module is implemented.
- Current status reflects Session 3 setup completion, not full extraction capability.
