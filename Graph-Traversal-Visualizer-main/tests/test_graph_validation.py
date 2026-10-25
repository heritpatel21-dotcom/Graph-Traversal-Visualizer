"""Unit tests for graph validation and builder operations."""
import pytest
import networkx as nx
from graph_utils.graph_builder import (
    create_empty_graph,
    add_node,
    remove_node,
    add_edge,
    remove_edge,
    convert_directed_mode,
    convert_weighted_mode
)
from graph_utils.graph_validation import (
    validate_node_addition,
    validate_node_deletion,
    validate_edge_addition,
    validate_edge_deletion,
    validate_traversal_request
)


def test_node_addition_validation():
    """Test node addition rules."""
    g = create_empty_graph()
    
    valid, _ = validate_node_addition(g, "Alpha")
    assert valid is True
    add_node(g, "Alpha")
    
    valid, err = validate_node_addition(g, "Alpha")
    assert valid is False
    assert "already exists" in err.lower()

    valid, err = validate_node_addition(g, "   ")
    assert valid is False
    assert "empty" in err.lower()

    valid, err = validate_node_addition(g, None)
    assert valid is False


def test_node_deletion_validation():
    """Test node deletion rules."""
    g = create_empty_graph()
    add_node(g, "X")

    valid, _ = validate_node_deletion(g, "X")
    assert valid is True
    remove_node(g, "X")
    assert "X" not in g

    valid, err = validate_node_deletion(g, "X")
    assert valid is False
    assert "does not exist" in err.lower()


def test_edge_addition_validation():
    """Test edge addition rules."""
    g = create_empty_graph()
    add_node(g, "1")
    add_node(g, "2")

    valid, _ = validate_edge_addition(g, "1", "2", weight=3.5)
    assert valid is True
    add_edge(g, "1", "2", weight=3.5)
    assert g.has_edge("1", "2")

    valid, err = validate_edge_addition(g, "1", "2")
    assert valid is False
    assert "already exists" in err.lower()

    valid, err = validate_edge_addition(g, "1", "1", allow_self_loops=False)
    assert valid is False
    assert "self-loops" in err.lower()

    valid, err = validate_edge_addition(g, "1", "99")
    assert valid is False
    assert "does not exist" in err.lower()

    add_node(g, "3")
    valid, err = validate_edge_addition(g, "2", "3", weight="not_a_number")
    assert valid is False
    assert "numerical" in err.lower()


def test_edge_deletion_validation():
    """Test edge deletion rules."""
    g = create_empty_graph()
    add_node(g, "A")
    add_node(g, "B")
    add_edge(g, "A", "B")

    valid, _ = validate_edge_deletion(g, "A", "B")
    assert valid is True
    remove_edge(g, "A", "B")
    assert not g.has_edge("A", "B")

    valid, err = validate_edge_deletion(g, "A", "B")
    assert valid is False
    assert "does not exist" in err.lower()


def test_traversal_request_validation():
    """Test validation of traversal parameters."""
    g = create_empty_graph()

    valid, err = validate_traversal_request(g, "A")
    assert valid is False
    assert "empty graph" in err.lower()

    add_node(g, "A")
    valid, err = validate_traversal_request(g, "B")
    assert valid is False
    assert "does not exist" in err.lower()

    valid, _ = validate_traversal_request(g, "A")
    assert valid is True


def test_mode_conversions():
    """Test toggling directed and weighted modes."""
    g = create_empty_graph(directed=False, weighted=False)
    add_node(g, "A")
    add_node(g, "B")
    add_edge(g, "A", "B", weight=5.0)

    g_dir = convert_directed_mode(g, make_directed=True)
    assert g_dir.is_directed() is True
    assert g_dir.has_edge("A", "B")

    convert_weighted_mode(g_dir, make_weighted=True)
    assert g_dir.graph["is_weighted"] is True
