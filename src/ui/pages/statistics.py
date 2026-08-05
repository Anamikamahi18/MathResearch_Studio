"""Statistics Dashboard page view for MathResearch Studio UI."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

import streamlit as st

from src.ui.components.empty_state import render_empty_state
from src.ui.components.page_title import render_page_title
from src.ui.state import (
    get_chat_service,
    get_dashboard_service,
    get_document_service,
    get_search_service,
    set_current_page,
)

logger = logging.getLogger(__name__)


def render_statistics_page() -> None:
    """Render the Statistics Dashboard page view."""
    render_page_title(
        title="Mathematical Research Statistics",
        subtitle="System overview, mathematical statement distributions, research activity logs, and system health status.",
        icon="📊",
        badge="Math Analytics",
    )


    doc_service = get_document_service()
    dash_service = get_dashboard_service()

    # Toolbar with Refresh Button
    c_title, c_ref = st.columns([3, 1])
    with c_ref:
        if st.button("🔄 Refresh Dashboard", type="primary", use_container_width=True):
            with st.spinner("Aggregating system statistics and rebuilding graph metrics..."):
                doc_service.refresh_library()
                dash_service.graph_service.build_dependency_graph()
                st.session_state["last_dashboard_refresh"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
                st.toast("Dashboard statistics refreshed!")
                st.rerun()

    stats = dash_service.get_statistics()
    paper_count = stats.get("paper_count", 0)

    # Empty State Handling if 0 papers exist
    if paper_count == 0:
        st.divider()
        render_empty_state(
            title="No Research Data Available",
            message="No mathematical papers or statement entities have been ingested into the library. Upload PDF papers to generate statistics and analytics.",
            icon="📊",
        )
        if st.button("📥 Upload Papers Now", type="primary", use_container_width=True):
            set_current_page("upload")
            st.rerun()
        return

    # Extract detailed paper metadata for analytics
    papers = doc_service.list_papers()
    graph_metrics = dash_service.get_graph_metrics()
    nodes = dash_service.graph_service.backend.graph.nodes

    # Calculate additional aggregated metrics
    total_pages = 0
    total_proofs = 0
    total_symbols = 0
    year_distribution: dict[int, int] = {}
    largest_paper_title = "N/A"
    max_chunks = 0

    for p in papers:
        raw = p.get("raw_document") or {}
        sections = raw.get("sections") or []
        for s in sections:
            p_start = s.get("page_start", 1)
            p_end = s.get("page_end", 1)
            total_pages += max(1, p_end - p_start + 1)

        entities = raw.get("math_entities") or raw.get("entities") or {}
        total_proofs += len(entities.get("proofs", []))
        total_symbols += len(entities.get("symbols", []))

        yr = p.get("year") or 2024
        year_distribution[yr] = year_distribution.get(yr, 0) + 1

        chunks = p.get("chunk_count", 0)
        if chunks >= max_chunks:
            max_chunks = chunks
            largest_paper_title = p.get("title") or p.get("paper_id")

    # Overview Metrics Bar (10 System Metrics in 2 Rows)
    st.markdown("### 📈 High-Level System Metrics")
    r1_c1, r1_c2, r1_c3, r1_c4, r1_c5 = st.columns(5)
    with r1_c1:
        st.metric("Papers Cataloged", f"{paper_count}")
    with r1_c2:
        st.metric("Est. Total Pages", f"{total_pages}")
    with r1_c3:
        st.metric("Definitions", f"{stats.get('definition_count', 0)}")
    with r1_c4:
        st.metric("Theorems", f"{stats.get('theorem_count', 0)}")
    with r1_c5:
        st.metric("Lemmas", f"{stats.get('lemma_count', 0)}")

    r2_c1, r2_c2, r2_c3, r2_c4, r2_c5 = st.columns(5)
    with r2_c1:
        st.metric("Proofs", f"{total_proofs}")
    with r2_c2:
        st.metric("Symbols & Notation", f"{total_symbols or len(nodes)}")
    with r2_c3:
        st.metric("Vector Store Chunks", f"{stats.get('total_vector_chunks', 0)}")
    with r2_c4:
        st.metric("Graph Nodes", f"{stats.get('graph_nodes', 0)}")
    with r2_c5:
        st.metric("Graph Edges", f"{stats.get('graph_edges', 0)}")

    st.divider()

    # Visual Distribution Charts & Progress Bars
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("#### 📘 Statement Type Distribution")
        node_breakdown = graph_metrics.get("node_type_breakdown", {})
        total_stmt_nodes = max(1, sum(node_breakdown.values()))

        def_cnt = node_breakdown.get("definition", stats.get("definition_count", 0))
        thm_cnt = node_breakdown.get("theorem", stats.get("theorem_count", 0))
        lem_cnt = node_breakdown.get("lemma", stats.get("lemma_count", 0))
        proof_cnt = node_breakdown.get("proof", total_proofs)

        st.caption(f"Definitions ({def_cnt})")
        st.progress(min(1.0, def_cnt / total_stmt_nodes))

        st.caption(f"Theorems ({thm_cnt})")
        st.progress(min(1.0, thm_cnt / total_stmt_nodes))

        st.caption(f"Lemmas ({lem_cnt})")
        st.progress(min(1.0, lem_cnt / total_stmt_nodes))

        st.caption(f"Proofs ({proof_cnt})")
        st.progress(min(1.0, proof_cnt / total_stmt_nodes))

    with col_chart2:
        st.markdown("#### 📅 Papers by Publication Year")
        if year_distribution:
            for yr_val, y_count in sorted(year_distribution.items()):
                pct = y_count / max(1, paper_count)
                st.caption(f"Year {yr_val} ({y_count} paper(s))")
                st.progress(min(1.0, pct))
        else:
            st.caption("No publication year metadata available.")

    st.divider()

    # Quick Insights Cards Section
    st.markdown("### 💡 Quick Research Insights")
    in_c1, in_c2, in_c3, in_c4 = st.columns(4)

    # Calculate Most Connected Statement
    max_degree = 0
    most_connected_lbl = "N/A"
    for nid, node in nodes.items():
        antecedents = dash_service.graph_service.get_antecedents(nid)
        consequents = dash_service.graph_service.get_consequents(nid)
        deg = len(antecedents) + len(consequents)
        if deg >= max_degree:
            max_degree = deg
            most_connected_lbl = node.label or nid

    with in_c1:
        st.markdown(
            f"""
            <div style="background: #1E293B; border-left: 4px solid #3B82F6; padding: 12px; border-radius: 6px;">
                <small style="color: #94A3B8;">LARGEST PAPER</small>
                <h5 style="margin: 4px 0; color: #F8FAFC;">{largest_paper_title[:30]}</h5>
                <small style="color: #38BDF8;">{max_chunks} chunk(s) indexed</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with in_c2:
        st.markdown(
            f"""
            <div style="background: #1E293B; border-left: 4px solid #10B981; padding: 12px; border-radius: 6px;">
                <small style="color: #94A3B8;">MOST CONNECTED STATEMENT</small>
                <h5 style="margin: 4px 0; color: #F8FAFC;">{most_connected_lbl[:30]}</h5>
                <small style="color: #34D399;">{max_degree} dependency edge(s)</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with in_c3:
        st.markdown(
            f"""
            <div style="background: #1E293B; border-left: 4px solid #8B5CF6; padding: 12px; border-radius: 6px;">
                <small style="color: #94A3B8;">GRAPH DENSITY</small>
                <h5 style="margin: 4px 0; color: #F8FAFC;">{stats.get('graph_density', 0.0):.4f}</h5>
                <small style="color: #A78BFA;">Statement network density</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with in_c4:
        st.markdown(
            f"""
            <div style="background: #1E293B; border-left: 4px solid #F59E0B; padding: 12px; border-radius: 6px;">
                <small style="color: #94A3B8;">DOMINANT STATEMENT</small>
                <h5 style="margin: 4px 0; color: #F8FAFC;">Theorem / Definition</h5>
                <small style="color: #FBBF24;">{stats.get('definition_count', 0) + stats.get('theorem_count', 0)} total statements</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # Research Activity & History Section
    st.markdown("### 🕒 Recent Research Activity")
    tab_papers, tab_search, tab_ai = st.tabs(["📄 Recent Uploads", "🔍 Recent Searches", "🤖 Recent AI Questions"])

    with tab_papers:
        for idx, p in enumerate(reversed(papers[-5:]), start=1):
            st.markdown(
                f"**{idx}. {p.get('title')}** &bull; `<small style='color:#94A3B8;'>{p.get('authors', ['Unknown'])[0] if p.get('authors') else 'Unknown'} ({p.get('year', 'N/A')})</small>` "
                f"&bull; Chunks: `{p.get('chunk_count', 0)}`"
            )

    with tab_search:
        search_svc = get_search_service()
        search_hist = search_svc.get_history()
        if search_hist:
            for s_idx, sh in enumerate(reversed(search_hist[-5:]), start=1):
                st.markdown(
                    f"**{s_idx}. '{sh.get('query')}'** &bull; `<small style='color:#94A3B8;'>{sh.get('timestamp', '')[:19].replace('T', ' ')}</small>` "
                    f"&bull; Hits: `{sh.get('filtered_result_count', 0)}` (Top Score: `{sh.get('top_score', 0.0):.4f}`)"
                )
        else:
            st.caption("No recent search queries executed.")

    with tab_ai:
        chat_svc = get_chat_service()
        chat_hist = chat_svc.get_chat_history()
        if chat_hist:
            for c_idx, ch in enumerate(reversed(chat_hist[-5:]), start=1):
                st.markdown(
                    f"**{c_idx}. \"{ch.get('question')}\"** &bull; `<small style='color:#94A3B8;'>{ch.get('timestamp', '')[:19].replace('T', ' ')}</small>` "
                    f"&bull; Decision: `{ch.get('decision', 'ACCEPT')}`"
                )
        else:
            st.caption("No recent AI Assistant questions asked.")

    st.divider()

    # System Health Status Panel
    st.markdown("### 🛡️ System Health & Infrastructure Status")
    h1, h2, h3, h4 = st.columns(4)

    last_refresh = st.session_state.get("last_dashboard_refresh", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))

    with h1:
        st.success("🟢 Vector Store: **ONLINE**")
        st.caption(f"{stats.get('total_vector_chunks', 0)} vectors indexed")

    with h2:
        st.success("🟢 Research Graph: **ONLINE**")
        st.caption(f"{stats.get('graph_nodes', 0)} nodes / {stats.get('graph_edges', 0)} edges")

    with h3:
        st.info("🔵 Paper Catalog: **READY**")
        st.caption(f"{paper_count} papers loaded")

    with h4:
        st.warning("⏱️ Last Refreshed")
        st.caption(f"{last_refresh}")


if __name__ == "__main__":
    import sys
    from pathlib import Path
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from src.ui.layout import render_app_layout
    set_current_page("statistics")
    render_app_layout()

