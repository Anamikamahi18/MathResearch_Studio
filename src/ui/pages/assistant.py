"""AI Research Assistant page view for MathResearch Studio UI."""

from __future__ import annotations

import logging
import time
from typing import Any

import streamlit as st

from src.ui.components.empty_state import render_empty_state
from src.ui.components.page_title import render_page_title
from src.ui.state import get_chat_service, get_document_service

logger = logging.getLogger(__name__)

EXAMPLE_QUESTIONS = [
    "What is the rigorous definition of a Hilbert Space and inner product norm?",
    "Explain the proof structure and antecedents of the Banach Fixed Point Theorem.",
    "Summarize the main theorems, lemmas, and LaTeX equations across the ingested math papers.",
]


def render_decision_badge(decision_val: str) -> tuple[str, str, str]:
    """Get background color, text color, and icon for guardrail decision."""
    val = str(decision_val).upper()
    if val in ("RETURN", "PASS", "ACCEPT"):
        return "rgba(16, 185, 129, 0.15)", "#34D399", "✅ Passed Guardrails"
    elif val in ("RETURN_WITH_WARNING", "WARNING", "MODIFY", "ASK_FOR_CLARIFICATION", "INSUFFICIENT_EVIDENCE"):
        return "rgba(245, 158, 11, 0.15)", "#FBBF24", f"⚠️ {val.replace('_', ' ').title()}"
    else:
        return "rgba(239, 68, 68, 0.15)", "#F87171", f"🛑 {val.replace('_', ' ').title()}"



