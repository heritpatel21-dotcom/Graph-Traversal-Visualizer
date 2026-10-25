"""Sidebar navigation and quick action controls."""
from typing import Tuple, Callable
import streamlit as st
import networkx as nx
from graph_utils.sample_graphs import get_small_connected_graph


PAGES = [
    "Dashboard",
    "Graph Editor",
    "Traversal Visualizer",
    "Algorithm Explorer",
    "Complexity Analysis",
    "About Project"
]


def render_sidebar(graph: nx.Graph, on_reset_graph: Callable[[], None]) -> str:
    """Render the sidebar with brand logo, navigation links, graph summary, and reset action."""
    with st.sidebar:
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px; padding-bottom:14px; border-bottom:1px solid #334155;">
                <div style="background:linear-gradient(135deg, #6366F1, #8B5CF6); width:38px; height:38px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:20px; box-shadow:0 0 12px rgba(99,102,241,0.5);">
                    🕸️
                </div>
                <div>
                    <div style="font-size:17px; font-weight:800; color:#F8FAFC; letter-spacing:-0.02em;">Graph Visualizer</div>
                    <div style="font-size:11px; font-weight:500; color:#818CF8; text-transform:uppercase; letter-spacing:0.06em;">DSA Learning Suite</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "<div style='font-size:11px; font-weight:700; text-transform:uppercase; color:#94A3B8; letter-spacing:0.06em; margin-bottom:8px;'>Navigation</div>",
            unsafe_allow_html=True
        )

        current_page = st.radio(
            "Go to page",
            PAGES,
            index=0,
            label_visibility="collapsed"
        )

        st.markdown("<hr style='border-color:#334155; margin:16px 0;'>", unsafe_allow_html=True)

        n_nodes = graph.number_of_nodes() if graph else 0
        n_edges = graph.number_of_edges() if graph else 0
        is_dir = "Directed" if (graph and graph.is_directed()) else "Undirected"
        is_w = "Weighted" if (graph and graph.graph.get("is_weighted", False)) else "Unweighted"

        st.markdown(
            f"""
            <div style="background:#1E293B; border:1px solid #334155; border-radius:8px; padding:12px; margin-bottom:14px;">
                <div style="font-size:11px; font-weight:700; color:#94A3B8; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:6px;">Active Graph Info</div>
                <div style="display:flex; justify-content:space-between; font-size:13px; color:#E2E8F0; margin-bottom:4px;">
                    <span>Nodes (V): <b>{n_nodes}</b></span>
                    <span>Edges (E): <b>{n_edges}</b></span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#818CF8;">
                    <span>{is_dir}</span>
                    <span>{is_w}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("🔄 Reset Graph to Default", use_container_width=True, help="Reset the graph to the default 6-node example"):
            on_reset_graph()
            st.rerun()

        st.markdown(
            """
            <div style="font-size:11px; color:#64748B; text-align:center; margin-top:20px; line-height:1.4;">
                Graph Traversal Visualizer v1.0<br>
                Python 3.11+ • Streamlit • Plotly
            </div>
            """,
            unsafe_allow_html=True
        )

    return current_page
