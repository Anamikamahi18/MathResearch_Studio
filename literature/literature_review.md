# Literature Review

Aim: Review 20 to 40 papers over a month, prioritising recent work from arXiv and major AI and mathematical knowledge management venues.

## Today's Target

Aim to review 3 to 5 papers today.

## Suggested Reading Topics

- Mathematical Knowledge Management
- Scientific Document Understanding
- Retrieval Augmented Generation for Research
- Theorem Extraction
- Proof Mining
- Scientific NLP
- Mathematical Information Retrieval
- Semantic Scholar
- arXiv

## Daily 5-Paper Review Method

Use this repeatable routine each day:

1. 20 minutes: shortlist 8 to 10 candidate papers from arXiv or Semantic Scholar.
2. 15 minutes: skim title, abstract, and conclusion for all candidates.
3. 15 minutes: pick top 5 papers using relevance to MathResearch Studio v1.
4. 90 minutes: deep read 3 core papers (about 30 minutes each).
5. 40 minutes: lighter review of 2 supporting papers (about 20 minutes each).
6. 30 minutes: fill the review table fields for all 5 papers.
7. 10 minutes: extract 3 actionable product ideas for tomorrow.

Prioritization rule:
- 2 papers on document understanding/parsing
- 2 papers on retrieval/RAG/search
- 1 paper on mathematical reasoning/proof or theorem-related representation

## Today: 5 Paper Reviews

These are filled examples using influential papers relevant to your project direction.

---

## Paper 1

**Title**  
Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

**Authors**  
Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Kuttler, Mike Lewis, Wen-tau Yih, Tim Rocktaschel, Sebastian Riedel, Douwe Kiela

**Year**  
2020

**Source**  
NeurIPS 2020 / arXiv

**Problem**  
Large language models hallucinate and have limited up-to-date factual grounding.

**Method**  
Combines a neural retriever over an external document index with a generator so answers are conditioned on retrieved passages.

**Strengths**  
Introduced a practical retrieval-generation paradigm, improved factuality compared with pure parametric generation, and enabled updateable knowledge via index refresh.

**Limitations**  
Quality depends heavily on retriever performance and chunking strategy; retrieval errors propagate into generated answers.

**Research Gap**  
Grounded QA for technical domains with dense notation remains difficult; citation quality and traceability need stronger guarantees.

**Ideas**  
Implement citation-first answers in MathResearch Studio where every response includes paper name, section, and excerpt. Add confidence flags when retrieval evidence is weak.

---

## Paper 2

**Title**  
SciBERT: A Pretrained Language Model for Scientific Text

**Authors**  
Iz Beltagy, Kyle Lo, Arman Cohan

**Year**  
2019

**Source**  
EMNLP-IJCNLP 2019 / arXiv

**Problem**  
General-domain language models underperform on scientific text due to domain mismatch in vocabulary and style.

**Method**  
Pretrains a BERT-style model on a large corpus of scientific papers, with scientific vocabulary and domain-adapted representations.

**Strengths**  
Demonstrated strong gains on scientific NLP tasks and established domain-adapted language modeling as high-impact for scholarly text.

**Limitations**  
Model is general scientific, not specifically tuned for symbolic mathematics notation and theorem-proof structure.

**Research Gap**  
Need models specialized for mathematical language, symbolic expressions, and formal statement extraction.

**Ideas**  
Use domain-specific embeddings for scientific text first, then add math-focused adaptation for theorem/definition extraction.

---

## Paper 3

**Title**  
SPECTER: Document-level Representation Learning using Citation-informed Transformers

**Authors**  
Arman Cohan, Sergey Feldman, Iz Beltagy, Doug Downey, Daniel S. Weld

**Year**  
2020

**Source**  
ACL 2020 / arXiv

**Problem**  
Traditional keyword search in scientific corpora misses semantic and citation-context relationships between papers.

**Method**  
Learns paper embeddings informed by citation relationships, enabling semantically meaningful retrieval at document level.

**Strengths**  
Strong semantic retrieval for scientific documents and better related-paper discovery than standard lexical methods.

**Limitations**  
Citation signals are uneven across subfields and weaker for very recent papers; not tailored to statement-level mathematical retrieval.

