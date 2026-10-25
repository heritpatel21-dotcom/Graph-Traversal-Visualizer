"""Dashboard view: Main workspace combining metrics, interactive canvas, controls, and live state."""
import streamlit as st
import networkx as nx
from algorithms.traversal_engine import TraversalEngine
from components.metrics import render_statistics_cards, render_algorithm_info_panel
from components.graph_view import create_graph_figure
from components.traversal_controls import render_traversal_controls
from components.page_setup import init_page


def render_dashboard(graph: nx.Graph, engine: TraversalEngine) -> None:
    """Render the primary interactive dashboard."""
    st.markdown(
        """
        <div style="margin-bottom:18px;">
            <div style="font-size:24px; font-weight:800; color:#F8FAFC; letter-spacing:-0.02em;">
                Graph Traversal Dashboard
            </div>
            <div style="font-size:14px; color:#94A3B8; margin-top:2px;">
                Interactive step-by-step exploration of Breadth-First Search (BFS) and Depth-First Search (DFS) on custom & preset graphs.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    current_step = engine.get_current_step()
    total_steps = engine.get_total_steps()
    current_idx = engine.current_step_index

    render_statistics_cards(
        graph=graph,
        current_step=current_step,
        total_steps=total_steps,
        current_step_idx=current_idx
    )

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    render_traversal_controls(engine=engine, graph=graph, key_prefix="dash")

    col_graph, col_info = st.columns([1.7, 1.3])

    with col_graph:
        st.markdown(
            """
            <div style="font-size:13px; font-weight:700; color:#CBD5E1; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:6px;">
                Interactive Canvas (Plotly)
            </div>
            """,
            unsafe_allow_html=True
        )
        fig = create_graph_figure(
            graph=graph,
            current_step=current_step,
            start_node=engine.start_node,
            height=580
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True, "scrollZoom": True})

    with col_info:
        render_algorithm_info_panel(
            algorithm=engine.algorithm,
            current_step=current_step,
            total_steps=total_steps,
            current_step_idx=current_idx
        )


if __name__ == "__main__":
    graph, engine = init_page("Dashboard", "📊")
    render_dashboard(graph, engine)
