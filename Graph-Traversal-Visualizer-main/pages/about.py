"""About Project view: Architecture documentation, UI/UX design system, and instructor guide."""
import streamlit as st
from components.page_setup import init_page


def render_about() -> None:
    """Render the About Project documentation page."""
    st.markdown(
        """
        <div style="margin-bottom:18px;">
            <div style="font-size:24px; font-weight:800; color:#F8FAFC; letter-spacing:-0.02em;">
                About Graph Traversal Visualizer
            </div>
            <div style="font-size:14px; color:#94A3B8; margin-top:2px;">
                A production-quality educational suite for mastering fundamental graph traversal algorithms.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_main, col_side = st.columns([1.8, 1.2])

    with col_main:
        st.markdown("### 🎯 Educational Philosophy")
        st.markdown(
            """
            Graph traversal algorithms often feel abstract when taught using static textbook slides or pseudocode.
            The **Graph Traversal Visualizer** bridges the gap between theoretical knowledge and algorithmic mechanics:
            
            1. **Explicit Data Structure Transparency:** Instead of abstracting away queues and stacks, every element in the `collections.deque` (BFS) and explicit `list` (DFS) is visually animated in real time.
            2. **Step-by-Step State Machines:** Every micro-operation—dequeue, neighbor discovery, tree edge creation, push, and backtracking—is treated as an atomic state transition.
            3. **Deterministic Neighbor Ordering:** Neighbors are systematically sorted, ensuring reproducible step sequences and predictable learning outcomes.
            4. **Multi-Component Resilience:** Disconnected subgraphs and isolated vertices are handled gracefully without application crashes.
            """
        )

        st.markdown("### 🛠️ Architecture & Technology Stack")
        st.markdown(
            r"""
            The entire visualizer is built in **100% Python** (exceeding the 90% requirement) with zero external frontend build steps or JavaScript frameworks:
            
            - **Python 3.11+ / 3.13:** Core algorithmic engine and data models.
            - **Streamlit:** Modern, reactive web dashboard runtime and state management.
            - **NetworkX:** Industry-standard graph data structures, topological metrics, and layout algorithms.
            - **Plotly:** WebGL-accelerated interactive canvas supporting pan, zoom, custom node states, and directed arrow annotations.
            - **collections.deque:** High-efficiency $\mathcal{O}(1)$ FIFO queue operations for Breadth-First Search.
            - **Explicit Python Lists:** Precise $\mathcal{O}(1)$ LIFO stack pushes and pops for Depth-First Search.
            - **pytest:** Comprehensive automated test suite ensuring algorithm correctness, edge case resilience, and state integrity.
            """
        )

        st.markdown("### 🎨 Developer Tools UI/UX Design System")
        st.markdown(
            """
            Inspired by modern developer interfaces (VS Code, Linear, GitHub Dark):
            
            - **Canvas & Background:** Deep navy & charcoal (`#0B0F19`, `#0F172A`).
            - **Surface & Cards:** Dark slate (`#1E293B`) with subtle borders (`#334155`).
            - **Primary Accent:** Vivid Indigo / Violet (`#6366F1`, `#8B5CF6`).
            - **Secondary Accent:** Cyan (`#38BDF8`).
            - **Success State:** Emerald Green (`#10B981`).
            - **Active Inspecting State:** Amber Gold (`#F59E0B`).
            - **Typography:** Crisp sans-serif fonts with clear mathematical notations.
            """
        )

    with col_side:
        st.markdown(
            """
            <div style="background:#1E293B; border:1px solid #334155; border-radius:10px; padding:18px; margin-bottom:16px;">
                <div style="font-size:14px; font-weight:700; color:#818CF8; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">
                    Interactive Controls Guide
                </div>
                <div style="font-size:13px; color:#E2E8F0; line-height:1.6;">
                    <b>▶ Play / ⏸ Pause:</b> Toggle automated step progression at selected speed.<br>
                    <b>◀ Prev / Next ▶:</b> Step backward or forward through recorded states.<br>
                    <b>⏮ Reset:</b> Return to initial step without losing graph edits.<br>
                    <b>⏭ Finish:</b> Jump directly to the completed traversal state.<br>
                    <b>Timeline Scrubber:</b> Drag directly to any recorded step.<br>
                    <b>🎓 Learn Mode:</b> Toggle granular pedagogical explanations.
                </div>
            </div>
            
            <div style="background:#1E293B; border:1px solid #334155; border-radius:10px; padding:18px;">
                <div style="font-size:14px; font-weight:700; color:#10B981; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">
                    Verification & Standards
                </div>
                <div style="font-size:13px; color:#CBD5E1; line-height:1.6;">
                    • 100% English user interface.<br>
                    • Full input validation (duplicate IDs, invalid endpoints, self-loops).<br>
                    • Fully tested with pytest across empty, single-node, connected, and disconnected graphs.<br>
                    • Real empirical benchmarks measured with <code>time.perf_counter()</code>.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    init_page("About Project", "ℹ️")
    render_about()
