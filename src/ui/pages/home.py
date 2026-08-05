"""Home / Research Overview landing page view."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

from src.ui.components.page_title import render_page_title
from src.ui.state import (
    get_dashboard_service,
    get_document_service,
    set_current_page,
)


def render_home_page() -> None:
    """Render the Home / Research Overview landing page."""
    render_page_title(
        title="Research Overview",
        subtitle="Central AI workspace for mathematical paper analysis, knowledge graph exploration, and grounded RAG research assistance.",
        icon="🏠",
        badge="Workspace Overview",
    )

    doc_service = get_document_service()
    dash_service = get_dashboard_service()
    papers = doc_service.list_papers()

    # Quick System Metrics Bar
    stats = dash_service.get_statistics()
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Catalog Papers", stats["paper_count"])
    with m2:
        st.metric("Vector Chunks", stats["total_vector_chunks"])
    with m3:
        st.metric("Extracted Theorems", stats["theorem_count"])
    with m4:
        st.metric("Graph Nodes", stats["graph_nodes"])

    st.markdown("<br>", unsafe_allow_html=True)

    # Core Workflow Action Cards Grid
    st.markdown("### 🚀 End-to-End Research Workflow")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="mrs-card">
                <h4>📥 1. Ingest Literature</h4>
                <p style="color: #94A3B8; font-size: 0.85rem;">Upload mathematics PDF preprints, parse sections, and extract definitions, theorems, lemmas, and proofs.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Go to PDF Upload", use_container_width=True, key="btn_home_upload"):
            set_current_page("upload")
            st.rerun()

    with c2:
        st.markdown(
            """
            <div class="mrs-card">
                <h4>🔍 2. Semantic Search</h4>
                <p style="color: #94A3B8; font-size: 0.85rem;">Search natural language math queries across uploaded papers with cosine relevance scores and chunk highlights.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Go to Search", use_container_width=True, key="btn_home_search"):
            set_current_page("search")
            st.rerun()

    with c3:
        st.markdown(
            """
            <div class="mrs-card">
                <h4>🤖 3. AI Assistant</h4>
                <p style="color: #94A3B8; font-size: 0.85rem;">Ask source-grounded research questions with sentence-level evidence mapping and academic citations.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Go to AI Assistant", use_container_width=True, key="btn_home_assistant"):
            set_current_page("assistant")
            st.rerun()

    c4, c5, c6 = st.columns(3)

    with c4:
        st.markdown(
            """
            <div class="mrs-card">
                <h4>🕸️ 4. Research Graph</h4>
                <p style="color: #94A3B8; font-size: 0.85rem;">Explore interactive theorem dependency networks, antecedent proof chains, and statement node degrees.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Go to Research Graph", use_container_width=True, key="btn_home_graph"):
            set_current_page("graph")
            st.rerun()

    with c5:
        st.markdown(
            """
            <div class="mrs-card">
                <h4>🔣 5. Notation Dictionary</h4>
                <p style="color: #94A3B8; font-size: 0.85rem;">Search and browse extracted LaTeX mathematical symbols, domain categories, and definitions.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Go to Notation Dict", use_container_width=True, key="btn_home_notation"):
            set_current_page("notation")
            st.rerun()

    with c6:
        st.markdown(
            """
            <div class="mrs-card">
                <h4>📤 6. Export Center</h4>
                <p style="color: #94A3B8; font-size: 0.85rem;">Export structured research notes, summaries, and graphs to Markdown, JSON, CSV, and PDF formats.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Go to Export Center", use_container_width=True, key="btn_home_export"):
            set_current_page("export")
            st.rerun()

    # Recent Library Summary
    st.divider()
    st.markdown("### 📚 Ingested Library Catalog")
    if papers:
        for p in papers[:3]:
            st.markdown(
                f"- **{p.get('title', 'Untitled')}** (`{p.get('paper_id')}`) &bull; "
                f"Authors: *{', '.join(p.get('authors', [])) or 'N/A'}* &bull; "
                f"Sections: `{p.get('section_count', 0)}` &bull; Chunks: `{p.get('chunk_count', 0)}`"
            )
    else:
        st.info("No papers currently ingested. Click **Go to PDF Upload** above to import your first paper!")


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from src.ui.layout import render_app_layout
    set_current_page("home")
    render_app_layout()