**Research Gap**  
Need hybrid retrieval that combines semantic vectors with structure-level fields like theorem names, symbols, and section types.

**Ideas**  
Add two-level retrieval in MathResearch Studio: paper-level nearest neighbors and statement-level nearest neighbors for theorem/proof chunks.

---

## Paper 4

**Title**  
LayoutLM: Pre-training of Text and Layout for Document Image Understanding

**Authors**  
Yiheng Xu, Minghao Li, Lei Cui, Shaohan Huang, Furu Wei, Ming Zhou

**Year**  
2020

**Source**  
KDD 2020 / arXiv

**Problem**  
OCR text alone loses spatial structure from documents, hurting extraction quality.

**Method**  
Jointly models text tokens and 2D layout coordinates during pretraining.

**Strengths**  
Showed that layout-aware modeling improves document understanding tasks such as form understanding and information extraction.

**Limitations**  
Scientific PDFs with equations and complex notation remain challenging; layout cues alone are insufficient for math semantics.

**Research Gap**  
Need combined layout plus symbolic parsing pipelines for robust mathematical entity extraction.

**Ideas**  
Store section coordinates and page anchors so extracted definitions/theorems can be traced back to exact PDF positions in the UI.

---

## Paper 5

**Title**  
Nougat: Neural Optical Understanding for Academic Documents

**Authors**  
Lukas Blecher, Guillem Cucurull, Thomas Scialom, Robert Stojnic

**Year**  
2023

**Source**  
arXiv

**Problem**  
Conventional OCR pipelines often fail on scientific PDFs with formulas and structured content.

**Method**  
Uses a vision-to-text transformer approach specialized for academic documents to generate structured textual outputs from page images.

**Strengths**  
Improved extraction quality for scholarly documents and better handling of complex scientific layouts compared with generic OCR baselines.

**Limitations**  
Mathematical notation fidelity can still degrade; post-processing and validation are required for critical research workflows.

**Research Gap**  
High-precision equation and theorem boundary extraction from heterogeneous math PDFs remains open.

**Ideas**  
Build a parser fallback chain: text-based extraction first, OCR/vision-based fallback second, then confidence scoring and manual correction queue.

---

## Day 2 Session 1: Scientific Document Parsing Focus

### Focus Topics

- Scientific Document Understanding
- PDF Parsing
- Mathematical OCR
- Digital Libraries
- Scientific NLP

### 5 Additional Papers Reviewed (Parsing Pipeline)

#### Paper A

**Title**  
PubLayNet: Largest Dataset Ever for Document Layout Analysis

**Source**  
ICDAR 2019 / arXiv

**Key Insight**  
Large-scale layout datasets significantly improve section and block detection quality in scholarly documents.

**Possible Improvement for MathResearch Studio**  
Add layout-aware section segmentation as a second-stage refinement after text extraction.

#### Paper B

**Title**  
DocBank: A Benchmark Dataset for Document Layout Analysis

**Source**  
COLING 2020 / arXiv

**Key Insight**  
Token-level layout labels help with fine-grained scientific document parsing, not just page-level block detection.

**Possible Improvement for MathResearch Studio**  
Keep token/page metadata in parser outputs so downstream extraction can use position-aware heuristics.

#### Paper C

**Title**  
Donut: Document Understanding Transformer without OCR

**Source**  
ECCV 2022 / arXiv

**Key Insight**  
OCR-free models can handle complex documents end-to-end and reduce errors introduced by separate OCR pipelines.

**Possible Improvement for MathResearch Studio**  
Prototype an OCR-free fallback for image-heavy PDFs and compare against text plus OCR pipeline quality.

#### Paper D

**Title**  
Im2LaTeX: Translating Math Formula Images to LaTeX Sequences

**Source**  
ICML 2017 / arXiv

**Key Insight**  
Formula-specific sequence modeling is crucial for preserving mathematical meaning in extracted text.

**Possible Improvement for MathResearch Studio**  
Flag equation-heavy regions and route them through formula-aware extraction before final JSON serialization.

#### Paper E

**Title**  
LayoutLMv3: Pre-training for Document AI with Unified Text and Image Masking

