# Research Directory

This directory stores supplementary research materials for MathResearch Studio — sample papers, annotation data, and research experiment outputs.

## Structure

```
research/
├── sample_papers/        # Sample PDF mathematics papers for testing and demos
│   └── (add PDF files here)
│
├── annotations/          # Manually annotated ground-truth entity extractions
│   └── (add .json annotation files here)
│
├── experiments/          # Research experiment notes and results
│   └── (add experiment markdown files here)
│
└── references/           # Key reference papers cited in the project
    └── (add citation files or PDF links here)
```

## Sample Papers

To use MathResearch Studio, you need at least one text-layer mathematics PDF.

### Where to Find Mathematics PDFs

- **arXiv.org** — Free, open-access mathematics preprints: [arxiv.org/list/math/recent](https://arxiv.org/list/math/recent)
- **Project Euclid** — Open-access journals
- **EMS Press** — European Mathematical Society open-access papers

### Recommended Sample Papers (arXiv)

| Paper | Topic | arXiv ID |
|---|---|---|
| "An Introduction to Graph Theory" | Graph theory fundamentals | Search on arXiv |
| "Introduction to Functional Analysis" | Functional analysis | Search on arXiv |
| "Elementary Number Theory" | Number theory | Search on arXiv |

### Adding Sample Papers

1. Download a text-layer PDF from arXiv
2. Place it in `research/sample_papers/`
3. Launch the application: `streamlit run src/ui/app.py`
4. Go to **Upload Papers** → drag and drop the PDF

> **Note**: Only text-layer PDFs work in v1.0.0. Scanned image PDFs are not yet supported. LaTeX-generated arXiv papers work well.

## Annotation Data

Ground-truth annotations for entity extraction evaluation are stored as JSON:

```json
{
  "paper_id": "sample_paper_001",
  "entities": [
    {
      "type": "theorem",
      "text": "Every compact subset of a Hausdorff space is closed.",
      "page": 5,
      "section": "2.3 Compactness"
    }
  ]
}
```

To contribute annotations, see [`CONTRIBUTING.md`](../CONTRIBUTING.md).

## Research Experiments (v2.0+)

Future research experiment notebooks will be stored in [`notebooks/`](../notebooks/) and results documented here.

---

*MathResearch Studio v1.0.0 · Research Directory*
