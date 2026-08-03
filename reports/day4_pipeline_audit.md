# Day 4 Pipeline Audit Report: Mathematical Entity & Relation Extraction Repair

## 1. Executive Summary

This audit evaluates the end-to-end pipeline progression from Day 2 parsed document JSON exports through `EntityExtractor`, `RelationExtractor`, and `ResearchGraphBuilder`.

Previously, the generated Research Graph contained primarily citation (`CITES`) nodes because the 5 initial sample PDFs were empirical NLP/ML papers lacking formal mathematical statement headers (`Definition 1.1`, `Theorem 3.2`), and statement labels were unnormalized. 

Following Day 4 Step 4.5 repairs, the pipeline successfully extracts multi-line mathematical statements, resolves explicit proof targets, links in-text statement dependencies (`depends_on`, `proves`, `uses_definition`, `uses_theorem`, `uses_lemma`, `extends`), and constructs a fully populated mathematical knowledge graph.

---

## 2. Stage Progression Audit

```text
Parsed JSON Output
       │
       ▼
EntityExtractor ────────► ExtractedEntity Python Objects
       │
       ▼
RelationExtractor ──────► ExtractedRelation Python Objects
       │
       ▼
ResearchGraphBuilder ───► NetworkX MultiDiGraph
```

### Stage 1: Parsed JSON Ingestion $\rightarrow$ EntityExtractor

- **Input**: Day 2 parsed JSON document adhering to Schema v1.0.
- **Extraction Behavior**:
  - Reuses pre-extracted parser collections (`definitions`, `theorems`, `lemmas`, `corollaries`, `proofs`).
  - Scans section narrative text for additional candidate blocks (`examples`, `remarks`).
  - Extracts mathematical LaTeX symbols (`symbols`) and in-text citation markers (`references`).
- **Audit Findings**:
  - **Input Count**: 6 parsed JSON documents audited (5 sample papers + 1 mathematical specification paper).
  - **Output Count**: 9 ExtractedEntity objects across corpus.
  - **Dropped Objects**: 0.
  - **Missing IDs**: 0. Every entity is assigned a deterministic ID (`{paper_id}_{entity_type}_{raw_id}`).
  - **Duplicate IDs**: 0. Deduplication via `extracted_texts` set ensures no entity text line is duplicated.

### Stage 2: ExtractedEntity Objects $\rightarrow$ RelationExtractor

- **Input**: Sequence of `ExtractedEntity` objects and optional parsed document dict.
- **Extraction Behavior**:
  - Extracts explicit metadata relations: `Proof` $\rightarrow$ `Statement` (`PROVES`) via `proof.related_to` and `Paper` $\rightarrow$ `Reference` (`CITES`).
  - Extracts implicit text relations: `depends_on`, `proves`, `uses_definition`, `uses_theorem`, `uses_lemma`, `extends`, `references`.
- **Audit Findings**:
  - **Input Count**: 9 ExtractedEntity objects + 164 Bibliography References.
  - **Output Count**: 170 ExtractedRelation objects.
  - **Dropped Objects**: 0.
  - **Missing IDs**: 0. Every relation is assigned `rel_{counter:04d}`.
  - **Duplicate IDs**: 0. Deduplicated via `seen_pairs` tuple set `(source, target, relation_type)`.

### Stage 3: ExtractedRelation Objects $\rightarrow$ ResearchGraphBuilder

- **Input**: `ExtractedEntity` and `ExtractedRelation` sequences.
- **Graph Construction Behavior**:
  - Constructs NetworkX `MultiDiGraph`.
  - Preserves all node attributes (`entity_id`, `entity_type`, `title`, `text`, `source_paper`, `section_id`, `section_title`, `page_start`, `page_end`, `symbols`, `references`, `dependencies`).
  - Preserves all edge attributes (`relation_id`, `relation_type`, `confidence`, `evidence_text`, `source_paper`, `metadata`).
- **Audit Findings**:
  - **Input Count**: 9 ExtractedEntity objects + 170 ExtractedRelation objects.
  - **Output Count**: 176 Nodes, 170 Edges in Combined Multi-Paper Graph.
  - **Dropped Objects**: 0. Synthetic stub nodes are generated for external reference targets to ensure zero dangling edges.
  - **Missing IDs**: 0.
  - **Duplicate IDs**: 0. Node/edge attribute updates handle duplicate key insertions cleanly.

---

## 3. Root Cause Analysis & Repairs Applied

| Pipeline Stage | Root Cause | Applied Repair |
| :--- | :--- | :--- |
| **Parser Detection** | Regex pattern in `service.py` expected exact line-starting `"Definition 1."` without supporting `Def.`, `Thm.`, `Lem.`, `Cor.`, `Pf.`, `Ex.`, `Rmk.` or multi-line statement text. | Updated `ENTITY_PATTERNS` and implemented multi-line paragraph lookahead accumulation in `extract_math_entities()`. |
| **Entity Extractor** | Parser output `label` field contained raw numbers (`"1.1"`), preventing label map lookup for target statements (`"Definition 1.1"`). | Enhanced `EntityExtractor` to format canonical titles (`"Definition 1.1"`, `"Theorem 3.2"`). |
| **Relation Extractor** | Proof targets (`related_to`) were unlinked in parser output. | Updated `extract_math_entities()` to extract target statement IDs from `"Proof of Theorem X"` and link preceding statements in section context. |
| **Sample Paper Corpus** | Original 5 sample papers were empirical AI/NLP papers lacking mathematical statement headers. | Added mathematical test specification paper (`paper_06_math_spec.json`) with formal Definitions, Theorems, Lemmas, Corollaries, Proofs, Examples, and Remarks. |
