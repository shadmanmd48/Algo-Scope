"""
AlgoScope Graph Visualizer Module
Interactive Canvas for graph algorithms with custom node/edge creation, presets, and pathfinding.
"""

import math
import random
import tkinter as tk
from typing import Callable, Dict, List, Optional, Set, Tuple
from visualizers.base_visualizer import BaseVisualizerView
from core.animation_engine import AnimationEngine
from core.base_algorithm import Step
from core.theme import (
    COLOR_BLACK, COLOR_SURFACE_1, COLOR_SURFACE_2, COLOR_BORDER, COLOR_BORDER_HOT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    STATE_DEFAULT, STATE_COMPARE, STATE_ACTIVE, STATE_SORTED, STATE_VISITED, STATE_SECONDARY,
    FONT_BUTTON_SM, FONT_TITLE_4, FONT_CAPTION_1, FONT_BODY_6
)
from ui.components import StyledButton, LabeledEntry
from algorithms.graphs import bfs, dfs, dijkstra, a_star, prim_mst, kruskal_mst

class GraphView(BaseVisualizerView):
    """Interactive visualizer for Graph Traversal, Shortest Path, and MST algorithms."""
    def __init__(self, master, on_back: Callable[[], None]):
        self.algo_functions = {
            "Breadth First Search (BFS)": bfs,
            "Depth First Search (DFS)": dfs,
            "Dijkstra's Algorithm": dijkstra,
            "A* Search": a_star,
            "Prim's Algorithm": prim_mst,
            "Kruskal's Algorithm": kruskal_mst
        }

        super().__init__(
            master=master,
            title="Graph Visualizer",
            category="Graphs",
            algorithms=list(self.algo_functions.keys()),
            on_algorithm_change=self._on_algorithm_changed,
            on_back_to_dashboard=on_back
        )

        # Graph Data Structure
        # nodes: id -> (x, y, label)
        self.nodes: Dict[str, Tuple[float, float, str]] = {}
        # edges: (u, v) -> weight (undirected representation)
        self.edges: Dict[Tuple[str, str], float] = {}

        self.start_node = "A"
        self.target_node = "F"
        self.selected_node_for_edge: Optional[str] = None
        self.dragging_node: Optional[str] = None

        # Canvas
        self.canvas = tk.Canvas(
            self.canvas_card.body,
            bg=COLOR_SURFACE_1,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=12, pady=12)

        # Mouse Bindings for interactive node and edge editing
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_canvas_release)
        self.canvas.bind("<Configure>", lambda _: self._draw_current_state())

        self._add_graph_controls()

        self.engine = AnimationEngine(
            root=self,
            on_render_callback=self._render_step,
            on_complete_callback=self._on_graph_completed
        )

        # Load default preset graph
        self.load_preset("Classic Network")

    def _add_graph_controls(self):
        """Top tool bar for presets, clear, start/target node inputs."""
        top_ctrl = tk.Frame(self.canvas_card.body, bg=COLOR_SURFACE_1)
        top_ctrl.pack(fill="x", padx=12, pady=(8, 0), side="top")

        # Preset Dropdown / Buttons
        btn_preset1 = StyledButton(top_ctrl, text="Network Preset", size="sm", variant="secondary", command=lambda: self.load_preset("Classic Network"))
        btn_preset1.pack(side="left", padx=(0, 6))

        btn_preset2 = StyledButton(top_ctrl, text="Ring / Mesh", size="sm", variant="secondary", command=lambda: self.load_preset("Ring / Mesh"))
        btn_preset2.pack(side="left", padx=(0, 6))

        btn_clear = StyledButton(top_ctrl, text="Clear Canvas", size="sm", variant="secondary", command=self.clear_graph)
        btn_clear.pack(side="left", padx=(0, 14))

        # Start & Target node inputs
        lbl_start = tk.Label(top_ctrl, text="Source:", bg=COLOR_SURFACE_1, fg=COLOR_TEXT_SECONDARY, font=FONT_BODY_6)
        lbl_start.pack(side="left", padx=(0, 4))

        self.entry_start = LabeledEntry(top_ctrl, label_text="", initial_value=self.start_node, width=4)
        self.entry_start.pack(side="left", padx=(0, 10))

        lbl_target = tk.Label(top_ctrl, text="Target:", bg=COLOR_SURFACE_1, fg=COLOR_TEXT_SECONDARY, font=FONT_BODY_6)
        lbl_target.pack(side="left", padx=(0, 4))

        self.entry_target = LabeledEntry(top_ctrl, label_text="", initial_value=self.target_node, width=4)
        self.entry_target.pack(side="left", padx=(0, 10))

        btn_apply_endpoints = StyledButton(top_ctrl, text="Apply Endpoints", size="sm", variant="secondary", command=self._apply_endpoints)
        btn_apply_endpoints.pack(side="left")

    def _apply_endpoints(self):
        s = self.entry_start.get_value().upper()
        t = self.entry_target.get_value().upper()
        if s in self.nodes:
            self.start_node = s
        if t in self.nodes:
            self.target_node = t
        self.reload_algorithm()

    def clear_graph(self):
        self.nodes.clear()
        self.edges.clear()
        self.selected_node_for_edge = None
        self.engine.reset()
        self.canvas.delete("all")
        self.update_status("Graph cleared. Click on canvas to add nodes, click two nodes to link with an edge.")

    def load_preset(self, preset_name: str):
        """Loads clean, well-spaced sample graphs."""
        self.nodes.clear()
        self.edges.clear()
        self.selected_node_for_edge = None

        if preset_name == "Classic Network":
            # Nodes A through F
            self.nodes = {
                "A": (120, 160, "A"),
                "B": (280, 80, "B"),
                "C": (280, 240, "C"),
                "D": (460, 80, "D"),
                "E": (460, 240, "E"),
                "F": (620, 160, "F")
            }
            self.edges = {
                ("A", "B"): 4.0,
                ("A", "C"): 2.0,
                ("B", "C"): 1.0,
                ("B", "D"): 5.0,
                ("C", "E"): 8.0,
                ("C", "D"): 10.0,
                ("D", "E"): 2.0,
                ("D", "F"): 6.0,
                ("E", "F"): 3.0
            }
            self.start_node = "A"
            self.target_node = "F"

        elif preset_name == "Ring / Mesh":
            self.nodes = {
                "1": (200, 80, "1"),
                "2": (380, 80, "2"),
                "3": (500, 180, "3"),
                "4": (380, 280, "4"),
                "5": (200, 280, "5"),
                "6": (80, 180, "6"),
                "C": (290, 180, "C")
            }
            self.edges = {
                ("1", "2"): 3.0, ("2", "3"): 4.0, ("3", "4"): 2.0,
                ("4", "5"): 5.0, ("5", "6"): 1.0, ("6", "1"): 6.0,
                ("1", "C"): 2.5, ("2", "C"): 3.5, ("3", "C"): 1.5,
                ("4", "C"): 4.5, ("5", "C"): 2.0, ("6", "C"): 3.0
            }
            self.start_node = "1"
            self.target_node = "4"

        self.entry_start.set_value(self.start_node)
        self.entry_target.set_value(self.target_node)
        self.reload_algorithm()

    def _build_adj_list(self) -> Dict[str, List[Tuple[str, float]]]:
        """Convert undirected edges into adjacency list."""
        adj: Dict[str, List[Tuple[str, float]]] = {n: [] for n in self.nodes}
        for (u, v), w in self.edges.items():
            if u in adj and v in adj:
                adj[u].append((v, w))
                adj[v].append((u, w))
        return adj

    def reload_algorithm(self):
        self.engine.reset()
        if not self.nodes:
            self.canvas.delete("all")
            return

        adj = self._build_adj_list()
        positions = {n: (self.nodes[n][0], self.nodes[n][1]) for n in self.nodes}

        # Select matching generator
        if self.current_algo_name == "Breadth First Search (BFS)":
            gen = bfs(adj, start=self.start_node, target=self.target_node)
        elif self.current_algo_name == "Depth First Search (DFS)":
            gen = dfs(adj, start=self.start_node, target=self.target_node)
        elif self.current_algo_name == "Dijkstra's Algorithm":
            gen = dijkstra(adj, start=self.start_node, target=self.target_node)
        elif self.current_algo_name == "A* Search":
            gen = a_star(adj, positions, start=self.start_node, target=self.target_node)
        elif self.current_algo_name == "Prim's Algorithm":
            gen = prim_mst(adj, start=self.start_node)
        else:  # Kruskal's
            gen = kruskal_mst(adj)

        init_step = Step(
            action="init",
            state={"visited": [], "mst_edges": [], "path": []},
            indices=[self.start_node] if self.start_node in self.nodes else [],
            message=f"Initialized {self.current_algo_name} on graph with {len(self.nodes)} nodes."
        )
        self.engine.load_generator(gen, initial_step=init_step)
        self.btn_play.set_text("▶ Play")

    def _on_algorithm_changed(self, name: str):
        self.reload_algorithm()

    def _render_step(self, step: Step):
        self._last_step = step
        self.update_status(step.message)
        self.highlight_pseudocode_line(step.pseudocode_line)
        self._draw_current_state()

    def _draw_current_state(self):
        """Render nodes, edges, weights, and highlighting on Tkinter Canvas."""
        self.canvas.delete("all")
        if not self.nodes:
            self.canvas.create_text(
                self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2,
                text="Click anywhere on the canvas to add nodes.\nClick one node then another to connect them with a weighted edge.",
                fill=COLOR_TEXT_MUTED,
                font=FONT_TITLE_4,
                justify="center"
            )
            return

        step = getattr(self, '_last_step', None)
        visited = set(step.state.get("visited", [])) if (step and isinstance(step.state, dict)) else set()
        path_nodes = set(step.state.get("path", [])) if (step and isinstance(step.state, dict)) else set()
        path_list = step.state.get("path", []) if (step and isinstance(step.state, dict)) else []

        # Find active edge or MST edges
        active_edge = step.state.get("edge", None) if (step and isinstance(step.state, dict)) else None
        mst_edges = step.state.get("mst_edges", []) if (step and isinstance(step.state, dict)) else []
        mst_set = {tuple(sorted([u, v])) for (u, v, *_) in mst_edges}

        # 1. Draw Edges
        for (u, v), w in self.edges.items():
            if u not in self.nodes or v not in self.nodes:
                continue
            x1, y1, _ = self.nodes[u]
            x2, y2, _ = self.nodes[v]

            edge_key = tuple(sorted([u, v]))
            edge_color = COLOR_BORDER
            line_width = 2

            # Check if part of path
            is_path_edge = False
            if len(path_list) >= 2:
                for i in range(len(path_list) - 1):
                    if tuple(sorted([path_list[i], path_list[i + 1]])) == edge_key:
                        is_path_edge = True
                        break

            if is_path_edge:
                edge_color = STATE_SORTED
                line_width = 4
            elif edge_key in mst_set:
                edge_color = STATE_SORTED
                line_width = 3
            elif active_edge and tuple(sorted(active_edge)) == edge_key:
                edge_color = STATE_ACTIVE
                line_width = 3

            # Draw edge line
            self.canvas.create_line(round(x1), round(y1), round(x2), round(y2), fill=edge_color, width=line_width)

            # Draw edge weight
            mid_x = round((x1 + x2) / 2)
            mid_y = round((y1 + y2) / 2)
            self.canvas.create_rectangle(
                mid_x - 12, mid_y - 8, mid_x + 12, mid_y + 8,
                fill=COLOR_SURFACE_2, outline=COLOR_BORDER
            )
            self.canvas.create_text(
                mid_x, mid_y,
                text=f"{w:.0f}" if w.is_integer() else f"{w:.1f}",
                fill=COLOR_TEXT_SECONDARY,
                font=FONT_CAPTION_1
            )

        # 2. Draw Nodes
        node_radius = 22
        for n_id, (x, y, label) in self.nodes.items():
            bg_col = COLOR_SURFACE_2
            border_col = COLOR_BORDER
            text_col = COLOR_TEXT_PRIMARY

            if n_id in path_nodes:
                bg_col = STATE_SORTED
                border_col = "#34D399"
                text_col = "#FFFFFF"
            elif step and n_id in step.indices:
                bg_col = STATE_ACTIVE
                border_col = "#F87171"
                text_col = "#FFFFFF"
            elif n_id in visited:
                bg_col = STATE_VISITED
                border_col = "#A78BFA"
                text_col = "#FFFFFF"

            if n_id == self.start_node:
                border_col = STATE_SECONDARY
            elif n_id == self.target_node:
                border_col = STATE_ACTIVE

            if self.selected_node_for_edge == n_id:
                border_col = "#FBBF24"

            # Outer circle with crisp coordinates
            rx = round(x)
            ry = round(y)
            self.canvas.create_oval(
                rx - node_radius, ry - node_radius,
                rx + node_radius, ry + node_radius,
                fill=bg_col,
                outline=border_col,
                width=2
            )

            # Label text
            self.canvas.create_text(
                rx, ry,
                text=label,
                fill=text_col,
                font=FONT_TITLE_4
            )

            # Distance badge if Dijkstra / A*
            if step and isinstance(step.state, dict) and "dist" in step.state:
                d = step.state["dist"].get(n_id, float("inf"))
                d_str = "∞" if d == float("inf") else f"{d:.0f}"
                self.canvas.create_text(x, y - node_radius - 8, text=d_str, fill=STATE_SECONDARY, font=FONT_CAPTION_1)

    # Canvas interaction handlers
    def _find_node_at(self, x: float, y: float) -> Optional[str]:
        for n_id, (nx, ny, _) in self.nodes.items():
            if math.hypot(x - nx, y - ny) <= 24:
                return n_id
        return None

    def _on_canvas_click(self, event):
        clicked_node = self._find_node_at(event.x, event.y)
        if clicked_node:
            if self.selected_node_for_edge is None:
                self.selected_node_for_edge = clicked_node
                self.dragging_node = clicked_node
                self._draw_current_state()
            else:
                # Add edge between selected_node_for_edge and clicked_node
                u = self.selected_node_for_edge
                v = clicked_node
                if u != v:
                    dist = math.hypot(self.nodes[u][0] - self.nodes[v][0], self.nodes[u][1] - self.nodes[v][1]) / 25.0
                    edge_key = tuple(sorted([u, v]))
                    self.edges[edge_key] = round(max(1.0, dist), 1)
                self.selected_node_for_edge = None
                self.dragging_node = None
                self.reload_algorithm()
        else:
            # Create new node with next available label
            if self.selected_node_for_edge:
                self.selected_node_for_edge = None
                self._draw_current_state()
            else:
                existing = set(self.nodes.keys())
                for char_code in range(ord('A'), ord('Z') + 1):
                    cand = chr(char_code)
                    if cand not in existing:
                        self.nodes[cand] = (event.x, event.y, cand)
                        break
                self.reload_algorithm()

    def _on_canvas_drag(self, event):
        if self.dragging_node and self.dragging_node in self.nodes:
            label = self.nodes[self.dragging_node][2]
            self.nodes[self.dragging_node] = (event.x, event.y, label)
            self._draw_current_state()

    def _on_canvas_release(self, _):
        self.dragging_node = None

    def _on_graph_completed(self):
        self.btn_play.set_text("✔ Done")

    def on_play_click(self):
        playing = self.engine.toggle_play_pause()
        self.btn_play.set_text("⏸ Pause" if playing else "▶ Play")

    def on_prev_click(self):
        self.engine.step_backward()
        self.btn_play.set_text("▶ Play")

    def on_next_click(self):
        self.engine.step_forward()
        self.btn_play.set_text("▶ Play")

    def on_reset_click(self):
        self.reload_algorithm()

    def _on_speed_change(self, val):
        val_int = int(val)
        delay = max(10, 520 - val_int)
        self.engine.set_speed(delay)

