# Research Graph Design Specification

## 1. Overview & Concept

The **Mathematical Research Graph** in MathResearch Studio is a structured knowledge representation of mathematical literature. Unlike general scientific knowledge graphs that treat papers as monolithic text nodes or simple citation networks, the Research Graph extracts fine-grained mathematical entities—**Definitions, Theorems, Lemmas, Corollaries, Proofs, Examples, and Remarks**—and connects them through directed, semantic dependency edges.

---

## 2. Fundamental Questions & Design Principles

### Q1: What is a mathematical knowledge graph?
A mathematical knowledge graph (MKG) is a directed property multigraph $G = (V, E)$ where nodes $V$ represent discrete mathematical statement blocks, definitions, proofs, equations, or papers, and edges $E$ represent logical dependencies, proof derivations, definition usages, extensions, and bibliographic citations.

### Q2: Which mathematical entities become graph nodes?
Graph nodes correspond to structural statement objects extracted by `EntityExtractor`:
- **Definition**: Formal definitions of mathematical concepts, structures, or operators.
- **Theorem**: Major mathematical statements established by proof.
- **Lemma**: Auxiliary helper statements supporting major theorems.
- **Corollary**: Direct implications following immediately from a theorem.
- **Proof**: Multi-line deduction blocks verifying a theorem, lemma, or corollary.
- **Example**: Concrete mathematical illustrations or counterexamples.
- **Remark**: Explanatory notes, historical context, or informal remarks.
- **Reference**: Bibliographic publication references cited by papers.
- **Paper / Section**: Structural document containers.

### Q3: Which relationships become graph edges?
Graph edges correspond to semantic relations identified by `RelationExtractor`:
- `depends_on`: Statement $A$ relies on statement $B$.
- `proves`: Proof $P$ verifies statement $T$ ($P \xrightarrow{\text{PROVES}} T$).
- `uses_definition`: Statement or proof utilizes Definition $D$.
- `uses_theorem`: Statement or proof invokes Theorem $T$.
- `uses_lemma`: Statement or proof invokes Lemma $L$.
- `extends`: Statement $A$ generalizes or extends previous Theorem $B$.
- `cites`: Paper $P_1$ cites bibliographic Reference $R_2$ or Paper $P_2$.

### Q4: How should proofs connect to theorems?
Every `Proof` node connects to its target `Theorem`, `Lemma`, or `Corollary` node via a directed `proves` edge:
$$\text{Proof node (prf\_001)} \xrightarrow{\text{PROVES}} \text{Theorem node (thm\_001)}$$
If explicit target mapping (`proof.related_to`) is available, it is linked directly. If unlinked, text-based coreference matching (`"Proof of Theorem 3.2"`) or section proximity links the proof to the nearest preceding statement.

### Q5: How should citations connect papers?
Citations connect paper nodes or statement nodes to bibliographic `Reference` nodes:
$$\text{Paper node (paper\_A)} \xrightarrow{\text{CITES}} \text{Reference node (ref\_001)}$$
When multiple papers in the corpus cite the same reference or when paper $A$ cites paper $B$, cross-paper edges link independent graphs into a unified research graph collection.

---

## 3. Node Attributes Schema

Every graph node preserves comprehensive document metadata:
- `entity_id`: Unique deterministic identifier (`{paper_id}_{entity_type}_{raw_id}`).
- `entity_type`: Category string (`definition`, `theorem`, `lemma`, `corollary`, `proof`, `example`, `remark`, `reference`, `paper`, `section`).
- `title`: Canonical label (`"Definition 1.1"`, `"Theorem 3.2"`).
- `text`: Complete text body snippet.
- `source_paper`: Paper title or file name.
- `section_id`: Parent section ID (`"s1"`).
- `section_title`: Parent section heading.
- `page_start` & `page_end`: Page range.
- `symbols`: List of LaTeX mathematical symbols (`["\\chi(G)", "V", "E"]`).
- `references`: Extracted citation identifiers.

---

## 4. Edge Attributes Schema

Every graph edge preserves relation metadata:
- `relation_id`: Unique edge key (`rel_0001`).
- `relation_type`: Edge category (`depends_on`, `proves`, `uses_definition`, `uses_theorem`, `uses_lemma`, `extends`, `cites`).
- `confidence`: Confidence score (0.0 – 1.0).
- `evidence_text`: Extracted sentence text serving as evidence for the relationship.
- `source_paper`: Paper title.
- `metadata`: Additional rule context or extraction mode metadata.
