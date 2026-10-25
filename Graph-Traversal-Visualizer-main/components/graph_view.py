"""Plotly-based interactive graph visualization component."""
import math
from typing import Optional, Dict, Tuple, Any, List
import networkx as nx
import plotly.graph_objects as go
from algorithms import TraversalStep
from graph_utils.graph_builder import ensure_node_positions


COLOR_BACKGROUND = "#0F172A"
COLOR_CARD = "#1E293B"
COLOR_UNVISITED = "#334155"
COLOR_BORDER_UNVISITED = "#64748B"
COLOR_CURRENT = "#F59E0B"
COLOR_CURRENT_BORDER = "#FDE68A"
COLOR_FRONTIER = "#8B5CF6"
COLOR_FRONTIER_BORDER = "#C4B5FD"
COLOR_VISITED = "#10B981"
COLOR_VISITED_BORDER = "#6EE7B7"
COLOR_START_RING = "#38BDF8"

COLOR_EDGE_REGULAR = "#475569"
COLOR_EDGE_TREE = "#10B981"
COLOR_EDGE_ACTIVE = "#F59E0B"
COLOR_TEXT = "#F8FAFC"


def create_graph_figure(
    graph: nx.Graph,
    current_step: Optional[TraversalStep] = None,
    start_node: Optional[str] = None,
    height: int = 540
) -> go.Figure:
    """Generate a high-performance, interactive Plotly visualization for the graph."""
    fig = go.Figure()

    if graph is None or graph.number_of_nodes() == 0:
        fig.add_annotation(
            text="Graph is empty.<br>Use the Graph Editor or select a Sample Graph to start.",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#94A3B8")
        )
        fig.update_layout(
            paper_bgcolor=COLOR_BACKGROUND,
            plot_bgcolor=COLOR_BACKGROUND,
            height=height,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        return fig

    pos = ensure_node_positions(graph)
    is_directed = graph.is_directed()
    is_weighted = graph.graph.get("is_weighted", False)

    visited_nodes = set(current_step.visited_nodes) if current_step else set()
    frontier_nodes = set(current_step.frontier_nodes) if current_step else set()
    current_node = current_step.current_node if current_step else None
    active_edge = current_step.active_edge if current_step else None
    
    tree_edges_set = set()
    if current_step and current_step.tree_edges:
        for u, v in current_step.tree_edges:
            tree_edges_set.add((str(u), str(v)))
            if not is_directed:
                tree_edges_set.add((str(v), str(u)))

    regular_edge_x, regular_edge_y = [], []
    tree_edge_x, tree_edge_y = [], []
    active_edge_x, active_edge_y = [], []
    
    edge_annotations = []
    weight_annotations = []

    for u, v, data in graph.edges(data=True):
        u_str, v_str = str(u), str(v)
        if u_str not in pos or v_str not in pos:
            continue
        x0, y0 = pos[u_str]
        x1, y1 = pos[v_str]
        w = data.get("weight", 1.0)

        is_active = (
            active_edge is not None and (
                (active_edge[0] == u_str and active_edge[1] == v_str) or
                (not is_directed and active_edge[0] == v_str and active_edge[1] == u_str)
            )
        )
        is_tree = (u_str, v_str) in tree_edges_set or (not is_directed and (v_str, u_str) in tree_edges_set)

        if is_active:
            active_edge_x.extend([x0, x1, None])
            active_edge_y.extend([y0, y1, None])
        elif is_tree:
            tree_edge_x.extend([x0, x1, None])
            tree_edge_y.extend([y0, y1, None])
        else:
            regular_edge_x.extend([x0, x1, None])
            regular_edge_y.extend([y0, y1, None])

        if is_weighted:
            mx = (x0 + x1) / 2.0
            my = (y0 + y1) / 2.0
            dx = x1 - x0
            dy = y1 - y0
            dist = math.sqrt(dx * dx + dy * dy) or 1.0
            offset_dist = 0.04
            ox = mx - (dy / dist) * offset_dist
            oy = my + (dx / dist) * offset_dist
            
            weight_text = f"{w:g}" if isinstance(w, (int, float)) else str(w)
            weight_annotations.append(
                dict(
                    x=ox, y=oy,
                    xref="x", yref="y",
                    text=weight_text,
                    showarrow=False,
                    font=dict(size=11, color="#CBD5E1", family="monospace"),
                    bgcolor="rgba(15, 23, 42, 0.85)",
                    bordercolor="#475569",
                    borderwidth=1,
                    borderpad=2
                )
            )

        if is_directed:
            dx = x1 - x0
            dy = y1 - y0
            length = math.sqrt(dx * dx + dy * dy) or 1.0
            node_radius_offset = 0.08
            if length > node_radius_offset * 2:
                target_x = x1 - (dx / length) * node_radius_offset
                target_y = y1 - (dy / length) * node_radius_offset
                source_x = x0 + (dx / length) * node_radius_offset
            else:
                target_x, target_y = x1, y1
                source_x, source_y = x0, y0

            arrow_color = COLOR_EDGE_ACTIVE if is_active else (COLOR_EDGE_TREE if is_tree else COLOR_EDGE_REGULAR)
            edge_annotations.append(
                dict(
                    ax=source_x, ay=source_y,
                    x=target_x, y=target_y,
                    xref="x", yref="y",
                    axref="x", ayref="y",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1.2,
                    arrowwidth=2.5 if (is_tree or is_active) else 1.5,
                    arrowcolor=arrow_color,
                    opacity=0.9
                )
            )

    if regular_edge_x:
        fig.add_trace(
            go.Scatter(
                x=regular_edge_x, y=regular_edge_y,
                mode="lines",
                line=dict(color=COLOR_EDGE_REGULAR, width=1.8),
                hoverinfo="none",
                showlegend=False
            )
        )

    if tree_edge_x:
        fig.add_trace(
            go.Scatter(
                x=tree_edge_x, y=tree_edge_y,
                mode="lines",
                line=dict(color=COLOR_EDGE_TREE, width=3.5),
                hoverinfo="none",
                name="Traversal Tree Edge",
                showlegend=False
            )
        )

    if active_edge_x:
        fig.add_trace(
            go.Scatter(
                x=active_edge_x, y=active_edge_y,
                mode="lines",
                line=dict(color=COLOR_EDGE_ACTIVE, width=3.5, dash="dash"),
                hoverinfo="none",
                name="Inspecting Edge",
                showlegend=False
            )
        )

    node_x, node_y = [], []
    node_text = []
    node_colors = []
    node_border_colors = []
    node_sizes = []
    node_hover = []

    level_or_depth = current_step.depth_or_level if current_step else {}

    for node in graph.nodes():
        node_str = str(node)
        if node_str not in pos:
            continue
        x, y = pos[node_str]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node_str)

        degree = graph.degree(node)
        in_deg = graph.in_degree(node) if is_directed else degree
        out_deg = graph.out_degree(node) if is_directed else degree

        dist_val = level_or_depth.get(node_str, "N/A")
        metric_label = "Level (BFS)" if (current_step and current_step.algorithm == "BFS") else "Depth (DFS)"

        if node_str == current_node:
            state_label = "Current Active Node"
            c = COLOR_CURRENT
            bc = COLOR_CURRENT_BORDER
            size = 38
        elif node_str in frontier_nodes:
            state_label = "In Queue / Stack (Frontier)"
            c = COLOR_FRONTIER
            bc = COLOR_FRONTIER_BORDER
            size = 32
        elif node_str in visited_nodes:
            state_label = "Visited"
            c = COLOR_VISITED
            bc = COLOR_VISITED_BORDER
            size = 30
        else:
            state_label = "Unvisited"
            c = COLOR_UNVISITED
            bc = COLOR_BORDER_UNVISITED
            size = 28

        if node_str == start_node and node_str != current_node:
            bc = COLOR_START_RING

        node_colors.append(c)
        node_border_colors.append(bc)
        node_sizes.append(size)

        deg_info = f"In: {in_deg} | Out: {out_deg}" if is_directed else f"Degree: {degree}"
        hover_str = (
            f"<b>Node: {node_str}</b><br>"
            f"Status: {state_label}<br>"
            f"{metric_label}: {dist_val}<br>"
            f"{deg_info}"
        )
        node_hover.append(hover_str)

    fig.add_trace(
        go.Scatter(
            x=node_x, y=node_y,
            mode="markers+text",
            text=node_text,
            textposition="middle center",
            textfont=dict(color=COLOR_TEXT, size=13, family="sans-serif", weight="bold"),
            hoverinfo="text",
            hovertext=node_hover,
            hoverlabel=dict(
                bgcolor=COLOR_CARD,
                bordercolor="#6366F1",
                font=dict(color="#F8FAFC", size=13)
            ),
            marker=dict(
                color=node_colors,
                size=node_sizes,
                line=dict(color=node_border_colors, width=2.5),
                symbol="circle"
            ),
            showlegend=False
        )
    )

    legend_items = [
        ("Current Active Node", COLOR_CURRENT, COLOR_CURRENT_BORDER),
        ("In Queue / Stack", COLOR_FRONTIER, COLOR_FRONTIER_BORDER),
        ("Visited", COLOR_VISITED, COLOR_VISITED_BORDER),
        ("Unvisited", COLOR_UNVISITED, COLOR_BORDER_UNVISITED),
    ]
    for label, col, border_col in legend_items:
        fig.add_trace(
            go.Scatter(
                x=[None], y=[None],
                mode="markers",
                marker=dict(size=12, color=col, line=dict(color=border_col, width=1.5)),
                name=label,
                showlegend=True
            )
        )

    all_annotations = edge_annotations + weight_annotations

    if pos:
        xs = [coord[0] for coord in pos.values()]
        ys = [coord[1] for coord in pos.values()]
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        x_pad = max((x_max - x_min) * 0.18, 0.4)
        y_pad = max((y_max - y_min) * 0.18, 0.4)
        x_range = [x_min - x_pad, x_max + x_pad]
        y_range = [y_min - y_pad, y_max + y_pad]
    else:
        x_range = [-2, 2]
        y_range = [-2, 2]

    fig.update_layout(
        paper_bgcolor=COLOR_BACKGROUND,
        plot_bgcolor=COLOR_BACKGROUND,
        height=height,
        margin=dict(l=15, r=15, t=15, b=15),
        hovermode="closest",
        dragmode="pan",
        xaxis=dict(
            showgrid=False, zeroline=False, showticklabels=False,
            range=x_range, fixedrange=False
        ),
        yaxis=dict(
            showgrid=False, zeroline=False, showticklabels=False,
            range=y_range, fixedrange=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(color="#CBD5E1", size=11),
            bgcolor="rgba(15, 23, 42, 0.75)",
            bordercolor="#334155",
            borderwidth=1
        ),
        annotations=all_annotations
    )

    return fig
