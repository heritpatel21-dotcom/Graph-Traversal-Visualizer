"""Unit tests for authentication, XSS sanitization, and security boundaries."""
import pytest
import networkx as nx
from components.security import (
    verify_credentials,
    hash_password,
    sanitize_identifier,
    MAX_GRAPH_NODES,
    MAX_EDGE_WEIGHT,
    MIN_EDGE_WEIGHT
)
from graph_utils.graph_validation import (
    validate_node_addition,
    validate_edge_addition,
    sanitize_input
)
from graph_utils.graph_builder import create_empty_graph


def test_credential_verification():
    assert verify_credentials("admin", "GraphAdmin@2026") is True
    assert verify_credentials("student", "LearnDSA@2026") is True
    assert verify_credentials("admin", "WrongPassword") is False
    assert verify_credentials("fake_user", "AnyPassword") is False
    assert verify_credentials("", "") is False


def test_xss_sanitization():
    xss_payload = "<script>alert('xss')</script>"
    cleaned = sanitize_identifier(xss_payload)
    assert "<script>" not in cleaned
    assert "&lt;script&gt;" in cleaned

    img_payload = "<img src=x onerror=alert(1)>"
    cleaned_img = sanitize_input(img_payload)
    assert "<img" not in cleaned_img
    assert "&lt;img" in cleaned_img

    null_byte_payload = "Node\x00Name\x1b"
    cleaned_null = sanitize_identifier(null_byte_payload)
    assert "\x00" not in cleaned_null
    assert "\x1b" not in cleaned_null


def test_graph_capacity_dos_protection():
    g = create_empty_graph()
    for i in range(MAX_GRAPH_NODES):
        g.add_node(f"N{i}")

    valid, err = validate_node_addition(g, "OverflowNode")
    assert valid is False
    assert "capacity reached" in err.lower()


def test_weight_safety_bounds():
    g = create_empty_graph()
    g.add_node("A")
    g.add_node("B")

    valid_huge, err_huge = validate_edge_addition(g, "A", "B", weight=MAX_EDGE_WEIGHT + 1000)
    assert valid_huge is False
    assert "out of bounds" in err_huge.lower()

    valid_neg, err_neg = validate_edge_addition(g, "A", "B", weight=MIN_EDGE_WEIGHT - 1000)
    assert valid_neg is False
    assert "out of bounds" in err_neg.lower()

    valid_ok, _ = validate_edge_addition(g, "A", "B", weight=500.0)
    assert valid_ok is True
