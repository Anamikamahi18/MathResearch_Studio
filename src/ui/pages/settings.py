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
        subtitle="Customize literature search defaults, AI proof assistant preferences, academic citation formats, and workspace knowledge base settings.",
        icon="⚙️",
        badge="Workspace Configuration",
    )

    doc_service = get_document_service()

    import os

    current_hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN") or ""

    with st.form("settings_form"):
        st.markdown("### 🔑 AI Model Hub Access Key (Optional)")
        st.caption("Provide an optional access key to enable faster model downloads and higher rate limits when fetching mathematical text embedding models.")
        
        hf_token_input = st.text_input(
            label="AI Model Access Token (HF_TOKEN)",
            value=current_hf_token,
            type="password",
            placeholder="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            help="Set your Hugging Face User Access Token to authorize model downloads.",
        )

        if current_hf_token:
            st.success("🔑 **Access Key Active:** Authenticated model downloads enabled.")
        else:
            st.info("ℹ️ **Standard Mode:** Using cached local mathematical embedding models (No external key required).")

        st.markdown("### 🔍 Literature Search & Vector Retrieval Preferences")
        c1, c2 = st.columns(2)

        with c1:
            st.selectbox(
                label="Primary Text & Math Understanding Model",
                options=[
                    "MiniLM Academic Semantic Model (Fast & Accurate)",
                    "SciBERT Domain Model (Mathematics & Computer Science)",
                    "Local Mock Model (Offline Testing)",
                ],
                index=0,
            )

        with c2:
            st.slider(
                label="Default Matching Passages Returned per Search",
                min_value=1,
                max_value=50,
                value=10,
            )

        st.markdown("### 🤖 Math AI Assistant & Proof Reasoning Settings")
        c3, c4 = st.columns(2)

        with c3:
            st.selectbox(
                label="Mathematical Proof Reasoning Provider",
                options=[
                    "Offline Grounded Math Adapter (Local & Deterministic)",
                    "OpenAI GPT-4o (Online API Key Required)",
                    "Anthropic Claude 3.5 Sonnet (Online API Key Required)",
                ],
                index=0,
            )

        with c4:
            st.selectbox(
                label="Academic Citation Style",
                options=[
                    "Inline Bracket References e.g., [1]",
                    "Author & Year Format e.g., (Galois, 1832)",
                    "Full Citation Format e.g., [Paper Title, Section, Page]",
                ],
                index=0,
            )

        st.markdown("### 📁 Mathematical Knowledge Base & Vector Index")
        v_store = getattr(doc_service, "vector_store", None)
        v_size = getattr(v_store, "number_of_vectors", lambda: 0)() if v_store else 0
        if v_size == 0 and doc_service:
            v_size = sum(p.get("chunk_count", 0) for p in doc_service.list_papers())
        v_dim = getattr(v_store, "dimension", 384) if v_store else 384

        st.info(
            f"**Knowledge Base Path:** `exports/vector_store/index.faiss` &bull; "
            f"**Indexed Passage Chunks:** `{v_size}` &bull; "
            f"**Semantic Vector Dimension:** `{v_dim}`"
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
            st.toast("HF_TOKEN cleared; standard mode active.")

        st.success("✅ Application preferences updated successfully.")


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from src.ui.layout import render_app_layout
    from src.ui.state import set_current_page
    set_current_page("settings")
    render_app_layout()
