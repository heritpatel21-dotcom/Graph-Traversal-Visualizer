"""Metrics and state summary display components."""
from typing import Optional, Dict, Any, List
import streamlit as st
import networkx as nx
from algorithms import TraversalStep


def render_statistics_cards(
    graph: nx.Graph,
    current_step: Optional[TraversalStep] = None,
    total_steps: int = 0,
    current_step_idx: int = 0
) -> None:
    """Render top 4 key metric cards: Nodes, Edges, Visited, and Progress."""
    num_nodes = graph.number_of_nodes() if graph else 0
    num_edges = graph.number_of_edges() if graph else 0

    visited_count = len(current_step.visited_nodes) if current_step else 0
    visited_pct = (visited_count / num_nodes * 100) if num_nodes > 0 else 0.0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div style="background:#1E293B; border-radius:10px; border:1px solid #334155; padding:16px 18px; box-shadow:0 4px 6px -1px rgba(0,0,0,0.2);">
                <div style="font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; color:#94A3B8;">Total Nodes (V)</div>
                <div style="font-size:26px; font-weight:700; color:#F8FAFC; margin-top:4px;">{num_nodes}</div>
                <div style="font-size:11px; color:#64748B; margin-top:2px;">Graph Vertices</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        is_dir_badge = "Directed" if (graph and graph.is_directed()) else "Undirected"
        st.markdown(
            f"""
            <div style="background:#1E293B; border-radius:10px; border:1px solid #334155; padding:16px 18px; box-shadow:0 4px 6px -1px rgba(0,0,0,0.2);">
                <div style="font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; color:#94A3B8;">Total Edges (E)</div>
                <div style="font-size:26px; font-weight:700; color:#818CF8; margin-top:4px;">{num_edges}</div>
                <div style="font-size:11px; color:#64748B; margin-top:2px;">{is_dir_badge} Mode</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style="background:#1E293B; border-radius:10px; border:1px solid #334155; padding:16px 18px; box-shadow:0 4px 6px -1px rgba(0,0,0,0.2);">
                <div style="font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; color:#94A3B8;">Visited Nodes</div>
                <div style="font-size:26px; font-weight:700; color:#10B981; margin-top:4px;">{visited_count} <span style="font-size:14px; color:#6EE7B7;">/ {num_nodes}</span></div>
                <div style="font-size:11px; color:#64748B; margin-top:2px;">{visited_pct:.1f}% of graph</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        progress_val = 0.0
        if total_steps > 1:
            progress_val = (current_step_idx / (total_steps - 1)) * 100.0
        elif total_steps == 1:
            progress_val = 100.0

        st.markdown(
            f"""
            <div style="background:#1E293B; border-radius:10px; border:1px solid #334155; padding:16px 18px; box-shadow:0 4px 6px -1px rgba(0,0,0,0.2);">
                <div style="font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; color:#94A3B8;">Traversal Progress</div>
                <div style="font-size:26px; font-weight:700; color:#38BDF8; margin-top:4px;">{progress_val:.0f}%</div>
                <div style="font-size:11px; color:#64748B; margin-top:2px;">Step {current_step_idx + 1 if total_steps > 0 else 0} of {total_steps}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_algorithm_info_panel(
    algorithm: str,
    current_step: Optional[TraversalStep] = None,
    total_steps: int = 0,
    current_step_idx: int = 0
) -> None:
    """Render the detailed algorithm state, data structure inspector, and step commentary."""
    ds_name = "FIFO Queue (deque)" if algorithm == "BFS" else "LIFO Stack (list)"
    ds_badge_color = "#6366F1" if algorithm == "BFS" else "#EC4899"
    time_c = "O(V + E)"
    space_c = "O(V)"

    current_node_display = current_step.current_node if (current_step and current_step.current_node) else "None / Finished"
    visited_list = current_step.visited_nodes if current_step else []
    traversal_order = current_step.traversal_order if current_step else []
    ds_state = current_step.data_structure_state if current_step else []
    explanation = current_step.explanation if current_step else "Select an algorithm and press Run or Next Step."
    action_type = current_step.action if current_step else "IDLE"

    action_colors = {
        "INITIALIZE": "#6366F1",
        "NEW_COMPONENT": "#8B5CF6",
        "DEQUEUE": "#F59E0B",
        "POP_AND_VISIT": "#F59E0B",
        "DISCOVER_NEIGHBOR": "#10B981",
        "PUSH_NEIGHBORS": "#38BDF8",
        "ALREADY_VISITED": "#64748B",
        "BACKTRACK": "#EC4899",
        "COMPLETE": "#10B981",
        "IDLE": "#475569"
    }
    action_badge_color = action_colors.get(action_type, "#6366F1")

    st.markdown(
        f"""
        <div style="background:#1E293B; border-radius:10px; border:1px solid #334155; padding:18px; margin-top:14px; box-shadow:0 4px 6px -1px rgba(0,0,0,0.2);">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #334155; padding-bottom:10px; margin-bottom:12px;">
                <div style="font-size:16px; font-weight:700; color:#F8FAFC;">
                    <span style="color:#818CF8;">{algorithm}</span> Traversal State Machine
                </div>
                <div style="display:flex; gap:8px;">
                    <span style="background:{action_badge_color}; color:#FFFFFF; font-size:11px; font-weight:700; padding:3px 8px; border-radius:6px; letter-spacing:0.04em;">
                        {action_type}
                    </span>
                    <span style="background:#0F172A; border:1px solid #475569; color:#94A3B8; font-size:11px; padding:3px 8px; border-radius:6px;">
                        Step {current_step_idx + 1 if total_steps > 0 else 0} / {total_steps}
                    </span>
                </div>
            </div>
            
            <div style="background:#0F172A; border-left:4px solid #6366F1; border-radius:6px; padding:12px 14px; margin-bottom:14px;">
                <div style="font-size:12px; font-weight:600; color:#818CF8; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:2px;">Step Narrative & Commentary</div>
                <div style="font-size:14px; color:#E2E8F0; line-height:1.45;">{explanation}</div>
            </div>

            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px;">
                <div style="background:#0F172A; border-radius:8px; border:1px solid #334155; padding:10px 12px;">
                    <div style="font-size:11px; font-weight:600; color:#94A3B8; text-transform:uppercase;">Current Active Node</div>
                    <div style="font-size:18px; font-weight:700; color:#F59E0B; margin-top:2px;">{current_node_display}</div>
                </div>
                <div style="background:#0F172A; border-radius:8px; border:1px solid #334155; padding:10px 12px;">
                    <div style="font-size:11px; font-weight:600; color:#94A3B8; text-transform:uppercase;">Time / Space Bounds</div>
                    <div style="font-size:14px; font-weight:600; color:#38BDF8; margin-top:4px;">
                        Time: {time_c} | Space: {space_c}
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="background:#1E293B; border-radius:10px; border:1px solid #334155; padding:16px; margin-top:12px; box-shadow:0 4px 6px -1px rgba(0,0,0,0.2);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <span style="font-size:13px; font-weight:700; color:#E2E8F0; text-transform:uppercase; letter-spacing:0.05em;">
                    Live Data Structure: <span style="color:{ds_badge_color};">{ds_name}</span>
                </span>
                <span style="font-size:12px; color:#94A3B8;">Elements: <b>{len(ds_state)}</b></span>
            </div>
        """,
        unsafe_allow_html=True
    )

    if ds_state:
        badges_html = []
        for i, elem in enumerate(ds_state):
            if algorithm == "BFS":
                tag = "FRONT" if i == 0 else ("REAR" if i == len(ds_state) - 1 else f"#{i}")
                border_glow = "border:2px solid #818CF8; background:#312E81;" if i == 0 else "border:1px solid #4338CA; background:#1E1B4B;"
            else:
                tag = "TOP (Next Pop)" if i == len(ds_state) - 1 else ("BOTTOM" if i == 0 else f"#{i}")
                border_glow = "border:2px solid #F472B6; background:#831843;" if i == len(ds_state) - 1 else "border:1px solid #BE185D; background:#500724;"

            badge = f"""
            <div style="display:inline-flex; flex-direction:column; align-items:center; min-width:54px; padding:6px 10px; border-radius:8px; {border_glow} margin-right:8px; margin-bottom:6px;">
                <span style="font-size:10px; font-weight:700; color:#CBD5E1; letter-spacing:0.03em;">{tag}</span>
                <span style="font-size:16px; font-weight:700; color:#FFFFFF;">{elem}</span>
            </div>
            """
            badges_html.append(badge)

        flow_direction = "➔ Dequeue from Front (Left)" if algorithm == "BFS" else "➔ Pop from Top (Right)"
        st.markdown(
            f"""
            <div style="display:flex; flex-wrap:wrap; align-items:center; background:#0F172A; border-radius:8px; padding:12px; border:1px solid #334155;">
                {''.join(badges_html)}
            </div>
            <div style="font-size:11px; color:#64748B; margin-top:6px; font-style:italic;">{flow_direction}</div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="background:#0F172A; border-radius:8px; padding:12px; border:1px dashed #475569; text-align:center; color:#94A3B8; font-size:13px;">
                [ Empty - No nodes currently waiting in queue/stack ]
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    order_str = " -> ".join(traversal_order) if traversal_order else "(none yet)"
    visited_str = ", ".join(visited_list) if visited_list else "(none yet)"

    st.markdown(
        f"""
        <div style="background:#1E293B; border-radius:10px; border:1px solid #334155; padding:16px; margin-top:12px; box-shadow:0 4px 6px -1px rgba(0,0,0,0.2);">
            <div style="margin-bottom:8px;">
                <span style="font-size:12px; font-weight:700; color:#94A3B8; text-transform:uppercase;">Completed Traversal Sequence:</span>
                <div style="font-family:monospace; font-size:14px; font-weight:600; color:#10B981; background:#0F172A; border-radius:6px; padding:8px 10px; border:1px solid #334155; margin-top:4px; word-break:break-all;">
                    {order_str}
                </div>
            </div>
            <div>
                <span style="font-size:12px; font-weight:700; color:#94A3B8; text-transform:uppercase;">Visited Nodes Set ({len(visited_list)}):</span>
                <div style="font-family:monospace; font-size:13px; color:#CBD5E1; background:#0F172A; border-radius:6px; padding:8px 10px; border:1px solid #334155; margin-top:4px;">
                    {{{visited_str}}}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
