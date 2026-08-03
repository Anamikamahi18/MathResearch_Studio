# Parser Design (Day 2)

## Purpose

Build the scientific document parsing pipeline for MathResearch Studio v1 so uploaded mathematics PDFs can be converted into structured, searchable data.

The parser is not intended to verify mathematical correctness. Its goal is to extract document structure and research entities with enough quality for downstream search, RAG, and note export.

## Input

- PDF files uploaded by users
- Optional upload metadata (uploader name, tags, topic)
- Runtime configuration from environment or config files

Supported document types:
- Text-based PDFs (preferred)
- Scanned or image-heavy PDFs (fallback pipeline)

## Output

Primary output is a structured JSON document per paper.

### Output JSON (v1 schema)

```json
{
  "paper_id": "uuid",
  "file_name": "example_paper.pdf",
  "metadata": {
    "title": "",
    "authors": [],
    "year": null,
    "source": "",
    "doi": ""
  },
  "document_type": "text_pdf|scanned_pdf|mixed",
  "sections": [
    {
      "section_id": "s1",
      "heading": "Introduction",
      "page_start": 1,
      "page_end": 2,
      "text": "..."
    }
  ],
  "entities": {
    "definitions": [],
    "theorems": [],
    "lemmas": [],
    "proofs": []
  },
  "chunks": [
    {
      "chunk_id": "c1",
      "section_id": "s1",
      "text": "...",
      "page": 1
    }
  ],
  "quality": {
    "extraction_confidence": 0.0,
    "ocr_used": false,
    "warnings": []
  }
}
```

## Components

1. Upload Handler
- Accepts PDF files and validates format/size.
- Stores files in uploads directory.

2. PDF Classifier
- Detects whether PDF is text-based or image-heavy.
- Chooses text extraction or OCR fallback path.

3. Text Extractor
- Extracts page-wise text from text-based PDFs.
- Preserves page boundaries for traceability.

4. OCR Fallback Extractor
- Runs OCR for scanned/image pages.
- Merges OCR output into page-wise document text.

5. Metadata Extractor
- Extracts title, authors, year, and source where possible.
- Applies heuristic fallback when metadata is missing.

6. Section Detector
- Identifies major sections (abstract, introduction, methods, references).
- For math papers, highlights candidate theorem/proof regions.

7. Math Entity Extractor
- Detects candidate definitions, theorems, lemmas, and proofs.
- Uses heading patterns and lexical rules first (v1 baseline).

8. Chunking Service
- Splits cleaned text into retrieval-ready chunks.
- Associates chunk metadata (section, page, offsets).

9. JSON Serializer
- Writes normalized structured JSON to database or filesystem.
- Guarantees schema consistency for downstream modules.

10. Quality Scorer
- Computes extraction confidence and warning flags.
- Marks low-quality outputs for manual review.

## Data Flow

1. User uploads PDF.
2. Upload handler validates and stores file.
3. PDF classifier selects extraction path.
4. Text extractor (or OCR fallback) produces page text.
5. Metadata extractor parses bibliographic signals.
6. Section detector segments the document.
7. Math entity extractor identifies definitions/theorems/lemmas/proofs.
8. Chunking service builds retrieval chunks.
9. JSON serializer writes structured output.
10. Quality scorer adds confidence and warnings.
11. Structured JSON is passed to embeddings and RAG modules.

## Limitations

- Mathematical notation extraction remains imperfect in v1.
- Theorem/proof boundaries can be noisy in heterogeneous PDF layouts.
- OCR quality may degrade on low-resolution scans.
- Metadata extraction is heuristic and may miss uncommon formats.
- Cross-paper entity linking is out of scope for v1.

## Future Improvements

- Layout-aware parsing with bounding-box-aware models.
- Better equation and symbol-aware extraction.
- Learned theorem/proof classifiers beyond rule-based detection.
- Improved OCR ensemble and page-level confidence calibration.
- Human-in-the-loop correction interface for low-confidence outputs.
- Incremental parsing updates for revised paper versions.
