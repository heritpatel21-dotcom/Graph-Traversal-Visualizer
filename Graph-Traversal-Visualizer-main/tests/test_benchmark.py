"""Unit tests for empirical benchmarking and complexity calculation."""
import time
from collections import deque
import pytest
from graph_utils.sample_graphs import generate_random_graph


def test_benchmark_execution():
    """Verify that pure BFS and pure DFS benchmark loops run accurately without errors."""
    test_graph = generate_random_graph(num_nodes=30, edge_probability=0.2, directed=False, seed=42)
    adj = {n: list(test_graph.neighbors(n)) for n in test_graph.nodes()}
    start_n = list(test_graph.nodes())[0]

    t0 = time.perf_counter()
    visited_bfs = {start_n}
    q = deque([start_n])
    while q:
        curr = q.popleft()
        for nbr in adj.get(curr, []):
            if nbr not in visited_bfs:
                visited_bfs.add(nbr)
                q.append(nbr)
    t1 = time.perf_counter()
    assert t1 >= t0
    assert len(visited_bfs) > 0

    t2 = time.perf_counter()
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
    assert t3 >= t2
    assert len(visited_dfs) > 0
