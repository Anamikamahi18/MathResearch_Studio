# Embedding Architecture & Semantic Search Design

## 1. Purpose of Embeddings

In **MathResearch Studio**, text embeddings serve as dense vector representations of parsed mathematical research paper chunks. They project raw textual passages, mathematical definitions, theorems, lemmas, corollaries, and proofs into a shared high-dimensional vector space ($\mathbb{R}^{384}$).

By capturing semantic meaning rather than relying solely on exact character strings, vector embeddings enable the platform to index, discover, and retrieve relevant mathematical concepts, statements, and sections across large research paper collections.

---

## 2. Why Semantic Search Instead of Keyword Search

Traditional lexical search algorithms (e.g., BM25, TF-IDF, exact keyword matching) face significant limitations when applied to mathematical literature:

* **Vocabulary Mismatch**: Mathematical literature frequently uses distinct terminology or notation for equivalent concepts across different subfields (e.g., *"compact manifold"* vs. *"closed bounded surface"*, or *"isomorphism"* vs. *"bijective homomorphism"*).
* **Paraphrasing & Contextual Queries**: Researchers often search by concepts or high-level descriptions rather than verbatim paper phrasing (e.g., querying *"methods for solving non-linear differential equations"* rather than a specific formula string).
* **Formula & Notation Discrepancies**: Latex notation variations (such as `\frac{a}{b}` vs `a/b` or `\mathbb{R}` vs `R`) degrade keyword matching accuracy, whereas dense embeddings capture the underlying mathematical context.

Semantic search maps queries and document chunks into a unified vector space where closeness is measured via **Cosine Similarity**, enabling conceptual discovery even when query keywords do not explicitly appear in the target text.

---

## 3. Embedding Model Selection

The embedding layer in MathResearch Studio is built around the **Dependency Inversion Principle**. The abstract interface `EmbeddingProvider` decouples all downstream vector indexing and retrieval services from specific neural network libraries.

Key criteria for selecting embedding models in MathResearch Studio include:
1. **Semantic Quality**: Strong performance on academic text and conceptual retrieval benchmarks (MTEB).
2. **Computational Efficiency**: Fast CPU/GPU inference latency for responsive local interaction.
3. **Memory Footprint**: Low RAM/VRAM footprint suitable for local developer workspaces.
4. **Vector Dimension**: Compact dimensionality (e.g., 384 dimensions) for lightweight FAISS vector indexing.

---

## 4. Why `all-MiniLM-L6-v2` Was Chosen for Version 1

For Version 1 (MVP), **`sentence-transformers/all-MiniLM-L6-v2`** was selected as the default embedding model due to its optimal balance of efficiency and performance:

* **Performance**: 384-dimensional dense output embeddings with top-tier performance on general semantic similarity benchmarks.
* **Speed & Light Weight**: Extremely lightweight architecture (~80MB model file), running efficiently on standard CPU environments without requiring dedicated GPU acceleration.
* **Zero Infrastructure Cost**: Fully open-source and run locally offline via `sentence-transformers` and PyTorch.
* **Standard Compatibility**: Produces normalized 384-dimensional vectors that integrate seamlessly with FAISS `IndexFlatIP` vector storage.

---

## 5. Support for Specialized & Future Models

While `all-MiniLM-L6-v2` serves as the Version 1 default, the system architecture supports seamless replacement with domain-specific or cloud-based embedding models:

* **SciBERT (`allenai/scibert_scivocab_uncased`)**: Pre-trained on 1.14M scientific publications from Semantic Scholar. Provides specialized tokenization (`SCIVOCAB`) optimized for scientific literature and academic terminology.
* **MathBERT / Specter**: Pre-trained specifically on mathematical formulas, arXiv preprints, and academic citation graphs to capture formula structure and scientific citation context.
* **Commercial Cloud Embeddings (OpenAI `text-embedding-3-small` / `text-embedding-3-large`, Cohere)**: High-dimensional API-backed embeddings for large-scale enterprise or multi-document research libraries.

Because `EmbeddingProvider` is an abstract interface, changing the underlying model requires zero modifications to chunking, vector storage, or retrieval code.

---

## 6. Chunk Embedding Workflow

The embedding generation workflow processes parsed mathematical documents through a multi-stage pipeline:

1. **Parsed JSON Ingestion**: Receives schema-validated output from the Day 2 PDF parser (`paper_id`, metadata, sections, math statement entities).
2. **Section & Entity-Aware Chunking**: `MathDocumentChunker` extracts mathematical statements (`definitions`, `theorems`, `lemmas`, `corollaries`, `proofs`) as unbroken atomic chunks, while narrative sections are split using sentence/paragraph boundaries with sliding overlap.
3. **Batch Embedding**: `EmbeddingPipeline` batches text strings and passes them to `EmbeddingProvider.embed_texts()`.
4. **Vector Normalization**: Embeddings are $L_2$-normalized to unit length ($\|v\|_2 = 1$).
5. **Payload Association**: Vectors are paired with `chunk_id` and complete `ChunkMetadata` to create `EmbeddedChunk` instances.

---

## 7. Batch Embedding Strategy

To optimize processing throughput when embedding large academic papers containing dozens or hundreds of chunks, the pipeline enforces a **Batch Embedding Strategy**:

* **Tensor Parallelism**: Groups text chunks into configurable batches (default: `batch_size = 32`) to leverage batched matrix multiplication in PyTorch/Transformers.
* **Reduced Overhead**: Minimizes Python loop iterations and device transfer latency.
* **Memory Safety**: Prevents Out-Of-Memory (OOM) failures by controlling peak memory consumption during inference.

---

## 8. Advantages of the Architecture

* **Mathematical Entity Preservation**: Math statement blocks remain intact as single atomic chunks, preventing fragmented definitions or severed proofs in vector space.
* **Full Provenance Traceability**: Every embedded chunk retains paper metadata, section titles, section types, and exact PDF page ranges for accurate citation generation.
* **Modular Provider Interchangeability**: Switching between local Transformer models and external cloud APIs requires only instantiating a different `EmbeddingProvider` subclass.
* **Optimized FAISS Search**: $L_2$-normalized vectors enable hardware-accelerated Inner Product search (`IndexFlatIP`), delivering exact Cosine Similarity scores.

---

## 9. Limitations

* **General Domain Default**: `all-MiniLM-L6-v2` is trained on general web text and may not capture complex LaTeX syntax or highly specialized mathematical symbolism as effectively as a math-tuned BERT model.
* **Fixed Context Window**: Standard Transformer embedding models enforce a maximum token sequence length (e.g., 256 or 512 tokens), requiring long narrative sections to be chunked.
* **Text-Only Embedding**: Version 1 embeds extracted text and LaTeX string representations, but does not currently compute multi-modal embeddings for raw rendered PDF formula images or figures.

---

## 10. Future Improvements

* **Math-Tuned Fine-Tuning**: Fine-tune custom sentence-transformer models on mathematical corpora (arXiv math preprints, OEIS, stacks project) to improve mathematical symbol awareness.
* **Hybrid Retrieval (Dense + Sparse)**: Combine FAISS dense semantic retrieval with sparse lexical indexing (BM25) to achieve hybrid search (retrieving both exact variable names and broad concepts).
* **Formula Tree Embeddings**: Compute embeddings over mathematical Abstract Syntax Trees (ASTs) for structure-aware formula search.
* **Multi-Vector Indexing (ColBERT / Late Interaction)**: Transition to multi-vector token-level representations to improve fine-grained mathematical statement matching.
