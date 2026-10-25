"""Traversal engine managing step-by-step playback, navigation, and state transitions."""
from typing import List, Optional, Tuple
import networkx as nx
from . import TraversalStep
from .bfs import run_bfs
from .dfs import run_dfs


class TraversalEngine:
    """Manages traversal step execution, navigation, and playback state."""

    def __init__(self) -> None:
        self.algorithm: str = "BFS"
        self.start_node: Optional[str] = None
        self.traverse_all_components: bool = False
        self.steps: List[TraversalStep] = []
        self.current_step_index: int = 0
        self.is_playing: bool = False
        self.speed: float = 1.0
        self.learning_mode: bool = True

    def initialize_traversal(
        self,
        graph: nx.Graph,
        algorithm: str = "BFS",
        start_node: Optional[str] = None,
        traverse_all_components: bool = False
    ) -> bool:
        """Run algorithm and cache all steps for interactive step-through."""
        self.algorithm = algorithm.upper()
        self.traverse_all_components = traverse_all_components
        
        nodes = list(graph.nodes())
        if not nodes:
            self.start_node = None
            self.steps = []
            self.current_step_index = 0
            self.is_playing = False
            return False

        if start_node is None or start_node not in graph:
            self.start_node = nodes[0]
        else:
            self.start_node = str(start_node)

        if self.algorithm == "BFS":
            self.steps = run_bfs(graph, self.start_node, self.traverse_all_components)
        else:
            self.steps = run_dfs(graph, self.start_node, self.traverse_all_components)

        self.current_step_index = 0
        self.is_playing = False
        return True

    def step_forward(self) -> bool:
        """Advance one step forward in traversal."""
        if not self.steps:
            return False
        if self.current_step_index < len(self.steps) - 1:
            self.current_step_index += 1
            return True
        else:
            self.is_playing = False
            return False

    def step_backward(self) -> bool:
        """Step one snapshot backwards."""
        if not self.steps:
            return False
        if self.current_step_index > 0:
            self.current_step_index -= 1
            return True
        return False

    def reset_traversal(self) -> None:
        """Reset traversal back to step 0."""
        self.current_step_index = 0
        self.is_playing = False

    def jump_to_step(self, step_idx: int) -> None:
        """Jump directly to a specific step index."""
        if not self.steps:
            self.current_step_index = 0
            return
        clamped = max(0, min(int(step_idx), len(self.steps) - 1))
        self.current_step_index = clamped

    def get_current_step(self) -> Optional[TraversalStep]:
        """Return the current TraversalStep snapshot."""
        if not self.steps or self.current_step_index >= len(self.steps):
            return None
        return self.steps[self.current_step_index]

    def get_total_steps(self) -> int:
        """Return total number of recorded steps."""
        return len(self.steps)

    def get_progress_ratio(self) -> float:
        """Return fractional progress between 0.0 and 1.0."""
        total = len(self.steps)
        if total <= 1:
            return 1.0 if total == 1 else 0.0
        return round(self.current_step_index / (total - 1), 3)

    def is_finished(self) -> bool:
        """Return whether traversal has reached the terminal step."""
        if not self.steps:
            return True
        return self.current_step_index >= len(self.steps) - 1
