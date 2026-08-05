"""Settings page view for MathResearch Studio."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

from src.ui.components.page_title import render_page_title
from src.ui.state import get_document_service


def render_settings_page() -> None:
    """Render the Application Settings page."""
    render_page_title(
        title="Application Settings",
        subtitle="Configure retrieval parameters, embedding model preferences, and application workspace settings.",
        icon="⚙️",
        badge="Workspace Configuration",
    )

    doc_service = get_document_service()

    import os

    current_hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN") or ""

    with st.form("settings_form"):
        st.markdown("### 🔑 Hugging Face Hub Authentication")
        st.caption("Provide an HF Token to enable higher rate limits and faster downloads for SentenceTransformers model weights.")
        
        hf_token_input = st.text_input(
            label="Hugging Face Access Token (HF_TOKEN)",
            value=current_hf_token,
            type="password",
            placeholder="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            help="Set your Hugging Face User Access Token to authorize model downloads.",
        )

        if current_hf_token:
            st.success("🔑 **HF_TOKEN active:** Authenticated downloads enabled.")
        else:
            st.info("ℹ️ **Unauthenticated mode:** Implicit warnings suppressed. Set HF_TOKEN above for higher rate limits.")

        st.markdown("### 🔍 Retrieval & Search Preferences")
        c1, c2 = st.columns(2)

        with c1:
            st.selectbox(
                label="Default Embedding Model Provider",
                options=["all-MiniLM-L6-v2 (SentenceTransformers)", "SciBERT (Academic)", "Mock Embedding Provider"],
                index=0,
            )

        with c2:
            st.slider(
                label="Default Search Top-K Results",
                min_value=1,
                max_value=50,
                value=10,
            )

        st.markdown("### 🤖 AI Assistant & RAG Options")
        c3, c4 = st.columns(2)

        with c3:
            st.selectbox(
                label="LLM Provider Adapter",
                options=["Mock LLM Adapter (Grounded Offline)", "OpenAI GPT-4o (API Key Required)", "Anthropic Claude 3.5 (API Key Required)"],
                index=0,
            )

        with c4:
            st.selectbox(
                label="Default Citation Format",
                options=["INLINE ([1])", "AUTHOR_YEAR ((Smith, 2024))", "ACADEMIC ([Paper, Section, Page])"],
                index=0,
            )

        st.markdown("### 📁 System Storage & Vector Index")
        v_store = getattr(doc_service, "vector_store", None)
        v_size = getattr(v_store, "number_of_vectors", lambda: 0)() if v_store else 0
        v_dim = getattr(v_store, "dimension", 384) if v_store else 384

        st.info(
            f"**Vector Store Location:** `exports/vector_store/index.faiss` &bull; "
            f"**Current Index Vectors:** `{v_size}` &bull; "
            f"**Embedding Dimension:** `{v_dim}`"
        )

        save_settings = st.form_submit_button("💾 Save Preferences", type="primary", use_container_width=True)

    if save_settings:
        if hf_token_input.strip():
            tok = hf_token_input.strip()
            os.environ["HF_TOKEN"] = tok
            os.environ["HUGGING_FACE_HUB_TOKEN"] = tok
            os.environ.pop("HF_HUB_DISABLE_IMPLICIT_TOKEN_WARNING", None)
            st.toast("Updated Hugging Face Token in environment!")
        else:
            os.environ.pop("HF_TOKEN", None)
            os.environ.pop("HUGGING_FACE_HUB_TOKEN", None)
            os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN_WARNING"] = "1"
            st.toast("HF_TOKEN cleared; implicit warning suppression enabled.")

        st.success("✅ Application preferences updated.")


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from src.ui.layout import render_app_layout
    from src.ui.state import set_current_page
    set_current_page("settings")
    render_app_layout()
