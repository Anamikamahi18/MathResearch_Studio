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
        title="Upload Research Papers",
        subtitle="Ingest academic papers (Mathematics, Computer Science, Physics, Biology, Economics, etc.) into the vector store, parser, and Knowledge Graph.",
        icon="📤",
        badge="Document Ingestion",
    )



    doc_service = get_document_service()

    st.markdown(
        """
        <div class="mrs-card">
            <h3>PDF Document Ingestion Pipeline</h3>
            <p style="color: #94A3B8; margin-bottom: 0.5rem;">
                Select or drag-and-drop PDF research papers below. The ingestion pipeline extracts section hierarchies,
                LaTeX equations, references, mathematical entities (definitions, theorems, lemmas, proofs), generates
                embeddings into FAISS, and updates the statement dependency graph.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_files = st.file_uploader(
        label="Select PDF Files",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more mathematical PDF research papers.",
    )

    if uploaded_files:
        st.markdown(f"### Selected Files ({len(uploaded_files)})")

        for u_file in uploaded_files:
            file_size_str = format_file_size(len(u_file.getvalue()))
            st.caption(f"📄 **{u_file.name}** ({file_size_str})")

        if st.button("🚀 Process & Ingest Papers", type="primary", use_container_width=True):
            st.divider()
            results: list[dict[str, Any]] = []
            errors: list[dict[str, Any]] = []

            for idx, u_file in enumerate(uploaded_files, start=1):
                filename = u_file.name
                file_bytes = u_file.getvalue()

                st.markdown(f"#### Processing [{idx}/{len(uploaded_files)}]: `{filename}`")

                try:
                    # 1. Upload paper PDF
                    with st.spinner(f"Saving '{filename}' to upload directory..."):
                        saved_path = doc_service.upload_paper(file_bytes, filename=filename)
                        st.write(f"✓ Saved to `{saved_path}`")

                    # 2. Parse paper PDF
                    with st.spinner(f"Parsing LaTeX equations, sections, & entities in '{filename}'..."):
                        parsed_doc = doc_service.parse_paper(saved_path)
                        paper_id = parsed_doc.get("paper_id", "")
                        title = parsed_doc.get("metadata", {}).get("title") or filename
                        st.write(f"✓ Parsed `{paper_id}` ('{title}')")

                    # 3. Store & Index in Vector Store + Knowledge Graph
                    with st.spinner(f"Generating FAISS embeddings & building graph for '{filename}'..."):
                        store_metrics = doc_service.store_paper(parsed_doc)
                        results.append(store_metrics)
                        st.write(
                            f"✓ Indexed {store_metrics['chunk_count']} vector chunks & "
                            f"{store_metrics['graph_node_count']} graph nodes"
                        )

                except Exception as exc:
                    logger.error("Failed to process file '%s': %s", filename, exc, exc_info=True)
                    errors.append({"filename": filename, "error": str(exc)})

            # Render Summary Callouts
            if results:
                st.success(f"Successfully processed and ingested {len(results)} paper(s)!")
                for res in results:
                    st.markdown(
                        f"""
                        <div class="mrs-card" style="border-left: 4px solid #10B981;">
                            <h4 style="margin: 0 0 0.25rem 0; color: #F8FAFC;">{res['title']}</h4>
                            <p style="margin: 0; font-size: 0.85rem; color: #94A3B8;">
                                <strong>Paper ID:</strong> <code>{res['paper_id']}</code> &bull; 
                                <strong>Chunks Indexed:</strong> {res['chunk_count']} &bull; 
                                <strong>Graph Nodes:</strong> {res['graph_node_count']} &bull; 
                                <strong>Graph Edges:</strong> {res['graph_edge_count']}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("📚 View Document Library", type="secondary", use_container_width=True):
                        set_current_page("library")
                        st.rerun()

            if errors:
                for err in errors:
                    render_error_banner(
                        title=f"Failed to Process '{err['filename']}'",
                        message="An error occurred during parsing or indexing.",
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

