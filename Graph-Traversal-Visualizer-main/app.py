"""Graph Traversal Visualizer - Main Application Entrypoint.

A production-quality educational suite built with Streamlit, NetworkX, and Plotly.
"""
import streamlit as st
from components.page_setup import init_page
from pages.dashboard import render_dashboard


def main() -> None:
    """Main application entrypoint rendering the primary Dashboard."""
    graph, engine = init_page(page_title="Dashboard", page_icon="🕸️")
    render_dashboard(graph=graph, engine=engine)


if __name__ == "__main__":
    main()
