# Gap Analysis

## Overview

This document identifies the practical problems mathematics researchers face when working through large volumes of academic literature and highlights where MathResearch Studio can provide meaningful assistance. The goal is not to automate mathematical discovery, but to reduce friction in reading, organising, searching, and connecting research knowledge.

## What problems do mathematics researchers face when reading many papers?

Mathematics researchers often work across dozens of papers that introduce dense notation, layered definitions, and long proof chains. The main difficulties include understanding unfamiliar terminology, tracing how results depend on earlier lemmas or external references, comparing notational conventions across authors, and retaining key ideas over time. Reading papers is also slow because mathematical writing is highly compressed and often assumes substantial prior background.

## Why are definitions, theorems, and proofs difficult to organise?

Definitions, theorems, lemmas, and proofs are tightly interdependent. A single theorem may rely on many earlier concepts, and those concepts may be defined differently across subfields or papers. Researchers often extract these manually into personal notes, but this process is time-consuming and inconsistent. Proofs add another layer of difficulty because their structure is often informal, spread across paragraphs, and dependent on notation introduced earlier.

## What limitations do current research tools have?

Many current research tools are strong at citation management, general PDF annotation, or broad semantic search, but they usually do not model mathematical content in a structured way. They often treat papers as plain text rather than as collections of definitions, statements, symbols, and proof relationships. Tools focused on symbolic mathematics or theorem proving also do not address the everyday workflow of literature reading and research note organisation.

## Where can AI assist without replacing mathematical reasoning?

AI can assist in extracting document structure, identifying candidate definitions and theorem-like statements, normalising notation references, generating searchable summaries, building dependency graphs, and answering questions grounded in uploaded papers. These tasks support comprehension and navigation. The actual act of verifying proofs, forming conjectures, and producing new mathematics remains with the researcher.

## Which features would genuinely save researchers time?

The most valuable features are likely to be PDF ingestion, automatic extraction of definitions and results, theorem-proof linking, notation dictionaries, paper-level and collection-level search, dependency graph generation, and exportable structured notes. These features reduce repetitive manual note-taking and make it easier to revisit a body of literature after days or weeks.

## What do existing tools miss?

Existing tools often miss the structural richness of mathematical writing. They rarely capture relationships between definitions, lemmas, theorems, and proofs in a form that researchers can browse or query. They also tend to perform poorly on mathematical notation, theorem numbering, and cross-paper comparison of related concepts.

## Why are mathematicians still manually reading papers?

Mathematical papers require careful interpretation, not just information retrieval. Researchers need to judge subtle assumptions, understand proof strategies, resolve notation overload, and decide whether a result is relevant to their own work. Because current tools do not reliably represent these subtleties, manual reading remains essential.

## What is difficult about mathematical notation?

Mathematical notation is highly context-dependent. The same symbol can mean different things across papers, and different authors may use different symbols for the same concept. Notation may also rely on formatting, layout, subscripts, superscripts, and implicit conventions that are hard for generic text-processing systems to interpret correctly.

## What workflow is missing?

A major missing workflow is a research environment that moves seamlessly from paper upload to structured extraction, searchable knowledge, dependency exploration, notation tracking, grounded question answering, and note export. Researchers often assemble this workflow manually using separate tools for storage, annotation, search, and writing.

## Opportunities for MathResearch Studio

- Build a structured reading workflow tailored to mathematical literature rather than general academic PDFs.
- Extract definitions, theorems, lemmas, and proofs into reusable research objects.
- Create dependency graphs that help researchers trace how results build on one another.
- Maintain a notation dictionary that reduces confusion across papers.
- Support search and question answering grounded only in uploaded research documents.
- Generate exportable research notes that researchers can refine for reports, surveys, or thesis writing.
- Reduce time lost to manual note-taking and repeated re-reading of dense papers.
- Provide a practical AI-assisted workflow that complements, rather than replaces, mathematical reasoning.

## Is the Gap Analysis Complete?

It is complete enough for Version 1 planning, but not complete in the research sense.

For product planning, this document already identifies the main workflow problems, the missing capabilities, and the product opportunities.

