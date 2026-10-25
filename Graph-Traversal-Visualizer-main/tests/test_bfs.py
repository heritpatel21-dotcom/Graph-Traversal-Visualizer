"""Unit tests for Breadth-First Search (BFS) implementation."""
import pytest
import networkx as nx
from algorithms.bfs import run_bfs
from graph_utils.sample_graphs import (
    get_small_connected_graph,
    get_disconnected_graph,
    get_directed_sample_graph
)
from graph_utils.graph_builder import create_empty_graph


def test_bfs_connected_graph():
    """Test BFS traversal on a standard 6-node connected graph."""
    g = get_small_connected_graph()
    steps = run_bfs(g, start_node="A", traverse_all_components=False)

    assert len(steps) > 0
    init_step = steps[0]
    assert init_step.action == "INITIALIZE"
    assert init_step.current_node == "A"
    assert "A" in init_step.visited_nodes

    final_step = steps[-1]
    assert final_step.action == "COMPLETE"
    assert len(final_step.traversal_order) == 6
    assert final_step.traversal_order[0] == "A"
    assert final_step.traversal_order[1:3] == ["B", "C"]
    
    assert final_step.depth_or_level["A"] == 0
    assert final_step.depth_or_level["B"] == 1
    assert final_step.depth_or_level["C"] == 1


def test_bfs_single_node_graph():
    """Test BFS on a graph containing only a single isolated node."""
    g = create_empty_graph()
    g.add_node("Single")

    steps = run_bfs(g, start_node="Single", traverse_all_components=False)
    assert len(steps) >= 2
    final_step = steps[-1]
    assert final_step.action == "COMPLETE"
    assert final_step.traversal_order == ["Single"]
    assert final_step.depth_or_level["Single"] == 0


def test_bfs_disconnected_graph():
    """Test BFS on a disconnected graph with both component traversal modes."""
    g = get_disconnected_graph()

    steps_single = run_bfs(g, start_node="A", traverse_all_components=False)
    final_single = steps_single[-1]
    assert set(final_single.traversal_order) == {"A", "B", "C", "D"}
    assert "E" not in final_single.traversal_order
    assert "H" not in final_single.traversal_order

    steps_all = run_bfs(g, start_node="A", traverse_all_components=True)
    final_all = steps_all[-1]
    assert set(final_all.traversal_order) == {"A", "B", "C", "D", "E", "F", "G", "H"}
    assert len(final_all.traversal_order) == 8


def test_bfs_empty_graph():
    """Test BFS on an empty graph gracefully handled without raising exceptions."""
    g = create_empty_graph()
    steps = run_bfs(g, start_node="A")
    assert len(steps) == 1
    assert steps[0].action == "EMPTY_GRAPH"
    assert steps[0].current_node is None


def test_bfs_invalid_start_node():
    """Test BFS with a starting node that is not present in the graph."""
    g = get_small_connected_graph()
    steps = run_bfs(g, start_node="NonExistentNode")
    assert len(steps) == 1
    assert steps[0].action == "INVALID_START"


def test_bfs_directed_graph():
    """Test BFS on a directed graph respects directionality."""
    g = nx.DiGraph()
    g.add_edge("1", "2")
    g.add_edge("2", "3")
    g.add_edge("1", "4")
    g.add_edge("3", "1")

    steps = run_bfs(g, start_node="1", traverse_all_components=False)
    final_step = steps[-1]
    assert final_step.traversal_order == ["1", "2", "4", "3"]
    assert final_step.depth_or_level["1"] == 0
    assert final_step.depth_or_level["2"] == 1
    assert final_step.depth_or_level["4"] == 1
    assert final_step.depth_or_level["3"] == 2
