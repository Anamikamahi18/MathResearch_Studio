"""Semantic Search page view for MathResearch Studio UI."""

from __future__ import annotations

import logging
import time
from typing import Any

import streamlit as st

from src.ui.components.empty_state import render_empty_state
from src.ui.components.page_title import render_page_title
from src.ui.state import get_document_service, get_search_service

logger = logging.getLogger(__name__)


def get_score_badge_style(score: float) -> tuple[str, str, str]:
    """Get background color, text color, and label for similarity score badge."""
    if score >= 0.7:
        return "rgba(16, 185, 129, 0.15)", "#34D399", "High Match"
    elif score >= 0.5:
        return "rgba(79, 70, 229, 0.15)", "#818CF8", "Moderate Match"
    else:
        return "rgba(245, 158, 11, 0.15)", "#FBBF24", "Low Match"


def render_search_page() -> None:
    """Render the Semantic Search page view."""
    render_page_title(
        title="Semantic Vector Search",
        subtitle="Search mathematical document chunks using vector embeddings, section types, and entity metadata.",
        icon="🔍",
        badge="Semantic Retrieval",
    )


    doc_service = get_document_service()
    search_service = get_search_service()

    # Search Form Input & Controls
    with st.form(key="semantic_search_form", clear_on_submit=False):
        query_text = st.text_input(
            label="Search Query",
            placeholder="Enter natural language query or mathematical concept (e.g. 'What is a Hilbert Space definition?')...",
            key="search_query_input",
        )

        c_topk, c_min_score, c_sec_type, c_ent_type = st.columns(4)

        with c_topk:
            top_k = st.selectbox(
                label="Top-K Results",
                options=[5, 10, 20],
                index=0,
                help="Maximum number of candidate chunks to retrieve.",
            )

        with c_min_score:
            min_score = st.slider(
                label="Min Relevance Score",
                min_value=0.0,
                max_value=1.0,
                value=0.0,
                step=0.05,
                help="Filter out results below this similarity threshold.",
            )

        with c_sec_type:
            sec_type_opt = st.selectbox(
                label="Section Type Filter",
                options=["All", "definition", "theorem", "lemma", "proof", "other"],
                index=0,
            )

        with c_ent_type:
            ent_type_opt = st.selectbox(
                label="Entity Type Filter",
                options=["All", "definition", "theorem", "lemma", "proof"],
                index=0,
            )

        # Paper Filter Options
        papers = doc_service.list_papers()
        paper_options = {p.get("title", p.get("paper_id")): p.get("paper_id") for p in papers}
        selected_paper_titles = st.multiselect(
            label="Filter by Paper(s)",
            options=list(paper_options.keys()),
            placeholder="Search all papers in library...",
        )

        submit_search = st.form_submit_button("🔍 Search Literature", type="primary", use_container_width=True)

    # Assemble Filters Dictionary
    filters: dict[str, Any] = {}
    if min_score > 0.0:
        filters["min_score"] = min_score
    if sec_type_opt != "All":
        filters["section_type"] = sec_type_opt
    if ent_type_opt != "All":
        filters["entity_type"] = ent_type_opt
    if selected_paper_titles:
        selected_ids = [paper_options[t] for t in selected_paper_titles if t in paper_options]
        if selected_ids:
            filters["paper_id"] = selected_ids if len(selected_ids) > 1 else selected_ids[0]

    # Handle Search Execution
    if submit_search and query_text.strip():
        start_time = time.perf_counter()

        with st.spinner("Generating query vector embeddings & searching FAISS index..."):
            results = search_service.semantic_search(
                query=query_text.strip(),
                top_k=top_k,
                filters=filters if filters else None,
            )
            duration_ms = int((time.perf_counter() - start_time) * 1000)

        st.session_state["active_search_results"] = results
        st.session_state["active_search_query"] = query_text.strip()
        st.session_state["active_search_duration_ms"] = duration_ms

    # Render Search Results if present in session state
    active_results = st.session_state.get("active_search_results")
    active_query = st.session_state.get("active_search_query")
    active_duration = st.session_state.get("active_search_duration_ms", 0)

    if active_query:
        st.divider()

        if active_results:
            top_score = active_results[0].get("score", 0.0) if active_results else 0.0
            st.markdown(
                f"### Search Results ({len(active_results)}) "
                f"<span style='font-size: 0.85rem; color: #94A3B8; font-weight: normal;'>"
                f"&bull; Executed in `{active_duration} ms` &bull; Top Score: `{top_score:.4f}`</span>",
                unsafe_allow_html=True,
            )

            for idx, res in enumerate(active_results, start=1):
                score = float(res.get("score", 0.0))
                bg_color, text_color, match_label = get_score_badge_style(score)
                chunk_id = res.get("chunk_id", f"chunk_{idx}")
                paper_id = res.get("paper_id", "Unknown")
                paper_title = res.get("paper_title") or paper_id
                section_title = res.get("section_title") or res.get("section_id") or "Section"
                section_type = res.get("section_type", "other")
                page_start = res.get("page_start", 1)
                page_end = res.get("page_end", 1)
                text = res.get("text", "")

                with st.expander(f"#{idx} [{score:.4f}] **{paper_title}** - *{section_title}*"):
                    col_meta, col_score = st.columns([4, 1])

                    with col_meta:
                        st.markdown(
                            f"""
                            <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 0.5rem;">
                                <strong>Paper ID:</strong> <code>{paper_id}</code> &bull; 
                                <strong>Section Type:</strong> <code>{section_type}</code> &bull; 
                                <strong>Page:</strong> {page_start}{f'-{page_end}' if page_end > page_start else ''}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    with col_score:
                        st.markdown(
                            f"""
                            <span class="mrs-badge" style="background: {bg_color}; color: {text_color}; border-color: {text_color}44;">
                                Score: {score:.4f} ({match_label})
                            </span>
                            """,
                            unsafe_allow_html=True,
                        )

                    st.markdown("**Retrieved Chunk Text:**")
                    st.info(text)

                    # Detail Inspection Popover
                    with st.popover(f"🔍 Inspect Chunk `{chunk_id}` Metadata"):
                        st.json(res)

        else:
            st.warning("⚠️ **No relevant passages were found.**")
            st.caption(
                "Try broadening your search keywords, reducing the minimum relevance score threshold, or clearing section/paper filters."
            )

    # Render Initial Search Guidance if no search active
    elif not active_query:
        render_empty_state(
            title="Perform Semantic Search Across Papers",
            message="Enter a natural language question, formula description, or mathematical concept above to retrieve ranked text passages from indexed literature.",
            icon="🔍",
        )

    # Search History Drawer / Expander
    history = search_service.get_history()
    if history:
        st.divider()
        with st.expander(f"📜 Search Query History ({len(history)})"):
            for h_idx, item in enumerate(reversed(history), start=1):
                q_text = item.get("query", "")
                ts = item.get("timestamp", "")[:19].replace("T", " ")
                count = item.get("filtered_result_count", 0)
                t_score = item.get("top_score", 0.0)

                st.markdown(
                    f"**{h_idx}. '{q_text}'** &bull; `<small style='color:#94A3B8;'>{ts}</small>` &bull; "
                    f"Found `{count}` passage(s) (Top Score: `{t_score:.4f}`)"
                )

            if st.button("🗑️ Clear Search History", use_container_width=True):
                search_service.clear_history()
                st.toast("Search history cleared!")
                st.rerun()


if __name__ == "__main__":
    import sys
    from pathlib import Path
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from src.ui.layout import render_app_layout
    set_current_page("search")
    render_app_layout()