def render_assistant_page() -> None:
    """Render the AI Research Assistant page view."""
    render_page_title(
        title="Mathematics AI Research Assistant",
        subtitle="Ask grounded questions across mathematical literature powered by multi-stage RAG, proof evidence mapping, and mathematical guardrails.",
        icon="🤖",
        badge="Math AI Assistant",
    )


    doc_service = get_document_service()
    chat_service = get_chat_service()

    # Suggested Example Questions Chips
    st.markdown("**Suggested Research Questions:**")
    cols_ex = st.columns(len(EXAMPLE_QUESTIONS))
    selected_example = None
    for i, ex_q in enumerate(EXAMPLE_QUESTIONS):
        with cols_ex[i]:
            if st.button(f"💡 {ex_q[:35]}...", key=f"ex_btn_{i}", use_container_width=True):
                selected_example = ex_q

    # Manage input query text in session state
    default_q = selected_example or st.session_state.get("pending_assistant_query", "")

    # Question Input Form
    with st.form(key="assistant_question_form", clear_on_submit=False):
        question_text = st.text_area(
            label="Research Question",
            value=default_q,
            placeholder="Ask a technical question or query mathematical concepts across your library...",
            height=100,
            key="assistant_question_input",
        )

        c_topk, c_papers = st.columns([1, 3])

        with c_topk:
            top_k = st.selectbox(
                label="Evidence Top-K",
                options=[5, 10, 20],
                index=0,
                help="Maximum candidate passages to retrieve for grounding.",
            )

        with c_papers:
            papers = doc_service.list_papers()
            paper_options = {p.get("title", p.get("paper_id")): p.get("paper_id") for p in papers}
            selected_paper_titles = st.multiselect(
                label="Scope to Paper(s)",
                options=list(paper_options.keys()),
                placeholder="Search across all library documents...",
            )

        submit_ask = st.form_submit_button("🤖 Ask AI Assistant", type="primary", use_container_width=True)

    # Assemble Filter Criteria
    filters: dict[str, Any] = {}
    if selected_paper_titles:
        selected_ids = [paper_options[t] for t in selected_paper_titles if t in paper_options]
        if selected_ids:
            filters["paper_id"] = selected_ids if len(selected_ids) > 1 else selected_ids[0]

    # Handle Form Submission
    if submit_ask and question_text.strip():
        start_time = time.perf_counter()

        with st.spinner("Executing 8-stage RAG pipeline (Retrieval, Prompt, Answer, Evidence, Citations, Grounding, Guardrails)..."):
            try:
                response = chat_service.receive_question(
                    question=question_text.strip(),
                    top_k=top_k,
                    filters=filters if filters else None,
                )
                duration_ms = int((time.perf_counter() - start_time) * 1000)

                st.session_state["active_assistant_response"] = response
                st.session_state["active_assistant_question"] = question_text.strip()
                st.session_state["active_assistant_duration_ms"] = duration_ms
            except Exception as exc:
                logger.error("Failed to execute RAG pipeline: %s", exc, exc_info=True)
                st.error(f"❌ Error generating answer: {exc}")

    # Render Active Response View
    active_response = st.session_state.get("active_assistant_response")
    active_question = st.session_state.get("active_assistant_question")
    active_duration = st.session_state.get("active_assistant_duration_ms", 0)

    if active_question and active_response:
        st.divider()

        # Decision & Metrics Header Bar
        dec_val = active_response.decision.value if hasattr(active_response.decision, "value") else str(active_response.decision)
        bg_color, text_color, dec_label = render_decision_badge(dec_val)
        confidence_pct = int(active_response.confidence * 100) if hasattr(active_response, "confidence") else 0
        retrieved_count = len(active_response.metadata.get("retrieved_candidates", [])) if isinstance(active_response.metadata, dict) else 0

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(
                f"""
                <div style="background: {bg_color}; color: {text_color}; border: 1px solid {text_color}44; border-radius: 8px; padding: 10px; text-align: center; font-weight: bold;">
                    {dec_label}
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m2:
            st.metric("Grounding Confidence", f"{confidence_pct}%")
        with m3:
            st.metric("Pipeline Duration", f"{active_duration} ms")
        with m4:
            st.metric("Evidence Passages", f"{retrieved_count}")

        # Guardrail Warnings
        if active_response.warnings:
            for w in active_response.warnings:
                st.warning(f"⚠️ **Guardrail Warning:** {w}")

        # Answer Section
        st.markdown(f"### Question: *\"{active_question}\"*")
        st.markdown(
            f"""
            <div style="background: #1E293B; border-left: 4px solid #6366F1; padding: 16px; border-radius: 4px; margin-bottom: 20px;">
                {active_response.answer_text}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Tabs for Evidence and Citations
        tab_ev, tab_cit, tab_raw = st.tabs(["📚 Supporting Evidence", "🏷️ Citations & Bibliography", "🔍 Raw Pipeline Inspection"])

        with tab_ev:
            evidence_items = active_response.metadata.get("evidence_items", []) if isinstance(active_response.metadata, dict) else []
            retrieved_cands = active_response.metadata.get("retrieved_candidates", []) if isinstance(active_response.metadata, dict) else []

            passages = evidence_items or retrieved_cands

            if passages:
                for idx, item in enumerate(passages, start=1):
                    # Handle dict or object attributes
                    paper_title = getattr(item, "paper_title", None) or (item.get("paper_title") if isinstance(item, dict) else "Unknown Paper")
                    section_title = getattr(item, "section_title", None) or (item.get("section_title") if isinstance(item, dict) else "Section")
                    score = getattr(item, "final_score", None) or getattr(item, "score", 0.0) or (item.get("score", 0.0) if isinstance(item, dict) else 0.0)
                    text = getattr(item, "text", None) or (item.get("text", "") if isinstance(item, dict) else "")
                    page_start = getattr(item, "page_start", 1) or (item.get("page_start", 1) if isinstance(item, dict) else 1)

                    with st.expander(f"Passage #{idx} [{float(score):.4f}] **{paper_title}** - *{section_title}* (Page {page_start})"):
                        st.info(text)
            else:
                st.caption("No specific evidence passages mapped for this answer.")

        with tab_cit:
            citations = active_response.citations
            bibliography = active_response.bibliography

            if citations:
                st.markdown("#### In-Text Citations")
                for cit in citations:
                    st.markdown(f"- 🏷️ {cit}")

            if bibliography:
                st.markdown("#### Bibliography & References")
                for bib in bibliography:
                    st.markdown(f"- 📄 {bib}")

            if not citations and not bibliography:
                st.caption("No explicit academic citations generated for this answer.")

        with tab_raw:
            st.json(active_response.to_dict())

    # Render Empty Guidance State if no question submitted yet
    elif not active_question:
        render_empty_state(
            title="Ask AI Research Assistant",
            message="Enter a question above or select an example question to generate grounded answers backed by evidence passages, citations, and guardrails.",
            icon="🤖",
        )

    # Conversation History Section
    history = chat_service.get_chat_history()
    if history:
        st.divider()
        with st.expander(f"💬 Q&A Conversation History ({len(history)})"):
            for h_idx, turn in enumerate(reversed(history), start=1):
                q_txt = turn.get("question", "")
                ts = turn.get("timestamp", "")[:19].replace("T", " ")
                dec = turn.get("decision", "ACCEPT")
                bg, fg, lbl = render_decision_badge(dec)

                st.markdown(
                    f"**{h_idx}. Q: \"{q_txt}\"** &bull; `<small style='color:#94A3B8;'>{ts}</small>` "
                    f"<span style='background:{bg}; color:{fg}; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem;'>{lbl}</span>",
                    unsafe_allow_html=True,
                )
                prev_resp = turn.get("response")
                if prev_resp and hasattr(prev_resp, "answer_text"):
                    st.caption(f"A: {prev_resp.answer_text[:200]}...")

            if st.button("🗑️ Clear Conversation History", use_container_width=True):
                chat_service.clear_chat_history()
                st.toast("Conversation history cleared!")
                st.rerun()


if __name__ == "__main__":
    import sys
    from pathlib import Path
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from src.ui.layout import render_app_layout
    set_current_page("assistant")
    render_app_layout()

