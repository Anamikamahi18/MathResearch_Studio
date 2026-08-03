# Document Parsing Workflow (Day 2 Session 3)

## Objective

Define the conceptual parsing workflow for MathResearch Studio v1 so mathematical research PDFs can be converted into structured, searchable JSON outputs.

## Workflow Order

1. Upload PDF
2. Validate file
3. Extract metadata
4. Extract text
5. Detect sections
6. Identify equations
7. Extract references
8. Store structured JSON

## Step Details

### 1) Upload PDF

- Accept one or more PDF files from the user interface.
- Assign a temporary upload ID and preserve original filename.
- Store upload in a controlled workspace location.

### 2) Validate File

- Confirm extension and MIME type indicate PDF.
- Check size limits and basic readability.
- Compute file hash for deduplication and audit trail.
- Reject unsupported or corrupted files with clear error messages.

### 3) Extract Metadata

- Extract title, authors, year, source, DOI, and keyword candidates where available.
- Use PDF metadata first, then fallback heuristics from first-page text.
- Record field-level confidence values.

### 4) Extract Text

- Use text-layer extraction for text-based PDFs.
- Use OCR fallback for scanned/image-heavy pages.
- Preserve page boundaries and source offsets for traceability.

### 5) Detect Sections

- Segment document into hierarchical sections (abstract, introduction, methods, references, appendices).
- Track section start and end pages.
- Produce section IDs for linking downstream entities.

### 6) Identify Equations

- Detect equation-like blocks and labels.
- Preserve raw equation text or OCR output.
- Save optional normalized representation (for future LaTeX-aware processing).

### 7) Extract References

- Detect bibliography region and parse entries.
- Store raw citation text and structured fields (title/authors/year/venue/doi/url when possible).
- Keep extraction confidence and unresolved fields.

### 8) Store Structured JSON

- Serialize extracted content to the parser JSON schema.
- Include quality metadata (confidence, warnings, extraction mode, processing time).
- Store output for downstream embeddings, RAG, graph analysis, and export modules.

## Expected Outputs

- One structured JSON file per uploaded PDF
- Intermediate logs and warnings for debugging
- Provenance links from extracted entities back to pages/sections

## Non-Goals for This Session

- Full theorem-proof linking accuracy
- Perfect equation parsing across all paper layouts
- Cross-document entity resolution

These remain iterative improvements after baseline parser stability.
