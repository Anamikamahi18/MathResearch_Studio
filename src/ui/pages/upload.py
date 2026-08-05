"""PDF Upload page view for MathResearch Studio UI."""

from __future__ import annotations

import logging
from typing import Any

import streamlit as st

from src.ui.components.error import render_error_banner
from src.ui.components.page_title import render_page_title
from src.ui.state import get_document_service, set_current_page

logger = logging.getLogger(__name__)


def format_file_size(size_bytes: int) -> str:
    """Format size in bytes to human-readable string (KB/MB)."""
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / (1024 * 1024):.2f} MB"


def render_upload_page() -> None:
    """Render the PDF Upload page view."""
    render_page_title(
        title="Upload Mathematical Papers",
        subtitle="Import mathematical PDF research papers and preprints (Abstract Algebra, Real & Complex Analysis, Topology, Geometry, PDE, Number Theory, etc.) into your research library.",
        icon="📤",
        badge="Math Paper Upload",
    )

    doc_service = get_document_service()

    st.markdown(
        """
        <div class="mrs-card">
            <h3 style="margin-top: 0;">📄 Supported Formats & Processing Guidelines</h3>
            <div style="color: #94A3B8; font-size: 0.88rem; line-height: 1.6;">
                <p><strong>Primary Format:</strong> PDF (<code>.pdf</code>) — the standard format for arXiv preprints, journal papers, and compiled LaTeX manuscripts.</p>
                <p><strong>File Size Limit:</strong> Up to <strong>200 MB</strong> per uploaded paper.</p>
                <p><strong>Images & Figures:</strong> Embedded diagrams, commutative charts, plots, and figures within PDFs are processed automatically; text sections, LaTeX equations (<code>$ ... $</code> and <code>$$ ... $$</code>), and mathematical statements are extracted.</p>
                <p><strong>Automatic Extraction:</strong> Paper title, authors, abstract, section structure, definitions, theorems, lemmas, corollaries, proofs, and references.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_files = st.file_uploader(
        label="Select PDF Files",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more mathematical PDF research papers (up to 200 MB each).",
    )

    if uploaded_files:
        st.markdown(f"### Selected Files ({len(uploaded_files)})")

        for u_file in uploaded_files:
            file_size_str = format_file_size(len(u_file.getvalue()))
            st.caption(f"📄 **{u_file.name}** ({file_size_str})")

        if st.button("📥 Process & Add Papers to Library", type="primary", use_container_width=True):
            st.divider()
            results: list[dict[str, Any]] = []
            errors: list[dict[str, Any]] = []

            for idx, u_file in enumerate(uploaded_files, start=1):
                filename = u_file.name
                file_bytes = u_file.getvalue()

                st.markdown(f"#### Processing Paper [{idx}/{len(uploaded_files)}]: `{filename}`")

                try:
                    # 1. Save uploaded file
                    with st.spinner(f"Importing '{filename}' into workspace library..."):
                        saved_path = doc_service.upload_paper(file_bytes, filename=filename)
                        st.write(f"✓ Imported `{filename}` ({format_file_size(len(file_bytes))})")

                    # 2. Parse paper structure and LaTeX
                    with st.spinner(f"Parsing LaTeX equations, sections, & statements in '{filename}'..."):
                        parsed_doc = doc_service.parse_paper(saved_path)
                        paper_id = parsed_doc.get("paper_id", "")
                        title = parsed_doc.get("title") or parsed_doc.get("metadata", {}).get("title") or filename
                        st.write(f"✓ Parsed `{title}`")

                    # 3. Store and index statements
                    with st.spinner(f"Indexing passages & building statement relationships for '{filename}'..."):
                        store_metrics = doc_service.store_paper(parsed_doc)
                        store_metrics["filename"] = filename
                        results.append(store_metrics)
                        st.write(
                            f"✓ Indexed {store_metrics['chunk_count']} passages & "
                            f"{store_metrics['graph_node_count']} statement connections"
                        )

                except Exception as exc:
                    logger.error("Failed to process file '%s': %s", filename, exc, exc_info=True)
                    errors.append({"filename": filename, "error": str(exc)})

            # Render Summary Callouts
            if results:
                st.success(f"Successfully processed and added {len(results)} paper(s) to your research library!")
                for res in results:
                    fname = res.get("filename", "")
                    st.markdown(
                        f"""
                        <div class="mrs-card" style="border-left: 4px solid #10B981;">
                            <h4 style="margin: 0 0 0.25rem 0; color: #F8FAFC;">{res['title']}</h4>
                            <p style="margin: 0; font-size: 0.85rem; color: #94A3B8;">
                                <strong>File:</strong> <code>{fname}</code> &bull; 
                                <strong>Reference ID:</strong> <code>{res['paper_id']}</code> &bull; 
                                <strong>Passages Processed:</strong> {res['chunk_count']} &bull; 
                                <strong>Statements Extracted:</strong> {res['graph_node_count']} &bull; 
                                <strong>Connections Built:</strong> {res['graph_edge_count']}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("📚 Go to Mathematical Library", type="secondary", use_container_width=True):
                        set_current_page("library")
                        st.rerun()

            if errors:
                for err in errors:
                    render_error_banner(
                        title=f"Failed to Process '{err['filename']}'",
                        message="An error occurred during paper parsing or indexing.",
                        details=err["error"],
                    )


if __name__ == "__main__":
    import sys
    from pathlib import Path
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from src.ui.layout import render_app_layout
    set_current_page("upload")
    render_app_layout()

