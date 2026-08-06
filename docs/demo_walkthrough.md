# MathResearch Studio v1.0.0 — Live Demo Walkthrough

**Purpose**: Step-by-step operator guide for reproducing the complete live demonstration.  
**Total Duration**: ~5 minutes (live) | ~10 minutes (with commentary)  
**Entry Point**: `streamlit run src/ui/app.py`

---

## Pre-Flight Checks

Before starting any step, confirm:

```
[ ] Python virtual environment is active:  venv\Scripts\activate
[ ] All dependencies installed:            pip install -r requirements.txt
[ ] Application starts cleanly:            streamlit run src/ui/app.py
[ ] Browser opens at:                      http://localhost:8501
[ ] Sample PDF paper is ready
[ ] uploads/ directory exists (created automatically on first run)
```

---

## Step 1 — Launch Application

### Action
```powershell
streamlit run src/ui/app.py
```

### Expected Output
- Terminal prints: `You can now view your Streamlit app in your browser.`
- Browser opens automatically at `http://localhost:8501`.
- Home page renders with dark theme (`#0F172A` background).
- Navigation sidebar visible on the left with 9 module links.
- Home page headline: **MathResearch Studio** visible.

### Possible Failure
**Error**: `ModuleNotFoundError: No module named 'streamlit'`  
**Recovery**: Run `pip install -r requirements.txt` in the activated virtual environment.

**Error**: `Port 8501 is already in use`  
**Recovery**: Run `streamlit run src/ui/app.py --server.port 8502` and open `http://localhost:8502`.

**Error**: `torch` import error or CUDA not found  
**Recovery**: Uninstall and reinstall torch: `pip install torch --index-url https://download.pytorch.org/whl/cpu`

---

## Step 2 — Upload Mathematics Paper

### Action
1. Click **📤 Upload Papers** in the left sidebar.
2. On the Upload page, locate the file upload widget.
3. Click **Browse files** or drag-and-drop your sample mathematics PDF.
4. Confirm the filename appears below the upload widget.
5. Click **Upload & Process** (or equivalent submit button on the page).

### Expected Output
- Progress bar or spinner appears: *"Processing paper..."*
- Success message: *"✅ Paper uploaded and processed successfully."*
- Paper title, authors, and year extracted and displayed.
- Page count and abstract preview shown.

### Possible Failure
**Issue**: File upload widget accepts file but shows no confirmation.  
**Recovery**: Refresh the page (`F5`), re-navigate to Upload Papers, and try again with the same PDF.

**Issue**: *"Failed to parse PDF"* error message.  
**Recovery**: Ensure the PDF has a text layer (not a scanned image). Try a different PDF. Scanned PDFs require OCR pre-processing.

**Issue**: Upload widget is greyed out or non-functional.  
**Recovery**: Clear browser cache (`Ctrl+Shift+R`), restart the Streamlit app, and reload.

---

## Step 3 — Parse Document & View Extraction Results

### Action
1. After upload completes, navigate to **📚 Document Library** in the sidebar.
2. Locate the newly uploaded paper in the library list.
3. Click the paper title or expand arrow to open the detail view.

### Expected Output
- Paper card displays: title, authors, publication year, page count.
- Expandable sections appear for:
  - **Definitions** — formal mathematical definitions with section and page references.
  - **Theorems** — theorem statements extracted with conditions.
  - **Lemmas** — auxiliary mathematical lemmas.
  - **Proofs** — formal proof text linked to theorem statements.
- Entity counts visible (e.g., *"3 Definitions, 5 Theorems, 2 Lemmas, 4 Proofs"*).

### Possible Failure
**Issue**: Paper shows 0 definitions, 0 theorems, 0 lemmas.  
**Cause**: The PDF may not contain formal LaTeX-style mathematical environments (`\begin{theorem}`, `\begin{definition}`).  
**Recovery**: Use a paper with formal mathematical environments (e.g., a paper from arXiv with standard LaTeX formatting). Alternatively, demonstrate that the system correctly identifies "no formal environments found" — this is expected behaviour for informal papers.

**Issue**: Library page shows empty / no papers listed.  
**Recovery**: Navigate back to Upload Papers and re-upload. Verify `uploads/` directory contains the PDF file.

---

## Step 4 — Generate Proof Dependency Graph

### Action
1. Click **🕸️ Research Graph** in the left sidebar.
2. Allow the graph to render (PyVis interactive graph loads in the right panel).
3. Hover over nodes to see entity labels.
4. Click-and-drag nodes to explore the layout.

