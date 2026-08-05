"""Main Streamlit application entry point for MathResearch Studio."""

import os
import sys
import warnings
from pathlib import Path

# Set environment defaults to suppress unauthenticated HF Hub warnings and parallelism warnings
os.environ.setdefault("HF_HUB_DISABLE_IMPLICIT_TOKEN_WARNING", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
warnings.filterwarnings("ignore", message=".*unauthenticated requests to the HF Hub.*")
warnings.filterwarnings("ignore", category=UserWarning, module="huggingface_hub")

# Ensure project root is on sys.path when launching via `streamlit run src/ui/app.py`
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ui.layout import render_app_layout

if __name__ == "__main__":
    render_app_layout()


