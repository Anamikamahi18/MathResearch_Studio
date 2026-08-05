# Research Note & Knowledge Export Design Specification

## 1. Executive Summary

The **Export Center** in **MathResearch Studio v1** provides structured research knowledge export capabilities. Researchers can extract paper summaries, search results, AI Q&A transcripts, notation dictionaries, dependency graph metrics, and system statistics into standardized file formats: **Markdown (`.md`)**, **JSON (`.json`)**, **CSV (`.csv`)**, and **PDF (`.pdf`)**.

The export functionality is implemented in `src/application/export_service.py` and exposed to the user workspace in `src/ui/pages/export.py`.

---

## 2. Export Format Matrix

| Export Target Data | Markdown (`.md`) | JSON (`.json`) | CSV (`.csv`) | PDF (`.pdf`) | Primary Use Case |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Paper Metadata & Summaries** | ✅ | ✅ | ✅ | ✅ | Literature review tables, paper catalog indexing |
| **Search Results & History** | ✅ | ✅ | ✅ | ✅ | Audit logging of literature search queries |
| **AI Q&A Conversations** | ✅ | ✅ | ✅ | ✅ | Research survey drafts, Q&A transcripts |
| **Notation Dictionary** | ✅ | ✅ | ✅ | ✅ | Symbol reference tables for thesis writing |
| **Dependency Graph Metrics** | ✅ | ✅ | ✅ | ✅ | Network topology analysis, graph degree tables |
| **Dashboard Statistics** | ✅ | ✅ | ✅ | ✅ | System performance and catalog metrics |

---

## 3. Data Serialization & Format Schemas

### 1. Markdown (`.md`) Schema
```markdown
# Research Query Notes

**Question**: What is the definition of a Riemannian Metric?
**Guardrail Decision**: `allow` (Status: `success`)
**Reason**: Question directly answered by catalog evidence
**Confidence**: `0.9421`

## Answer
A Riemannian metric g on a smooth manifold M is a smooth inner product tensor field...

## Citations
- [1] Riemann, B. (1854), "Differential Geometry and Riemannian Manifolds", Section 1, p. 2

## Bibliography
- Riemann, B. Göttinger Abhandlungen, 1854. DOI: 10.1000/riemann.1854
```

### 2. JSON (`.json`) Schema
```json
{
  "export_metadata": {
    "generated_at": "2026-08-05T10:00:00Z",
    "target": "Paper Metadata & Summaries",
    "paper_count": 2
  },
  "papers": [
    {
      "paper_id": "paper_001",
      "title": "On the Hypotheses Which Lie at the Bases of Geometry",
      "authors": ["Bernhard Riemann"],
      "year": 1854,
      "sections_count": 5,
      "chunks_count": 12
    }
  ]
}
```

### 3. CSV (`.csv`) Schema
```csv
paper_id,title,authors,year,sections_count,chunks_count
paper_001,"On the Hypotheses Which Lie at the Bases of Geometry","['Bernhard Riemann']",1854,5,12
```

---

## 4. Export Workflow Architecture

```
+-----------------------------------------------------------------------------------+
| 1. EXPORT CENTER UI (`src/ui/pages/export.py`)                                   |
| - Select Target Data Category                                                     |
| - Select Target Format (MD, JSON, CSV, PDF)                                       |
| - Select Paper Scope & Toggle Features                                           |
| - Render Real-Time Configuration Preview Card                                     |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| 2. APPLICATION SERVICE LAYER (`src/application/export_service.py`)               |
| - `export_summaries()` / `export_research_notes()`                                |
| - Data serialization, JSON formatting, Markdown rendering, CSV DictWriter        |
| - Writes output file to `exports/` folder                                         |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| 3. FILE DOWNLOAD & HISTORY AUDIT                                                  |
| - Direct browser file download via `st.download_button()`                         |
| - Session state export history tracking (`st.session_state['export_history']`)    |
+-----------------------------------------------------------------------------------+
```
