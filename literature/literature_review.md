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