**Source**  
ACM MM 2022 / arXiv

**Key Insight**  
Joint text-image pretraining provides better robustness for mixed-layout documents than text-only approaches.

**Possible Improvement for MathResearch Studio**  
Add optional multimodal parsing mode for PDFs where section detection confidence is low.

### Day 2 Extraction Design Insights

- Treat parser as a multi-path pipeline, not a single extractor.
- Preserve page and section provenance for every extracted entity.
- Add confidence scores and warning flags to all parser outputs.
- Separate concerns: extraction, sectioning, entity detection, and chunking should remain independent stages.
- Keep JSON schema stable so RAG and graph modules can evolve without parser rewrites.

---

## Day 3: Dense Retrieval & Semantic Search Focus

### Focus Topics

- Dense Retrieval
- Sentence Transformers
- FAISS
- Scientific Search
- Mathematical Information Retrieval
- Embedding Models for Scientific Documents

---

### Topic 1: Dense Retrieval

**Summary**  
Dense retrieval maps queries and documents into a shared continuous vector space using deep neural encoders (e.g., dual-encoders), replacing token-matching with vector similarity search (e.g., inner product or cosine distance).

**Strengths**  
Captures semantic intent and paraphrasing, overcomes vocabulary mismatch, handles non-verbatim query formulations, and supports dense similarity search algorithms.

**Weaknesses**  
Struggles with exact keyword/symbol matching, out-of-vocabulary technical jargon, rare variable names, and requires high computational resources for index generation.

**Research Gap**  
Optimal hybrid fusion techniques combining dense semantic vectors with exact sparse lexical signals (BM25) for specialized technical domains.

**Ideas for MathResearch Studio**  
Integrate dense semantic retrieval as the core search mechanism for conceptual queries, while preparing a hybrid sparse-dense re-ranking stage for exact symbol and formula lookups.

---

### Topic 2: Sentence Transformers

**Summary**  
Sentence Transformers (using Siamese or triplet network architectures) fine-tune pre-trained Transformer language models to generate dense, semantically meaningful sentence- and passage-level embeddings suitable for fast vector comparison.

**Strengths**  
Generates fixed-size dense vectors ($L_2$-normalized), enables rapid cosine similarity search, runs efficiently on standard hardware (e.g., `all-MiniLM-L6-v2`), and integrates easily with local Python environments.

**Weaknesses**  
Fixed sequence length truncation limits context window capacity; standard general-domain models lack deep pre-training on complex LaTeX mathematical syntax.

**Research Gap**  
Fine-tuning sentence-transformer architectures specifically on mathematical definition-theorem pairs and LaTeX formulas to improve mathematical similarity representation.

**Ideas for MathResearch Studio**  
Use `sentence-transformers` with an abstract `EmbeddingProvider` interface, defaulting to `all-MiniLM-L6-v2` for MVP, with a seamless extension path to fine-tuned mathematical sentence models.

---

### Topic 3: FAISS (Facebook AI Similarity Search)

**Summary**  
FAISS is an open-source library for efficient dense vector similarity search and clustering. It supports hardware-accelerated matrix operations and indexing structures (e.g., `IndexFlatIP`, `IndexHNSW`, `IndexIVFFlat`) over high-dimensional vector spaces.

**Strengths**  
Extremely fast similarity search (sub-millisecond $k$-NN lookup over millions of vectors), supports $L_2$-normalized Inner Product search for exact Cosine Similarity, and provides simple disk serialization (`write_index`, `read_index`).

**Weaknesses**  
FAISS indices store only numeric vector arrays and integer IDs without internal payload storage for document metadata, requiring external metadata synchronization.

**Research Gap**  
Dynamic payload mapping and atomic transactional index updates for multi-tenant, streaming document ingestion pipelines.

**Ideas for MathResearch Studio**  
Implement `FAISSVectorStore` using `faiss.IndexFlatIP` paired with a synchronized JSON metadata store (`exports/vector_store/metadata.json`) preserving full paper provenance and section hierarchy.

---

### Topic 4: Scientific Search

**Summary**  
Scientific search focuses on discovery, retrieval, and contextual exploration across academic paper collections, moving beyond standard web search to handle metadata graphs, citations, and scholarly structure.

