"""Document Library page view for MathResearch Studio UI."""

from __future__ import annotations

import logging
from typing import Any

import streamlit as st

from src.ui.components.empty_state import render_empty_state
from src.ui.components.page_title import render_page_title
from src.ui.state import get_dashboard_service, get_document_service, set_current_page

logger = logging.getLogger(__name__)


def filter_papers_by_keyword(papers: list[dict[str, Any]], keyword: str) -> list[dict[str, Any]]:
    """Filter list of paper summary records by keyword match across title, authors, paper_id, filename, abstract, keywords, or section text."""
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
        abstract = (raw_doc.get("abstract") or "").lower()
        keywords = " ".join(raw_doc.get("keywords") or []).lower()
        sections_text = " ".join(
            (sec.get("heading") or "") + " " + (sec.get("text") or "")
            for sec in raw_doc.get("sections", [])
        ).lower()

        if (
            kw in title
            or kw in paper_id
            or kw in authors
            or kw in filename
            or kw in abstract
            or kw in keywords
            or kw in sections_text
        ):
            filtered.append(p)

    return filtered


def count_math_entity_type(paper_summary: dict[str, Any], entity_type: str) -> int:
    """Count math entities of a given type ('definitions', 'theorems', 'lemmas', 'corollaries', 'proofs') in paper."""
    raw_doc = paper_summary.get("raw_document") or {}
    items = raw_doc.get(entity_type)
    if items is not None and isinstance(items, list):
        return len(items)
    entities = raw_doc.get("math_entities") or raw_doc.get("entities") or {}
    return len(entities.get(entity_type, []))


