"""Shared page initialization and session state management for multi-page support."""
from typing import Tuple, Callable
import streamlit as st
import networkx as nx
from algorithms.traversal_engine import TraversalEngine
from graph_utils.sample_graphs import get_small_connected_graph
from components.security import render_security_gate, is_authenticated, logout_user


DARK_THEME_CSS = """
<style>
.stApp {
    background-color: #0B0F19;
    color: #F8FAFC;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #1F2937;
}

[data-testid="stMetricValue"] {
    font-size: 24px !important;
    font-weight: 700 !important;
    color: #F8FAFC !important;
}
[data-testid="stMetricLabel"] {
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #94A3B8 !important;
    text-transform: uppercase;
}

.streamlit-expanderHeader {
    background-color: #1E293B !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    color: #E2E8F0 !important;
}

div.stButton > button:first-child {
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s ease-in-out;
}
div.stButton > button:hover {
    border-color: #818CF8;
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.35);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px;
    padding: 8px 16px;
    background-color: #1E293B;
    color: #94A3B8;
}
.stTabs [aria-selected="true"] {
    background-color: #312E81 !important;
    color: #F8FAFC !important;
    font-weight: 700;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""


def ensure_session_state() -> Tuple[nx.Graph, TraversalEngine]:
    """Ensure persistent session state exists for graph topology and traversal engine."""
    if "graph" not in st.session_state:
        st.session_state.graph = get_small_connected_graph()

    if "traversal_engine" not in st.session_state:
        engine = TraversalEngine()
        nodes = list(st.session_state.graph.nodes())
        start_n = nodes[0] if nodes else None
        engine.initialize_traversal(
            graph=st.session_state.graph,
            algorithm="BFS",
            start_node=start_n,
            traverse_all_components=False
        )
        st.session_state.traversal_engine = engine

    return st.session_state.graph, st.session_state.traversal_engine


def reset_graph_to_default() -> None:
    """Reset the graph topology back to the default small connected example."""
    st.session_state.graph = get_small_connected_graph()
    nodes = list(st.session_state.graph.nodes())
    start_n = nodes[0] if nodes else None
    if "traversal_engine" in st.session_state:
        st.session_state.traversal_engine.initialize_traversal(
            graph=st.session_state.graph,
            algorithm="BFS",
            start_node=start_n,
            traverse_all_components=False
        )


def sync_graph_update(new_graph: nx.Graph) -> None:
    """Synchronize graph updates into session state and re-initialize traversal engine."""
    st.session_state.graph = new_graph
    nodes = list(new_graph.nodes())
    if "traversal_engine" in st.session_state:
        curr_start = st.session_state.traversal_engine.start_node
        valid_start = curr_start if (curr_start in nodes) else (nodes[0] if nodes else None)
        st.session_state.traversal_engine.initialize_traversal(
            graph=new_graph,
            algorithm=st.session_state.traversal_engine.algorithm,
            start_node=valid_start,
            traverse_all_components=st.session_state.traversal_engine.traverse_all_components
        )


def init_page(page_title: str, page_icon: str = "🕸️") -> Tuple[nx.Graph, TraversalEngine]:
    """
    Standard initialization for all pages in the multi-page application.
    Enforces authentication security gate, sets page config, CSS, and renders sidebar controls.
    """
    try:
        st.set_page_config(
            page_title=f"{page_title} - Graph Traversal Visualizer",
            page_icon=page_icon,
            layout="wide",
            initial_sidebar_state="expanded"
        )
    except Exception:
        pass

    st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)
    
    if not render_security_gate():
        st.stop()

    graph, engine = ensure_session_state()

    with st.sidebar:
        auth_user = st.session_state.get("auth_user", "admin")
        st.markdown(
            f"""
            <div style="background:#0F172A; border:1px solid #334155; border-radius:6px; padding:6px 10px; margin-bottom:12px; display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:11px; color:#94A3B8;">User: <b style="color:#10B981;">{auth_user}</b></span>
                <span style="background:#059669; color:#FFFFFF; font-size:9px; font-weight:700; padding:1px 5px; border-radius:4px;">AUTHENTICATED</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px; padding-bottom:12px; border-bottom:1px solid #334155;">
                <div style="background:linear-gradient(135deg, #6366F1, #8B5CF6); width:36px; height:36px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:18px; box-shadow:0 0 12px rgba(99,102,241,0.5);">
                    🕸️
                </div>
                <div>
                    <div style="font-size:16px; font-weight:800; color:#F8FAFC; letter-spacing:-0.02em;">Graph Visualizer</div>
                    <div style="font-size:10px; font-weight:600; color:#818CF8; text-transform:uppercase; letter-spacing:0.06em;">DSA Learning Suite</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        n_nodes = graph.number_of_nodes() if graph else 0
        n_edges = graph.number_of_edges() if graph else 0
        is_dir = "Directed" if (graph and graph.is_directed()) else "Undirected"
        is_w = "Weighted" if (graph and graph.graph.get("is_weighted", False)) else "Unweighted"

        st.markdown(
            f"""
            <div style="background:#1E293B; border:1px solid #334155; border-radius:8px; padding:10px 12px; margin-bottom:12px;">
                <div style="font-size:10px; font-weight:700; color:#94A3B8; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:4px;">Active Graph Info</div>
                <div style="display:flex; justify-content:space-between; font-size:12px; color:#E2E8F0; margin-bottom:2px;">
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

        col_act1, col_act2 = st.columns(2)
        with col_act1:
            if st.button("🔄 Reset Graph", key=f"sidebar_reset_{page_title.lower().replace(' ', '_')}", use_container_width=True, help="Reset to default 6-node graph"):
                reset_graph_to_default()
                st.rerun()
        with col_act2:
            if st.button("🔒 Sign Out", key=f"sidebar_logout_{page_title.lower().replace(' ', '_')}", use_container_width=True, help="Sign out securely"):
                logout_user()
                st.rerun()

    return graph, engine
