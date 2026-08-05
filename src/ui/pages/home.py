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
        title="Mathematics Research Overview",
        subtitle="Interactive AI workspace for mathematical paper analysis, LaTeX equation parsing, theorem dependency networks, and grounded literature Q&A.",
        icon="🏠",
        badge="Math Studio Workspace v1.0.0",
    )

    doc_service = get_document_service()
    dash_service = get_dashboard_service()
    papers = doc_service.list_papers()

    # Quick System Metrics Bar
    stats = dash_service.get_statistics()
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Ingested Papers", stats.get("paper_count", 0))
    with m2:
        st.metric("Indexed Passages", stats.get("total_vector_chunks", 0))
    with m3:
        st.metric("Theorems & Definitions", stats.get("theorem_count", 0) + stats.get("definition_count", 0))
    with m4:
        st.metric("Statement Connections", stats.get("graph_nodes", 0))

    st.markdown("<br>", unsafe_allow_html=True)

    # Core Workflow Action Cards Grid
    st.markdown("### 🚀 End-to-End Research Workflow")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="mrs-card">
                <h4>📥 1. Upload Math Papers</h4>
                <p style="color: #94A3B8; font-size: 0.85rem;">Upload mathematical research PDFs to extract section hierarchies, inline & display LaTeX formulas, definitions, theorems, lemmas, and proofs.</p>
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
                <h4>🔍 2. Mathematical Search</h4>
                <p style="color: #94A3B8; font-size: 0.85rem;">Search natural language math queries, theorem names, or LaTeX concepts across uploaded papers with relevance scores and passage excerpts.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Go to Math Search", use_container_width=True, key="btn_home_search"):
            set_current_page("search")
            st.rerun()

    with c3:
        st.markdown(
            """
            <div class="mrs-card">
                <h4>🤖 3. Math AI Assistant</h4>
                <p style="color: #94A3B8; font-size: 0.85rem;">Ask research questions across your mathematical library backed by sentence-level evidence mapping, proof step tracing, and academic citations.</p>
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
                <h4>🕸️ 4. Theorem Dependency Network</h4>
                <p style="color: #94A3B8; font-size: 0.85rem;">Explore interactive statement networks showing how theorems depend on prior definitions, lemmas, and proof antecedents.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Go to Theorem Graph", use_container_width=True, key="btn_home_graph"):
            set_current_page("graph")
            st.rerun()

    with c5:
        st.markdown(
            """
            <div class="mrs-card">
                <h4>🔣 5. Notation Dictionary</h4>
                <p style="color: #94A3B8; font-size: 0.85rem;">Browse and search extracted LaTeX mathematical symbols, operator definitions, set notations, and variables across your literature.</p>
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
                <h4>📤 6. Research Export Center</h4>
                <p style="color: #94A3B8; font-size: 0.85rem;">Export structured research notes, theorem summaries, notation dictionaries, and citations into Markdown, JSON, CSV, or PDF formats.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Go to Export Center", use_container_width=True, key="btn_home_export"):
            set_current_page("export")
            st.rerun()

    # Recent Library Summary
    st.divider()
    st.markdown("### 📚 Mathematical Literature Catalog")
    if papers:
        for p in papers:
            title = p.get("title") or p.get("paper_id") or "Untitled Paper"
            authors_list = p.get("authors") or []
            authors_str = ", ".join(authors_list) if authors_list else "Author not specified"
            paper_id = p.get("paper_id", "")
            sec_cnt = p.get("section_count", 0)
            chunk_cnt = p.get("chunk_count", 0)
            eq_cnt = p.get("equation_count", 0)

            st.markdown(
                f"- **{title}** (`{paper_id}`) &bull; "
                f"Authors: *{authors_str}* &bull; "
                f"Sections: `{sec_cnt}` &bull; Passages: `{chunk_cnt}` &bull; LaTeX Equations: `{eq_cnt}`"
            )
    else:
        st.info("No mathematical papers currently ingested. Click **Go to PDF Upload** above to import your first paper!")


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from src.ui.layout import render_app_layout
    set_current_page("home")
    render_app_layout()