def render_library_page() -> None:
    """Render the Document Library page view."""
    render_page_title(
        title="Mathematics Document Library",
        subtitle="Browse, filter, inspect, and organize your mathematical literature library.",
        icon="📚",
        badge="Mathematical Catalog",
    )

    doc_service = get_document_service()
    dash_service = get_dashboard_service()
    papers = doc_service.list_papers()

    # Top Control Bar: Search Filter & Sync Library Button
    col_search, col_refresh = st.columns([4, 1])

    with col_search:
        search_query = st.text_input(
            label="Search Library",
            placeholder="Filter papers by title, author, filename, abstract, or keyword...",
            label_visibility="collapsed",
        )

    with col_refresh:
        if st.button("🔄 Sync Library", help="Re-scan library directory to synchronize papers and statements.", use_container_width=True):
            with st.spinner("Rescanning parsed paper directory..."):
                papers = doc_service.refresh_library()
                st.toast("Library synchronized successfully!")
                st.rerun()

    # Apply keyword filter
    filtered_papers = filter_papers_by_keyword(papers, search_query)

    # Empty State Handling
    if not papers:
        clicked = render_empty_state(
            title="No Research Papers Ingested",
            message="Your library is currently empty. Upload PDF research papers to extract equations, statements, and theorem networks.",
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
    total_cors = sum(count_math_entity_type(p, "corollaries") for p in papers)
    
    # Align total passages directly with vector store count
    stats = dash_service.get_statistics()
    total_chunks = stats.get("total_vector_chunks", sum(p.get("chunk_count", 0) for p in papers))

    # Metric Cards Row
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Total Papers", total_papers)
    m2.metric("Definitions", total_defs)
    m3.metric("Theorems", total_thms)
    m4.metric("Lemmas", total_lemmas)
    m5.metric("Corollaries", total_cors)
    m6.metric("Paper Passages", total_chunks)

    st.divider()

    if search_query and not filtered_papers:
        st.info(f"No papers found matching search query: '{search_query}'")
        return

    st.markdown(f"### Mathematical Papers Catalog ({len(filtered_papers)})")

    # Paper Cards List
    for p in filtered_papers:
        paper_id = p.get("paper_id", "Unknown")
        title = p.get("title") or paper_id
        authors = ", ".join(p.get("authors", [])) if p.get("authors") else "Author not specified"
        year = p.get("year") or "N/A"
        raw_doc = p.get("raw_document") or {}
        filename = raw_doc.get("source_file", {}).get("file_name") or f"{paper_id}.pdf"

        def_count = count_math_entity_type(p, "definitions")
        thm_count = count_math_entity_type(p, "theorems")
        lem_count = count_math_entity_type(p, "lemmas")
        cor_count = count_math_entity_type(p, "corollaries")
        proof_count = count_math_entity_type(p, "proofs")

        with st.expander(f"📄 **{title}** (`{filename}`)"):
            st.markdown(
                f"""
                <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 0.75rem;">
                    <strong>Authors:</strong> {authors} &bull; 
                    <strong>Year:</strong> {year} &bull; 
                    <strong>Reference ID:</strong> <code>{paper_id}</code> &bull; 
                    <strong>File:</strong> <code>{filename}</code>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Metadata Badges & Statistics
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"**Sections**: `{p.get('section_count', 0)}`")
            c2.markdown(f"**Passages**: `{p.get('chunk_count', 0)}`")
            c3.markdown(f"**LaTeX Equations**: `{p.get('equation_count', 0)}`")
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
                    <span class="mrs-badge" style="background: rgba(236, 72, 153, 0.15); color: #F472B6; border-color: rgba(244, 114, 182, 0.3);">
                        Corollaries: {cor_count}
                    </span>
                    <span class="mrs-badge" style="background: rgba(245, 158, 11, 0.15); color: #FBBF24; border-color: rgba(251, 191, 36, 0.3);">
                        Proofs: {proof_count}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Abstract Display
            abstract_text = raw_doc.get("abstract", "")
            if not abstract_text:
                sections = raw_doc.get("sections", [])
                for sec in sections:
                    if "abstract" in (sec.get("heading") or "").lower():
                        abstract_text = sec.get("text", "")
                        break
                if not abstract_text and sections:
                    abstract_text = sections[0].get("text", "")

            if abstract_text:
                st.markdown("**Abstract / Summary:**")
                st.info(abstract_text)

            # Structured Paper Inspector Drawer
            with st.popover("📖 View Paper Structure & Statements"):
                st.markdown(f"## {title}")
                st.markdown(f"**Authors**: *{authors}* | **File**: `{filename}` | **Year**: `{year}`")
                
                keywords = raw_doc.get("keywords") or []
                if keywords:
                    st.markdown(f"**Keywords**: {', '.join(keywords)}")

                st.divider()

                # 1. Section Outline
                sections = raw_doc.get("sections", [])
                st.markdown(f"### 📑 Section Structure ({len(sections)})")
                if sections:
                    for sec in sections:
                        h_level = sec.get("level", 1)
                        indent = "&nbsp;&nbsp;&nbsp;&nbsp;" * max(0, h_level - 1)
                        heading = sec.get("heading") or f"Section {sec.get('section_id')}"
                        p_start = sec.get("page_start", 1)
                        p_end = sec.get("page_end", 1)
                        st.markdown(f"{indent}• **{heading}** *(Pages {p_start}–{p_end})*")
                else:
                    st.caption("No sections detected.")

                st.divider()

                # 2. Extracted Mathematical Statements
                st.markdown("### 🧮 Mathematical Statements & Equations")
                defs = raw_doc.get("definitions", [])
                thms = raw_doc.get("theorems", [])
                lemmas = raw_doc.get("lemmas", [])
                cors = raw_doc.get("corollaries", [])
                proofs = raw_doc.get("proofs", [])

                if defs or thms or lemmas or cors or proofs:
                    for stmt_list, stmt_label in [
                        (defs, "Definitions"),
                        (thms, "Theorems"),
                        (lemmas, "Lemmas"),
                        (cors, "Corollaries"),
                        (proofs, "Proofs"),
                    ]:
                        if stmt_list:
                            st.markdown(f"#### {stmt_label} ({len(stmt_list)})")
                            for item in stmt_list:
                                if isinstance(item, dict):
                                    name = item.get("title") or item.get("name") or item.get("statement_id", "")
                                    stmt_body = item.get("text") or item.get("latex") or item.get("content", "")
                                    st.markdown(f"- **{name}**: {stmt_body}")
                                else:
                                    st.markdown(f"- {item}")
                else:
                    st.caption("No explicit formal theorem or definition environments extracted.")

                # 3. References List
                references = raw_doc.get("references", [])
                if references:
                    st.divider()
                    st.markdown(f"### 📚 Academic References ({len(references)})")
                    for r in references[:10]:
                        ref_title = r.get("title") or r.get("raw_text") or f"Reference {r.get('reference_id')}"
                        st.markdown(f"- {ref_title}")
                    if len(references) > 10:
                        st.caption(f"*... and {len(references) - 10} more reference(s).*")

                # Delete Paper Action Button
                st.divider()
                if st.button(f"🗑️ Delete Paper '{title}'", key=f"del_btn_{pid}_{idx}", type="secondary"):
                    deleted = doc_service.delete_paper(pid)
                    if deleted:
                        st.toast(f"Deleted paper '{title}' from library catalog.")
                        st.rerun()

                # Developer Collapse Toggle for Raw JSON
                with st.expander("🛠️ Technical JSON Data (Developer View)"):
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

