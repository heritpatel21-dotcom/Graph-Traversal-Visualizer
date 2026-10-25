"""Predefined sample graphs and random graph generator."""
import random
from typing import Dict, Tuple, List
import networkx as nx
from .graph_builder import create_empty_graph, ensure_node_positions


def get_small_connected_graph() -> nx.Graph:
    """
    6-node small connected graph (Diamond-bridge structure).
    Nodes: A, B, C, D, E, F
    Ideal for introductory BFS/DFS comparisons.
    """
    g = create_empty_graph(directed=False, weighted=False)
    positions = {
        "A": (-1.5, 0.0),
        "B": (-0.5, 1.0),
        "C": (-0.5, -1.0),
        "D": (0.5, 1.0),
        "E": (0.5, -1.0),
        "F": (1.5, 0.0),
    }
    for node, (x, y) in positions.items():
        g.add_node(node, x=x, y=y)

    edges = [
        ("A", "B", 2.0),
        ("A", "C", 4.0),
        ("B", "C", 1.0),
        ("B", "D", 7.0),
        ("C", "E", 3.0),
        ("D", "E", 2.0),
        ("D", "F", 5.0),
        ("E", "F", 1.0),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, weight=w)

    return g


def get_binary_tree_graph() -> nx.Graph:
    """
    7-node balanced binary tree structure.
    Nodes: 1 (Root), 2, 3 (Level 1), 4, 5, 6, 7 (Level 2).
    Perfect for contrasting BFS level-by-level exploration vs DFS depth exploration.
    """
    g = create_empty_graph(directed=False, weighted=False)
    positions = {
        "Node 1": (0.0, 1.5),
        "Node 2": (-1.2, 0.5),
        "Node 3": (1.2, 0.5),
        "Node 4": (-1.8, -0.8),
        "Node 5": (-0.6, -0.8),
        "Node 6": (0.6, -0.8),
        "Node 7": (1.8, -0.8),
    }
    for node, (x, y) in positions.items():
        g.add_node(node, x=x, y=y)

    edges = [
        ("Node 1", "Node 2", 1.0),
        ("Node 1", "Node 3", 1.0),
        ("Node 2", "Node 4", 1.0),
        ("Node 2", "Node 5", 1.0),
        ("Node 3", "Node 6", 1.0),
        ("Node 3", "Node 7", 1.0),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, weight=w)

    return g


def get_branching_graph() -> nx.Graph:
    """
    10-node complex branching network with cycles and cross branches.
    Nodes: A through J.
    """
    g = create_empty_graph(directed=False, weighted=False)
    positions = {
        "A": (-2.0, 0.0),
        "B": (-1.0, 1.2),
        "C": (-1.0, -1.2),
        "D": (0.0, 1.6),
        "E": (0.0, 0.0),
        "F": (0.0, -1.6),
        "G": (1.2, 1.2),
        "H": (1.2, -1.2),
        "I": (2.2, 0.6),
        "J": (2.2, -0.6),
    }
    for node, (x, y) in positions.items():
        g.add_node(node, x=x, y=y)

    edges = [
        ("A", "B", 3.0),
        ("A", "C", 2.0),
        ("B", "D", 4.0),
        ("B", "E", 1.0),
        ("C", "E", 5.0),
        ("C", "F", 6.0),
        ("D", "G", 2.0),
        ("E", "G", 3.0),
        ("E", "H", 4.0),
        ("F", "H", 1.0),
        ("G", "I", 2.0),
        ("H", "J", 5.0),
        ("I", "J", 3.0),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, weight=w)

    return g


def get_disconnected_graph() -> nx.Graph:
    """
    8-node disconnected graph with 3 components:
    Component 1: A, B, C, D (quadrilateral)
    Component 2: E, F, G (triangle)
    Component 3: H (isolated node)
    Tests disconnected handling and multi-component visualization.
    """
    g = create_empty_graph(directed=False, weighted=False)
    positions = {
        "A": (-2.0, 1.0),
        "B": (-1.0, 1.0),
        "C": (-1.0, 0.0),
        "D": (-2.0, 0.0),
        "E": (1.0, 1.0),
        "F": (2.2, 0.6),
        "G": (1.5, -0.4),
        "H": (0.0, -1.3),
    }
    for node, (x, y) in positions.items():
        g.add_node(node, x=x, y=y)

    edges = [
        ("A", "B", 1.0),
        ("B", "C", 2.0),
        ("C", "D", 1.5),
        ("D", "A", 2.5),
        ("E", "F", 3.0),
        ("F", "G", 2.0),
        ("G", "E", 4.0),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, weight=w)

    return g


def get_directed_sample_graph() -> nx.DiGraph:
    """
    6-node directed acyclic / cyclic graph.
    Demonstrates directional traversal edges and reachability constraints.
    """
    g = create_empty_graph(directed=True, weighted=False)
    positions = {
        "A": (-1.5, 0.0),
        "B": (-0.5, 1.0),
        "C": (-0.5, -1.0),
        "D": (0.5, 1.0),
        "E": (0.5, -1.0),
        "F": (1.5, 0.0),
    }
    for node, (x, y) in positions.items():
        g.add_node(node, x=x, y=y)

    edges = [
        ("A", "B", 2.0),
        ("A", "C", 1.0),
        ("B", "D", 4.0),
        ("C", "E", 3.0),
        ("D", "E", 2.0),
        ("D", "F", 5.0),
        ("E", "F", 1.0),
        ("E", "B", 2.0),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, weight=w)

    return g


def generate_random_graph(
    num_nodes: int = 7,
    edge_probability: float = 0.35,
    directed: bool = False,
    weighted: bool = False,
    seed: int = 42
) -> nx.Graph:
    """
    Generate an Erdos-Renyi random graph with configurable node count, density, and mode.
    Guarantees deterministic node labeling (A, B, C... or N1, N2...).
    """
    rng = random.Random(seed)
    g = create_empty_graph(directed=directed, weighted=weighted)

    node_names = []
    for i in range(num_nodes):
        if num_nodes <= 26:
            name = chr(ord("A") + i)
        else:
            name = f"N{i + 1}"
        node_names.append(name)
        g.add_node(name)

    for i in range(num_nodes):
        u = node_names[i]
        start_j = 0 if directed else i + 1
        for j in range(start_j, num_nodes):
            if i == j:
                continue
            v = node_names[j]
            if rng.random() < edge_probability:
                w = round(rng.uniform(1.0, 10.0), 1) if weighted else 1.0
                g.add_edge(u, v, weight=w)

    ensure_node_positions(g, seed=seed)
    return g


SAMPLE_GRAPHS = {
    "Small Connected (6 Nodes)": get_small_connected_graph,
    "Binary Tree (7 Nodes)": get_binary_tree_graph,
    "Branching Network (10 Nodes)": get_branching_graph,
    "Disconnected Components (8 Nodes)": get_disconnected_graph,
    "Directed Cycle Network (6 Nodes)": get_directed_sample_graph,
}
