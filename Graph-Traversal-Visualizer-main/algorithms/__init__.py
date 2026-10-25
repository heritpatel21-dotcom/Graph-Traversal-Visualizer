"""Algorithms package for BFS, DFS, and traversal execution."""
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, Any


@dataclass
class TraversalStep:
    """Represents a single atomic step during graph traversal."""
    step_number: int
    algorithm: str
    action: str
    current_node: Optional[str]
    active_edge: Optional[Tuple[str, str]]
    visited_nodes: List[str]
    data_structure_state: List[str]
    frontier_nodes: List[str]
    tree_edges: List[Tuple[str, str]]
    traversal_order: List[str]
    explanation: str
    depth_or_level: Dict[str, int] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
