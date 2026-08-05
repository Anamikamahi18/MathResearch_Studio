# Deployment Guide - MathResearch Studio v1.0.0

This guide explains how to install, configure, and run **MathResearch Studio v1.0.0** locally and discusses cloud deployment considerations for future releases.

---

## Local Deployment (Recommended for v1.0.0)

### Why Local Deployment

MathResearch Studio v1.0.0 is designed and verified for **local research workstation deployment**. The application has the following characteristics that make cloud deployment of v1.0.0 non-trivial:

1. **Large ML model dependency**: `torch==2.13.0` + `sentence-transformers==5.6.1` require ~1.5 GB of disk space and PyTorch CPU/GPU inference. This exceeds Streamlit Community Cloud's 1 GB RAM limit and makes cold starts very slow.
2. **Local disk state**: Uploaded PDFs (`uploads/`) and the FAISS vector index (`exports/vector_store/`) are stored on local disk. Cloud platforms without persistent storage (Streamlit Community Cloud) lose this data on every restart.
3. **No FastAPI backend**: v1.0.0 is a Streamlit-only application. FastAPI is listed as a dependency for future use but no backend API server is implemented in v1.0.0.
4. **CPU inference latency**: Embedding generation relies on CPU-only PyTorch inference, which is acceptable locally but would be slow on shared cloud instances.

Cloud deployment with full feature support is planned for **v2.0** (GPU inference, cloud vector database, persistent storage).

---

## Local Deployment: Step-by-Step

### Requirements

| Component | Minimum | Recommended |
|---|---|---|
| **Python** | 3.11 | 3.12 |
| **RAM** | 4 GB | 16 GB |
| **Disk** | 2 GB free | 10 GB free |
| **OS** | Windows 10 / macOS 12 / Ubuntu 20.04 | Windows 11 / macOS 14 / Ubuntu 22.04 |
| **Internet** | Required (first run only — model download ~90 MB) | Broadband |

---

### 1. Clone the Repository

```bash
git clone https://github.com/Anamikamahi18/MathResearch_Studio.git
cd MathResearch_Studio
```

---

### 2. Create and Activate a Virtual Environment

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

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required libraries including Streamlit, PyMuPDF, SentenceTransformers, FAISS, NetworkX, PyVis, FastAPI, and PyTorch.

> **Note**: PyTorch and SentenceTransformers will download the `all-MiniLM-L6-v2` model weights (~90 MB) on first run. Subsequent runs use the locally cached model.

---

### 4. Configure the Application (Optional)

Create a `.env` file in the project root to set optional configuration:

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

> The application runs fully without a `.env` file using the default offline `mock` LLM adapter.

---

### 5. Verify Installation

```bash
python -m pytest
```

Expected output: `225 passed`

---

### 6. Run End-to-End System Check

```bash
python scripts/verify_end_to_end.py
```

Expected output: `OVERALL SYSTEM INTEGRATION STATUS: [PASS]`

---

### 7. Launch the Research Dashboard

```bash
streamlit run src/ui/app.py
```

Open **http://localhost:8501** in your browser.

The Streamlit server will start with the theme and server settings defined in `.streamlit/config.toml`.

---

## Deployment URL

| Deployment | URL | Status |
|---|---|---|
| **Local (v1.0.0)** | `http://localhost:8501` | ✅ Active |
| **Cloud Frontend (v1.0.0)** | Not deployed — see Cloud Deployment Notes | ⏳ v2.0 |
| **Cloud Backend API (v1.0.0)** | Not deployed — see Cloud Deployment Notes | ⏳ v2.0 |

---

## Cloud Deployment Notes for v1.0.0

### Streamlit Community Cloud

**Status**: Partially supported with limitations.

To attempt a Streamlit Community Cloud deployment:

1. Ensure the GitHub repository is **public**.
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect the repository.
3. Set **Main file path** to: `src/ui/app.py`
4. Add secrets in the Streamlit Cloud dashboard under **Settings → Secrets** (equivalent to `.env`).
5. Click **Deploy**.

**Limitations on Streamlit Community Cloud:**
- PyTorch + SentenceTransformers may exceed the 1 GB RAM limit. Consider creating a `requirements_cloud.txt` with `sentence-transformers` pinned to a smaller version or using ONNX runtime instead.
- File uploads and FAISS index will reset on every app restart (no persistent storage).
- First cold start takes 3–5 minutes due to PyTorch model weight downloads.

**Workaround**: Deploy a demo version with pre-embedded sample papers stored in the repository's `exports/` directory (committed into git for demo purposes only).

### Render / Railway (FastAPI Backend)

**Status**: Not applicable for v1.0.0.

No FastAPI backend server is implemented in v1.0.0. All application logic runs inside the Streamlit process. FastAPI is listed as a dependency for future v2.0 backend API implementation.

When a FastAPI backend is built in v2.0, the startup command will be:
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

---

## Directory Layout After First Run

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

## Running CLI Utilities

```bash
# Parse PDFs directly (command line)
python -m src.parser.pipeline tests/sample_papers --output-dir exports/parser_outputs

# End-to-end system verification
python scripts/verify_end_to_end.py

# Performance benchmark
python scripts/benchmark_performance.py
```

---

## Redeployment Procedure

When pulling a new version of the code:

```bash
git pull origin main
pip install -r requirements.txt   # Install any new dependencies
python -m pytest                  # Verify all tests pass
streamlit run src/ui/app.py       # Restart the application
```

---

## Rollback Procedure

To roll back to the previous version:

```bash
git log --oneline -10              # Find the commit hash to roll back to
git checkout <commit-hash>         # Check out the previous version
pip install -r requirements.txt    # Re-install matching dependencies
streamlit run src/ui/app.py        # Restart
```

Or, to roll back to the v1.0.0 tag:
```bash
git checkout v1.0.0
pip install -r requirements.txt
streamlit run src/ui/app.py
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'src'` | Ensure you are running from the project root and the venv is activated. |
| Model download hangs | Set `HF_TOKEN` in `.env` for higher rate limits. |
| `FAISS index not found` warning | Click **Refresh Library** in the Document Library page to rebuild the vector index. |
| Upload fails silently | Check that the `uploads/` directory exists and is writable. |
| Streamlit shows blank page | Clear browser cache and reload. Check terminal for Python exceptions. |
| Port 8501 already in use | Run `streamlit run src/ui/app.py --server.port 8502` to use a different port. |

---

## Support

For bug reports or questions, open a [GitHub Issue](https://github.com/Anamikamahi18/MathResearch_Studio/issues).
