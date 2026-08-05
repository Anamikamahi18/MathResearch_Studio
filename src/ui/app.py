"""Main Streamlit application entry point for MathResearch Studio."""

import sys
from pathlib import Path

# Ensure project root is on sys.path when launching via `streamlit run src/ui/app.py`
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ui.layout import render_app_layout

if __name__ == "__main__":
    render_app_layout()

