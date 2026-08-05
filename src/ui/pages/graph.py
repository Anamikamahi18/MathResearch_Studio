"""Research Graph page view for MathResearch Studio UI."""

from __future__ import annotations

import html
import logging
import time
from typing import Any

import streamlit as st
import streamlit.components.v1 as components

from src.ui.components.empty_state import render_empty_state
from src.ui.components.page_title import render_page_title
from src.ui.state import get_document_service, get_graph_service

logger = logging.getLogger(__name__)

COLOR_MAP = {
    "definition": "#3B82F6",  # Blue
    "theorem": "#10B981",     # Green
    "lemma": "#F59E0B",       # Amber
    "proof": "#8B5CF6",       # Purple
    "other": "#64748B",       # Slate
}

ICON_MAP = {
    "definition": "📘",
    "theorem": "🟢",
    "lemma": "🟡",
    "proof": "🟣",
    "other": "⚪",
}


def render_graph_legend() -> None:
    """Render color and icon legend for graph statement types."""
    st.markdown(
        """
        <div style="display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 16px; padding: 10px 16px; background: #1E293B; border-radius: 8px; border: 1px solid #334155;">
            <span style="font-weight: bold; color: #94A3B8;">Legend:</span>
            <span><span style="color: #3B82F6;">●</span> <strong>Definition</strong></span>
            <span><span style="color: #10B981;">●</span> <strong>Theorem</strong></span>
            <span><span style="color: #F59E0B;">●</span> <strong>Lemma</strong></span>
            <span><span style="color: #8B5CF6;">●</span> <strong>Proof</strong></span>
            <span><span style="color: #64748B;">●</span> <strong>Other / Concept</strong></span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def generate_interactive_graph_html(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    layout: str = "Hierarchical (DAG)",
    height: int = 500,
) -> str:
    """Generate HTML/JS interactive network canvas for rendering the graph."""
    nodes_json_items = []
    for n in nodes:
        nid = n.get("node_id", "")
        lbl = n.get("label") or nid
        ntype = str(n.get("node_type", "other")).lower()
        color = COLOR_MAP.get(ntype, COLOR_MAP["other"])
        nodes_json_items.append(
            f"{{ id: '{html.escape(nid)}', label: '{html.escape(lbl)}', color: '{color}', type: '{ntype}' }}"
        )

    edges_json_items = []
    for e in edges:
        src = e.get("source_id", "")
        tgt = e.get("target_id", "")
        rel = e.get("relation_type", "depends_on")
        edges_json_items.append(
            f"{{ from: '{html.escape(src)}', to: '{html.escape(tgt)}', label: '{html.escape(rel)}' }}"
        )

    nodes_js = "[\n" + ",\n".join(nodes_json_items) + "\n]"
    edges_js = "[\n" + ",\n".join(edges_json_items) + "\n]"

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{
          margin: 0;
          padding: 0;
          background-color: #0F172A;
          color: #F8FAFC;
          font-family: system-ui, -apple-system, sans-serif;
          overflow: hidden;
        }}
        #canvas-container {{
          width: 100%;
          height: {height}px;
          position: relative;
          background: radial-gradient(circle, #1E293B 1px, transparent 1px);
          background-size: 20px 20px;
        }}
        svg {{
          width: 100%;
          height: 100%;
        }}
        .node {{
          cursor: pointer;
          transition: transform 0.2s;
        }}
        .node:hover {{
          filter: drop-shadow(0 0 6px rgba(255,255,255,0.6));
        }}
        .edge {{
          stroke: #475569;
          stroke-width: 1.5px;
          stroke-dasharray: 4,4;
        }}
        .node-text {{
          font-size: 11px;
          fill: #F8FAFC;
          font-weight: 500;
          pointer-events: none;
        }}
        .controls {{
          position: absolute;
          top: 10px;
          right: 10px;
          display: flex;
          gap: 6px;
        }}
        .btn {{
          background: #334155;
          color: white;
          border: none;
          padding: 6px 12px;
          border-radius: 4px;
          cursor: pointer;
          font-size: 12px;
        }}
        .btn:hover {{
          background: #475569;
        }}
      </style>
    </head>
    <body>
      <div id="canvas-container">
        <div class="controls">
          <button class="btn" onclick="resetZoom()">🔍 Reset View</button>
        </div>
        <svg id="graph-svg">
          <defs>
            <marker id="arrow" viewBox="0 0 10 10" refX="18" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748B" />
            </marker>
          </defs>
          <g id="viewport">
            <g id="edges-layer"></g>
            <g id="nodes-layer"></g>
          </g>
        </svg>
      </div>

      <script>
        const nodesData = {nodes_js};
        const edgesData = {edges_js};

        const svg = document.getElementById('graph-svg');
        const viewport = document.getElementById('viewport');
        const edgesLayer = document.getElementById('edges-layer');
        const nodesLayer = document.getElementById('nodes-layer');

        let zoom = 1;
        let panX = 0;
        let panY = 0;
        let isDragging = false;
        let startX, startY;

        // Position nodes on canvas
        const width = window.innerWidth || 800;
        const height = {height};
        const cx = width / 2;
        const cy = height / 2;
        const radius = Math.min(width, height) * 0.35;

        const nodePos = {{}};
        nodesData.forEach((n, i) => {{
          let x, y;
          if ("{layout}".includes("Circular")) {{
            const angle = (i / Math.max(nodesData.length, 1)) * 2 * Math.PI;
            x = cx + radius * Math.cos(angle);
            y = cy + radius * Math.sin(angle);
          }} else if ("{layout}".includes("Hierarchical")) {{
            const cols = Math.ceil(Math.sqrt(nodesData.length));
            const r = Math.floor(i / cols);
            const c = i % cols;
            x = 100 + c * 160;
            y = 80 + r * 120;
          }} else {{
            // Grid / Force layout
            const cols = 4;
            const r = Math.floor(i / cols);
            const c = i % cols;
            x = 120 + c * 170;
            y = 90 + r * 110;
          }}
          nodePos[n.id] = {{ x, y }};
        }});

        // Draw edges
        edgesData.forEach(e => {{
          const p1 = nodePos[e.from];
          const p2 = nodePos[e.to];
          if (p1 && p2) {{
            const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
            line.setAttribute("x1", p1.x);
            line.setAttribute("y1", p1.y);
            line.setAttribute("x2", p2.x);
            line.setAttribute("y2", p2.y);
            line.setAttribute("class", "edge");
            line.setAttribute("marker-end", "url(#arrow)");
            edgesLayer.appendChild(line);
          }}
        }});

        // Draw nodes
        nodesData.forEach(n => {{
          const pos = nodePos[n.id];
          if (!pos) return;

          const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
          g.setAttribute("class", "node");
          g.setAttribute("transform", `translate(${{pos.x}}, ${{pos.y}})`);

          const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
          circle.setAttribute("r", "14");
          circle.setAttribute("fill", n.color);
          circle.setAttribute("stroke", "#FFFFFF");
          circle.setAttribute("stroke-width", "1.5");
          g.appendChild(circle);

          const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
          text.setAttribute("x", "18");
          text.setAttribute("y", "4");
          text.setAttribute("class", "node-text");
          text.textContent = n.label.length > 25 ? n.label.substring(0, 22) + '...' : n.label;
          g.appendChild(text);

          nodesLayer.appendChild(g);
        }});

        // Pan and Zoom controls
        svg.addEventListener('mousedown', e => {{
          isDragging = true;
          startX = e.clientX - panX;
          startY = e.clientY - panY;
        }});

        window.addEventListener('mousemove', e => {{
          if (isDragging) {{
            panX = e.clientX - startX;
            panY = e.clientY - startY;
            updateTransform();
          }}
        }});

        window.addEventListener('mouseup', () => isDragging = false);

        svg.addEventListener('wheel', e => {{
          e.preventDefault();
          const zoomFactor = e.deltaY < 0 ? 1.1 : 0.9;
          zoom = Math.max(0.3, Math.min(3.0, zoom * zoomFactor));
          updateTransform();
        }});

        function updateTransform() {{
          viewport.setAttribute("transform", `translate(${{panX}}, ${{panY}}) scale(${{zoom}})`);
        }}

        function resetZoom() {{
          zoom = 1;
          panX = 0;
          panY = 0;
          updateTransform();
        }}
      </script>
    </body>
    </html>
    """
    return html_code


def render_graph_page() -> None:
    """Render the Research Graph page view."""
    render_page_title(
        title="Mathematical Research Graph",
        subtitle="Explore interactive statement dependencies, definitions, theorems, lemmas, and proof chains.",
        icon="🕸️",
        badge="Dependency Network",
    )


    doc_service = get_document_service()
    graph_service = get_graph_service()

    # Toolbar with Refresh Button
    c_title, c_ref = st.columns([3, 1])
    with c_ref:
        if st.button("🔄 Refresh Graph", type="primary", use_container_width=True):
            with st.spinner("Building dependency graph from parsed papers..."):
                graph_service.build_dependency_graph()
                st.toast("Dependency graph updated!")
                st.rerun()

    render_graph_legend()

    # Obtain Current Graph and Metrics
    graph = graph_service.build_dependency_graph()
    metrics = graph_service.get_graph_metrics()

    total_nodes = metrics.get("total_nodes", len(graph.nodes))
    total_edges = metrics.get("total_edges", len(graph.edges))
    density = metrics.get("density", 0.0)
    avg_deg = float(2 * total_edges / total_nodes) if total_nodes > 0 else 0.0

    # Display Metrics Summary Bar
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Nodes", f"{total_nodes}")
    with m2:
        st.metric("Total Edges", f"{total_edges}")
    with m3:
        st.metric("Average Degree", f"{avg_deg:.2f}")
    with m4:
        st.metric("Graph Density", f"{density:.4f}")

    if total_nodes == 0:
        st.divider()
        render_empty_state(
            title="No Dependency Graph Generated",
            message="No mathematical statements or dependency edges exist in the current library. Upload or parse papers on the Upload page to generate the research graph.",
            icon="🕸️",
        )
        return

    # Controls Panel
    st.divider()
    c_lay, c_src, c_type, c_paper = st.columns(4)

    with c_lay:
        layout_mode = st.selectbox(
            label="Graph Layout",
            options=["Hierarchical (DAG)", "Force-Directed (Spring)", "Circular", "Grid"],
            index=0,
        )

    with c_src:
        search_query = st.text_input(
            label="Search Node",
            placeholder="Search statement label or text...",
            key="graph_search_node_input",
        )

    with c_type:
        node_type_opt = st.selectbox(
            label="Filter Statement Type",
            options=["All", "definition", "theorem", "lemma", "proof"],
            index=0,
        )

    with c_paper:
        papers = doc_service.list_papers()
        paper_options = {p.get("title", p.get("paper_id")): p.get("paper_id") for p in papers}
        selected_paper_titles = st.multiselect(
            label="Filter by Paper",
            options=list(paper_options.keys()),
            placeholder="All papers...",
        )

    # Apply Filters via GraphService.node_lookup()
    type_filter = None if node_type_opt == "All" else node_type_opt
    query_filter = search_query.strip() if search_query.strip() else None

    matched_nodes = graph_service.node_lookup(query=query_filter, node_type=type_filter)

    # Filter by paper if specified
    if selected_paper_titles:
        selected_pids = set(paper_options[t] for t in selected_paper_titles if t in paper_options)
        matched_nodes = [n for n in matched_nodes if n.get("paper_id") in selected_pids]

    matched_node_ids = set(n.get("node_id") for n in matched_nodes)

    # Filter edges connecting matched nodes
    filtered_edges = [
        e.to_dict() if hasattr(e, "to_dict") else e
        for e in graph.edges.values()
        if e.source_id in matched_node_ids and e.target_id in matched_node_ids
    ]

    st.markdown(f"**Displaying {len(matched_nodes)} Node(s) & {len(filtered_edges)} Edge(s):**")

    # Render Interactive Graph Canvas
    graph_html = generate_interactive_graph_html(
        nodes=matched_nodes,
        edges=filtered_edges,
        layout=layout_mode,
        height=480,
    )
    components.html(graph_html, height=500)

    # Node Details Inspector Drawer
    st.divider()
    st.markdown("### 🔍 Statement Node Inspector")

    node_options_dict = {
        f"[{str(n.get('node_type', 'other')).upper()}] {n.get('label') or n.get('node_id')} ({n.get('paper_id')})": n.get("node_id")
        for n in matched_nodes
    }

    if node_options_dict:
        selected_node_label = st.selectbox(
            label="Select Statement Node to Inspect",
            options=list(node_options_dict.keys()),
            index=0,
        )
        selected_node_id = node_options_dict[selected_node_label]

        lookup_res = graph_service.node_lookup(node_id=selected_node_id)
        if lookup_res:
            n_data = lookup_res[0]

            col_details, col_deps = st.columns([2, 1])

            with col_details:
                ntype = str(n_data.get("node_type", "other")).lower()
                icon = ICON_MAP.get(ntype, "⚪")
                color = COLOR_MAP.get(ntype, "#64748B")

                st.markdown(
                    f"""
                    <div style="background: #1E293B; border-left: 4px solid {color}; padding: 16px; border-radius: 6px; margin-bottom: 12px;">
                        <h4 style="margin: 0; color: #F8FAFC;">{icon} {n_data.get('label') or n_data.get('node_id')}</h4>
                        <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 0.85rem;">
                            <strong>Node ID:</strong> <code>{n_data.get('node_id')}</code> &bull; 
                            <strong>Paper ID:</strong> <code>{n_data.get('paper_id')}</code> &bull; 
                            <strong>Section:</strong> {n_data.get('section_id', 'N/A')} &bull; 
                            <strong>Page:</strong> {n_data.get('page_start', 1)}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown("**Full Statement Text:**")
                st.info(n_data.get("text") or "No text excerpt available.")

            with col_deps:
                st.markdown("**Prerequisite Incoming Dependencies:**")
                antecedents = graph_service.get_antecedents(selected_node_id)
                if antecedents:
                    for a in antecedents:
                        a_lbl = a.get("label") or a.get("node_id")
                        st.markdown(f"- ⬅️ **{a_lbl}** (`{a.get('node_type')}`)")
                else:
                    st.caption("No prerequisite dependencies.")

                st.markdown("**Outgoing Consequent Statements:**")
                consequents = graph_service.get_consequents(selected_node_id)
                if consequents:
                    for c in consequents:
                        c_lbl = c.get("label") or c.get("node_id")
                        st.markdown(f"- ➡️ **{c_lbl}** (`{c.get('node_type')}`)")
                else:
                    st.caption("No downstream consequents.")

    else:
        st.caption("No statement nodes match the current filter criteria.")


if __name__ == "__main__":
    import sys
    from pathlib import Path
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from src.ui.layout import render_app_layout
    set_current_page("graph")
    render_app_layout()

