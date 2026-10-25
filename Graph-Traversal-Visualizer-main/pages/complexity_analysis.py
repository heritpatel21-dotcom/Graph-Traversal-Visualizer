"""Complexity Analysis view: Empirical Python performance benchmarks, Big-O limits, and comparisons."""
import time
from collections import deque
from typing import List, Dict, Any
import streamlit as st
import networkx as nx
import plotly.graph_objects as go
from algorithms.bfs import run_bfs
from algorithms.dfs import run_dfs
from graph_utils.sample_graphs import generate_random_graph
from graph_utils.graph_builder import get_graph_metrics
from components.page_setup import init_page


def render_complexity_analysis(graph: nx.Graph) -> None:
    """Render the Complexity Analysis and Empirical Benchmarking dashboard."""
    st.markdown(
        """
        <div style="margin-bottom:18px;">
            <div style="font-size:24px; font-weight:800; color:#F8FAFC; letter-spacing:-0.02em;">
                Complexity Analysis & Empirical Benchmarks
            </div>
            <div style="font-size:14px; color:#94A3B8; margin-top:2px;">
                Theoretical asymptotic boundaries, real-time memory profile, and actual measured CPU execution timings.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    metrics = get_graph_metrics(graph)

    col_bfs_card, col_dfs_card = st.columns(2)

    with col_bfs_card:
        st.markdown(
            """
            <div style="background:#1E293B; border-radius:10px; border:1px solid #334155; padding:18px; box-shadow:0 4px 6px -1px rgba(0,0,0,0.2);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span style="font-size:16px; font-weight:700; color:#818CF8;">BFS Asymptotic Bounds</span>
                    <span style="background:#312E81; color:#A5B4FC; font-size:11px; font-weight:700; padding:2px 8px; border-radius:4px;">FIFO Queue</span>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:10px;">
                    <div style="background:#0F172A; border-radius:6px; padding:10px; border:1px solid #334155;">
                        <div style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Time Complexity</div>
                        <div style="font-size:20px; font-weight:700; color:#10B981;">O(V + E)</div>
                    </div>
                    <div style="background:#0F172A; border-radius:6px; padding:10px; border:1px solid #334155;">
                        <div style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Auxiliary Space</div>
                        <div style="font-size:20px; font-weight:700; color:#38BDF8;">O(V)</div>
                    </div>
                </div>
                <div style="font-size:12px; color:#94A3B8; margin-top:10px; line-height:1.45;">
                    <b>Queue Space:</b> Proportional to maximum level width (frontier). In a balanced tree of branching factor <i>b</i>, space reaches O(b<sup>d</sup>).
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_dfs_card:
        st.markdown(
            """
            <div style="background:#1E293B; border-radius:10px; border:1px solid #334155; padding:18px; box-shadow:0 4px 6px -1px rgba(0,0,0,0.2);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span style="font-size:16px; font-weight:700; color:#EC4899;">DFS Asymptotic Bounds</span>
                    <span style="background:#831843; color:#FBCFE8; font-size:11px; font-weight:700; padding:2px 8px; border-radius:4px;">LIFO Stack</span>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:10px;">
                    <div style="background:#0F172A; border-radius:6px; padding:10px; border:1px solid #334155;">
                        <div style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Time Complexity</div>
                        <div style="font-size:20px; font-weight:700; color:#10B981;">O(V + E)</div>
                    </div>
                    <div style="background:#0F172A; border-radius:6px; padding:10px; border:1px solid #334155;">
                        <div style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Auxiliary Space</div>
                        <div style="font-size:20px; font-weight:700; color:#38BDF8;">O(V)</div>
                    </div>
                </div>
                <div style="font-size:12px; color:#94A3B8; margin-top:10px; line-height:1.45;">
                    <b>Stack Space:</b> Proportional to maximum branch depth. In a balanced tree, space is O(log V); in a degenerated line graph, space is O(V).
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    st.markdown("### Active Graph Operational Profile")

    nodes = list(graph.nodes())
    if nodes:
        start_node = nodes[0]
        bfs_steps = run_bfs(graph, start_node, traverse_all_components=True)
        dfs_steps = run_dfs(graph, start_node, traverse_all_components=True)

        max_bfs_queue = max([len(s.data_structure_state) for s in bfs_steps]) if bfs_steps else 0
        max_dfs_stack = max([len(s.data_structure_state) for s in dfs_steps]) if dfs_steps else 0

        p1, p2, p3, p4 = st.columns(4)
        p1.metric("Graph Vertices (V)", metrics["num_nodes"])
        p2.metric("Graph Edges (E)", metrics["num_edges"])
        p3.metric("Peak BFS Queue Size", f"{max_bfs_queue} nodes")
        p4.metric("Peak DFS Stack Size", f"{max_dfs_stack} nodes")

        st.markdown(
            f"""
            <div style="background:#1E293B; border:1px solid #334155; border-radius:8px; padding:14px; margin-top:10px;">
                <div style="font-size:13px; font-weight:700; color:#E2E8F0; margin-bottom:4px;">Comparative Observations for Current Topology:</div>
                <div style="font-size:13px; color:#CBD5E1; line-height:1.5;">
                    • <b>BFS Steps:</b> {len(bfs_steps)} total state snapshots recorded.<br>
                    • <b>DFS Steps:</b> {len(dfs_steps)} total state snapshots recorded.<br>
                    • <b>Memory Footprint:</b> Peak frontier queue size was <b>{max_bfs_queue}</b> nodes vs peak stack depth of <b>{max_dfs_stack}</b> nodes.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info("Current graph is empty. Add nodes to view active operational profile.")

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("### Live Empirical Execution Benchmark (Real CPU Measurement)")
    st.markdown(
        """
        Measure actual algorithmic execution times across synthetic graphs of scaling sizes.
        These measurements run standard `bfs` and `dfs` (without UI snapshot overhead) directly in Python using `time.perf_counter()`.
        """
    )

    col_bench_cfg, col_bench_btn = st.columns([3, 1])
    with col_bench_cfg:
        graph_sizes_to_test = st.multiselect(
            "Select Graph Vertex Sizes to Benchmark (V)",
            options=[20, 50, 100, 200, 400, 800],
            default=[20, 50, 100, 200, 400]
        )
    with col_bench_btn:
        st.write("")
        st.write("")
        run_bench = st.button("🚀 Run Live Benchmark", key="btn_run_bench", type="primary", use_container_width=True)

    if run_bench and graph_sizes_to_test:
        with st.spinner("Executing empirical Python benchmark..."):
            sizes_sorted = sorted(graph_sizes_to_test)
            bfs_times_ms = []
            dfs_times_ms = []
            edge_counts = []

            for v_size in sizes_sorted:
                test_graph = generate_random_graph(num_nodes=v_size, edge_probability=0.15, directed=False, seed=42)
                adj = {n: list(test_graph.neighbors(n)) for n in test_graph.nodes()}
                start_n = list(test_graph.nodes())[0]
                edge_counts.append(test_graph.number_of_edges())

                trials = 5
                t0 = time.perf_counter()
                for _ in range(trials):
                    visited = {start_n}
                    q = deque([start_n])
                    while q:
                        curr = q.popleft()
                        for nbr in adj.get(curr, []):
                            if nbr not in visited:
                                visited.add(nbr)
                                q.append(nbr)
                t1 = time.perf_counter()
                bfs_avg_ms = ((t1 - t0) / trials) * 1000.0
                bfs_times_ms.append(round(bfs_avg_ms, 4))

                t2 = time.perf_counter()
                for _ in range(trials):
                    visited_dfs = set()
                    stk = [start_n]
                    while stk:
                        curr = stk.pop()
                        if curr not in visited_dfs:
                            visited_dfs.add(curr)
                            for nbr in adj.get(curr, []):
                                if nbr not in visited_dfs:
                                    stk.append(nbr)
                t3 = time.perf_counter()
                dfs_avg_ms = ((t3 - t2) / trials) * 1000.0
                dfs_times_ms.append(round(dfs_avg_ms, 4))

            fig_bench = go.Figure()
            fig_bench.add_trace(
                go.Scatter(
                    x=sizes_sorted,
                    y=bfs_times_ms,
                    mode="lines+markers",
                    name="BFS (collections.deque)",
                    line=dict(color="#6366F1", width=3),
                    marker=dict(size=8, symbol="circle")
                )
            )
            fig_bench.add_trace(
                go.Scatter(
                    x=sizes_sorted,
                    y=dfs_times_ms,
                    mode="lines+markers",
                    name="DFS (explicit list stack)",
                    line=dict(color="#EC4899", width=3),
                    marker=dict(size=8, symbol="diamond")
                )
            )

            fig_bench.update_layout(
                paper_bgcolor="#0F172A",
                plot_bgcolor="#0F172A",
                font=dict(color="#CBD5E1"),
                title=dict(
                    text="Empirical Traversal Time vs. Number of Vertices (V)",
                    font=dict(size=15, color="#F8FAFC")
                ),
                xaxis=dict(
                    title="Vertices (V)",
                    gridcolor="#334155",
                    zerolinecolor="#334155"
                ),
                yaxis=dict(
                    title="Execution Time (milliseconds)",
                    gridcolor="#334155",
                    zerolinecolor="#334155"
                ),
                legend=dict(
                    bgcolor="rgba(15, 23, 42, 0.8)",
                    bordercolor="#334155",
                    borderwidth=1
                ),
                margin=dict(l=40, r=40, t=50, b=40)
            )
            st.plotly_chart(fig_bench, use_container_width=True)

            bench_table = []
            for i, sz in enumerate(sizes_sorted):
                bench_table.append({
                    "Vertices (V)": sz,
                    "Edges (E)": edge_counts[i],
                    "BFS Time (ms)": f"{bfs_times_ms[i]:.4f}",
                    "DFS Time (ms)": f"{dfs_times_ms[i]:.4f}",
                    "Faster Algorithm": "BFS" if bfs_times_ms[i] < dfs_times_ms[i] else "DFS"
                })
            st.dataframe(bench_table, use_container_width=True, hide_index=True)
            st.caption("Measurements conducted dynamically on your host CPU. Averaged over 5 runs per sample size.")

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("### Decision Guide: Choosing Between BFS and DFS")
    st.markdown(
        r"""
| Scenario / Requirement | Recommended Algorithm | Reason & Trade-off |
| :--- | :---: | :--- |
| **Shortest path on unweighted graph** | **BFS** | BFS explores by radius; guarantees minimum edge hops. |
| **Target node is expected to be near the root** | **BFS** | Explores level 1, then level 2; finds shallow targets faster. |
| **Target node is expected to be deep in the graph** | **DFS** | Directly dives into deep branches without exploring all wide peers. |
| **Graph has very large branching factor (wide graph)** | **DFS** | BFS queue can explode in size $\mathcal{O}(b^d)$; DFS stack only holds current path. |
| **Graph is extremely deep or infinite** | **BFS** | DFS can get stuck exploring an endless branch or cause stack overflow. |
| **Topological Sort / DAG Dependency Resolution** | **DFS** | Post-order DFS traversal directly yields reverse topological order. |
| **Cycle detection in directed graph** | **DFS** | Back-edges detected during DFS branch exploration immediately prove cycles. |
        """
    )


if __name__ == "__main__":
    graph, _ = init_page("Complexity Analysis", "📈")
    render_complexity_analysis(graph)
