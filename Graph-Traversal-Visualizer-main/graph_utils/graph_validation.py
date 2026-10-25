"""Validation helpers for graph editing and traversal."""
import html
import re
from typing import Tuple, Any, Optional
import networkx as nx

MAX_GRAPH_NODES = 50
MIN_EDGE_WEIGHT = -1000000.0
MAX_EDGE_WEIGHT = 1000000.0
MAX_NODE_LENGTH = 30


def sanitize_input(text: Optional[str]) -> str:
    if text is None:
        return ""
    cleaned = str(text).strip()
    cleaned = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", cleaned)
    return html.escape(cleaned, quote=True)


def validate_node_addition(graph: nx.Graph, node_id: str) -> Tuple[bool, str]:
    """Validate adding a new node to the graph."""
    if node_id is None:
        return False, "Node identifier cannot be None."
    
    node_str = sanitize_input(node_id)
    if not node_str:
        return False, "Node name cannot be empty or blank spaces."
    
    if len(node_str) > MAX_NODE_LENGTH:
        return False, f"Node name must be at most {MAX_NODE_LENGTH} characters long."

    if graph.number_of_nodes() >= MAX_GRAPH_NODES:
        return False, f"Maximum graph capacity reached ({MAX_GRAPH_NODES} nodes). Remove nodes to add new ones."
    
    if node_str in graph:
        return False, f"Node '{node_str}' already exists in the graph."
    
    return True, ""


def validate_node_deletion(graph: nx.Graph, node_id: str) -> Tuple[bool, str]:
    """Validate removing a node from the graph."""
    if node_id is None:
        return False, "Node identifier cannot be None."
    
    node_str = sanitize_input(node_id)
    if not node_str:
        return False, "Node name cannot be empty."
    
    if node_str not in graph:
        return False, f"Node '{node_str}' does not exist in the graph."
    
    return True, ""


def validate_edge_addition(
    graph: nx.Graph,
    source: str,
    target: str,
    weight: Optional[Any] = 1.0,
    allow_self_loops: bool = False
) -> Tuple[bool, str]:
    """Validate adding a new edge to the graph."""
    if source is None or target is None:
        return False, "Source and target nodes must be provided."
    
    src = sanitize_input(source)
    tgt = sanitize_input(target)
    
    if not src or not tgt:
        return False, "Source and target node names cannot be empty."
    
    if src not in graph:
        return False, f"Source node '{src}' does not exist in the graph."
    
    if tgt not in graph:
        return False, f"Target node '{tgt}' does not exist in the graph."
    
    if src == tgt and not allow_self_loops:
        return False, "Self-loops are not permitted in simple graph traversal mode."

    if weight is not None:
        try:
            val = float(weight)
            if val != val or abs(val) == float("inf"):
                return False, "Edge weight must be a valid finite number."
            if val < MIN_EDGE_WEIGHT or val > MAX_EDGE_WEIGHT:
                return False, f"Edge weight out of bounds ({MIN_EDGE_WEIGHT:g} to {MAX_EDGE_WEIGHT:g})."
        except (ValueError, TypeError):
            return False, "Edge weight must be a numerical value."

    if graph.has_edge(src, tgt):
        return False, f"Edge ({src} -> {tgt}) already exists."
            
    return True, ""


def validate_edge_deletion(graph: nx.Graph, source: str, target: str) -> Tuple[bool, str]:
    """Validate removing an edge from the graph."""
    src = sanitize_input(source)
    tgt = sanitize_input(target)
    
    if not src or not tgt:
        return False, "Source and target node names must be provided."
    
    if not graph.has_edge(src, tgt):
        return False, f"Edge between '{src}' and '{tgt}' does not exist in the graph."
    
    return True, ""


def validate_traversal_request(graph: nx.Graph, start_node: Optional[str]) -> Tuple[bool, str]:
    """Validate that the graph and start node are ready for traversal."""
    if graph is None or graph.number_of_nodes() == 0:
        return False, "Cannot execute traversal on an empty graph. Add nodes first."
    
    if start_node is None:
        return False, "Please select a valid starting node."
    
    start_str = sanitize_input(start_node)
    if not start_str:
        return False, "Starting node cannot be empty."
    
    if start_str not in graph:
        return False, f"Starting node '{start_str}' does not exist in the graph."
    
    return True, ""
