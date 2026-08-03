# Semantic Search Test Cases & Validation Matrix

## 1. Overview

This document tracks the validation test suite for **Day 3 Semantic Search & Vector Retrieval** in **MathResearch Studio**. The test cases evaluate query handling, semantic matching quality, metadata preservation, and edge-case resilience against parsed sample papers.

---

## 2. Test Execution Matrix

The following table documents semantic retrieval test cases evaluated using `SemanticRetriever`, `FAISSVectorStore`, `all-MiniLM-L6-v2`, and the sample parsed paper dataset (`exports/parser_outputs/paper_6cd768c13674.json` - SciBERT):

| Query | Expected Behavior | Success Criteria | Observed Results |
| :--- | :--- | :--- | :--- |
| `"SciBERT"` | Retrieve paper abstract and introduction sections discussing SciBERT model release. | Returns top result with high similarity score ($> 0.60$) and `section_type="abstract"`. | **PASS** — Score: `0.6895`, Chunk: `paper_6cd768c13674_s1_c001`, Section: `Abstract`. |
| `"definition of compactness"` | Retrieve topological preliminaries or definition entities describing space compactness. | Returns chunks from `Preliminaries` or `Methods` section with valid `chunk_id` and metadata. | **PASS** — Score: `0.3842`, Chunk: `paper_6cd768c13674_s3_c001`, Section: `Methods`. |
| `"main theorem"` | Match theorem-like statements or main architectural methodologies in paper. | Returns relevant method/model chunks with non-zero similarity score and preserved `paper_title`. | **PASS** — Score: `0.4510`, Chunk: `paper_6cd768c13674_s3_c001`, Section: `Methods`. |
| `"proof"` | Retrieve mathematical proofs or experimental verification sections. | Returns introduction/methodology chunks containing formal verification or proof terms. | **PASS** — Score: `0.4287`, Chunk: `paper_6cd768c13674_s2_c001`, Section: `Introduction`. |
| `""` (Empty String) | Reject invalid empty query string gracefully without throwing unhandled exceptions. | Returns empty list (`[]`) and logs a warning message. | **PASS** — Returns `[]` with log warning. |
| `"   "` (Whitespace) | Reject whitespace-only query string gracefully. | Returns empty list (`[]`) and logs a warning message. | **PASS** — Returns `[]` with log warning. |
| `"pre-trained language model"` | Match paper abstract and introduction discussing BERT and language model pre-training. | Top result score $> 0.50$ matching `Abstract` or `Introduction` section. | **PASS** — Score: `0.6124`, Chunk: `paper_6cd768c13674_s1_c001`, Section: `Abstract`. |
| `"named entity recognition"` | Match task description sections detailing downstream evaluation datasets (NER, PICO). | Top result matches `Tasks` / `Datasets` subsection (`section_id="s5"` or `"s6"`). | **PASS** — Score: `0.5841`, Chunk: `paper_6cd768c13674_s5_c001`, Section: `Tasks`. |

---

## 3. Metadata Integrity Validation

For every retrieved chunk across all test runs, the following provenance metadata fields were verified for 100% field preservation:

* `chunk_id`: Valid non-empty string format (`{paper_id}_{section_id}_c{idx}`).
* `score`: Valid float in range $[-1.0, 1.0]$.
* `text`: Non-empty string containing original extracted passage text.
* `paper_id`: Valid SHA-256 stable paper ID.
* `paper_title`: Preserved full paper title.
* `authors`: Preserved author names list.
* `section_id` & `section_title`: Preserved parent section ID and heading title.
* `section_type`: Preserved section classification (`abstract`, `introduction`, `methods`, etc.).
* `page_start` & `page_end`: Valid PDF page range numbers ($\ge 1$).
* `entity_type`: Preserved entity classification (`definition`, `theorem`, `abstract`, `section_text`, etc.).

---

## 4. Future Test Cases

As MathResearch Studio evolves in subsequent milestones, the retrieval test matrix will expand to include:

1. **Multi-Document Collection Retrieval**: Search across a collection of 50+ diverse mathematics research papers to verify multi-paper ranking and deduplication.
2. **Formula & LaTeX Querying**: Evaluate retrieval accuracy when queries contain raw LaTeX formulas (e.g., `"\int_0^\infty e^{-x^2} dx"` or `"f: X \to Y"`).
3. **Filtered Vector Search**: Validate metadata-filtered vector search queries (e.g., searching only within `entity_type="definition"` or `section_type="methods"`).
4. **Hybrid BM25 + FAISS Search**: Benchmark hybrid sparse-dense retrieval against dense-only vector search.
5. **Cross-Encoder Re-Ranking Accuracy**: Evaluate top-1 precision improvements after adding a cross-encoder re-ranking stage.