### Expected Output
- Interactive HTML graph rendered inside the Streamlit page.
- Nodes representing: theorems (one colour), lemmas (another colour), definitions (another colour).
- Directed edges showing dependency relationships (arrows from prerequisite to dependent).
- Graph metrics displayed: node count, edge count, average degree, density.
- If only one paper is uploaded: a smaller graph is expected. Multiple papers produce a denser graph.

### Possible Failure
**Issue**: Graph area shows empty or no graph rendered.  
**Cause**: No dependency relationships found in the uploaded paper (paper may have no explicit theorem-lemma chains).  
**Recovery**: This is valid behaviour. Explain: *"With a single paper, we see [N] nodes. As more papers are added, the cross-paper dependency network grows."*

**Issue**: PyVis graph iframe does not appear, shows `None` or blank.  
**Recovery**: Refresh the Research Graph page. The graph file is written to a temp HTML file; a second render usually resolves this.

---

## Step 5 — Open Notation Dictionary

### Action
1. Click **📖 Notation Dictionary** in the left sidebar.
2. Browse the automatically populated symbol table.
3. Use the search/filter box (if available) to search for a symbol (e.g., "sigma" or "λ").

### Expected Output
- Table of mathematical symbols extracted from all uploaded papers.
- Columns: Symbol, Name/Description, Category (Greek letters, operators, sets, matrices), Source paper.
- Categories visible: *Greek Letters*, *Operators*, *Sets*, *Matrices*, *Variables*.

### Possible Failure
**Issue**: Notation dictionary is empty.  
**Cause**: No LaTeX symbols detected in the uploaded PDF.  
**Recovery**: Use a mathematics paper that explicitly uses LaTeX notation in its PDF text layer (e.g., papers with `\alpha`, `\beta`, `\Sigma` visible in the extracted text).

---

## Step 6 — Perform Semantic Search

### Action
1. Click **🔎 Semantic Search** in the left sidebar.
2. In the search input box, type a natural language query.  
   **Recommended sample queries:**
   - `"compactness of bounded linear operators"`
   - `"proof of convergence in Hilbert space"`
   - `"definition of metric space"`
   - `"eigenvalue decomposition theorem"`
3. Press **Enter** or click the **Search** button.

### Expected Output
- Results panel populates with 3–5 ranked passages.
- Each result card shows:
  - **Relevance score** (0.0–1.0 cosine similarity)
  - **Paper title** and **page number**
  - **Highlighted passage excerpt** from the retrieved chunk.
- Results are ordered by descending relevance.

### Possible Failure
**Issue**: Search returns 0 results.  
**Cause**: FAISS vector index may not yet contain the uploaded paper's embeddings.  
**Recovery**: Go to Document Library → click **🔄 Refresh Library** to rebuild the vector index. Return to Semantic Search and retry.

**Issue**: Embedding model loading takes 30+ seconds on first search.  
**Recovery**: Expected on cold start — SentenceTransformers loads `all-MiniLM-L6-v2` weights (~90 MB) on first call. Subsequent searches are fast (~244 ms).

---

## Step 7 — Ask AI Research Assistant

### Action
1. Click **💬 AI Research Assistant** in the left sidebar.
2. In the input text area, type a research question.  
   **Recommended sample questions:**
   - `"What is the main theorem proved in this paper and what conditions does it require?"`
   - `"Explain the key definitions used in the proof of [theorem name from the paper]."`
   - `"What mathematical tools are used to establish convergence?"`
3. Click **Ask** or press **Ctrl+Enter**.

### Expected Output
The response is rendered in 5 structured sections:

1. **📋 Summary** — one-paragraph direct answer.
2. **📝 Detailed Explanation** — expanded mathematical discussion.
3. **📖 Relevant Definitions** — formal definitions cited from the paper.
4. **📐 Relevant Theorems** — theorem statements cited from the paper.
5. **⚠️ Caveats** — limitations, scope qualifications.

**Below the answer:**
- Inline citations: `[1]`, `[2]` embedded in the answer text.
- **Grounding score**: a 0–1 score indicating what fraction of the answer is evidence-backed.
- **Evidence mapping**: `DIRECT`, `PARTIAL`, or `WEAK` labels on each retrieved chunk.
- **Bibliography**: author, title, section, page number for each cited chunk.

**Response time**: ~34 ms (offline mock LLM adapter).

### Possible Failure
**Issue**: AI Assistant responds with *"⚠️ Insufficient Evidence: No relevant mathematical evidence was retrieved."*  
**Cause**: The query is too general or does not match any uploaded paper content.  
**Recovery**: Rephrase the question using specific terms from the paper. First check Semantic Search to verify relevant passages exist.

**Issue**: Answer appears but shows no citations.  
**Recovery**: This should not occur by design — every response includes citations. Refresh and re-ask. If persistent, this indicates the citation engine returned empty — restart the Streamlit app.

