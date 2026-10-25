"""Traversal control panel component for playback, step controls, and parameter selection."""
import time
from typing import Optional, List
import streamlit as st
import networkx as nx
from algorithms.traversal_engine import TraversalEngine


def render_traversal_controls(
    engine: TraversalEngine,
    graph: nx.Graph,
    key_prefix: str = "ctrl"
) -> None:
    """Render the playback control bar, algorithm switcher, and step navigation."""
    nodes = sorted(list(graph.nodes()), key=lambda x: str(x))
    
    st.markdown(
        """
        <div style="background:#1E293B; border-radius:10px; border:1px solid #334155; padding:16px; margin-bottom:14px; box-shadow:0 4px 6px -1px rgba(0,0,0,0.2);">
            <div style="font-size:14px; font-weight:700; color:#E2E8F0; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:12px;">
                Traversal Control Panel
            </div>
        """,
        unsafe_allow_html=True
    )

    if not nodes:
        st.warning("Graph has no nodes. Please add nodes in Graph Editor or load a sample graph.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    col_algo, col_start, col_mode, col_speed = st.columns([1.5, 1.5, 1.8, 1.4])

    with col_algo:
        algo_options = ["BFS (Breadth-First)", "DFS (Depth-First)"]
        curr_algo_idx = 0 if engine.algorithm == "BFS" else 1
        selected_algo_label = st.selectbox(
            "Algorithm",
            algo_options,
            index=curr_algo_idx,
            key=f"{key_prefix}_algo_select",
            help="Choose Breadth-First Search (level-by-level) or Depth-First Search (branch-by-branch)."
        )
        new_algo = "BFS" if "BFS" in selected_algo_label else "DFS"

    with col_start:
        curr_start = engine.start_node if (engine.start_node in nodes) else nodes[0]
        start_idx = nodes.index(curr_start) if curr_start in nodes else 0
        selected_start = st.selectbox(
            "Start Node",
            nodes,
            index=start_idx,
            key=f"{key_prefix}_start_select",
            help="Select the starting root vertex for graph traversal."
        )

    with col_mode:
        traverse_all = st.checkbox(
            "Traverse All Components",
            value=engine.traverse_all_components,
            key=f"{key_prefix}_all_components",
            help="If checked, traversal visits all disconnected components in the graph."
        )

    with col_speed:
        speed = st.slider(
            "Delay (sec/step)",
            min_value=0.2,
            max_value=2.0,
            value=float(engine.speed),
            step=0.1,
            key=f"{key_prefix}_speed_slider",
            help="Speed of automated playback animation."
        )
        engine.speed = speed

    config_changed = (
        new_algo != engine.algorithm or
        selected_start != engine.start_node or
        traverse_all != engine.traverse_all_components or
        not engine.steps
    )

    if config_changed:
        engine.initialize_traversal(
            graph=graph,
            algorithm=new_algo,
            start_node=selected_start,
            traverse_all_components=traverse_all
        )
        st.rerun()

    col_btn1, col_btn2, col_btn3, col_btn4, col_btn5, col_btn6 = st.columns([1.2, 1.2, 1.5, 1.2, 1.2, 1.2])

    with col_btn1:
        if st.button("⏮ Reset", key=f"{key_prefix}_btn_reset", use_container_width=True, help="Reset traversal to step 0"):
            engine.reset_traversal()
            st.rerun()

    with col_btn2:
        prev_disabled = engine.current_step_index <= 0 or engine.is_playing
        if st.button("◀ Prev", key=f"{key_prefix}_btn_prev", disabled=prev_disabled, use_container_width=True, help="Step backward"):
            engine.step_backward()
            st.rerun()

    with col_btn3:
        if engine.is_playing:
            if st.button("⏸ Pause", key=f"{key_prefix}_btn_pause", use_container_width=True, type="secondary"):
                engine.is_playing = False
                st.rerun()
        else:
            play_disabled = engine.is_finished()
            if st.button("▶ Play", key=f"{key_prefix}_btn_play", disabled=play_disabled, use_container_width=True, type="primary"):
                engine.is_playing = True
                st.rerun()

    with col_btn4:
        next_disabled = engine.is_finished() or engine.is_playing
        if st.button("Next ▶", key=f"{key_prefix}_btn_next", disabled=next_disabled, use_container_width=True, help="Step forward"):
            engine.step_forward()
            st.rerun()

    with col_btn5:
        finish_disabled = engine.is_finished() or engine.is_playing
        if st.button("⏭ Finish", key=f"{key_prefix}_btn_finish", disabled=finish_disabled, use_container_width=True, help="Jump to final completed step"):
            engine.jump_to_step(len(engine.steps) - 1)
            st.rerun()

    with col_btn6:
        learning_toggle = st.checkbox(
            "🎓 Learn Mode",
            value=engine.learning_mode,
            key=f"{key_prefix}_learn_toggle",
            help="Show educational insights and step breakdowns"
        )
        engine.learning_mode = learning_toggle

    total_steps = len(engine.steps)
    if total_steps > 1:
        scrubber_val = st.slider(
            "Timeline Scrubber",
            min_value=0,
            max_value=total_steps - 1,
            value=engine.current_step_index,
            key=f"{key_prefix}_step_scrubber",
            help="Drag slider to inspect any step directly."
        )
        if scrubber_val != engine.current_step_index and not engine.is_playing:
            engine.jump_to_step(scrubber_val)
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    if engine.is_playing:
        if not engine.is_finished():
            time.sleep(engine.speed)
            engine.step_forward()
            st.rerun()
        else:
            engine.is_playing = False
            st.rerun()
