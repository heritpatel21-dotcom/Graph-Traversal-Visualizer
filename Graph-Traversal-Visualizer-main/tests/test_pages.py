"""Unit tests ensuring all page rendering functions execute without error."""
import pytest
from graph_utils.sample_graphs import get_small_connected_graph
from algorithms.traversal_engine import TraversalEngine
from pages.dashboard import render_dashboard
from pages.graph_editor import render_graph_editor
from pages.traversal_visualizer import render_traversal_visualizer
from pages.algorithm_explorer import render_algorithm_explorer
from pages.complexity_analysis import render_complexity_analysis
from pages.about import render_about


def test_pages_renderable():
    """Verify that all page rendering functions can be invoked without unhandled exceptions."""
    g = get_small_connected_graph()
    engine = TraversalEngine()
    engine.initialize_traversal(g, "BFS", "A")

    render_algorithm_explorer()
    render_about()

    render_dashboard(g, engine)
    render_traversal_visualizer(g, engine)

    render_complexity_analysis(g)

    def mock_update(new_g):
        pass
    render_graph_editor(g, mock_update)