---

## Step 8 — View Citations

### Action
1. Scroll down below the AI assistant's answer.
2. Locate the **Citations** or **Bibliography** section.
3. Review the citation list.

### Expected Output
- Numbered citation list, e.g.:
  ```
  [1] Author(s) (Year). Paper Title, Section Name, pp. X–Y. [Chunk ID: abc123]
  [2] Author(s) (Year). Paper Title, Section Name, pp. X–Y. [Chunk ID: def456]
  ```
- Inline references `[1]`, `[2]` within the answer text are visible.
- Grounding score shown as a coloured progress indicator or percentage.

### Possible Failure
**Issue**: Citations section missing entirely.  
**Recovery**: The CitationEngine requires at least one retrieved chunk. Retry with a more specific research question after verifying content exists via Semantic Search.

---

## Step 9 — Open Statistics Dashboard

### Action
1. Click **📊 Statistics** in the left sidebar.
2. Review all displayed metric cards and charts.

### Expected Output
Metric cards displaying:
- **Total Papers Catalogued** — count of uploaded PDFs.
- **Definitions Extracted** — total definition entities found.
- **Theorems Extracted** — total theorem entities found.
- **Lemmas Extracted** — total lemma entities found.
- **Proofs Extracted** — total proof entities found.
- **Vector Passages Indexed** — total FAISS vector chunks.
- **Graph Nodes** — total dependency graph vertices.
- **Graph Edges** — total dependency graph directed edges.

Charts:
- **Statement Type Distribution** — bar or pie chart of entity types.
- **Publication Year Distribution** — histogram of papers by year.

### Possible Failure
**Issue**: All statistics show 0.  
**Recovery**: Navigate to Document Library and ensure papers are listed. If library is empty, re-upload the sample PDF and return to Statistics.

---

## Step 10 — Export Research Notes

### Action
1. Click **💾 Export Center** in the left sidebar.
2. Review the available export format buttons:
   - **Markdown** — research notes for thesis writing.
   - **JSON** — structured data for downstream analysis.
   - **CSV** — paper metadata spreadsheet.
   - **PDF** — printable research summary.
3. Click one export button to trigger a download.

### Expected Output
- File download begins immediately in the browser.
- Filename is clean and descriptive (e.g., `paper_summaries.md`, `research_notes.json`).
- Downloaded file contains structured content matching what was shown in the Document Library.

### Possible Failure
**Issue**: Download button triggers but no file downloads.  
**Recovery**: Check browser download permissions. Allow downloads from `localhost:8501`. Try a different export format (Markdown usually works most reliably).

**Issue**: Exported Markdown file is empty.  
**Recovery**: Ensure papers are in the Document Library before exporting. The ExportService reads from the parsed JSON outputs in `uploads/`.

---

## Step 11 — Shutdown Application

### Action
1. Return to the terminal where Streamlit is running.
2. Press `Ctrl+C` to stop the server.

### Expected Output
```
  Stopping...
```
Terminal returns to prompt. Browser tab shows Streamlit's disconnected state.

### Notes
- All uploaded papers persist in `uploads/` between sessions.
- The FAISS vector index persists in `exports/vector_store/`.
- On next launch, the library is restored automatically.

---

## Full Workflow Summary Table

| # | Step | Page | Time | Key Output |
|---|---|---|---|---|
| 1 | Launch app | Terminal | 5 sec | Browser opens at localhost:8501 |
| 2 | Upload PDF | 📤 Upload Papers | 30 sec | Paper parsed and catalogued |
| 3 | View extraction | 📚 Document Library | 30 sec | Definitions, theorems, lemmas, proofs listed |
| 4 | Dependency graph | 🕸️ Research Graph | 20 sec | Interactive directed graph rendered |
| 5 | Notation dictionary | 📖 Notation Dictionary | 15 sec | Symbol table with categories |
| 6 | Semantic search | 🔎 Semantic Search | 20 sec | Ranked passages with relevance scores |
| 7 | Ask AI assistant | 💬 AI Research Assistant | 45 sec | 5-section answer with citations |
| 8 | View citations | 💬 AI Research Assistant | 15 sec | Numbered bibliography, grounding score |
| 9 | Statistics | 📊 Statistics | 15 sec | Entity counts, year distribution |
| 10 | Export | 💾 Export Center | 15 sec | File downloaded |
| 11 | Shutdown | Terminal | 5 sec | Ctrl+C, server stopped |

**Total demo time: ~3.5–5 minutes**

---

*MathResearch Studio v1.0.0 · Live Demo Walkthrough · 2026*
