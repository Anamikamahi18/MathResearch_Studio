"""Document Library page view for MathResearch Studio UI."""

from __future__ import annotations

import logging
from typing import Any

import streamlit as st

from src.ui.components.empty_state import render_empty_state
from src.ui.components.page_title import render_page_title
from src.ui.state import get_document_service, set_current_page

logger = logging.getLogger(__name__)


def filter_papers_by_keyword(papers: list[dict[str, Any]], keyword: str) -> list[dict[str, Any]]:
    """Filter list of paper summary records by keyword match across title, authors, or paper_id."""
    if not keyword or not keyword.strip():
        return papers

    kw = keyword.strip().lower()
    filtered: list[dict[str, Any]] = []

    for p in papers:
        title = (p.get("title") or "").lower()
        paper_id = (p.get("paper_id") or "").lower()
        authors = " ".join(p.get("authors") or []).lower()
        raw_doc = p.get("raw_document") or {}
        filename = (raw_doc.get("source_file", {}).get("file_name") or "").lower()

        if kw in title or kw in paper_id or kw in authors or kw in filename:
            filtered.append(p)

    return filtered


def count_math_entity_type(paper_summary: dict[str, Any], entity_type: str) -> int:
    """Count math entities of a given type ('definitions', 'theorems', 'lemmas', 'proofs') in paper."""
    raw_doc = paper_summary.get("raw_document") or {}
    entities = raw_doc.get("math_entities") or raw_doc.get("entities") or {}
    return len(entities.get(entity_type, []))


def render_library_page() -> None:
    """Render the Document Library page view."""
    render_page_title(
        title="Document Library",
        subtitle="Browse, filter, inspect, and refresh ingested mathematical research papers.",
        icon="📚",
        badge="Catalog Library",
    )


    doc_service = get_document_service()
    papers = doc_service.list_papers()

    # Top Control Bar: Search Filter & Refresh Library Button
    col_search, col_refresh = st.columns([4, 1])

    with col_search:
        search_query = st.text_input(
            label="Search Library",
            placeholder="Filter papers by title, author, or filename...",
            label_visibility="collapsed",
        )

    with col_refresh:
        if st.button("🔄 Refresh Library", use_container_width=True):
            with st.spinner("Rescanning parsed paper JSON directory..."):
                papers = doc_service.refresh_library()
                st.toast("Library refreshed successfully!")
                st.rerun()

    # Apply keyword filter
    filtered_papers = filter_papers_by_keyword(papers, search_query)

    # Empty State Handling
    if not papers:
        clicked = render_empty_state(
            title="No Research Papers Ingested",
            message="Your library is currently empty. Upload PDF research papers to extract equations, statements, and knowledge graph dependencies.",
            icon="📭",
            action_label="📤 Go to Upload Papers",
        )
        if clicked:
            set_current_page("upload")
            st.rerun()
        return

    # Aggregate Library Metrics
    total_papers = len(papers)
    total_defs = sum(count_math_entity_type(p, "definitions") for p in papers)
    total_thms = sum(count_math_entity_type(p, "theorems") for p in papers)
    total_lemmas = sum(count_math_entity_type(p, "lemmas") for p in papers)
    total_chunks = sum(p.get("chunk_count", 0) for p in papers)

    # Metric Cards Row
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Papers", total_papers)
    m2.metric("Definitions", total_defs)
    m3.metric("Theorems", total_thms)
    m4.metric("Lemmas", total_lemmas)
    m5.metric("Vector Chunks", total_chunks)

    st.divider()

    if search_query and not filtered_papers:
        st.info(f"No papers found matching keyword search: '{search_query}'")
        return

    st.markdown(f"### Catalog Papers ({len(filtered_papers)})")

    # Paper Cards List
    for p in filtered_papers:
        paper_id = p.get("paper_id", "Unknown")
        title = p.get("title", "Untitled Paper")
        authors = ", ".join(p.get("authors", [])) if p.get("authors") else "Unknown Author(s)"
        year = p.get("year") or "N/A"
        raw_doc = p.get("raw_document") or {}
        filename = raw_doc.get("source_file", {}).get("file_name") or f"{paper_id}.pdf"

        def_count = count_math_entity_type(p, "definitions")
        thm_count = count_math_entity_type(p, "theorems")
        lem_count = count_math_entity_type(p, "lemmas")
        proof_count = count_math_entity_type(p, "proofs")

        with st.expander(f"📄 **{title}** (`{paper_id}`)"):
            st.markdown(
                f"""
                <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 0.75rem;">
                    <strong>Authors:</strong> {authors} &bull; 
                    <strong>Year:</strong> {year} &bull; 
                    <strong>File:</strong> <code>{filename}</code>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Metadata Badges & Statistics
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"**Sections**: `{p.get('section_count', 0)}`")
            c2.markdown(f"**Vector Chunks**: `{p.get('chunk_count', 0)}`")
            c3.markdown(f"**Equations**: `{p.get('equation_count', 0)}`")
            c4.markdown(f"**References**: `{p.get('reference_count', 0)}`")

            st.markdown(
                f"""
                <div style="margin-top: 0.5rem; margin-bottom: 0.75rem;">
                    <span class="mrs-badge" style="background: rgba(16, 185, 129, 0.15); color: #34D399; border-color: rgba(52, 211, 153, 0.3);">
                        Defs: {def_count}
                    </span>
                    <span class="mrs-badge" style="background: rgba(79, 70, 229, 0.15); color: #818CF8; border-color: rgba(129, 140, 248, 0.3);">
                        Theorems: {thm_count}
                    </span>
                    <span class="mrs-badge" style="background: rgba(6, 182, 212, 0.15); color: #22D3EE; border-color: rgba(34, 211, 238, 0.3);">
                        Lemmas: {lem_count}
                    </span>
                    <span class="mrs-badge" style="background: rgba(245, 158, 11, 0.15); color: #FBBF24; border-color: rgba(251, 191, 36, 0.3);">
                        Proofs: {proof_count}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Abstract Preview
            sections = raw_doc.get("sections", [])
            abstract_text = ""
            for sec in sections:
                if "abstract" in (sec.get("heading") or "").lower():
                    abstract_text = sec.get("text", "")
                    break
            if not abstract_text and sections:
                abstract_text = sections[0].get("text", "")

            if abstract_text:
                st.markdown("**Abstract / Preview:**")
                st.info(abstract_text[:400] + ("..." if len(abstract_text) > 400 else ""))

            # Raw Document JSON Inspection Toggle
            with st.popover("🔍 Inspect Raw Document JSON"):
                st.json(raw_doc)


if __name__ == "__main__":
    import sys
    from pathlib import Path
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from src.ui.layout import render_app_layout
    set_current_page("library")
    render_app_layout()

