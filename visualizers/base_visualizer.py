"""
AlgoScope Base Visualizer Framework
Standard container providing unified control bar, pseudocode viewer, complexity drawer, and metrics.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, List, Optional
from core.theme import (
    COLOR_BLACK, COLOR_SURFACE_1, COLOR_SURFACE_2, COLOR_BORDER, COLOR_BORDER_HOT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    STATE_DEFAULT, STATE_COMPARE, STATE_ACTIVE, STATE_SORTED,
    FONT_HEADING_4, FONT_HEADING_6, FONT_TITLE_2, FONT_TITLE_3, FONT_TITLE_4,
    FONT_BODY_3, FONT_BODY_6, FONT_CODE_SM, FONT_BUTTON_SM, FONT_CAPTION_1,
    SPACING_50, SPACING_75, SPACING_100, SPACING_200, SPACING_300, BTN_PAD_X, BTN_PAD_Y
)
from ui.components import StyledButton, CardFrame, Badge, LabeledEntry, SlidingPillNav
from data.algorithm_info import ALGORITHM_DATA, AlgorithmInfo

class BaseVisualizerView(tk.Frame):
    """Unified layout for all AlgoScope visualization modules."""
    def __init__(
        self,
        master,
        title: str,
        category: str,
        algorithms: List[str],
        on_algorithm_change: Callable[[str], None],
        on_back_to_dashboard: Callable[[], None],
        **kwargs
    ):
        super().__init__(master, bg=COLOR_BLACK, **kwargs)
        self.title_str = title
        self.category = category
        self.algorithms = algorithms
        self.on_algorithm_change_cb = on_algorithm_change
        self.on_back_to_dashboard = on_back_to_dashboard

        self.current_algo_name = algorithms[0] if algorithms else ""
        self.pseudocode_labels: List[tk.Label] = []

        self._build_header()
        self._build_main_content()
        self._build_control_bar()

        # Update initial info
        self.set_algorithm_info(self.current_algo_name)

    def _build_header(self):
        """Top bar with back button, module title, and prominent algorithm tabs strip."""
        # Top title row
        self.header = tk.Frame(self, bg=COLOR_SURFACE_1, height=52)
        self.header.pack(fill="x", side="top")

        left_box = tk.Frame(self.header, bg=COLOR_SURFACE_1)
        left_box.pack(side="left", padx=SPACING_200, pady=SPACING_75)

        # Back to Dashboard button
        self.btn_back = StyledButton(
            left_box,
            text="← Dashboard",
            command=self.on_back_to_dashboard,
            variant="secondary",
            size="sm"
        )
        self.btn_back.pack(side="left", padx=(0, SPACING_200))

        # Title
        self.lbl_title = tk.Label(
            left_box,
            text=self.title_str,
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_HEADING_4
        )
        self.lbl_title.pack(side="left")

        # 1px divider
        border_top = tk.Frame(self, bg=COLOR_BORDER, height=1)
        border_top.pack(fill="x", side="top")

        # Dedicated Horizontal Algorithm Selector Bar directly below the header
        self.algo_strip = tk.Frame(self, bg=COLOR_SURFACE_1, height=48)
        self.algo_strip.pack(fill="x", side="top")

        algo_inner = tk.Frame(self.algo_strip, bg=COLOR_SURFACE_1)
        algo_inner.pack(side="left", padx=SPACING_200, pady=(6, 6))

        lbl_algo = tk.Label(
            algo_inner,
            text="Algorithm:",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_MUTED,
            font=FONT_CAPTION_1
        )
        lbl_algo.pack(side="left", padx=(0, SPACING_100))

        initial_idx = 0
        if self.current_algo_name in self.algorithms:
            initial_idx = self.algorithms.index(self.current_algo_name)

        self.algo_nav = SlidingPillNav(
            algo_inner,
            items=self.algorithms,
            initial_index=initial_idx,
            on_select=lambda idx, name: self.select_algorithm(name),
            height=36,
            padding_x=14,
            font_size=9,
            bg_parent=COLOR_SURFACE_1
        )
        self.algo_nav.pack(side="left")

        # 1px border below algorithm strip
        border_bottom = tk.Frame(self, bg=COLOR_BORDER, height=1)
        border_bottom.pack(fill="x", side="top")

    def select_algorithm(self, name: str):
        self.current_algo_name = name
        if hasattr(self, 'algo_nav'):
            self.algo_nav.select_by_name(name, trigger_callback=False, animate=True)
        self.set_algorithm_info(name)
        if self.on_algorithm_change_cb:
            self.on_algorithm_change_cb(name)

    def _build_main_content(self):
        """Split view: Left Canvas area + Right Information Drawer."""
        self.content_frame = tk.Frame(self, bg=COLOR_BLACK)
        self.content_frame.pack(fill="both", expand=True, padx=SPACING_100, pady=SPACING_100)

        # Left Canvas Container
        self.canvas_card = CardFrame(self.content_frame, bg=COLOR_SURFACE_1)
        self.canvas_card.pack(side="left", fill="both", expand=True, padx=(0, SPACING_100))

        # Right Information Drawer
        self.info_card = CardFrame(self.content_frame, bg=COLOR_SURFACE_1, width=340)
        self.info_card.pack(side="right", fill="y", expand=False)
        self.info_card.pack_propagate(False)

        self._build_info_drawer(self.info_card.body)

    def _build_info_drawer(self, parent):
        """Builds Pseudocode viewer, Complexity metrics, and Explanation cards."""
        # Section 1: Complexities
        comp_frame = tk.Frame(parent, bg=COLOR_SURFACE_1)
        comp_frame.pack(fill="x", padx=SPACING_100, pady=SPACING_100)

        lbl_comp_title = tk.Label(
            comp_frame,
            text="Complexity Analysis",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_TITLE_2
        )
        lbl_comp_title.pack(anchor="w", pady=(0, 6))

        # Grid for best, avg, worst, space
        grid_f = tk.Frame(comp_frame, bg=COLOR_SURFACE_1)
        grid_f.pack(fill="x")

        def make_metric(p, label, row, col):
            f = tk.Frame(p, bg=COLOR_SURFACE_2, padx=8, pady=4)
            f.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
            l_name = tk.Label(f, text=label, bg=COLOR_SURFACE_2, fg=COLOR_TEXT_MUTED, font=FONT_CAPTION_1)
            l_name.pack(anchor="w")
            l_val = tk.Label(f, text="-", bg=COLOR_SURFACE_2, fg=COLOR_TEXT_PRIMARY, font=FONT_TITLE_4)
            l_val.pack(anchor="w")
            return l_val

        grid_f.columnconfigure(0, weight=1)
        grid_f.columnconfigure(1, weight=1)

        self.lbl_best = make_metric(grid_f, "Best Case", 0, 0)
        self.lbl_avg = make_metric(grid_f, "Average Case", 0, 1)
        self.lbl_worst = make_metric(grid_f, "Worst Case", 1, 0)
        self.lbl_space = make_metric(grid_f, "Space Complexity", 1, 1)

        # Divider line
        tk.Frame(parent, bg=COLOR_BORDER, height=1).pack(fill="x", pady=SPACING_75)

        # Section 2: Pseudocode Viewer
        lbl_pseudo_title = tk.Label(
            parent,
            text="Pseudocode Execution",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_TITLE_2
        )
        lbl_pseudo_title.pack(anchor="w", padx=SPACING_100, pady=(4, 4))

        self.pseudo_container = tk.Frame(parent, bg=COLOR_SURFACE_2, padx=6, pady=6)
        self.pseudo_container.pack(fill="x", padx=SPACING_100, pady=2)

        # Section 3: Explanation & Use Cases
        tk.Frame(parent, bg=COLOR_BORDER, height=1).pack(fill="x", pady=SPACING_75)

        lbl_desc_title = tk.Label(
            parent,
            text="How It Works",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_TITLE_2
        )
        lbl_desc_title.pack(anchor="w", padx=SPACING_100, pady=(4, 2))

        self.lbl_description = tk.Label(
            parent,
            text="",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY_6,
            wraplength=310,
            justify="left"
        )
        self.lbl_description.pack(anchor="w", padx=SPACING_100, pady=(0, 6))

        lbl_use_title = tk.Label(
            parent,
            text="Practical Use Cases",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_TITLE_2
        )
        lbl_use_title.pack(anchor="w", padx=SPACING_100, pady=(4, 2))

        self.lbl_use_cases = tk.Label(
            parent,
            text="",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY_6,
            wraplength=310,
            justify="left"
        )
        self.lbl_use_cases.pack(anchor="w", padx=SPACING_100)

    def _build_control_bar(self):
        """Unified playback and metrics control bar at bottom."""
        border_top = tk.Frame(self, bg=COLOR_BORDER, height=1)
        border_top.pack(fill="x", side="bottom")

        self.control_bar = tk.Frame(self, bg=COLOR_SURFACE_1, height=72)
        self.control_bar.pack(fill="x", side="bottom")

        # Inner container
        inner = tk.Frame(self.control_bar, bg=COLOR_SURFACE_1)
        inner.pack(fill="both", expand=True, padx=SPACING_200, pady=SPACING_75)

        # Left section: Status & Metrics
        left_f = tk.Frame(inner, bg=COLOR_SURFACE_1)
        left_f.pack(side="left")

        self.lbl_status = tk.Label(
            left_f,
            text="Ready to execute.",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_TITLE_3
        )
        self.lbl_status.pack(anchor="w")

        self.metrics_bar = tk.Frame(left_f, bg=COLOR_SURFACE_1)
        self.metrics_bar.pack(anchor="w", pady=(2, 0))

        self.lbl_metric_1 = tk.Label(self.metrics_bar, text="Comparisons: 0", bg=COLOR_SURFACE_1, fg=COLOR_TEXT_SECONDARY, font=FONT_CAPTION_1)
        self.lbl_metric_1.pack(side="left", padx=(0, 16))

        self.lbl_metric_2 = tk.Label(self.metrics_bar, text="Swaps: 0", bg=COLOR_SURFACE_1, fg=COLOR_TEXT_SECONDARY, font=FONT_CAPTION_1)
        self.lbl_metric_2.pack(side="left", padx=(0, 16))

        self.lbl_step_counter = tk.Label(self.metrics_bar, text="Step: 0", bg=COLOR_SURFACE_1, fg=COLOR_TEXT_SECONDARY, font=FONT_CAPTION_1)
        self.lbl_step_counter.pack(side="left")

        # Right section: Speed Slider + Custom buttons slot
        right_f = tk.Frame(inner, bg=COLOR_SURFACE_1)
        right_f.pack(side="right")

        lbl_speed = tk.Label(right_f, text="Speed:", bg=COLOR_SURFACE_1, fg=COLOR_TEXT_SECONDARY, font=FONT_BODY_6)
        lbl_speed.pack(side="left", padx=(0, 4))

        self.speed_slider = tk.Scale(
            right_f,
            from_=5,
            to=500,
            orient="horizontal",
            showvalue=False,
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_PRIMARY,
            troughcolor=COLOR_SURFACE_2,
            highlightthickness=0,
            length=110,
            command=self._on_speed_change
        )
        self.speed_slider.set(50)
        self.speed_slider.pack(side="left", padx=(0, 16))

        # Center section: Playback Buttons
        center_f = tk.Frame(inner, bg=COLOR_SURFACE_1)
        center_f.pack(side="right", padx=(0, 20))

        self.btn_reset = StyledButton(center_f, text="↺ Reset", size="sm", variant="secondary", command=self.on_reset_click)
        self.btn_reset.pack(side="left", padx=2)

        self.btn_prev = StyledButton(center_f, text="⏮ Step", size="sm", variant="secondary", command=self.on_prev_click)
        self.btn_prev.pack(side="left", padx=2)

        self.btn_play = StyledButton(center_f, text="▶ Play", size="sm", variant="accent", command=self.on_play_click)
        self.btn_play.pack(side="left", padx=2)

        self.btn_next = StyledButton(center_f, text="Step ⏭", size="sm", variant="secondary", command=self.on_next_click)
        self.btn_next.pack(side="left", padx=2)

    def set_algorithm_info(self, name: str):
        """Load and update pseudocode, complexities, and explanations from info database."""
        info: Optional[AlgorithmInfo] = ALGORITHM_DATA.get(name)
        if not info:
            return

        self.lbl_best.config(text=info.best_time)
        self.lbl_avg.config(text=info.avg_time)
        self.lbl_worst.config(text=info.worst_time)
        self.lbl_space.config(text=info.space_complexity)
        self.lbl_description.config(text=info.description)
        self.lbl_use_cases.config(text="\n".join([f"• {u}" for u in info.use_cases]))

        # Rebuild pseudocode labels
        for w in self.pseudo_container.winfo_children():
            w.destroy()
        self.pseudocode_labels.clear()

        for idx, line in enumerate(info.pseudocode):
            lbl = tk.Label(
                self.pseudo_container,
                text=line,
                bg=COLOR_SURFACE_2,
                fg=COLOR_TEXT_SECONDARY,
                font=FONT_CODE_SM,
                anchor="w",
                padx=4,
                pady=1
            )
            lbl.pack(fill="x")
            self.pseudocode_labels.append(lbl)

    def highlight_pseudocode_line(self, line_idx: int):
        """Highlights the active pseudocode line, resetting all others."""
        for i, lbl in enumerate(self.pseudocode_labels):
            if i == line_idx:
                lbl.config(bg="#3B82F6", fg="#FFFFFF")
            else:
                lbl.config(bg=COLOR_SURFACE_2, fg=COLOR_TEXT_SECONDARY)

    def update_status(self, message: str):
        self.lbl_status.config(text=message)

    def update_metrics(self, comps: Optional[int] = None, swaps: Optional[int] = None, step: Optional[int] = None):
        if comps is not None:
            self.lbl_metric_1.config(text=f"Comparisons: {comps}")
        if swaps is not None:
            self.lbl_metric_2.config(text=f"Swaps / Ops: {swaps}")
        if step is not None:
            self.lbl_step_counter.config(text=f"Step: {step}")

    # Subclasses override these playback hooks
    def on_play_click(self):
        pass

    def on_prev_click(self):
        pass

    def on_next_click(self):
        pass

    def on_reset_click(self):
        pass

    def _on_speed_change(self, val):
        pass

