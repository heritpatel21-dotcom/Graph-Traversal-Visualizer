"""Unit tests for sample graph presets and random graph generation."""
import pytest
import networkx as nx
from graph_utils.sample_graphs import (
    SAMPLE_GRAPHS,
    get_small_connected_graph,
    get_binary_tree_graph,
    get_branching_graph,
    get_disconnected_graph,
    get_directed_sample_graph,
    generate_random_graph
)
from graph_utils.graph_builder import get_graph_metrics


def test_preset_graphs_loadable():
    """Verify all predefined sample graphs load with valid nodes, edges, and coordinates."""
    for name, factory_fn in SAMPLE_GRAPHS.items():
        g = factory_fn()
        assert g.number_of_nodes() > 0, f"Preset '{name}' has no nodes."
        assert g.number_of_edges() >= 0, f"Preset '{name}' has invalid edge count."
        
        for node, data in g.nodes(data=True):
            assert "x" in data and "y" in data, f"Node '{node}' in '{name}' lacks 2D position."
            assert isinstance(data["x"], (int, float))
            assert isinstance(data["y"], (int, float))


def test_random_graph_generator():
    """Test Erdos-Renyi random graph generator parameters."""
    g_rnd = generate_random_graph(num_nodes=10, edge_probability=0.4, directed=False, weighted=True, seed=123)
    assert g_rnd.number_of_nodes() == 10
    assert g_rnd.graph["is_weighted"] is True
    assert g_rnd.is_directed() is False
    
    g_rnd2 = generate_random_graph(num_nodes=10, edge_probability=0.4, directed=False, weighted=True, seed=123)
    assert list(g_rnd.edges()) == list(g_rnd2.edges())


def test_graph_metrics_calculation():
    """Test graph metrics utility."""
    g = get_disconnected_graph()
    metrics = get_graph_metrics(g)
    assert metrics["num_nodes"] == 8
    assert metrics["num_components"] == 3
    assert metrics["is_connected"] is False
    assert metrics["has_isolated_nodes"] is True
    assert "H" in metrics["isolated_nodes"]