**Strengths**  
Organizes literature by section structure, author networks, and citations; enables targeted search within specific paper sections (e.g., abstract, methodology, results).

**Weaknesses**  
Traditional scientific search engines rely heavily on metadata or abstracts, failing to index deep mathematical statement entities (definitions, theorems, proofs) within paper bodies.

**Research Gap**  
Granular, entity-aware scientific search that indexes mathematical statement blocks as first-class searchable domain objects.

**Ideas for MathResearch Studio**  
Combine document section detection with entity preservation so researchers can filter scientific search specifically by `entity_type` (e.g., searching only for definitions or theorems).

---

### Topic 5: Mathematical Information Retrieval (MIR)

**Summary**  
Mathematical Information Retrieval is a specialized domain focused on indexing, searching, and retrieving mathematical expressions, LaTeX formulas, and formal mathematical statements across technical literature.

**Strengths**  
Preserves formula syntax, handles structural expression matching, and respects mathematical statement boundaries (definitions, theorems, lemmas, proofs).

**Weaknesses**  
Formula-only search misses surrounding natural language context, while text-only search ignores symbolic formula equivalences; current MIR tools lack unified RAG capabilities.

**Research Gap**  
Unified dual-representation retrieval models that embed natural language text and LaTeX formula expressions into a single aligned vector space.

**Ideas for MathResearch Studio**  
Enforce atomic entity-preserving chunking in `MathDocumentChunker` so definitions, theorems, lemmas, and proofs remain complete, unbroken units during vector indexing.

---

### Topic 6: Embedding Models for Scientific Documents

**Summary**  
Embedding models specialized for scientific literature (e.g., SciBERT, SPECTER, MathBERT, Specter2) leverage domain-specific pre-training on academic publications (such as Semantic Scholar or arXiv) to capture scientific vocabulary and citation context.

**Strengths**  
Captures academic terminology, multi-word technical concepts, and scholarly syntax better than general web-trained models.

**Weaknesses**  
Higher computational overhead, larger model weights, and potential dependency on domain-specific tokenizers (`SCIVOCAB`).

**Research Gap**  
Lightweight scientific embedding models optimized for edge/local developer execution that balance mathematical formula understanding with fast inference latency.

**Ideas for MathResearch Studio**  
Design `src/embeddings/provider.py` with an abstract interface so users can easily toggle between lightweight general models (`all-MiniLM-L6-v2`) and domain-specialized models (`SciBERT` / `MathBERT`).

---

## Day 4 Focus: Mathematical Knowledge Graphs & Statement Dependency Networks

### Topic 7: Mathematical Knowledge Management (MKM) & Knowledge Graphs

**Summary**  
Mathematical Knowledge Management (MKM) focuses on representing, organizing, and querying mathematical knowledge across formal and informal literature (Kohlhase, 2006). Mathematical Knowledge Graphs (MKGs) model mathematical statements as discrete graph nodes and logical dependencies as directed edges.

**Strengths**  
- Enables multi-hop logical dependency tracking (`Definition` $\rightarrow$ `Lemma` $\rightarrow$ `Theorem` $\rightarrow$ `Proof`).
- Allows topological traversal of proof antecedents and consequents.

**Weaknesses**  
- Manual graph creation requires expensive expert annotation; automated extraction on unformatted PDFs must handle noisy LaTeX and OCR text.

**Research Gap**  
- Automated end-to-end pipelines that parse unformatted PDFs into fine-grained statement nodes and directed dependency multigraphs.

**Ideas for MathResearch Studio**  
- Build `ResearchGraphBuilder` using NetworkX `MultiDiGraph` to represent fine-grained mathematical statement nodes (`definition`, `theorem`, `lemma`, `proof`) connected by semantic dependency edges (`uses_definition`, `depends_on`, `proves`).

---

### Topic 8: Scientific Entity and Relation Extraction (NER & RE)

**Summary**  
Scientific Named Entity Recognition (NER) and Relation Extraction (RE) extract domain concepts and typed relations from scientific publications (Luan et al., 2018 - *SciERC*). In mathematical literature, entity extraction identifies definitions, theorems, lemmas, corollaries, and proofs, while relation extraction classifies dependencies (`proves`, `extends`, `uses_definition`, `cites`).

