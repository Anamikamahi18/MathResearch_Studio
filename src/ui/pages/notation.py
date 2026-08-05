"""Notation Dictionary page view for MathResearch Studio UI."""

from __future__ import annotations

import logging
from typing import Any

import streamlit as st

from src.ui.components.empty_state import render_empty_state
from src.ui.components.page_title import render_page_title
from src.ui.state import get_document_service, get_graph_service

logger = logging.getLogger(__name__)

CATEGORY_COLORS = {
    "Function": "#3B82F6",    # Blue
    "Variable": "#10B981",    # Green
    "Set": "#8B5CF6",         # Purple
    "Operator": "#F59E0B",   # Amber
    "Matrix": "#EC4899",     # Pink
    "Concept": "#06B6D4",    # Cyan
    "Other": "#64748B",      # Slate
}

CATEGORY_ICONS = {
    "Function": "ƒ(x)",
    "Variable": "x",
    "Set": "ℤ",
    "Operator": "∑</math",
    "Matrix": "<b>[M]</b>",
    "Concept": "💡",
    "Other": "🏷️",
}


NON_NOTATION_KEYWORDS = (
    "http", "www.", "isbn", "doi", "vol.", "volume", "issue", "impact factor", "college",
    "journal", "proceedings", "conference", "university", "department", "press", "wiley",
    "springer", "marcel dekker", "wikibooks", "khanacademy", "sosmath", "mashupstack",
    "reference", "ref ", "ref_", "1970", "1991", "1992", "1995", "1997", "2004", "2005",
    "2012", "2013", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"
)

SECTION_TITLE_STRINGS = {
    "introduction", "abstract", "methods", "models", "experiments", "results",
    "discussion", "related work", "conclusions", "references", "setup", "decoding",
    "data augmentation", "datasets", "metrics", "comparison", "conclusion",
    "acknowledgments", "overview", "analysis", "inference", "tasks"
}


def classify_notation_category(item: dict[str, Any]) -> str:
    """Classify a notation item dictionary into a mathematical category."""
    lbl = (item.get("label") or item.get("node_id") or "").lower()
    text = (item.get("text") or "").lower()
    ntype = str(item.get("node_type", "")).lower()

    if ntype == "concept":
        return "Concept"
    if "matrix" in lbl or "vector space" in lbl or "linear map" in lbl:
        return "Matrix"
    if any(k in lbl or k in text for k in ("set", "space", "field", "\\mathbb", "group", "algebra", "manifold", "hilbert space", "topological space")):
        return "Set"
    if any(k in lbl or k in text for k in ("function", "mapping", "f(", "g(", "h(", "transformation", "eigenvalue")):
        return "Function"
    if any(k in lbl or k in text for k in ("operator", "integral", "sum", "product", "norm", "inner product", "\\sum", "\\int")):
        return "Operator"
    if any(k in lbl for k in ("x", "y", "z", "t", "n", "k", "variable", "eq (", "equation")):
        return "Variable"

    return "Concept"


def is_valid_notation_item(item: dict[str, Any]) -> bool:
    """Filter out section headings, paper nodes, URL/citation strings, and raw internal IDs."""
    ntype = str(item.get("node_type", "")).lower()
    lbl = str(item.get("label") or item.get("node_id") or "").strip()
    lbl_lower = lbl.lower()

    # Reject paper nodes, section nodes, and reference citation nodes
    if ntype in ("paper", "section", "reference", "bib"):
        return False
    if any(lbl_lower.startswith(p) for p in ("paper_", "section_", "ref_")):
        return False
    if any(k in lbl_lower for k in NON_NOTATION_KEYWORDS):
        return False
    if lbl_lower in SECTION_TITLE_STRINGS:
        return False

    return True


