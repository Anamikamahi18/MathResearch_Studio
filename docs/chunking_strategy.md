# Mathematical Document Chunking Strategy

## 1. Why Chunking is Necessary

Dense vector retrieval and Large Language Model (LLM) context windows cannot ingest entire multi-page academic papers as single monolithic inputs. Splitting documents into smaller, semantically coherent segments ("chunks") is necessary for several key reasons:

* **Context Window Limits**: Neural embedding models (such as `all-MiniLM-L6-v2` or `SciBERT`) operate on fixed maximum token limits (e.g., 256 or 512 tokens).
* **Retrieval Granularity**: Searching across multi-page PDFs requires isolating the specific paragraph, definition, or theorem that answers a researcher's query, rather than retrieving an entire 30-page paper.
* **Noise Reduction**: Smaller chunks improve signal-to-noise ratio in vector space, allowing vector similarity search to match precise mathematical statements accurately.

---

## 2. Section-Aware Chunking

Generic document chunkers split text at arbitrary character or word boundaries, which severs headings from content and destroys paper organization. **MathResearch Studio** uses a **Section-Aware Chunking Strategy**:

* **Document Structure Respect**: Uses the section hierarchy extracted during Day 2 PDF parsing (`Abstract`, `Introduction`, `Methods`, `Results`, `Discussion`, `Appendices`).
* **Heading & Context Retention**: Every chunk maintains explicit reference to its parent section ID, heading title, and section type.
* **Domain-Specific Boundaries**: Abstract, references, and mathematical statement blocks are processed differently from long narrative sections.

---

## 3. Mathematical Entity Preservation

A core architectural principle of MathResearch Studio is that **mathematical statement entities must never be split across chunk boundaries**.

In mathematical literature, a definition, theorem, lemma, corollary, or proof forms an indivisible logical unit. Splitting a theorem midway through its hypotheses or separating a proof from its conclusion renders the vector embedding incomplete and uninterpretable.

The chunker isolates mathematical entities in a dedicated first pass, creating **unbroken atomic chunks** regardless of character length.

---

## 4. Definition Chunks

* **Atomic Unit**: Definitions describe mathematical concepts, notation, or formal constraints.
* **Formatting**: Formatted with their formal label prepended to the body (e.g., `"Definition 2.1: A topological space X is compact if..."`).
* **Entity Tagging**: Metadata field `entity_type` is set explicitly to `"definition"`.
* **Vector Property**: Ensures that searching for a concept definition retrieves the complete formal statement in a single search result.

---

## 5. Theorem, Lemma, & Corollary Chunks

* **Atomic Unit**: Formal mathematical assertions (Theorems, Lemmas, Corollaries) are treated as self-contained logical statements.
* **Label Association**: Theorem numbers and titles are attached directly to the text (e.g., `"Theorem 3.4 (Central Limit Theorem): Let X1, X2..."`).
* **Entity Tagging**: Metadata field `entity_type` is set to `"theorem"`, `"lemma"`, or `"corollary"`.
* **Retrieval Advantage**: Allows researchers to search specifically for main theorems or supporting lemmas without missing mathematical conditions.

---

## 6. Proof Chunks

* **Atomic Unit**: Mathematical proofs demonstrate the validity of theorems or lemmas.
* **Preservation**: Kept intact as single atomic chunks to preserve the step-by-step deductive chain.
* **Entity Tagging**: Metadata field `entity_type` is set to `"proof"`.
* **Traceability**: Linked back to parent section IDs and page ranges so researchers can verify proofs alongside their corresponding theorems.

---

## 7. Narrative Section Chunking

For general descriptive text in sections such as `Introduction`, `Background`, `Discussion`, or `Methods`, text is chunked using a sentence- and paragraph-aware sliding window:

1. **Paragraph Splits**: Primary splitting occurs at double newlines (`\n\n`) to preserve paragraph boundaries.
2. **Sentence Splits**: If a single paragraph exceeds the target chunk size (`max_chunk_size = 800` characters), it is split along sentence boundaries (`. `, `! `, `? `).
3. **Formula Boundary Protection**: Sentence splitting protects inline LaTeX formulas and mathematical expressions from being cut midway.

---

## 8. Chunk Overlap

To prevent loss of context at chunk boundaries in long narrative sections, the chunker enforces a configurable sliding overlap (`chunk_overlap = 150` characters):

* **Context Continuity**: The tail end of chunk $N$ is carried over to the beginning of chunk $N+1$.
* **Boundary Query Protection**: Ensures that queries matching concepts spanning across sentence or paragraph boundaries are successfully retrieved.

---

## 9. Metadata Preservation

Every text chunk created by `MathDocumentChunker` carries a complete `ChunkMetadata` payload preserving full paper and structural provenance:

* `paper_id`: Unique stable hash identifier of the paper.
* `paper_title`: Full title of the research paper.
* `authors`: List of paper author names.
* `section_id`: Section identifier (e.g., `"s2"`).
* `section_title`: Section heading (e.g., `"3. Preliminaries"`).
* `section_type`: Classification (`abstract`, `introduction`, `methods`, `appendix`, etc.).
* `page_start` & `page_end`: PDF page range where the chunk appears.
* `entity_type`: Mathematical entity classification (`definition`, `theorem`, `lemma`, `corollary`, `proof`, `abstract`, or `section_text`).

This metadata enables exact page and section citations when retrieved by AI assistants or rendered in the workspace UI.

---

## 10. Future Chunking Improvements

* **Formula AST Aware Chunking**: Parse LaTeX formulas into Abstract Syntax Trees (ASTs) to chunk complex multi-line display equations cleanly.
* **Theorem-Proof Paired Chunks**: Create composite chunks that combine a theorem statement directly with its proof for unified RAG reasoning.
* **Hierarchical Multi-Level Chunking**: Store parent section summaries alongside child paragraph chunks to enable hierarchical retrieval (retrieving high-level section context along with detailed passages).
* **Cross-Reference Linking**: Link internal citation markers (`[12]`, `Eq. 4`, `Theorem 2`) directly within chunk metadata to support interactive graph exploration.