**Strengths**  
- Discovers non-trivial cross-paper relationships and structural citation networks.
- Enables graph-augmented retrieval (Graph-RAG) combining topological graph walk with semantic search.

**Weaknesses**  
- Pure regex extraction can miss informal or unnumbered statements; pure ML extractors require domain-specific training data.

**Research Gap**  
- Hybrid extraction pipelines combining metadata-first parsing with fallback rule-based regex and pluggable ML strategy patterns.

**Ideas for MathResearch Studio**  
- Implement `BaseRelationExtractor` strategy interface so rule-based extractors can be seamlessly replaced or enhanced with LLM/NER classifiers without altering downstream graph components.

---

## Day 5 Focus: Retrieval-Augmented Generation (RAG), Scientific QA, Hallucination Reduction, & Citation Grounding

### Topic 9: Retrieval-Augmented Generation for Scientific Question Answering (Scientific RAG)

**Summary**  
Retrieval-Augmented Generation (Lewis et al., 2020) combines neural passage retrieval with pre-trained generative language models. In scientific QA contexts (e.g. BioASQ, SciQ, arXiv-QA), RAG grounds model generation in authoritative document excerpts, significantly improving factual recall over un-augmented language models.

**Advantages**  
- Grounds generated answers directly in uploaded scientific paper passages.
- Eliminates the need to continuously re-train or fine-tune LLMs when literature changes.
- Limits context window distraction by supplying only top-K relevant chunks.

**Weaknesses**  
- Basic RAG models rely on pure dense vector similarity, which often fails to capture mathematical symbol definitions ($\lambda$, $\mathcal{H}$) or graph dependency structures.
- Naive passage chunking splits mathematical definitions across boundaries, breaking logical proofs.

**Research Gap**  
- Multi-signal hybrid retrieval frameworks that seamlessly combine dense semantic vectors, exact symbol/entity matches, and knowledge graph adjacency weights.

**Ideas for MathResearch Studio**  
- Implement `HybridRetriever` combining FAISS vector similarity, entity/symbol overlap, intent classification, and Day 4 Research Graph topology scores.

---

### Topic 10: LLM Hallucination Mitigation & Factual Grounding in STEM Literature

**Summary**  
Large language models frequently hallucinate non-existent mathematical theorems, false proof steps, or fictitious author citations when generating technical text (Ji et al., 2023 - *Survey of Hallucination in Natural Language Generation*). Factual grounding techniques measure sentence-level context alignment to detect unsupported model assertions before returning outputs to researchers.

**Advantages**  
- Sentence-level claim alignment detects subtle hallucination artifacts in multi-paragraph technical answers.
- Provides quantitative grounding scores ($\text{GroundingScore} \in [0, 1]$) to evaluate factual confidence.

**Weaknesses**  
- LLM-based hallucination evaluators are slow, expensive, and subject to self-reflection bias.
- Pure word-overlap metrics miss mathematical equivalence (e.g. $\text{tr}(A)$ vs $\sum \lambda_i$).

**Research Gap**  
- Fast, deterministic sentence alignment engines that evaluate mathematical claim support without invoking secondary LLM API calls.

**Ideas for MathResearch Studio**  
- Build `AlignmentEngine` and `ClaimVerifier` in `src/rag/evidence/` and `src/rag/grounding/` using rule-based token overlap and entity matching to verify answer grounding deterministically in $\le 5\text{ms}$.

---

### Topic 11: Citation Grounding & Traceable Scientific Attribution

**Summary**  
Citation grounding (Gao et al., 2023 - *RARR: Research-Assembled Retrieval and Repair*) ensures that every generated factual statement is explicitly paired with a verifiable source passage, including paper title, section heading, page range, and chunk identifier.

**Advantages**  
- Increases researcher trust by providing direct one-click attribution to source PDF passages.
- Supports multiple academic citation formats (`[1]`, `(Author, Year)`, `[Paper, Section, Page]`).

**Weaknesses**  
- Naive citation insertion tools frequently attach duplicate citations or hallucinate page numbers not present in source metadata.