def extract_all_notation_items(
    notation_graph: dict[str, Any],
    all_nodes: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Extract and deduplicate valid notation items across notation graph and statement nodes."""
    seen_ids = set()
    items = []

    # 1. From notation graph summary
    for cat_key in ("symbols", "concepts", "equations"):
        for n in notation_graph.get(cat_key, []):
            nid = n.get("node_id")
            if nid and nid not in seen_ids and is_valid_notation_item(n):
                seen_ids.add(nid)
                n["category"] = classify_notation_category(n)
                items.append(n)

    # 2. From all graph nodes (symbols, concepts, equations, definitions, theorems, lemmas)
    for n in all_nodes:
        nid = n.get("node_id")
        if nid and nid not in seen_ids and is_valid_notation_item(n):
            seen_ids.add(nid)
            n_item = dict(n)
            n_item["category"] = classify_notation_category(n_item)
            items.append(n_item)

    return items


def render_notation_page() -> None:
    """Render the Notation Dictionary page view."""
    render_page_title(
        title="Mathematical Notation Dictionary",
        subtitle="Browse, search, and inspect mathematical symbols, variables, operator definitions, matrix notations, and LaTeX expressions extracted from your library.",
        icon="📖",
        badge="Symbol Dictionary",
    )

    doc_service = get_document_service()
    graph_service = get_graph_service()

    # Pre-build paper catalog title mapping
    papers = doc_service.list_papers()
    paper_title_map: dict[str, str] = {}
    paper_options: dict[str, str] = {}

    for p in papers:
        pid = p.get("paper_id")
        if pid:
            t = p.get("title") or pid
            paper_title_map[pid] = t
            paper_options[t] = pid

    # Toolbar with Sync Button
    c_title, c_ref = st.columns([3, 1])
    with c_ref:
        if st.button("🔄 Sync Notation Dictionary", type="primary", use_container_width=True):
            with st.spinner("Building notation graph..."):
                graph_service.build_notation_graph()
                st.toast("Notation dictionary updated!")
                st.rerun()

    notation_graph = graph_service.build_notation_graph()
    all_nodes = graph_service.node_lookup()
    notation_items = extract_all_notation_items(notation_graph, all_nodes)

    # Calculate Category Statistics
    counts: dict[str, int] = {
        "Function": 0,
        "Variable": 0,
        "Set": 0,
        "Operator": 0,
        "Matrix": 0,
        "Concept": 0,
    }
    for item in notation_items:
        cat = item.get("category", "Concept")
        counts[cat] = counts.get(cat, 0) + 1

    # Render Statistics Bar
    st.markdown("### 📊 Notation Statistics")
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    with m1:
        st.metric("Total Items", f"{len(notation_items)}")
    with m2:
        st.metric("Functions", f"{counts['Function']}")
    with m3:
        st.metric("Variables & Vectors", f"{counts['Variable']}")
    with m4:
        st.metric("Sets & Spaces", f"{counts['Set']}")
    with m5:
        st.metric("Operators", f"{counts['Operator']}")
    with m6:
        st.metric("Matrices & Concepts", f"{counts['Matrix'] + counts['Concept']}")

    if not notation_items:
        st.divider()
        render_empty_state(
            title="No Notation Items Found",
            message="No mathematical symbols, operator definitions, or concepts exist in the current library. Upload or parse papers on the Upload page to build the notation dictionary.",
            icon="📖",
        )
        return

    # Search & Controls Panel
    st.divider()
    c_src, c_cat, c_paper = st.columns([2, 1, 1])

    with c_src:
        search_term = st.text_input(
            label="Search Notation",
            placeholder="Search symbol, LaTeX, variable name, or definition...",
            key="notation_search_input",
        )

    with c_cat:
        category_opt = st.selectbox(
            label="Symbol Category",
            options=["All", "Function", "Variable", "Set", "Operator", "Matrix", "Concept"],
            index=0,
        )

    with c_paper:
        selected_paper_titles = st.multiselect(
            label="Scope to Paper(s)",
            options=list(paper_options.keys()),
            placeholder="All papers in library...",
        )

    # Alphabetical A-Z Filter Bar
    alpha_letters = ["All"] + [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    selected_letter = st.radio(
        label="Browse Alphabetically",
        options=alpha_letters,
        index=0,
        horizontal=True,
        key="notation_alpha_radio",
    )

    # Apply Filters
    filtered_items = list(notation_items)

    if search_term.strip():
        q = search_term.strip().lower()
        filtered_items = [
            i for i in filtered_items
            if q in (i.get("label") or "").lower()
            or q in (i.get("text") or "").lower()
            or q in (i.get("node_id") or "").lower()
            or q in (paper_title_map.get(i.get("paper_id", ""), "")).lower()
        ]

    if category_opt != "All":
        filtered_items = [i for i in filtered_items if i.get("category") == category_opt]

    if selected_paper_titles:
        selected_pids = set(paper_options[t] for t in selected_paper_titles if t in paper_options)
        filtered_items = [i for i in filtered_items if i.get("paper_id") in selected_pids]

    if selected_letter != "All":
        filtered_items = [
            i for i in filtered_items
            if (i.get("label") or i.get("node_id") or "").upper().startswith(selected_letter)
        ]

    st.markdown(f"**Found {len(filtered_items)} Notation Item(s):**")

    # Render Notation Cards Grid
    if filtered_items:
        cols_per_row = 2
        for row_start in range(0, len(filtered_items), cols_per_row):
            row_items = filtered_items[row_start : row_start + cols_per_row]
            cols = st.columns(cols_per_row)
            for idx, item in enumerate(row_items):
                with cols[idx]:
                    cat = item.get("category", "Concept")
                    color = CATEGORY_COLORS.get(cat, CATEGORY_COLORS["Other"])
                    icon = CATEGORY_ICONS.get(cat, "🏷️")
                    lbl = item.get("label") or item.get("node_id") or "Symbol"
                    paper_id = item.get("paper_id", "")
                    paper_title = paper_title_map.get(paper_id, paper_id)
                    sec_name = item.get("section_title") or item.get("section_id") or "General"

                    st.markdown(
                        f"""
                        <div style="background: #1E293B; border-top: 3px solid {color}; border-radius: 6px; padding: 12px 16px; margin-bottom: 12px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <h4 style="margin: 0; color: #F8FAFC;">{lbl}</h4>
                                <span style="background: {color}22; color: {color}; font-size: 0.75rem; padding: 2px 8px; border-radius: 4px; font-weight: bold;">
                                    {icon} {cat}
                                </span>
                            </div>
                            <p style="margin: 6px 0 0 0; color: #94A3B8; font-size: 0.82rem;">
                                <strong>Paper:</strong> {paper_title} &bull; <strong>Section:</strong> {sec_name}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        # Notation Detail & Relationship View Inspector
        st.divider()
        st.markdown("### 📖 Notation Details & Relationship View")

        item_options_dict = {
            f"[{i.get('category', 'Concept')}] {i.get('label') or i.get('node_id')} ({paper_title_map.get(i.get('paper_id', ''), i.get('paper_id'))})": i
            for i in filtered_items
        }

        selected_label = st.selectbox(
            label="Select Mathematical Notation Item to Inspect",
            options=list(item_options_dict.keys()),
            index=0,
        )
        selected_item = item_options_dict[selected_label]
        node_id = selected_item.get("node_id", "")
        paper_id = selected_item.get("paper_id", "")
        paper_title = paper_title_map.get(paper_id, paper_id)
        sec_name = selected_item.get("section_title") or selected_item.get("section_id") or "General"

        col_meta, col_flow = st.columns([1, 1])

        with col_meta:
            st.markdown(f"#### Symbol: `{selected_item.get('label') or node_id}`")
            st.markdown(f"**Category:** `{selected_item.get('category')}`")
            st.markdown(f"**Paper:** {paper_title}")
            st.markdown(f"**Section:** {sec_name}")
            st.markdown(f"**Page:** {selected_item.get('page_start', 1)}")

            # Definition Excerpt fallback
            excerpt_text = selected_item.get("text") or selected_item.get("description")
            if not excerpt_text:
                lookup_res = graph_service.node_lookup(node_id=node_id)
                if lookup_res:
                    excerpt_text = lookup_res[0].get("text")

            if not excerpt_text:
                excerpt_text = f"Notation '{selected_item.get('label') or node_id}' defined and utilized in section '{sec_name}' of paper '{paper_title}'."

            st.markdown("**Mathematical Definition / Literature Context:**")
            st.info(excerpt_text)

        with col_flow:
            st.markdown("#### 🔗 Statement Context & Dependency Flow")
            st.markdown(
                f"""
                <div style="background: #0F172A; border: 1px solid #334155; border-radius: 8px; padding: 14px; text-align: center;">
                    <div style="font-weight: bold; color: #38BDF8;">Notation: {selected_item.get('label') or node_id}</div>
                    <div style="color: #94A3B8; font-size: 1.2rem; margin: 4px 0;">↓</div>
                    <div style="font-weight: bold; color: #34D399;">Introduced in: {sec_name}</div>
                    <div style="color: #94A3B8; font-size: 1.2rem; margin: 4px 0;">↓</div>
                    <div style="font-weight: bold; color: #FBBF24;">Theorem & Proof Step Dependencies</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("**⬅️ Introduced / Defined In:**")
            antecedents = graph_service.get_antecedents(node_id)
            if antecedents:
                for a in antecedents:
                    st.markdown(f"- ⬅️ **{a.get('label') or a.get('node_id')}** (`{a.get('node_type')}`)")
            else:
                st.caption(f"Defined in paper '{paper_title}' ({sec_name}).")

            st.markdown("**➡️ Applied In Theorems & Proofs:**")
            consequents = graph_service.get_consequents(node_id)
            if consequents:
                for c in consequents:
                    st.markdown(f"- ➡️ **{c.get('label') or c.get('node_id')}** (`{c.get('node_type')}`)")
            else:
                st.caption("No downstream statement dependencies.")

    else:
        st.warning("No notation items match the selected search or filter criteria.")


if __name__ == "__main__":
    import sys
    from pathlib import Path
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from src.ui.layout import render_app_layout
    set_current_page("notation")
    render_app_layout()

