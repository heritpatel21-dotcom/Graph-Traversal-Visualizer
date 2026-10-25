"""Breadth-First Search (BFS) implementation using collections.deque."""
from collections import deque
from typing import List, Optional, Set, Dict, Tuple
import networkx as nx
from . import TraversalStep


def run_bfs(
    graph: nx.Graph,
    start_node: str,
    traverse_all_components: bool = False
) -> List[TraversalStep]:
    """
    Execute Breadth-First Search step-by-step using collections.deque.
    
    Generates a deterministic sequence of TraversalStep snapshots detailing
    queue operations, neighbor discoveries, level calculations, and tree edge tracking.
    """
    steps: List[TraversalStep] = []
    
    if graph is None or graph.number_of_nodes() == 0:
        return [
            TraversalStep(
                step_number=0,
                algorithm="BFS",
                action="EMPTY_GRAPH",
                current_node=None,
                active_edge=None,
                visited_nodes=[],
                data_structure_state=[],
                frontier_nodes=[],
                tree_edges=[],
                traversal_order=[],
                explanation="The graph contains no nodes. Nothing to traverse."
            )
        ]

    start_str = str(start_node).strip()
    if start_str not in graph:
        return [
            TraversalStep(
                step_number=0,
                algorithm="BFS",
                action="INVALID_START",
                current_node=None,
                active_edge=None,
                visited_nodes=[],
                data_structure_state=[],
                frontier_nodes=[],
                tree_edges=[],
                traversal_order=[],
                explanation=f"Starting node '{start_str}' does not exist in the graph."
            )
        ]

    visited: Set[str] = set()
    visited_order: List[str] = []
    traversal_order: List[str] = []
    tree_edges: List[Tuple[str, str]] = []
    levels: Dict[str, int] = {}
    queue: deque = deque()
    
    step_counter = 0

    def get_sorted_neighbors(node: str) -> List[str]:
        """Return deterministic, sorted list of out-neighbors."""
        if graph.is_directed():
            neighbors = list(graph.successors(node))
        else:
            neighbors = list(graph.neighbors(node))
        return sorted(neighbors, key=lambda x: str(x))

    nodes_to_visit = [start_str]
    if traverse_all_components:
        all_other_nodes = sorted([n for n in graph.nodes() if n != start_str], key=lambda x: str(x))
        nodes_to_visit.extend(all_other_nodes)

    for component_root in nodes_to_visit:
        if component_root in visited:
            continue

        queue.append(component_root)
        visited.add(component_root)
        visited_order.append(component_root)
        levels[component_root] = 0

        is_subsequent_component = component_root != start_str
        component_msg = (
            f" [Component boundary: exploring disconnected component rooted at '{component_root}']"
            if is_subsequent_component else ""
        )

        steps.append(
            TraversalStep(
                step_number=step_counter,
                algorithm="BFS",
                action="INITIALIZE" if step_counter == 0 else "NEW_COMPONENT",
                current_node=component_root,
                active_edge=None,
                visited_nodes=list(visited_order),
                data_structure_state=list(queue),
                frontier_nodes=list(queue),
                tree_edges=list(tree_edges),
                traversal_order=list(traversal_order),
                explanation=(
                    f"Initialized BFS at starting node '{component_root}'. "
                    f"Marked as visited (Level 0) and added to the FIFO queue.{component_msg}"
                ),
                depth_or_level=dict(levels),
                metadata={"level": 0, "queue_size": len(queue)}
            )
        )
        step_counter += 1

        while len(queue) > 0:
            current = queue.popleft()
            traversal_order.append(current)
            curr_level = levels.get(current, 0)

            steps.append(
                TraversalStep(
                    step_number=step_counter,
                    algorithm="BFS",
                    action="DEQUEUE",
                    current_node=current,
                    active_edge=None,
                    visited_nodes=list(visited_order),
                    data_structure_state=list(queue),
                    frontier_nodes=list(queue),
                    tree_edges=list(tree_edges),
                    traversal_order=list(traversal_order),
                    explanation=(
                        f"Dequeued node '{current}' from the front of the FIFO queue. "
                        f"Current node is at Level {curr_level}. Now examining its adjacent neighbors."
                    ),
                    depth_or_level=dict(levels),
                    metadata={"level": curr_level, "queue_size": len(queue)}
                )
            )
            step_counter += 1

            neighbors = get_sorted_neighbors(current)
            if not neighbors:
                steps.append(
                    TraversalStep(
                        step_number=step_counter,
                        algorithm="BFS",
                        action="NO_NEIGHBORS",
                        current_node=current,
                        active_edge=None,
                        visited_nodes=list(visited_order),
                        data_structure_state=list(queue),
                        frontier_nodes=list(queue),
                        tree_edges=list(tree_edges),
                        traversal_order=list(traversal_order),
                        explanation=f"Node '{current}' has no outgoing unvisited neighbors to explore.",
                        depth_or_level=dict(levels),
                        metadata={"level": curr_level, "queue_size": len(queue)}
                    )
                )
                step_counter += 1
                continue

            for neighbor in neighbors:
                edge = (current, neighbor)
                if neighbor not in visited:
                    visited.add(neighbor)
                    visited_order.append(neighbor)
                    queue.append(neighbor)
                    tree_edges.append(edge)
                    levels[neighbor] = curr_level + 1

                    steps.append(
                        TraversalStep(
                            step_number=step_counter,
                            algorithm="BFS",
                            action="DISCOVER_NEIGHBOR",
                            current_node=current,
                            active_edge=edge,
                            visited_nodes=list(visited_order),
                            data_structure_state=list(queue),
                            frontier_nodes=list(queue),
                            tree_edges=list(tree_edges),
                            traversal_order=list(traversal_order),
                            explanation=(
                                f"Discovered unvisited neighbor '{neighbor}' via edge ({current} -> {neighbor}). "
                                f"Marked visited at Level {curr_level + 1} and enqueued to FIFO queue."
                            ),
                            depth_or_level=dict(levels),
                            metadata={"level": curr_level + 1, "queue_size": len(queue), "edge": edge}
                        )
                    )
                    step_counter += 1
                else:
                    steps.append(
                        TraversalStep(
                            step_number=step_counter,
                            algorithm="BFS",
                            action="ALREADY_VISITED",
                            current_node=current,
                            active_edge=edge,
                            visited_nodes=list(visited_order),
                            data_structure_state=list(queue),
                            frontier_nodes=list(queue),
                            tree_edges=list(tree_edges),
                            traversal_order=list(traversal_order),
                            explanation=(
                                f"Neighbor '{neighbor}' has already been visited or is in the queue. "
                                f"Cross/back edge ({current} -> {neighbor}) inspected; skipping."
                            ),
                            depth_or_level=dict(levels),
                            metadata={"level": curr_level, "queue_size": len(queue), "edge": edge}
                        )
                    )
                    step_counter += 1

        if not traverse_all_components:
            break

    steps.append(
        TraversalStep(
            step_number=step_counter,
            algorithm="BFS",
            action="COMPLETE",
            current_node=None,
            active_edge=None,
            visited_nodes=list(visited_order),
            data_structure_state=[],
            frontier_nodes=[],
            tree_edges=list(tree_edges),
            traversal_order=list(traversal_order),
            explanation=(
                f"BFS traversal complete! Visited {len(traversal_order)} node(s). "
                f"Final order: {' -> '.join(traversal_order)}."
            ),
            depth_or_level=dict(levels),
            metadata={"total_visited": len(traversal_order), "max_level": max(levels.values()) if levels else 0}
        )
    )

    return steps
