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
    """Render the Mathematical Search page view."""
    render_page_title(
        title="Mathematical Search",
        subtitle="Search mathematical document passages, theorem statements, definitions, and LaTeX formulas using semantic similarity.",
        icon="🔍",
        badge="Math Literature Search",
    )

    doc_service = get_document_service()
    search_service = get_search_service()

    # Pre-build catalog mapping for clean paper title and author resolution
    papers = doc_service.list_papers()
    paper_title_map: dict[str, str] = {}
    paper_author_map: dict[str, str] = {}
    paper_options: dict[str, str] = {}

    for p in papers:
        pid = p.get("paper_id")
        if pid:
            t = p.get("title") or pid
            paper_title_map[pid] = t
            paper_options[t] = pid
            a_list = p.get("authors") or []
            paper_author_map[pid] = ", ".join(a_list) if a_list else "Author not specified"

    # Mathematics Quick Query Presets
    st.markdown("**Suggested Mathematics Queries:**")
    c_q1, c_q2, c_q3, c_q4 = st.columns(4)
    preset_q = None
    with c_q1:
        if st.button("📐 Hilbert Space & Norm", key="btn_q1", use_container_width=True):
            preset_q = "Hilbert Space definition inner product norm completeness"
    with c_q2:
        if st.button("🔍 Cauchy-Schwarz Proof", key="btn_q2", use_container_width=True):
            preset_q = "Cauchy-Schwarz inequality proof steps and vector bounds"
    with c_q3:
        if st.button("🔢 Banach Fixed Point", key="btn_q3", use_container_width=True):
            preset_q = "Banach Fixed Point Theorem contraction mapping proof"
    with c_q4:
        if st.button("🕸️ Galois Field Extension", key="btn_q4", use_container_width=True):
            preset_q = "Galois group polynomial roots field extension automorphism"

    default_search_val = preset_q or st.session_state.get("active_search_query", "")

    # Search Form Input & Controls
    with st.form(key="semantic_search_form", clear_on_submit=False):
        query_text = st.text_input(
            label="Mathematical Query, Theorem Name, or Formula Concept",
            value=default_search_val,
            placeholder="Enter natural language query, LaTeX formula, or math concept (e.g., 'Hilbert Space norm', 'Cauchy-Schwarz inequality proof', 'Banach fixed point theorem')...",
            key="search_query_input",
        )

        c_topk, c_min_score, c_sec_type, c_ent_type = st.columns(4)

        with c_topk:
            top_k = st.selectbox(
                label="Max Passages to Show",
                options=[5, 10, 20],
                index=0,
                help="Select how many top relevant passage excerpts to display.",
            )

        with c_min_score:
            min_score = st.slider(
                label="Minimum Similarity Threshold",
                min_value=0.0,
                max_value=1.0,
                value=0.0,
                step=0.05,
                help="Filter out passage excerpts below this relevance score (0.00 = show all).",
            )

        with c_sec_type:
            sec_type_opt = st.selectbox(
                label="Section Filter",
                options=["All", "definition", "theorem", "lemma", "proof", "other"],
                index=0,
                help="Filter by section role within papers.",
            )

        with c_ent_type:
            ent_type_opt = st.selectbox(
                label="Statement Type Filter",
                options=["All", "definition", "theorem", "lemma", "corollary", "proof"],
                index=0,
                help="Filter passages containing specific mathematical statement types.",
            )

        # Paper Filter Options
        selected_paper_titles = st.multiselect(
            label="Filter by Mathematical Paper(s)",
            options=list(paper_options.keys()),
            placeholder="Search across all math papers in library...",
        )

        submit_search = st.form_submit_button("🔍 Search Mathematical Literature", type="primary", use_container_width=True)

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

        with st.spinner("Searching mathematical literature index..."):
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
                
                # Resolve real paper title and authors
                raw_title = res.get("paper_title") or res.get("title") or ""
                if paper_id in paper_title_map:
                    paper_title = paper_title_map[paper_id]
                elif not raw_title or raw_title.startswith("paper_") or "irjhis.com" in raw_title.lower() or "journal of" in raw_title.lower():
                    paper_title = paper_id
                else:
                    paper_title = raw_title

                authors_str = paper_author_map.get(paper_id, ", ".join(res.get("authors") or []) if res.get("authors") else "Author not specified")
                section_title = res.get("section_title") or res.get("section_id") or "Section Text"
                section_type = res.get("section_type", "other")
                page_start = res.get("page_start", 1)
                page_end = res.get("page_end", 1)
                text = res.get("text", "")

                with st.expander(f"#{idx} [{score:.4f}] **{paper_title}** — *{section_title}*"):
                    col_meta, col_score = st.columns([4, 1])

                    with col_meta:
                        st.markdown(
                            f"""
                            <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 0.5rem;">
                                <strong>Paper:</strong> {paper_title} &bull; 
                                <strong>Authors:</strong> {authors_str} &bull; 
                                <strong>Section:</strong> <code>{section_type}</code> &bull; 
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

                    st.markdown("**Retrieved Passage Text:**")
                    st.info(text)

                    # Detail Inspection Popover
                    with st.popover("📖 View Passage Details & Context"):
                        st.markdown(f"### {paper_title}")
                        st.markdown(f"**Authors**: *{authors_str}*")
                        st.markdown(f"**Section**: {section_title} | **Page**: {page_start}")
                        st.markdown(f"**Relevance Score**: `{score:.4f}` ({match_label})")
                        st.divider()
                        st.markdown("**Complete Excerpt:**")
                        st.markdown(text)
                        
                        with st.expander("🛠️ Technical JSON Data (Developer View)"):
                            st.json(res)

        else:
            st.warning("⚠️ **No relevant passages were found matching your criteria.**")
            st.caption(
                "Try broadening your search keywords, reducing the similarity threshold, or clearing section filters."
            )

    # Render Initial Search Guidance if no search active
    elif not active_query:
        render_empty_state(
            title="Search Mathematical Literature",
            message="Enter a natural language question, formula description, or mathematical concept above to retrieve ranked text passages from your library.",
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

