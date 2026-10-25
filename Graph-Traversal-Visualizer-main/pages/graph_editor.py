"""Graph Editor view: Interactive builder for adding/removing nodes, edges, weights, and generating graphs."""
from typing import Callable, Optional
import streamlit as st
import networkx as nx
from graph_utils.graph_builder import (
    add_node,
    remove_node,
    add_edge,
    remove_edge,
    convert_directed_mode,
    convert_weighted_mode,
    recalculate_layout,
    create_empty_graph,
    get_graph_metrics
)
from graph_utils.graph_validation import (
    validate_node_addition,
    validate_node_deletion,
    validate_edge_addition,
    validate_edge_deletion
)
from graph_utils.sample_graphs import SAMPLE_GRAPHS, generate_random_graph
from components.graph_view import create_graph_figure
from components.page_setup import init_page, sync_graph_update


def render_graph_editor(
    graph: nx.Graph,
    on_graph_updated: Callable[[nx.Graph], None]
) -> None:
    """Render the full Graph Editor interface."""
    st.markdown(
        """
        <div style="margin-bottom:18px;">
            <div style="font-size:24px; font-weight:800; color:#F8FAFC; letter-spacing:-0.02em;">
                Graph Editor & Topology Builder
            </div>
            <div style="font-size:14px; color:#94A3B8; margin-top:2px;">
                Create, customize, and validate custom graphs. Toggle directed/weighted modes, inspect live topology, or load sample graphs.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    metrics = get_graph_metrics(graph)
    nodes = sorted(list(graph.nodes()), key=lambda x: str(x))
    edges = list(graph.edges(data=True))
    is_directed = graph.is_directed()
    is_weighted = graph.graph.get("is_weighted", False)

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Nodes (V)", metrics["num_nodes"])
    m2.metric("Edges (E)", metrics["num_edges"])
    m3.metric("Density", f"{metrics['density']:.2f}")
    m4.metric("Components", metrics["num_components"])
    m5.metric("Avg Degree", f"{metrics['avg_degree']:.1f}")

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    col_controls, col_preview = st.columns([1.2, 1.3])

    with col_controls:
        with st.expander("⚙️ Graph Mode & Properties", expanded=True):
            col_d, col_w = st.columns(2)
            with col_d:
                dir_toggle = st.toggle("Directed Graph", value=is_directed, key="editor_dir_toggle")
                if dir_toggle != is_directed:
                    new_g = convert_directed_mode(graph, make_directed=dir_toggle)
                    on_graph_updated(new_g)
                    st.success(f"Converted graph to {'Directed' if dir_toggle else 'Undirected'} mode.")
                    st.rerun()

            with col_w:
                weight_toggle = st.toggle("Weighted Edges", value=is_weighted, key="editor_weight_toggle")
                if weight_toggle != is_weighted:
                    convert_weighted_mode(graph, make_weighted=weight_toggle)
                    on_graph_updated(graph)
                    st.success(f"{'Enabled' if weight_toggle else 'Disabled'} weighted edges.")
                    st.rerun()

            col_layout_btn, col_clear_btn = st.columns(2)
            with col_layout_btn:
                if st.button("🔀 Recalculate Layout", use_container_width=True):
                    recalculate_layout(graph, "spring")
                    on_graph_updated(graph)
                    st.success("Refreshed 2D node layout.")
                    st.rerun()

            with col_clear_btn:
                if st.button("🗑️ Clear All Nodes", use_container_width=True, type="secondary"):
                    empty_g = create_empty_graph(directed=is_directed, weighted=is_weighted)
                    on_graph_updated(empty_g)
                    st.warning("Cleared graph. All nodes and edges removed.")
                    st.rerun()

        with st.expander("📍 Node Operations", expanded=True):
            tab_add_n, tab_del_n = st.tabs(["Add Node", "Remove Node"])
            
            with tab_add_n:
                col_n_in, col_n_btn = st.columns([2.5, 1])
                with col_n_in:
                    default_next_node = chr(ord("A") + len(nodes)) if len(nodes) < 26 else f"N{len(nodes) + 1}"
                    new_node_input = st.text_input("Node Identifier", value=default_next_node, key="new_node_name").strip()
                with col_n_btn:
                    st.write("")
                    st.write("")
                    if st.button("Add Node", key="btn_add_node", use_container_width=True):
                        valid, err = validate_node_addition(graph, new_node_input)
                        if valid:
                            add_node(graph, new_node_input)
                            on_graph_updated(graph)
                            st.success(f"Added node '{new_node_input}'.")
                            st.rerun()
                        else:
                            st.error(err)

            with tab_del_n:
                if nodes:
                    col_del_in, col_del_btn = st.columns([2.5, 1])
                    with col_del_in:
                        node_to_del = st.selectbox("Select Node to Remove", nodes, key="select_del_node")
                    with col_del_btn:
                        st.write("")
                        st.write("")
                        if st.button("Remove", key="btn_del_node", use_container_width=True):
                            valid, err = validate_node_deletion(graph, node_to_del)
                            if valid:
                                remove_node(graph, node_to_del)
                                on_graph_updated(graph)
                                st.success(f"Removed node '{node_to_del}'.")
                                st.rerun()
                            else:
                                st.error(err)
                else:
                    st.info("No nodes in graph to remove.")

        with st.expander("🔗 Edge Operations", expanded=True):
            tab_add_e, tab_del_e = st.tabs(["Add Edge", "Remove Edge"])

            with tab_add_e:
                if len(nodes) >= 2:
                    col_src, col_tgt, col_wt = st.columns([1.2, 1.2, 1.0])
                    with col_src:
                        edge_src = st.selectbox("Source (u)", nodes, index=0, key="edge_src_sel")
                    with col_tgt:
                        tgt_default_idx = 1 if len(nodes) > 1 else 0
                        edge_tgt = st.selectbox("Target (v)", nodes, index=tgt_default_idx, key="edge_tgt_sel")
                    with col_wt:
                        edge_wt = st.number_input(
                            "Weight",
                            value=1.0,
                            step=0.5,
                            disabled=not is_weighted,
                            key="edge_wt_input"
                        )

                    if st.button("Add Edge", key="btn_add_edge", use_container_width=True):
                        valid, err = validate_edge_addition(graph, edge_src, edge_tgt, weight=edge_wt, allow_self_loops=False)
                        if valid:
                            add_edge(graph, edge_src, edge_tgt, weight=edge_wt)
                            on_graph_updated(graph)
                            st.success(f"Added edge ({edge_src} -> {edge_tgt}) with weight {edge_wt:g}.")
                            st.rerun()
                        else:
                            st.error(err)
                else:
                    st.info("Graph must have at least 2 nodes to add an edge.")

            with tab_del_e:
                if edges:
                    edge_options = [f"{u} -> {v}" for u, v, _ in edges]
                    selected_edge_str = st.selectbox("Select Edge to Remove", edge_options, key="del_edge_sel")
                    if st.button("Remove Edge", key="btn_del_edge", use_container_width=True):
                        parts = selected_edge_str.split(" -> ")
                        u_del, v_del = parts[0], parts[1]
                        valid, err = validate_edge_deletion(graph, u_del, v_del)
                        if valid:
                            remove_edge(graph, u_del, v_del)
                            on_graph_updated(graph)
                            st.success(f"Removed edge ({u_del} -> {v_del}).")
                            st.rerun()
                        else:
                            st.error(err)
                else:
                    st.info("Graph has no edges to remove.")

        with st.expander("📦 Preset Samples & Random Generator", expanded=True):
            tab_preset, tab_random = st.tabs(["Load Preset", "Random Graph Generator"])

            with tab_preset:
                preset_name = st.selectbox("Choose Preset Graph", list(SAMPLE_GRAPHS.keys()), key="preset_sel")
                if st.button("Load Preset Graph", key="btn_load_preset", use_container_width=True, type="primary"):
                    factory_fn = SAMPLE_GRAPHS[preset_name]
                    new_graph = factory_fn()
                    on_graph_updated(new_graph)
                    st.success(f"Loaded '{preset_name}'.")
                    st.rerun()

            with tab_random:
                col_rn_nodes, col_rn_prob = st.columns(2)
                with col_rn_nodes:
                    rn_nodes = st.slider("Node Count", min_value=3, max_value=20, value=8, key="rn_nodes_sl")
                with col_rn_prob:
                    rn_prob = st.slider("Edge Probability", min_value=0.1, max_value=0.8, value=0.35, step=0.05, key="rn_prob_sl")

                col_rn_dir, col_rn_wt = st.columns(2)
                with col_rn_dir:
                    rn_dir = st.checkbox("Directed", value=is_directed, key="rn_dir_check")
                with col_rn_wt:
                    rn_wt = st.checkbox("Weighted", value=is_weighted, key="rn_wt_check")

                if st.button("🎲 Generate Random Graph", key="btn_gen_random", use_container_width=True):
                    gen_g = generate_random_graph(
                        num_nodes=rn_nodes,
                        edge_probability=rn_prob,
                        directed=rn_dir,
                        weighted=rn_wt
                    )
                    on_graph_updated(gen_g)
                    st.success(f"Generated random graph with {rn_nodes} nodes.")
                    st.rerun()

    with col_preview:
        st.markdown(
            """
            <div style="font-size:13px; font-weight:700; color:#CBD5E1; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:6px;">
                Live Graph Preview
            </div>
            """,
            unsafe_allow_html=True
        )
        preview_fig = create_graph_figure(graph=graph, height=520)
        st.plotly_chart(preview_fig, use_container_width=True, config={"displayModeBar": True})

        st.markdown(
            """
            <div style="font-size:12px; font-weight:700; color:#94A3B8; text-transform:uppercase; letter-spacing:0.05em; margin-top:14px; margin-bottom:6px;">
                Adjacency List Representation
            </div>
            """,
            unsafe_allow_html=True
        )
        if nodes:
            adj_lines = []
            for node in nodes:
                if is_directed:
                    nbrs = [f"{v}{f' (w={d.get('weight', 1):g})' if is_weighted else ''}" for _, v, d in graph.out_edges(node, data=True)]
                else:
                    nbrs = [f"{v}{f' (w={d.get('weight', 1):g})' if is_weighted else ''}" for _, v, d in graph.edges(node, data=True)]
                adj_lines.append(f"<b>{node}</b>: [{', '.join(nbrs) if nbrs else 'None'}]")

            st.markdown(
                f"""
                <div style="background:#0F172A; border:1px solid #334155; border-radius:8px; padding:12px; font-family:monospace; font-size:12px; color:#E2E8F0; max-height:180px; overflow-y:auto; line-height:1.6;">
                    {'<br>'.join(adj_lines)}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("No nodes in the graph.")


if __name__ == "__main__":
    graph, _ = init_page("Graph Editor", "🛠️")
    render_graph_editor(graph, sync_graph_update)
