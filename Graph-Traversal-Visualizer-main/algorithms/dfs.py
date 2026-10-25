"""Depth-First Search (DFS) implementation using an explicit Python list as a LIFO stack."""
from typing import List, Optional, Set, Dict, Tuple
import networkx as nx
from . import TraversalStep


def run_dfs(
    graph: nx.Graph,
    start_node: str,
    traverse_all_components: bool = False
) -> List[TraversalStep]:
    """
    Execute Depth-First Search step-by-step using an explicit LIFO stack (Python list).
    
    Generates a deterministic sequence of TraversalStep snapshots recording stack
    pushes/pops, branch exploration, backtracking, depths, and tree edge tracking.
    """
    steps: List[TraversalStep] = []

    if graph is None or graph.number_of_nodes() == 0:
        return [
            TraversalStep(
                step_number=0,
                algorithm="DFS",
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
                algorithm="DFS",
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
    depths: Dict[str, int] = {}
    
    stack: List[Tuple[str, Optional[str], int]] = []
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

        stack.append((component_root, None, 0))
        stack_nodes_view = [item[0] for item in stack]

        is_subsequent = component_root != start_str
        comp_msg = (
            f" [Component boundary: exploring disconnected component rooted at '{component_root}']"
            if is_subsequent else ""
        )

        steps.append(
            TraversalStep(
                step_number=step_counter,
                algorithm="DFS",
                action="INITIALIZE" if step_counter == 0 else "NEW_COMPONENT",
                current_node=component_root,
                active_edge=None,
                visited_nodes=list(visited_order),
                data_structure_state=list(stack_nodes_view),
                frontier_nodes=list(stack_nodes_view),
                tree_edges=list(tree_edges),
                traversal_order=list(traversal_order),
                explanation=(
                    f"Initialized DFS at starting node '{component_root}'. "
                    f"Pushed to explicit LIFO stack (Depth 0).{comp_msg}"
                ),
                depth_or_level=dict(depths),
                metadata={"depth": 0, "stack_size": len(stack)}
            )
        )
        step_counter += 1

        while len(stack) > 0:
            current, parent, depth = stack.pop()
            stack_nodes_view = [item[0] for item in stack]

            if current in visited:
                steps.append(
                    TraversalStep(
                        step_number=step_counter,
                        algorithm="DFS",
                        action="ALREADY_VISITED",
                        current_node=current,
                        active_edge=(parent, current) if parent else None,
                        visited_nodes=list(visited_order),
                        data_structure_state=list(stack_nodes_view),
                        frontier_nodes=list(stack_nodes_view),
                        tree_edges=list(tree_edges),
                        traversal_order=list(traversal_order),
                        explanation=(
                            f"Popped node '{current}' from the LIFO stack, but it was already visited "
                            f"via an earlier path. Backtracking."
                        ),
                        depth_or_level=dict(depths),
                        metadata={"depth": depth, "stack_size": len(stack)}
                    )
                )
                step_counter += 1
                continue

            visited.add(current)
            visited_order.append(current)
            traversal_order.append(current)
            depths[current] = depth

            if parent is not None:
                tree_edges.append((parent, current))

            steps.append(
                TraversalStep(
                    step_number=step_counter,
                    algorithm="DFS",
                    action="POP_AND_VISIT",
                    current_node=current,
                    active_edge=(parent, current) if parent else None,
                    visited_nodes=list(visited_order),
                    data_structure_state=list(stack_nodes_view),
                    frontier_nodes=list(stack_nodes_view),
                    tree_edges=list(tree_edges),
                    traversal_order=list(traversal_order),
                    explanation=(
                        f"Popped '{current}' from stack top and marked as VISITED at Depth {depth}."
                        + (f" Formed tree edge ({parent} -> {current})." if parent else "")
                    ),
                    depth_or_level=dict(depths),
                    metadata={"depth": depth, "stack_size": len(stack)}
                )
            )
            step_counter += 1

            neighbors = get_sorted_neighbors(current)
            unvisited_neighbors = [nbr for nbr in neighbors if nbr not in visited]

            if not unvisited_neighbors:
                steps.append(
                    TraversalStep(
                        step_number=step_counter,
                        algorithm="DFS",
                        action="BACKTRACK",
                        current_node=current,
                        active_edge=None,
                        visited_nodes=list(visited_order),
                        data_structure_state=list(stack_nodes_view),
                        frontier_nodes=list(stack_nodes_view),
                        tree_edges=list(tree_edges),
                        traversal_order=list(traversal_order),
                        explanation=(
                            f"Node '{current}' has no unvisited neighbors. "
                            f"Reached end of branch; backtracking up the call stack."
                        ),
                        depth_or_level=dict(depths),
                        metadata={"depth": depth, "stack_size": len(stack)}
                    )
                )
                step_counter += 1
                continue

            for nbr in reversed(unvisited_neighbors):
                stack.append((nbr, current, depth + 1))

            stack_nodes_view = [item[0] for item in stack]
            steps.append(
                TraversalStep(
                    step_number=step_counter,
                    algorithm="DFS",
                    action="PUSH_NEIGHBORS",
                    current_node=current,
                    active_edge=None,
                    visited_nodes=list(visited_order),
                    data_structure_state=list(stack_nodes_view),
                    frontier_nodes=list(stack_nodes_view),
                    tree_edges=list(tree_edges),
                    traversal_order=list(traversal_order),
                    explanation=(
                        f"Pushed unvisited neighbors {unvisited_neighbors} of '{current}' onto LIFO stack. "
                        f"Next branch to explore will be '{unvisited_neighbors[0]}' (top of stack)."
                    ),
                    depth_or_level=dict(depths),
                    metadata={"depth": depth, "stack_size": len(stack), "neighbors": unvisited_neighbors}
                )
            )
            step_counter += 1

        if not traverse_all_components:
            break

    steps.append(
        TraversalStep(
            step_number=step_counter,
            algorithm="DFS",
            action="COMPLETE",
            current_node=None,
            active_edge=None,
            visited_nodes=list(visited_order),
            data_structure_state=[],
            frontier_nodes=[],
            tree_edges=list(tree_edges),
            traversal_order=list(traversal_order),
            explanation=(
                f"DFS traversal complete! Visited {len(traversal_order)} node(s). "
                f"Final order: {' -> '.join(traversal_order)}."
            ),
            depth_or_level=dict(depths),
            metadata={"total_visited": len(traversal_order), "max_depth": max(depths.values()) if depths else 0}
        )
    )

    return steps
