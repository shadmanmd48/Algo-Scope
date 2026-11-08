"""
AlgoScope Tree Visualizer Module
Interactive Canvas rendering BST & AVL Trees with dynamic layout, balance factors, rotations, and traversals.
"""

import math
import tkinter as tk
from typing import Any, Callable, Dict, List, Optional, Tuple
from visualizers.base_visualizer import BaseVisualizerView
from core.animation_engine import AnimationEngine
from core.base_algorithm import Step
from core.theme import (
    COLOR_BLACK, COLOR_SURFACE_1, COLOR_SURFACE_2, COLOR_BORDER, COLOR_BORDER_HOT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    STATE_DEFAULT, STATE_COMPARE, STATE_ACTIVE, STATE_SORTED, STATE_SPECIAL, STATE_SECONDARY,
    FONT_BUTTON_SM, FONT_TITLE_4, FONT_CAPTION_1, FONT_CAPTION_3, FONT_BODY_6
)
from ui.components import StyledButton, LabeledEntry
from algorithms.trees import TreeManager

class TreeView(BaseVisualizerView):
    """Visualizes Binary Search Tree and self-balancing AVL Tree on Canvas."""
    def __init__(self, master, on_back: Callable[[], None]):
        self.is_avl_mode = False
        self.tree_manager = TreeManager(is_avl=self.is_avl_mode)

        super().__init__(
            master=master,
            title="Tree Visualizer",
            category="Trees",
            algorithms=["Binary Search Tree (BST)", "AVL Tree"],
            on_algorithm_change=self._on_tree_type_changed,
            on_back_to_dashboard=on_back
        )

        # Canvas
        self.canvas = tk.Canvas(
            self.canvas_card.body,
            bg=COLOR_SURFACE_1,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=12, pady=12)
        self.canvas.bind("<Configure>", lambda _: self._draw_current_state())

        self._add_tree_controls()

        self.engine = AnimationEngine(
            root=self,
            on_render_callback=self._render_step,
            on_complete_callback=self._on_tree_completed
        )

        # Populate initial sample tree
        self._populate_sample_tree()

    def _add_tree_controls(self):
        """Tool bar for node operations: Insert, Delete, Search, Traversals."""
        top_ctrl = tk.Frame(self.canvas_card.body, bg=COLOR_SURFACE_1)
        top_ctrl.pack(fill="x", padx=12, pady=(8, 0), side="top")

        # Insert
        self.entry_val = LabeledEntry(top_ctrl, label_text="", initial_value="25", width=5)
        self.entry_val.pack(side="left", padx=(0, 4))

        btn_insert = StyledButton(top_ctrl, text="+ Insert", size="sm", variant="secondary", command=self._action_insert)
        btn_insert.pack(side="left", padx=(0, 6))

        btn_delete = StyledButton(top_ctrl, text="- Delete", size="sm", variant="secondary", command=self._action_delete)
        btn_delete.pack(side="left", padx=(0, 6))

        btn_search = StyledButton(top_ctrl, text="🔍 Search", size="sm", variant="secondary", command=self._action_search)
        btn_search.pack(side="left", padx=(0, 14))

        # Traversals
        lbl_trav = tk.Label(top_ctrl, text="Traverse:", bg=COLOR_SURFACE_1, fg=COLOR_TEXT_SECONDARY, font=FONT_BODY_6)
        lbl_trav.pack(side="left", padx=(0, 4))

        btn_in = StyledButton(top_ctrl, text="Inorder", size="sm", variant="secondary", command=lambda: self._action_traverse("inorder"))
        btn_in.pack(side="left", padx=2)

        btn_pre = StyledButton(top_ctrl, text="Preorder", size="sm", variant="secondary", command=lambda: self._action_traverse("preorder"))
        btn_pre.pack(side="left", padx=2)

        btn_post = StyledButton(top_ctrl, text="Postorder", size="sm", variant="secondary", command=lambda: self._action_traverse("postorder"))
        btn_post.pack(side="left", padx=2)

        btn_lvl = StyledButton(top_ctrl, text="Level Order", size="sm", variant="secondary", command=lambda: self._action_traverse("levelorder"))
        btn_lvl.pack(side="left", padx=2)

        btn_reset_tree = StyledButton(top_ctrl, text="Reset Tree", size="sm", variant="secondary", command=self._populate_sample_tree)
        btn_reset_tree.pack(side="right")

    def _populate_sample_tree(self):
        """Constructs an initial balanced tree."""
        self.tree_manager = TreeManager(is_avl=self.is_avl_mode)
        initial_keys = [45, 20, 65, 10, 30, 55, 80] if not self.is_avl_mode else [30, 20, 40, 10, 25, 35, 50]
        for k in initial_keys:
            # Run generator to completion to load initial state
            gen = self.tree_manager.insert(k)
            try:
                while True:
                    next(gen)
            except StopIteration:
                pass

        init_step = Step(
            action="init",
            state=self.tree_manager.snapshot(),
            indices=[],
            message=f"Initialized sample {'AVL Tree' if self.is_avl_mode else 'Binary Search Tree'}."
        )
        self.engine.load_steps([init_step])

    def _on_tree_type_changed(self, name: str):
        self.is_avl_mode = (name == "AVL Tree")
        self._populate_sample_tree()

    def _action_insert(self):
        val_str = self.entry_val.get_value()
        try:
            val = int(val_str)
            gen = self.tree_manager.insert(val)
            self.engine.load_generator(gen)
            self.btn_play.set_text("▶ Play")
        except ValueError:
            self.update_status("Please enter a valid integer to insert!")

    def _action_delete(self):
        val_str = self.entry_val.get_value()
        try:
            val = int(val_str)
            gen = self.tree_manager.delete(val)
            self.engine.load_generator(gen)
            self.btn_play.set_text("▶ Play")
        except ValueError:
            self.update_status("Please enter a valid integer to delete!")

    def _action_search(self):
        val_str = self.entry_val.get_value()
        try:
            val = int(val_str)
            gen = self.tree_manager.search(val)
            self.engine.load_generator(gen)
            self.btn_play.set_text("▶ Play")
        except ValueError:
            self.update_status("Please enter a valid integer to search!")

    def _action_traverse(self, mode: str):
        gen = self.tree_manager.traverse(mode)
        self.engine.load_generator(gen)
        self.btn_play.set_text("▶ Play")

    def _render_step(self, step: Step):
        self._last_step = step
        self.update_status(step.message)
        self.highlight_pseudocode_line(step.pseudocode_line)
        self._draw_current_state()

    def _draw_current_state(self):
        """Calculates dynamic tree layout and paints nodes on Tkinter Canvas."""
        self.canvas.delete("all")
        if not hasattr(self, '_last_step') or not self._last_step:
            return

        step = self._last_step
        tree_dict = step.state
        if not tree_dict:
            self.canvas.create_text(
                self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2,
                text="Tree is currently empty. Insert nodes to visualize.",
                fill=COLOR_TEXT_MUTED,
                font=FONT_TITLE_4
            )
            return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 10 or h <= 10:
            return

        # Recursive coordinate calculator
        coords: Dict[int, Tuple[float, float, Dict[str, Any]]] = {}

        def compute_coords(node_d: Dict[str, Any], depth: int, left_bound: float, right_bound: float):
            x = (left_bound + right_bound) / 2
            y = 50 + (depth * 68)
            coords[node_d["key"]] = (x, y, node_d)

            if node_d.get("left"):
                compute_coords(node_d["left"], depth + 1, left_bound, x)
            if node_d.get("right"):
                compute_coords(node_d["right"], depth + 1, x, right_bound)

        compute_coords(tree_dict, 0, 20, w - 20)

        # 1. Draw Connecting Branches
        for key, (x, y, node_d) in coords.items():
            if node_d.get("left"):
                child_k = node_d["left"]["key"]
                cx, cy, _ = coords[child_k]
                self.canvas.create_line(round(x), round(y), round(cx), round(cy), fill=COLOR_BORDER, width=2)
            if node_d.get("right"):
                child_k = node_d["right"]["key"]
                cx, cy, _ = coords[child_k]
                self.canvas.create_line(round(x), round(y), round(cx), round(cy), fill=COLOR_BORDER, width=2)

        # 2. Draw Nodes
        node_radius = 20
        for key, (x, y, node_d) in coords.items():
            bg_col = COLOR_SURFACE_2
            border_col = COLOR_BORDER
            text_col = COLOR_TEXT_PRIMARY

            if key in step.indices:
                if step.action in ("compare", "check_balance"):
                    bg_col = STATE_COMPARE
                    border_col = "#FBBF24"
                    text_col = "#000000"
                elif step.action in ("rotate_ll", "rotate_rr", "rotate_lr", "rotate_rl"):
                    bg_col = STATE_SPECIAL
                    border_col = "#F472B6"
                    text_col = "#FFFFFF"
                elif step.action in ("found", "traverse_visit"):
                    bg_col = STATE_SORTED
                    border_col = "#34D399"
                    text_col = "#FFFFFF"
                else:
                    bg_col = STATE_ACTIVE
                    border_col = "#F87171"
                    text_col = "#FFFFFF"
            elif key in step.secondary_indices:
                bg_col = STATE_SECONDARY
                border_col = "#22D3EE"
                text_col = "#000000"

            # Node circle with crisp integer coordinates
            rx = round(x)
            ry = round(y)
            self.canvas.create_oval(
                rx - node_radius, ry - node_radius,
                rx + node_radius, ry + node_radius,
                fill=bg_col,
                outline=border_col,
                width=2
            )

            # Key text
            self.canvas.create_text(
                rx, ry,
                text=str(key),
                fill=text_col,
                font=FONT_TITLE_4
            )

            # Balance factor & Height info (especially relevant for AVL)
            bal = node_d.get("balance", 0)
            bal_str = f"bf: {bal:+d}" if self.is_avl_mode else f"h:{node_d.get('height', 1)}"
            self.canvas.create_text(
                rx, ry - node_radius - 8,
                text=bal_str,
                fill=STATE_SECONDARY if bal == 0 else (STATE_ACTIVE if abs(bal) > 1 else COLOR_TEXT_MUTED),
                font=FONT_CAPTION_3
            )

    def _on_tree_completed(self):
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
        self._populate_sample_tree()

    def _on_speed_change(self, val):
        val_int = int(val)
        delay = max(10, 520 - val_int)
        self.engine.set_speed(delay)

