"""Dedicated Traversal Visualizer: Full-canvas view with step-by-step history and tree hierarchy."""
import streamlit as st
import networkx as nx
from algorithms.traversal_engine import TraversalEngine
from components.graph_view import create_graph_figure
from components.traversal_controls import render_traversal_controls
from components.metrics import render_statistics_cards
from components.page_setup import init_page


def render_traversal_visualizer(graph: nx.Graph, engine: TraversalEngine) -> None:
    """Render the dedicated Traversal Visualizer view."""
    st.markdown(
        """
        <div style="margin-bottom:18px;">
            <div style="font-size:24px; font-weight:800; color:#F8FAFC; letter-spacing:-0.02em;">
                Traversal Visualizer Studio
            </div>
            <div style="font-size:14px; color:#94A3B8; margin-top:2px;">
                High-immersion graph traversal canvas with complete step timeline, BFS level trees, and DFS recursion branches.
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

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    render_traversal_controls(engine=engine, graph=graph, key_prefix="viz_studio")

    fig = create_graph_figure(
        graph=graph,
        current_step=current_step,
        start_node=engine.start_node,
        height=620
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True, "scrollZoom": True})

    if current_step:
        st.markdown(
            f"""
            <div style="background:#1E293B; border-left:5px solid #10B981; border-radius:8px; padding:16px 20px; margin-top:14px; box-shadow:0 4px 6px -1px rgba(0,0,0,0.2);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <span style="font-size:12px; font-weight:700; color:#10B981; text-transform:uppercase; letter-spacing:0.06em;">
                        Step #{current_idx + 1} / {total_steps}: {current_step.action}
                    </span>
                    <span style="font-size:12px; color:#94A3B8;">
                        Active Node: <b style="color:#F59E0B;">{current_step.current_node or 'None'}</b>
                    </span>
                </div>
                <div style="font-size:15px; color:#F8FAFC; line-height:1.5;">
                    {current_step.explanation}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    tab_tree, tab_history = st.tabs(["🌳 Level / Depth Hierarchy", "📜 Step Execution History"])

    with tab_tree:
        if current_step and current_step.depth_or_level:
            metric_title = "BFS Level-Order Groups" if engine.algorithm == "BFS" else "DFS Depth Groups"
            grouped: dict[int, list[str]] = {}
            for node, dist in current_step.depth_or_level.items():
                grouped.setdefault(dist, []).append(node)

            st.markdown(f"**{metric_title}**")
            cols = st.columns(min(len(grouped), 6) or 1)
            for idx, lvl in enumerate(sorted(grouped.keys())):
                col_target = cols[idx % len(cols)]
                with col_target:
                    nodes_at_lvl = ", ".join(grouped[lvl])
                    st.markdown(
                        f"""
                        <div style="background:#1E293B; border:1px solid #334155; border-radius:8px; padding:12px; margin-bottom:8px; text-align:center;">
                            <div style="font-size:11px; font-weight:700; color:#818CF8; text-transform:uppercase;">Level / Depth {lvl}</div>
                            <div style="font-size:15px; font-weight:700; color:#F8FAFC; margin-top:4px;">[{nodes_at_lvl}]</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.info("Start traversal to observe levels and depth groupings.")

    with tab_history:
        if engine.steps:
            st.markdown(f"**Full Recorded Execution Log ({len(engine.steps)} steps)**")
            log_data = []
            for s in engine.steps:
                is_active = "👉" if s.step_number == current_idx else ""
                log_data.append({
                    "Active": is_active,
                    "Step": s.step_number + 1,
                    "Action": s.action,
                    "Current": s.current_node or "-",
                    "Queue / Stack": str(s.data_structure_state),
                    "Visited Count": len(s.visited_nodes),
                    "Explanation": s.explanation
                })
            st.dataframe(log_data, use_container_width=True, hide_index=True)
        else:
            st.info("No traversal steps recorded.")


if __name__ == "__main__":
    graph, engine = init_page("Traversal Visualizer", "🕸️")
    render_traversal_visualizer(graph, engine)
