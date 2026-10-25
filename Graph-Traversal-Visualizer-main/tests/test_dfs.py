"""Unit tests for Depth-First Search (DFS) implementation."""
import pytest
import networkx as nx
from algorithms.dfs import run_dfs
from graph_utils.sample_graphs import (
    get_small_connected_graph,
    get_disconnected_graph
)
from graph_utils.graph_builder import create_empty_graph


def test_dfs_connected_graph():
    """Test DFS traversal on a standard connected graph."""
    g = get_small_connected_graph()
    steps = run_dfs(g, start_node="A", traverse_all_components=False)

    assert len(steps) > 0
    init_step = steps[0]
    assert init_step.action == "INITIALIZE"
    assert init_step.current_node == "A"

    final_step = steps[-1]
    assert final_step.action == "COMPLETE"
    assert len(final_step.traversal_order) == 6
    assert final_step.traversal_order[0] == "A"
    
    assert final_step.traversal_order[1] == "B"


def test_dfs_single_node_graph():
    """Test DFS on a graph with only 1 node."""
    g = create_empty_graph()
    g.add_node("RootOnly")

    steps = run_dfs(g, start_node="RootOnly", traverse_all_components=False)
    final_step = steps[-1]
    assert final_step.action == "COMPLETE"
    assert final_step.traversal_order == ["RootOnly"]
    assert final_step.depth_or_level["RootOnly"] == 0


def test_dfs_disconnected_graph():
    """Test DFS on a disconnected graph with component settings."""
    g = get_disconnected_graph()

    steps_single = run_dfs(g, start_node="A", traverse_all_components=False)
    final_single = steps_single[-1]
    assert set(final_single.traversal_order) == {"A", "B", "C", "D"}
    assert "E" not in final_single.traversal_order

    steps_all = run_dfs(g, start_node="A", traverse_all_components=True)
    final_all = steps_all[-1]
    assert set(final_all.traversal_order) == {"A", "B", "C", "D", "E", "F", "G", "H"}
    assert len(final_all.traversal_order) == 8


def test_dfs_empty_graph():
    """Test DFS on empty graph."""
    g = create_empty_graph()
    steps = run_dfs(g, start_node="A")
    assert len(steps) == 1
    assert steps[0].action == "EMPTY_GRAPH"
    assert steps[0].current_node is None


def test_dfs_invalid_start_node():
    """Test DFS when starting node does not exist."""
    g = get_small_connected_graph()
    steps = run_dfs(g, start_node="MissingNode")
    assert len(steps) == 1
    assert steps[0].action == "INVALID_START"


def test_dfs_directed_graph_with_cycle():
    """Test DFS on directed graph with cycles."""
    g = nx.DiGraph()
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "A")
    g.add_edge("C", "D")

    steps = run_dfs(g, start_node="A", traverse_all_components=False)
    final_step = steps[-1]
    assert final_step.traversal_order == ["A", "B", "C", "D"]
    assert final_step.depth_or_level["A"] == 0
    assert final_step.depth_or_level["B"] == 1
    assert final_step.depth_or_level["C"] == 2
    assert final_step.depth_or_level["D"] == 3
