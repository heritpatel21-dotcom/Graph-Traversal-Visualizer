"""Algorithm Explorer view: In-depth educational guides, pseudocode, Python code, and comparison."""
import streamlit as st
from components.page_setup import init_page


def render_algorithm_explorer() -> None:
    """Render the comprehensive Algorithm Explorer page."""
    st.markdown(
        """
        <div style="margin-bottom:18px;">
            <div style="font-size:24px; font-weight:800; color:#F8FAFC; letter-spacing:-0.02em;">
                Algorithm Explorer & Theory Hub
            </div>
            <div style="font-size:14px; color:#94A3B8; margin-top:2px;">
                Master Breadth-First Search (BFS) and Depth-First Search (DFS) with pseudocode, production Python code, edge-case breakdowns, and pedagogical comparisons.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_bfs, tab_dfs, tab_compare, tab_pitfalls = st.tabs([
        "🌊 Breadth-First Search (BFS)",
        "🌲 Depth-First Search (DFS)",
        "⚖️ BFS vs. DFS Comparison",
        "⚠️ Common Pitfalls & Edge Cases"
    ])

    with tab_bfs:
        st.markdown("### Breadth-First Search (BFS) Architecture")
        st.markdown(
            """
            **Breadth-First Search** explores graph vertices systematically in concentric outward circles (level-by-level).
            Starting from a source vertex, BFS visits all immediate neighbors at distance 1 before proceeding to vertices at distance 2, and so forth.
            
            Because it discovers vertices strictly by increasing distance, **BFS guarantees the shortest path (minimum number of hops)** on unweighted graphs.
            """
        )

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown(
                """
                <div style="background:#1E293B; border-radius:8px; border:1px solid #334155; padding:14px; margin-bottom:14px;">
                    <div style="font-size:12px; font-weight:700; color:#818CF8; text-transform:uppercase;">Time Complexity</div>
                    <div style="font-size:22px; font-weight:700; color:#10B981; margin:4px 0;">O(V + E)</div>
                    <div style="font-size:12px; color:#94A3B8;">Each vertex is queued once; each edge is inspected at most twice (undirected) or once (directed).</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_c2:
            st.markdown(
                """
                <div style="background:#1E293B; border-radius:8px; border:1px solid #334155; padding:14px; margin-bottom:14px;">
                    <div style="font-size:12px; font-weight:700; color:#818CF8; text-transform:uppercase;">Space Complexity</div>
                    <div style="font-size:22px; font-weight:700; color:#38BDF8; margin:4px 0;">O(V)</div>
                    <div style="font-size:12px; color:#94A3B8;">The queue and visited set hold at most V vertices in the worst case (e.g. star graph frontier).</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        col_code1, col_code2 = st.columns(2)
        with col_code1:
            st.markdown("#### Pseudocode")
            st.code(
                """
ALGORITHM BFS(Graph, start_node):
    visited = set()
    queue = FIFO_Queue()

    visited.add(start_node)
    queue.enqueue(start_node)

    WHILE queue is not empty:
        current = queue.dequeue()
        PROCESS(current)

        FOR EACH neighbor IN Graph.neighbors(current):
            IF neighbor NOT IN visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)
                RECORD_EDGE(current, neighbor)
                """,
                language="text"
            )

        with col_code2:
            st.markdown("#### Production Python (`collections.deque`)")
            st.code(
                """
from collections import deque
from typing import Dict, List, Set

def bfs(graph: Dict[str, List[str]], start: str) -> List[str]:
    visited: Set[str] = {start}
    queue: deque[str] = deque([start])
    traversal_order: List[str] = []

    while queue:
        current = queue.popleft()  # O(1) FIFO pop
        traversal_order.append(current)

        for neighbor in sorted(graph.get(current, [])):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)  # Enqueue to rear

    return traversal_order
                """,
                language="python"
            )

        st.markdown("#### Primary Use Cases for BFS")
        st.markdown(
            """
            - **Shortest Path on Unweighted Graphs:** Finds the path with the minimum number of edges (e.g., social network degrees of separation, routing hops).
            - **Web Crawlers:** Crawling links by depth level to stay close to the seed domain.
            - **Bipartiteness Testing:** Two-coloring vertices by alternating levels.
            - **Connected Components Discovery:** Identifying all reachable nodes in a cluster.
            - **Finding Minimum Spanning Trees (Unweighted):** The BFS traversal tree forms a valid minimum spanning tree when edge weights are uniform.
            """
        )

    with tab_dfs:
        st.markdown("### Depth-First Search (DFS) Architecture")
        st.markdown(
            """
            **Depth-First Search** plunges deep along each branch before backtracking.
            Starting from a root node, DFS selects the first unvisited neighbor and continues exploring as far down that line of descent as possible.
            Only when it hits a dead-end (a node with no unvisited neighbors) does it backtrack to the most recent branching ancestor.
            
            DFS utilizes a **LIFO (Last-In, First-Out) stack**, either through explicit Python stack operations or programming language recursion.
            """
        )

        col_c3, col_c4 = st.columns(2)
        with col_c3:
            st.markdown(
                """
                <div style="background:#1E293B; border-radius:8px; border:1px solid #334155; padding:14px; margin-bottom:14px;">
                    <div style="font-size:12px; font-weight:700; color:#EC4899; text-transform:uppercase;">Time Complexity</div>
                    <div style="font-size:22px; font-weight:700; color:#10B981; margin:4px 0;">O(V + E)</div>
                    <div style="font-size:12px; color:#94A3B8;">Every vertex and edge is evaluated once during recursive discovery and backtracking.</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_c4:
            st.markdown(
                """
                <div style="background:#1E293B; border-radius:8px; border:1px solid #334155; padding:14px; margin-bottom:14px;">
                    <div style="font-size:12px; font-weight:700; color:#EC4899; text-transform:uppercase;">Space Complexity</div>
                    <div style="font-size:22px; font-weight:700; color:#38BDF8; margin:4px 0;">O(V)</div>
                    <div style="font-size:12px; color:#94A3B8;">Memory is bounded by maximum recursion/stack depth: O(h) where h ≤ V in linear graphs.</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        col_code3, col_code4 = st.columns(2)
        with col_code3:
            st.markdown("#### Pseudocode (Explicit Stack)")
            st.code(
                """
ALGORITHM DFS_Iterative(Graph, start_node):
    visited = set()
    stack = LIFO_Stack()

    stack.push(start_node)

    WHILE stack is not empty:
        current = stack.pop()

        IF current NOT IN visited:
            visited.add(current)
            PROCESS(current)

            FOR EACH neighbor IN REVERSED(Graph.neighbors(current)):
                IF neighbor NOT IN visited:
                    stack.push(neighbor)
                """,
                language="text"
            )

        with col_code4:
            st.markdown("#### Production Python (Explicit List Stack)")
            st.code(
                """
from typing import Dict, List, Set

def dfs(graph: Dict[str, List[str]], start: str) -> List[str]:
    visited: Set[str] = set()
    stack: List[str] = [start]
    traversal_order: List[str] = []

    while stack:
        current = stack.pop()  # O(1) LIFO pop
        if current not in visited:
            visited.add(current)
            traversal_order.append(current)

            # Reverse sorted order ensures alphabetical exploration
            for neighbor in reversed(sorted(graph.get(current, []))):
                if neighbor not in visited:
                    stack.append(neighbor)

    return traversal_order
                """,
                language="python"
            )

        st.markdown("#### Primary Use Cases for DFS")
        st.markdown(
            """
            - **Topological Sorting:** Ordering tasks with prerequisites (DAGs).
            - **Cycle Detection:** Detecting back-edges in directed and undirected graphs.
            - **Strongly Connected Components (SCC):** Tarjan's and Kosaraju's algorithms rely heavily on DFS finish times.
            - **Solving Mazes & Puzzles:** Exhaustively exploring paths (e.g., Sudoku solvers, chess move search, N-Queens).
            - **Biconnected Components & Bridges:** Identifying critical articulation points in networks.
            """
        )

    with tab_compare:
        st.markdown("### Side-by-Side Architectural Comparison")
        st.markdown(
            r"""
| Feature / Characteristic | Breadth-First Search (BFS) | Depth-First Search (DFS) |
| :--- | :--- | :--- |
| **Primary Data Structure** | `collections.deque` (FIFO Queue) | Python `list` / Call Stack (LIFO Stack) |
| **Exploration Strategy** | Level-by-level, radiating outward | Branch-by-branch, depth-first |
| **Guaranteed Shortest Path?** | **Yes** (unweighted graphs, min edges) | **No** (may find deep suboptimal paths) |
| **Time Complexity** | $\mathcal{O}(V + E)$ | $\mathcal{O}(V + E)$ |
| **Space Complexity** | $\mathcal{O}(V)$ (bounded by width / max level) | $\mathcal{O}(V)$ (bounded by max branch depth) |
| **Memory in Wide Trees** | High (must store entire active level) | Low (only stores current branch) |
| **Memory in Deep Trees** | Low (few nodes per level) | High (deep recursion stack) |
| **Tree Edge Construction** | Forms BFS Tree (shortest paths) | Forms DFS Tree (deep tree + back edges) |
| **Best For** | Shortest path, broadcasting, nearest-neighbors | Topological sorting, cycle detection, mazes |
            """
        )

    with tab_pitfalls:
        st.markdown("### Common Pitfalls & Mistakes")
        st.markdown(
            r"""
            1. **Marking Visited on Pop vs Enqueue in BFS:**
               - *Mistake:* Marking nodes visited only when dequeuing from the queue.
               - *Consequence:* The same node may be added multiple times by distinct neighbors, causing exponential queue explosion!
               - *Fix:* Always mark nodes visited *immediately upon enqueuing*.

            2. **Using Python `list.pop(0)` for BFS:**
               - *Mistake:* Using a standard Python list as a queue and calling `list.pop(0)`.
               - *Consequence:* `list.pop(0)` takes $\mathcal{O}(V)$ time because all remaining elements shift in memory, turning BFS from $\mathcal{O}(V + E)$ into $\mathcal{O}(V^2 + E)$.
               - *Fix:* Always use `collections.deque.popleft()`, which runs in guaranteed $\mathcal{O}(1)$ time.

            3. **Unchecked Recursion in Python DFS:**
               - *Mistake:* Implementing recursive DFS on large graphs without considering `sys.getrecursionlimit()` (default 1000).
               - *Consequence:* `RecursionError: maximum recursion depth exceeded`.
               - *Fix:* Use an explicit iterative stack using Python's `list.append()` and `list.pop()`.

            4. **Disconnected Graph Traversal:**
               - *Mistake:* Assuming a single traversal starting from node `start` visits the entire graph.
               - *Consequence:* Isolated nodes and disjoint components are completely missed.
               - *Fix:* When a full graph traversal is needed, loop through all vertices and trigger a new component traversal whenever an unvisited vertex is encountered.
            """
        )


if __name__ == "__main__":
    init_page("Algorithm Explorer", "📚")
    render_algorithm_explorer()