**Research Gap**  
- Automated citation formatters equipped with real-time integrity validators that check for orphan references, missing paper titles, or invalid page boundaries.

**Ideas for MathResearch Studio**  
- Implement `CitationEngine` and `CitationValidator` in `src/rag/citation_engine/` supporting `INLINE`, `AUTHOR_YEAR`, and `ACADEMIC` styles while enforcing strict metadata validation.

---

### Topic 12: Guardrails & Safe Decision Policies for AI Research Assistants

**Summary**  
AI safety guardrails (Reaver et al., 2023) act as policy decision filters that evaluate whether an AI assistant's generated response should be returned, annotated with warnings, refused, or deferred for user clarification.

**Advantages**  
- Prevents fabricated or zero-evidence answers from reaching researchers.
- Communicates uncertainty clearly when retrieved literature is insufficient.

**Weaknesses**  
- Hardcoded guardrails can become overly restrictive if thresholds are set arbitrarily without empirical validation.

**Research Gap**  
- Policy-driven guardrail decision engines that separate rule evaluation from generation, ensuring non-destructive answer handling.

**Ideas for MathResearch Studio**  
- Create `GuardrailDecisionEngine` in `src/rag/guardrails/` enforcing policy rules (`RETURN`, `RETURN_WITH_WARNING`, `REFUSE`, `ASK_FOR_CLARIFICATION`, `INSUFFICIENT_EVIDENCE`) over upstream RAG outputs.

---

### Topic 13: Research Software Interfaces & Human-Computer Interaction (HCI) for Scientists

**Summary**  
Scientific software interfaces often suffer from cognitive overload, unintuitive workflows, and lack of visual transparency (Munzner, 2014 - *Visualization Analysis and Design*; Shneiderman, 1996 - *The Eyes Have It: A Task by Data Type Taxonomy for Information Visualizations*). Designing interfaces for mathematical researchers requires balancing high information density (latex equations, theorem statements, proof dependencies) with clean visual hierarchies and low-friction navigation.

**Advantages**  
- Reduces visual fatigue and cognitive friction during multi-hour literature research sessions.
- Enables single-click access to paper metadata, mathematical definitions, and grounding citations.

**Weaknesses**  
- Existing academic software often presents raw JSON or unformatted text blocks, requiring manual formatting by researchers.

**Research Gap**  
- Integrated research workspace interfaces designed specifically for mathematical literature analysis that combine document ingestion, semantic search, interactive graph visualization, grounded AI Q&A, and multi-format exporting into a unified dashboard.

**Ideas for MathResearch Studio**  
- Build a single-page Streamlit application shell with persistent sidebar navigation (`src/ui/router.py`), dark-mode palette (`#0F172A`/`#1E293B`), and modular page components (`src/ui/pages/`) providing low-cognitive-load workflows for MSc students, PhD scholars, and faculty.

---

### Topic 14: Scientific Visualization & Interactive Knowledge Dashboards

**Summary**  
Interactive scientific dashboards (Heer et al., 2010 - *Declarative Language Design for Interactive Visualization*) allow researchers to explore complex multi-paper relationship networks, statement dependency trees, and mathematical symbol dictionaries dynamically. Providing interactive zoom/pan graph visualization, live configuration previews, and real-time metric cards significantly improves literature comprehension.

**Advantages**  
- Visualizing theorem dependency graphs helps researchers trace proof precedents and foundational definitions intuitively.
- Interactive filtering and export preview panels prevent export errors and improve trust in generated research outputs.

**Weaknesses**  
- Static visual images (PNG/SVG) lack interactivity, making large network graphs difficult to inspect.

**Research Gap**  
- Dynamic web dashboards that link interactive HTML graph visualizers (PyVis/NetworkX) directly with RAG retrieval engines and structured export centers.

**Ideas for MathResearch Studio**  
- Combine interactive PyVis network graphs (`src/ui/pages/graph.py`), symbol search dictionaries (`src/ui/pages/notation.py`), system statistics panels (`src/ui/pages/statistics.py`), and multi-format export engines (`src/ui/pages/export.py`) into the Streamlit dashboard architecture.


