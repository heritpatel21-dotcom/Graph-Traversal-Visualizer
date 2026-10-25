"""Graph builder utility for managing NetworkX graph instances, layout positions, and properties."""
import math
import random
from typing import Dict, Tuple, Optional, Any, List
import networkx as nx


def create_empty_graph(directed: bool = False, weighted: bool = False) -> nx.Graph:
    """Create a new empty NetworkX graph with graph-level metadata."""
    g = nx.DiGraph() if directed else nx.Graph()
    g.graph["is_directed"] = directed
    g.graph["is_weighted"] = weighted
    return g


def ensure_node_positions(graph: nx.Graph, seed: int = 42) -> Dict[str, Tuple[float, float]]:
    """
    Ensure all nodes have 2D coordinates ('x', 'y') assigned as node attributes.
    If positions are missing or graph was modified, existing positions are preserved
    and new nodes are placed intelligently.
    """
    n = graph.number_of_nodes()
    if n == 0:
        return {}

    existing_pos = {}
    missing_nodes = []
    for node, data in graph.nodes(data=True):
        if "x" in data and "y" in data and data["x"] is not None and data["y"] is not None:
            existing_pos[node] = (float(data["x"]), float(data["y"]))
        else:
            missing_nodes.append(node)

    if not missing_nodes and len(existing_pos) == n:
        return existing_pos

    if not existing_pos:
        if n == 1:
            pos = {list(graph.nodes())[0]: (0.0, 0.0)}
        elif n <= 4:
            pos = nx.circular_layout(graph)
        else:
            try:
                pos = nx.spring_layout(graph, seed=seed, k=1.2 / math.sqrt(n) if n > 0 else 1.0, iterations=50)
            except Exception:
                pos = nx.circular_layout(graph)
    else:
        try:
            pos = nx.spring_layout(graph, pos=existing_pos, fixed=list(existing_pos.keys()), seed=seed, iterations=25)
        except Exception:
            pos = dict(existing_pos)
            angle_step = (2 * math.pi) / max(len(missing_nodes), 1)
            for i, node in enumerate(missing_nodes):
                pos[node] = (math.cos(i * angle_step), math.sin(i * angle_step))

    for node, (x, y) in pos.items():
        graph.nodes[node]["x"] = round(float(x), 4)
        graph.nodes[node]["y"] = round(float(y), 4)

    return pos


def add_node(graph: nx.Graph, node_id: str, x: Optional[float] = None, y: Optional[float] = None) -> bool:
    """Add a node to the graph and assign initial coordinates."""
    node_str = str(node_id).strip()
    if not node_str or node_str in graph:
        return False

    graph.add_node(node_str)
    if x is not None and y is not None:
        graph.nodes[node_str]["x"] = round(float(x), 4)
        graph.nodes[node_str]["y"] = round(float(y), 4)
    else:
        ensure_node_positions(graph)
    return True


def remove_node(graph: nx.Graph, node_id: str) -> bool:
    """Remove a node and all incident edges from the graph."""
    node_str = str(node_id).strip()
    if node_str not in graph:
        return False
    graph.remove_node(node_str)
    return True


def add_edge(graph: nx.Graph, source: str, target: str, weight: float = 1.0) -> bool:
    """Add an edge between source and target with specified weight."""
    src = str(source).strip()
    tgt = str(target).strip()
    if src not in graph or tgt not in graph:
        return False

    is_weighted = graph.graph.get("is_weighted", False)
    edge_weight = float(weight) if is_weighted else 1.0
    graph.add_edge(src, tgt, weight=edge_weight)
    return True


def remove_edge(graph: nx.Graph, source: str, target: str) -> bool:
    """Remove edge between source and target."""
    src = str(source).strip()
    tgt = str(target).strip()
    if not graph.has_edge(src, tgt):
        return False
    graph.remove_edge(src, tgt)
    return True


def convert_directed_mode(graph: nx.Graph, make_directed: bool) -> nx.Graph:
    """Convert graph between directed and undirected modes while preserving nodes, edges, weights, and positions."""
    if graph.is_directed() == make_directed:
        graph.graph["is_directed"] = make_directed
        return graph

    if make_directed:
        new_g = nx.DiGraph()
    else:
        new_g = nx.Graph()

    new_g.graph["is_directed"] = make_directed
    new_g.graph["is_weighted"] = graph.graph.get("is_weighted", False)

    for node, data in graph.nodes(data=True):
        new_g.add_node(node, **data)

    for u, v, data in graph.edges(data=True):
        new_g.add_edge(u, v, **data)

    return new_g


def convert_weighted_mode(graph: nx.Graph, make_weighted: bool) -> None:
    """Toggle weighted edge mode on the graph."""
    graph.graph["is_weighted"] = make_weighted
    for _, _, data in graph.edges(data=True):
        if not make_weighted:
            data["weight"] = 1.0
        elif "weight" not in data or data["weight"] is None:
            data["weight"] = 1.0


def recalculate_layout(graph: nx.Graph, layout_type: str = "spring") -> None:
    """Force recomputation of layout coordinates."""
    n = graph.number_of_nodes()
    if n == 0:
        return

    if layout_type == "circular" or n <= 3:
        pos = nx.circular_layout(graph)
    elif layout_type == "kamada_kawai" and n > 1 and nx.is_connected(graph.to_undirected()):
        try:
            pos = nx.kamada_kawai_layout(graph)
        except Exception:
            pos = nx.spring_layout(graph, seed=42, k=1.0)
    else:
        k_val = 1.2 / math.sqrt(n) if n > 0 else 1.0
        pos = nx.spring_layout(graph, seed=42, k=k_val, iterations=60)

    for node, (x, y) in pos.items():
        graph.nodes[node]["x"] = round(float(x), 4)
        graph.nodes[node]["y"] = round(float(y), 4)


def get_graph_metrics(graph: nx.Graph) -> Dict[str, Any]:
    """Calculate key graph statistics and metrics."""
    n = graph.number_of_nodes()
    m = graph.number_of_edges()
    is_dir = graph.is_directed()

    if n == 0:
        return {
            "num_nodes": 0,
            "num_edges": 0,
            "density": 0.0,
            "is_directed": is_dir,
            "is_weighted": graph.graph.get("is_weighted", False),
            "num_components": 0,
            "is_connected": False,
            "avg_degree": 0.0,
            "has_isolated_nodes": False,
        }

    undirected_view = graph.to_undirected() if is_dir else graph
    components = list(nx.connected_components(undirected_view))
    num_components = len(components)
    is_conn = num_components == 1

    max_edges = n * (n - 1) if is_dir else (n * (n - 1)) / 2
    density = (m / max_edges) if max_edges > 0 else 0.0

    degrees = [d for _, d in graph.degree()]
    avg_degree = sum(degrees) / n if n > 0 else 0.0
    isolated_nodes = [node for node, deg in graph.degree() if deg == 0]

    return {
        "num_nodes": n,
        "num_edges": m,
        "density": round(density, 4),
        "is_directed": is_dir,
        "is_weighted": graph.graph.get("is_weighted", False),
        "num_components": num_components,
        "is_connected": is_conn,
        "avg_degree": round(avg_degree, 2),
        "has_isolated_nodes": len(isolated_nodes) > 0,
        "isolated_nodes": isolated_nodes,
    }
