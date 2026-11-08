"""
AlgoScope Main Dashboard
Interactive dashboard displaying module cards, learning stats, and quick launches.
"""

import tkinter as tk
from typing import Callable
from core.theme import (
    COLOR_BLACK, COLOR_SURFACE_1, COLOR_SURFACE_2, COLOR_BORDER, COLOR_BORDER_HOT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    STATE_DEFAULT, STATE_SORTED, STATE_COMPARE, STATE_SECONDARY,
    FONT_HEADING_3, FONT_HEADING_4, FONT_TITLE_2, FONT_TITLE_4, FONT_BODY_6,
    FONT_BUTTON_SM, FONT_CAPTION_1, SPACING_100, SPACING_200, SPACING_300
)
from ui.components import CardFrame, StyledButton, Badge

class DashboardView(tk.Frame):
    """The central hub providing quick access to all 6 DSA modules."""
    def __init__(self, master, on_open_module: Callable[[str], None], **kwargs):
        super().__init__(master, bg=COLOR_BLACK, **kwargs)
        self.on_open_module = on_open_module

        # Scrollable container for dashboard
        self.canvas = tk.Canvas(self, bg=COLOR_BLACK, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_content = tk.Frame(self.canvas, bg=COLOR_BLACK)

        self.scroll_content.bind(
            "<Configure>",
            lambda _: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.window_id = self.canvas.create_window((0, 0), window=self.scroll_content, anchor="nw")
        self.canvas.configure(xscrollcommand=None, yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.window_id, width=e.width)
        )
        # Bind mouse wheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self._build_dashboard_content()

    def _on_mousewheel(self, event):
        if self.winfo_ismapped():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _build_dashboard_content(self):
        container = tk.Frame(self.scroll_content, bg=COLOR_BLACK)
        container.pack(fill="both", expand=True, padx=SPACING_300, pady=SPACING_300)

        # 1. Welcome Header Banner
        banner_card = CardFrame(container, bg=COLOR_SURFACE_1)
        banner_card.pack(fill="x", pady=(0, SPACING_300))

        b_body = banner_card.body
        b_inner = tk.Frame(b_body, bg=COLOR_SURFACE_1, padx=SPACING_300, pady=SPACING_200)
        b_inner.pack(fill="both")

        lbl_head = tk.Label(
            b_inner,
            text="Interactive DSA & Algorithm Visualizer",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_HEADING_3
        )
        lbl_head.pack(anchor="w")

        lbl_sub = tk.Label(
            b_inner,
            text="Select any core module below to explore step-by-step visualizations driven by real algorithm execution, interactive controls, and performance metrics.",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY_6,
            wraplength=800,
            justify="left"
        )
        lbl_sub.pack(anchor="w", pady=(6, 0))

        # Quick stats pill strip
        stats_strip = tk.Frame(b_inner, bg=COLOR_SURFACE_1)
        stats_strip.pack(anchor="w", pady=(12, 0))

        def add_pill(text, bg_col):
            b = Badge(stats_strip, text=text, bg_color=bg_col)
            b.pack(side="left", padx=(0, 8))

        add_pill("6 Visualizer Modules", COLOR_SURFACE_2)
        add_pill("24 Interactive Algorithms", COLOR_SURFACE_2)
        add_pill("100% Real Time Execution", COLOR_SURFACE_2)
        add_pill("Zero External Dependencies", COLOR_SURFACE_2)

        # 2. Modules Grid (2 columns x 3 rows)
        grid_f = tk.Frame(container, bg=COLOR_BLACK)
        grid_f.pack(fill="both", expand=True)

        grid_f.columnconfigure(0, weight=1)
        grid_f.columnconfigure(1, weight=1)

        modules_data = [
            {
                "id": "Sorting",
                "title": "Sorting Visualizer",
                "badge": "6 Algorithms",
                "desc": "Real-time bar visualization highlighting comparisons, swaps, and sorted subarrays with custom input and speed control.",
                "tags": ["Bubble", "Selection", "Insertion", "Merge", "Quick", "Heap"],
                "color": "#3B82F6"
            },
            {
                "id": "Searching",
                "title": "Searching Visualizer",
                "badge": "4 Algorithms",
                "desc": "Sequential and interval search visualizers with target indexing, interval bounds, and array ordering enforcement.",
                "tags": ["Linear", "Binary", "Jump", "Interpolation"],
                "color": "#10B981"
            },
            {
                "id": "Graphs",
                "title": "Graph Visualizer",
                "badge": "6 Algorithms",
                "desc": "Interactive canvas where you can create nodes and weighted edges, drag elements, and run shortest path & MST algorithms.",
                "tags": ["BFS", "DFS", "Dijkstra", "A*", "Prim MST", "Kruskal MST"],
                "color": "#8B5CF6"
            },
            {
                "id": "Trees",
                "title": "Tree Visualizer",
                "badge": "BST & AVL",
                "desc": "Dynamic binary tree canvas with balance factor calculations, live AVL rotations (LL, RR, LR, RL), and 4 traversal modes.",
                "tags": ["BST Insert/Delete", "AVL Rotations", "Inorder", "Preorder", "Level Order"],
                "color": "#EC4899"
            },
            {
                "id": "Data Structures",
                "title": "Data Structures",
                "badge": "5 Core Structures",
                "desc": "Step-by-step memory animation for stacks, queues, ring buffers, linked lists, and hash table collision resolution.",
                "tags": ["Stack", "Queue", "Circular Queue", "Linked List", "Hash Table"],
                "color": "#06B6D4"
            },
            {
                "id": "Performance",
                "title": "Performance Analyzer",
                "badge": "Live Benchmarks",
                "desc": "Compare execution times, comparisons, and swaps across multiple sorting algorithms on arbitrary array sizes using live charts.",
                "tags": ["Wall-clock Runtime (ms)", "Real Operations Count", "Comparative Canvas Charts"],
                "color": "#F59E0B"
            }
        ]

        for i, mod in enumerate(modules_data):
            row = i // 2
            col = i % 2
            card = self._create_module_card(grid_f, mod)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

    def _create_module_card(self, parent, mod: dict) -> tk.Frame:
        card = CardFrame(parent, bg=COLOR_SURFACE_1)
        p = card.body

        inner = tk.Frame(p, bg=COLOR_SURFACE_1, padx=SPACING_200, pady=SPACING_200)
        inner.pack(fill="both", expand=True)

        # Header Row
        top_row = tk.Frame(inner, bg=COLOR_SURFACE_1)
        top_row.pack(fill="x", pady=(0, 6))

        lbl_title = tk.Label(
            top_row,
            text=mod["title"],
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_TITLE_2
        )
        lbl_title.pack(side="left")

        badge = Badge(top_row, text=mod["badge"], bg_color=COLOR_SURFACE_2)
        badge.pack(side="right")

        # Description
        lbl_desc = tk.Label(
            inner,
            text=mod["desc"],
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY_6,
            wraplength=380,
            justify="left"
        )
        lbl_desc.pack(anchor="w", pady=(0, 10))

        # Tag Pills
        tag_f = tk.Frame(inner, bg=COLOR_SURFACE_1)
        tag_f.pack(anchor="w", pady=(0, 14))

        for t in mod["tags"]:
            lbl_t = tk.Label(
                tag_f,
                text=t,
                bg=COLOR_SURFACE_2,
                fg=COLOR_TEXT_MUTED,
                font=FONT_CAPTION_1,
                padx=6,
                pady=2
            )
            lbl_t.pack(side="left", padx=(0, 4), pady=(0, 4))

        # Launch Button
        btn_launch = StyledButton(
            inner,
            text="Launch Visualizer →",
            variant="secondary",
            size="sm",
            command=lambda m_id=mod["id"]: self.on_open_module(m_id)
        )
        btn_launch.pack(anchor="w")

        return card

