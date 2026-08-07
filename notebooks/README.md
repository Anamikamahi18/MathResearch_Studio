# Notebooks Directory

This directory stores Jupyter notebooks for MathResearch Studio — for exploration, benchmarking, and research analysis.

## Planned Notebooks

```
notebooks/
├── 01_parser_exploration.ipynb        # Explore PDF parsing results interactively
├── 02_embedding_analysis.ipynb        # Visualise embedding distributions and clusters
├── 03_rag_pipeline_walkthrough.ipynb  # Step-by-step RAG pipeline demonstration
├── 04_graph_analysis.ipynb            # Analyse the proof dependency graph
├── 05_benchmark_results.ipynb         # Reproduce and visualise performance benchmarks
└── 06_research_workflow_demo.ipynb    # End-to-end research workflow demonstration
```

## Status

Notebooks are planned for **Version 2.0** as interactive companions to the application.  
For v1.0.0, use the Streamlit UI directly: `streamlit run src/ui/app.py`

## Running Notebooks (When Available)

```bash
# Activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux

# Install notebook dependencies
pip install jupyter notebook ipykernel

# Launch Jupyter
jupyter notebook
```

## Benchmark Reproduction

To reproduce the v1.0.0 performance benchmarks without notebooks:

```bash
python scripts/benchmark_performance.py
```

Results are documented in [`docs/performance.md`](../docs/performance.md).

---

*MathResearch Studio v1.0.0 · Notebooks Directory*