For stronger evidence, it should be validated with direct input from mathematicians, especially through short surveys or interviews. That means the analysis is currently a well-grounded working draft, not a final academic study.

## Can You Ask Researchers Directly Through a Google Form?

Yes. In fact, you should.

A Google Form is a good way to validate whether the problems identified here are real, frequent, and important to researchers. It helps convert assumptions into evidence.

### What to ask in the form

- How often do they read new papers?
- What is the hardest part of understanding a paper?
- Which tasks take the most time: reading, note-taking, searching, tracking definitions, or following proofs?
- How do they currently manage definitions, theorems, lemmas, and notation?
- What do they dislike about current tools?
- Would they trust AI assistance for summarization, search, or extraction?
- Which features would save them the most time?
- What would make them stop using such a tool?

### How to use the responses

- Rank the pain points by frequency and severity.
- Compare survey answers with the assumptions in this gap analysis.
- Use the results to refine the MVP scope and feature priorities.
- Quote the most common problems in your README, proposal, or project report.

## Gap Analysis of Existing AI Tools for Researchers

The tools below are useful in general research workflows, but none of them fully solve the day-to-day mathematical literature workflow that MathResearch Studio targets.

### ChatGPT

**Strengths**

- Strong general-purpose reasoning and summarization
- Good for brainstorming, drafting, and explanation
- Can help interpret text passages interactively

**Limitations**

- Not grounded by default in a private paper collection
- Can hallucinate citations or technical claims
- Does not natively track theorem-definition-proof structure across uploaded papers
- Weak at preserving exact mathematical notation and document-level provenance

**Gap for MathResearch Studio**

- Need source-grounded answers tied to uploaded papers only
- Need structured extraction of definitions, theorems, lemmas, and proofs
- Need notebook-like research notes rather than generic chat responses

### Gemini

**Strengths**

- Good general document understanding and multimodal support
- Useful for broad summaries and reasoning over long context
- Often helpful for extracting high-level insights from long documents

**Limitations**

- Still not specialized for mathematical literature workflows
- May summarize well but not organize mathematical entities reliably
- Not designed as a dedicated paper-workspace or knowledge-extraction system

**Gap for MathResearch Studio**

- Need repeatable extraction of mathematical structures from PDFs
- Need searchable collections of papers with math-specific indexing
- Need explicit support for notation dictionaries and dependency graphs

### Perplexity

**Strengths**

- Strong web-connected search and source citation behavior
- Convenient for quick literature discovery
- Good for broad research exploration and topic overview

**Limitations**

- Optimized for web search rather than private paper libraries
- Not focused on deep extraction of math structure from PDFs
- Citation quality depends on visible web sources, not internal research artifacts

**Gap for MathResearch Studio**

- Need closed-world search over uploaded papers
- Need extraction and organization of internal research notes
- Need workflow support for definitions, theorem links, and proof traversal

### Claude

**Strengths**

- Strong long-context reading and summarization
- Good at structured writing and document analysis
- Useful for nuanced explanations and synthesis

**Limitations**

- Still a general assistant rather than a dedicated research workflow system
- May not preserve mathematical structure and provenance as a first-class concept
- Not built around local paper ingestion, graph analysis, or note export for researchers

**Gap for MathResearch Studio**

- Need a research-specific interface for uploaded papers
- Need mathematics-aware extraction and retrieval pipelines
- Need support for organizing and exporting research knowledge over time

### Overall Tool Gap Summary

Existing AI tools are strong at conversation, summarization, and general reasoning, but they do not provide an end-to-end mathematical literature workflow.

What is missing is:

- Reliable paper ingestion for mathematical PDFs
- Structured extraction of definitions, theorems, lemmas, and proofs
- Notation dictionaries across papers
- Dependency graphs for mathematical concepts
- Search grounded only in uploaded research material
- Exportable research notes tailored to mathematicians

## Research Questions to Validate Next

- Which parts of reading papers are most painful for mathematicians?
- How often do they need to revisit older papers and reconstruct notation?
- Would they trust AI for extraction if every answer showed supporting evidence?
- What minimum workflow would make them adopt a new tool?
- Which existing AI tool do they already use, and what do they still do manually?

