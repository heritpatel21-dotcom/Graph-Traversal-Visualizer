"""Unit tests for the TraversalEngine state machine."""
import pytest
from algorithms.traversal_engine import TraversalEngine
from graph_utils.sample_graphs import get_small_connected_graph
from graph_utils.graph_builder import create_empty_graph


def test_engine_initialization():
    """Test engine initialization on graph."""
    g = get_small_connected_graph()
    engine = TraversalEngine()
    success = engine.initialize_traversal(g, algorithm="BFS", start_node="A")

    assert success is True
    assert engine.algorithm == "BFS"
    assert engine.start_node == "A"
    assert engine.current_step_index == 0
    assert engine.get_total_steps() > 0
    assert engine.is_finished() is False


def test_engine_step_forward_and_backward():
    """Test step forward and backward transitions."""
    g = get_small_connected_graph()
    engine = TraversalEngine()
    engine.initialize_traversal(g, algorithm="DFS", start_node="A")

    initial_step = engine.get_current_step()
    assert initial_step.step_number == 0

    advanced = engine.step_forward()
    assert advanced is True
    assert engine.current_step_index == 1
    assert engine.get_current_step().step_number == 1

    backed = engine.step_backward()
    assert backed is True
    assert engine.current_step_index == 0

    backed_again = engine.step_backward()
    assert backed_again is False
    assert engine.current_step_index == 0


def test_engine_jump_and_reset():
    """Test jumping to step index and reset."""
    g = get_small_connected_graph()
    engine = TraversalEngine()
    engine.initialize_traversal(g, algorithm="BFS", start_node="A")
    total = engine.get_total_steps()

    mid = total // 2
    engine.jump_to_step(mid)
    assert engine.current_step_index == mid

    engine.jump_to_step(9999)
    assert engine.current_step_index == total - 1
    assert engine.is_finished() is True

    engine.reset_traversal()
    assert engine.current_step_index == 0
    assert engine.is_playing is False


def test_engine_progress_ratio():
    """Test progress calculation ratio."""
    g = get_small_connected_graph()
    engine = TraversalEngine()
    engine.initialize_traversal(g, algorithm="BFS", start_node="A")

    assert engine.get_progress_ratio() == 0.0
    engine.jump_to_step(engine.get_total_steps() - 1)
    assert engine.get_progress_ratio() == 1.0


def test_engine_empty_graph():
    """Test engine handling when graph is empty."""
    g = create_empty_graph()
    engine = TraversalEngine()
    success = engine.initialize_traversal(g, algorithm="BFS")

    assert success is False
    assert engine.get_total_steps() == 0
    assert engine.get_current_step() is None
    assert engine.is_finished() is True
