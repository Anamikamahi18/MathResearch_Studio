"""Export Center page view for MathResearch Studio UI."""

from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import streamlit as st

from src.ui.components.empty_state import render_empty_state
from src.ui.components.page_title import render_page_title
from src.ui.state import (
    get_chat_service,
    get_dashboard_service,
    get_document_service,
    get_export_service,
    get_graph_service,
    get_search_service,
    set_current_page,
)

logger = logging.getLogger(__name__)

MIME_MAP = {
    "markdown": "text/markdown",
    "md": "text/markdown",
    "json": "application/json",
    "csv": "text/csv",
    "pdf": "application/pdf",
}


def get_mime_type(fmt: str) -> str:
    """Get MIME type string for download button."""
    return MIME_MAP.get(fmt.lower(), "text/plain")


def format_bytes_to_kb(b_size: int) -> str:
    """Format byte count to KB or MB string."""
    if b_size < 1024:
        return f"{b_size} B"
    elif b_size < 1024 * 1024:
        return f"{b_size / 1024:.1f} KB"
    else:
        return f"{b_size / (1024 * 1024):.2f} MB"


def render_export_page() -> None:
    """Render the Export Center page view."""
    render_page_title(
        title="Mathematics Export Center",
        subtitle="Export mathematical research notes, theorem summaries, search results, AI Q&A conversations, notation dictionaries, and graph metrics.",
        icon="📤",
        badge="Export Center",
    )


    doc_service = get_document_service()
    export_service = get_export_service()
    papers = doc_service.list_papers()

    # Empty State Handling if 0 papers exist
    if not papers:
        render_empty_state(
            title="No Research Data Available for Export",
            message="No papers or mathematical entities exist in the current library. Upload papers on the Upload page to enable research exports.",
            icon="📤",
        )
        if st.button("📥 Upload Papers Now", type="primary", use_container_width=True):
            set_current_page("upload")
            st.rerun()
        return

    # Export Selection & Controls Form
    with st.form(key="export_center_form", clear_on_submit=False):
        c_target, c_format = st.columns(2)

        with c_target:
            export_target = st.selectbox(
                label="Select Export Target Data",
                options=[
                    "Paper Metadata & Summaries",
                    "Search Results & History",
                    "AI Q&A Conversations",
                    "Notation Dictionary",
                    "Dependency Graph Metrics",
                    "Dashboard Statistics",
                ],
                index=0,
            )

        with c_format:
            export_format = st.radio(
                label="Target Export Format",
                options=["Markdown (.md)", "JSON (.json)", "CSV (.csv)", "PDF (.pdf)"],
                index=0,
                horizontal=True,
            )

        st.markdown("**Export Scope & Options:**")
        c_papers, c_toggles = st.columns([2, 2])

        with c_papers:
            paper_options = {p.get("title", p.get("paper_id")): p.get("paper_id") for p in papers}
            selected_paper_titles = st.multiselect(
                label="Scope to Specific Paper(s)",
                options=list(paper_options.keys()),
                placeholder="Include all catalog papers...",
            )

        with c_toggles:
            inc_cit = st.checkbox("Include In-Text Citations", value=True)
            inc_meta = st.checkbox("Include System Metadata", value=True)
            inc_graph = st.checkbox("Include Graph Density & Degree", value=True)
            inc_not = st.checkbox("Include Notation & Symbols", value=True)

        submit_export = st.form_submit_button("🚀 Generate Export File", type="primary", use_container_width=True)

    # Determine Extension & MIME Type
    fmt_clean = export_format.split()[0].lower()
    ext_map = {"markdown": "md", "json": "json", "csv": "csv", "pdf": "pdf"}
    file_ext = ext_map.get(fmt_clean, "md")
    mime_type = get_mime_type(fmt_clean)

    # Filter papers if specified
    if selected_paper_titles:
        selected_ids = set(paper_options[t] for t in selected_paper_titles if t in paper_options)
        target_papers = [p for p in papers if p.get("paper_id") in selected_ids]
    else:
        target_papers = papers

    # Export Live Preview Card
    st.divider()
    st.markdown("### 📋 Export Configuration Preview")
    prev_c1, prev_c2, prev_c3, prev_c4 = st.columns(4)

    est_items = len(target_papers)
    est_size_kb = max(1.2, est_items * 1.8)

    with prev_c1:
        st.metric("Target Data", export_target.split()[0])
    with prev_c2:
        st.metric("Format", export_format.split()[0])
    with prev_c3:
        st.metric("Catalog Scope", f"{est_items} paper(s)")
    with prev_c4:
        st.metric("Estimated Size", f"~{est_size_kb:.1f} KB")

    st.markdown(
        f"""
        <div style="background: #1E293B; border-left: 4px solid #6366F1; padding: 12px; border-radius: 4px; font-size: 0.85rem; color: #94A3B8;">
            <strong>Target Filename:</strong> <code>{export_target.lower().replace(' ', '_')}.{file_ext}</code> &bull; 
            <strong>Includes:</strong> Citations ({inc_cit}), Metadata ({inc_meta}), Graph ({inc_graph}), Notation ({inc_not})
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Handle Export Generation
    if submit_export:
        start_time = time.perf_counter()

        with st.spinner("Generating export file via ExportService..."):
            out_name = f"{export_target.lower().replace(' ', '_')}_{int(time.time())}.{file_ext}"
            out_file = export_service.export_dir / out_name

            # Assemble data payload based on target
            if "Paper Metadata" in export_target:
                exported_path = export_service.export_summaries(
                    documents_or_results=target_papers,
                    format=fmt_clean if fmt_clean in ("json", "csv", "markdown") else "markdown",
                    output_path=out_file,
                )
            elif "Search Results" in export_target:
                search_svc = get_search_service()
                s_hist = search_svc.get_history()
                exported_path = export_service.export_research_notes(
                    data={"search_history": s_hist, "scoped_papers": [p.get("paper_id") for p in target_papers]},
                    format=fmt_clean if fmt_clean in ("json", "csv", "markdown") else "markdown",
                    output_path=out_file,
                )
            elif "AI Q&A" in export_target:
                chat_svc = get_chat_service()
                c_hist = chat_svc.get_chat_history()
                exported_path = export_service.export_research_notes(
                    data={"chat_history": c_hist},
                    format=fmt_clean if fmt_clean in ("json", "csv", "markdown") else "markdown",
                    output_path=out_file,
                )
            elif "Notation" in export_target:
                graph_svc = get_graph_service()
                not_graph = graph_svc.build_notation_graph()
                exported_path = export_service.export_research_notes(
                    data=not_graph,
                    format=fmt_clean if fmt_clean in ("json", "csv", "markdown") else "markdown",
                    output_path=out_file,
                )
            else:
                dash_svc = get_dashboard_service()
                stats = dash_svc.get_statistics()
                exported_path = export_service.export_research_notes(
                    data=stats,
                    format=fmt_clean if fmt_clean in ("json", "csv", "markdown") else "markdown",
                    output_path=out_file,
                )

            duration_ms = int((time.perf_counter() - start_time) * 1000)
            file_bytes = exported_path.read_bytes() if exported_path.exists() else b""
            f_size = len(file_bytes)

            # Record in session state history
            if "export_history" not in st.session_state:
                st.session_state["export_history"] = []

            st.session_state["export_history"].append(
                {
                    "filename": exported_path.name,
                    "target": export_target,
                    "format": export_format,
                    "size_str": format_bytes_to_kb(f_size),
                    "duration_ms": duration_ms,
                    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "file_path": str(exported_path),
                    "bytes": file_bytes,
                    "mime": mime_type,
                }
            )

            st.session_state["active_export"] = {
                "path": exported_path,
                "bytes": file_bytes,
                "filename": exported_path.name,
                "mime": mime_type,
                "size_str": format_bytes_to_kb(f_size),
                "duration_ms": duration_ms,
            }

    # Render Active Download Section if available
    active_exp = st.session_state.get("active_export")
    if active_exp and active_exp.get("bytes"):
        st.success(
            f"✅ **Export generated successfully!** File size: `{active_exp['size_str']}` &bull; Duration: `{active_exp['duration_ms']} ms`"
        )
        st.download_button(
            label=f"📥 Download {active_exp['filename']}",
            data=active_exp["bytes"],
            file_name=active_exp["filename"],
            mime=active_exp["mime"],
            type="primary",
            use_container_width=True,
        )

    # Export History Section
    exp_history = st.session_state.get("export_history", [])
    if exp_history:
        st.divider()
        with st.expander(f"📜 Export Audit History ({len(exp_history)})"):
            for h_idx, item in enumerate(reversed(exp_history), start=1):
                fname = item.get("filename")
                ts = item.get("timestamp")
                sz = item.get("size_str")
                dur = item.get("duration_ms")

                col_info, col_dl = st.columns([3, 1])
                with col_info:
                    st.markdown(
                        f"**{h_idx}. `{fname}`** &bull; `<small style='color:#94A3B8;'>{ts}</small>` "
                        f"&bull; Size: `{sz}` &bull; Duration: `{dur} ms`",
                        unsafe_allow_html=True,
                    )
                with col_dl:
                    if item.get("bytes"):
                        st.download_button(
                            label="📥 Download",
                            data=item["bytes"],
                            file_name=fname,
                            mime=item.get("mime", "text/plain"),
                            key=f"dl_hist_{h_idx}",
                            use_container_width=True,
                        )

            if st.button("🗑️ Delete Export History", use_container_width=True):
                st.session_state["export_history"] = []
                st.session_state["active_export"] = None
                st.toast("Export history deleted!")
                st.rerun()


if __name__ == "__main__":
    import sys
    from pathlib import Path
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from src.ui.layout import render_app_layout
    set_current_page("export")
    render_app_layout()

