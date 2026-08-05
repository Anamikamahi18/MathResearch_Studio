# Deployment Guide - MathResearch Studio v1.0.0

This guide explains how to install, configure, and run **MathResearch Studio v1.0.0** for local research use.

---

## Requirements

| Component | Minimum | Recommended |
|---|---|---|
| **Python** | 3.11 | 3.12 |
| **RAM** | 4 GB | 16 GB |
| **Disk** | 2 GB free | 10 GB free |
| **OS** | Windows 10 / macOS 12 / Ubuntu 20.04 | Windows 11 / macOS 14 / Ubuntu 22.04 |
| **Internet** | Required (first run only, for model download) | Broadband |

> **Note**: After the initial `all-MiniLM-L6-v2` model download (~90 MB), the application runs fully offline.

---

## 1. Clone the Repository

```bash
git clone https://github.com/Anamikamahi18/MathResearch_Studio.git
cd MathResearch_Studio
```

---

## 2. Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required libraries including Streamlit, PyMuPDF, SentenceTransformers, FAISS, NetworkX, and PyVis.

---

## 4. Configure the Application (Optional)

Create a `.env` file in the project root:

```env
# Hugging Face Hub token — optional, increases model download rate limits
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# LLM Provider: "mock" (default, fully offline) | "openai" | "ollama"
LLM_PROVIDER=mock

# Upload directory for PDF papers
UPLOAD_DIR=uploads

# Export output directory
EXPORT_DIR=exports
```

> The application works fully without a `.env` file using the default offline `mock` LLM adapter.

---

## 5. Verify Installation

Run the full automated test suite to confirm all dependencies are correctly installed:

```bash
python -m pytest
```

Expected: `225 passed`

---

## 6. Launch the Research Dashboard

```bash
streamlit run src/ui/app.py
```

Open your browser at **http://localhost:8501**

---

## 7. First-Use Workflow

1. Navigate to **📤 Upload Papers** in the sidebar.
2. Drag and drop one or more mathematics PDF research papers.
3. Wait for parsing and indexing to complete (progress shown on screen).
4. Explore your papers via **📚 Document Library**, **🔎 Semantic Search**, **💬 AI Research Assistant**, and other pages.

---

## 8. Running CLI Utilities

**Parse PDFs directly (command line):**
```bash
python -m src.parser.pipeline tests/sample_papers --output-dir exports/parser_outputs
```

**End-to-end system verification:**
```bash
python scripts/verify_end_to_end.py
```

**Performance benchmark:**
```bash
python scripts/benchmark_performance.py
```

---

## 9. Directory Layout After First Run

```
exports/
├── parser_outputs/       # Structured JSON from parsed papers
├── vector_store/         # FAISS vector index (auto-generated, .gitignored)
│   ├── index.faiss
│   └── metadata.json
└── *.md / *.json / *.csv # Downloaded research export files
uploads/                  # Uploaded PDF papers (.gitignored)
```

---

## 10. Stopping the Application

Press `Ctrl+C` in the terminal where Streamlit is running.

---

## Known Limitations

See [known_issues.md](./known_issues.md) for the full list of current system limitations and workarounds.

---

## Support

For bug reports or questions, open a [GitHub Issue](https://github.com/Anamikamahi18/MathResearch_Studio/issues).
