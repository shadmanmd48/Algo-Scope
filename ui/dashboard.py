"""
AlgoScope Main Dashboard
Interactive dashboard displaying module cards, learning stats, and quick launches.
Strictly conforms to the ProFinance light design system and reference image 2.
"""

import tkinter as tk
from typing import Callable, Dict, List
from core.theme import (
    COLOR_PAGE_BG, COLOR_CONTAINER, COLOR_SURFACE_1, COLOR_SURFACE_2, COLOR_BORDER, COLOR_BORDER_HOT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED, COLOR_LIME,
    STATE_DEFAULT, STATE_SORTED, STATE_COMPARE, STATE_SECONDARY,
    FONT_HEADING_2, FONT_HEADING_3, FONT_HEADING_4, FONT_TITLE_1, FONT_TITLE_2, FONT_TITLE_4,
    FONT_BODY_3, FONT_BODY_6, FONT_BUTTON_SM, FONT_CAPTION_1,
    SPACING_100, SPACING_200, SPACING_300, SPACING_400
)
from ui.components import CardFrame, StyledButton, Badge

class DashboardView(tk.Frame):
    """The central hub providing quick access to all 6 DSA modules."""
    def __init__(self, master, on_open_module: Callable[[str], None], **kwargs):
        super().__init__(master, bg=COLOR_PAGE_BG, **kwargs)
        self.on_open_module = on_open_module

        # Scrollable container for dashboard
        self.canvas = tk.Canvas(self, bg=COLOR_PAGE_BG, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_content = tk.Frame(self.canvas, bg=COLOR_PAGE_BG)

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
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self._build_dashboard_content()

    def _on_mousewheel(self, event):
        if self.winfo_ismapped():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _build_dashboard_content(self):
        container = tk.Frame(self.scroll_content, bg=COLOR_PAGE_BG)
        container.pack(fill="both", expand=True, padx=SPACING_400, pady=SPACING_300)

        # 1. Section Header (Matching Reference Image 2)
        header_f = tk.Frame(container, bg=COLOR_PAGE_BG)
        header_f.pack(fill="x", pady=(SPACING_200, SPACING_300))

        lbl_head = tk.Label(
            header_f,
            text="Get the Most Out of Algorithms",
            bg=COLOR_PAGE_BG,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_HEADING_3
        )
        lbl_head.pack(anchor="w")

        lbl_sub = tk.Label(
            header_f,
            text="Six comprehensive visual laboratories designed to build deep algorithmic intuition through genuine execution.",
            bg=COLOR_PAGE_BG,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY_6,
            wraplength=900,
            justify="left"
        )
        lbl_sub.pack(anchor="w", pady=(8, 0))

        # 2. Modules Grid (2 or 3 columns matching reference cards)
        grid_f = tk.Frame(container, bg=COLOR_PAGE_BG)
        grid_f.pack(fill="both", expand=True)

        grid_f.columnconfigure(0, weight=1)
        grid_f.columnconfigure(1, weight=1)
        grid_f.columnconfigure(2, weight=1)

        modules_data = [
            {
                "id": "Sorting",
                "category": "01 / ARRAYS",
                "title": "Sorting Visualizer",
                "desc": "Bubble, Selection, Insertion, Merge, Quick, and Heap Sort with dynamic bar animations, pivot indicators, and live swap counters.",
                "color": "#3B82F6"
            },
            {
                "id": "Graphs",
                "category": "02 / NETWORKS",
                "title": "Graph Visualizer",
                "desc": "Interactive topology builder. Test BFS, DFS, Dijkstra's shortest path, A* search, and Prim's & Kruskal's Minimum Spanning Trees.",
                "color": "#8B5CF6"
            },
            {
                "id": "Searching",
                "category": "03 / SEARCH",
                "title": "Searching Visualizer",
                "desc": "Step-by-step element probing with Linear, Binary, Jump, and Interpolation search boundary tracking on sorted and unsorted sets.",
                "color": "#10B981"
            },
            {
                "id": "Trees",
                "category": "04 / HIERARCHY",
                "title": "Tree Visualizer",
                "desc": "Dynamic BST and self-balancing AVL trees. Follow balance factor computations, LL/RR/LR/RL rotation mechanics, and 4 traversals.",
                "color": "#EC4899"
            },
            {
                "id": "Data Structures",
                "category": "05 / MEMORY",
                "title": "Data Structures",
                "desc": "Watch Stacks (LIFO), Queues (FIFO), Circular Buffers, Singly & Doubly Linked Lists, and Hash Table collision resolution mutate in memory.",
                "color": "#06B6D4"
            },
            {
                "id": "Performance",
                "category": "06 / BENCHMARKS",
                "title": "Performance Analyzer",
                "desc": "Benchmark actual CPU wall-clock runtime in milliseconds with time.perf_counter(). Compare operations against Big-O bounds.",
                "color": "#F59E0B"
            }
        ]

        for i, mod in enumerate(modules_data):
            row = i // 3
            col = i % 3
            card = self._create_module_card(grid_f, mod)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        # 3. Bottom Feature Highlights (Matching "The difference is in the execution")
        bottom_f = tk.Frame(container, bg=COLOR_PAGE_BG)
        bottom_f.pack(fill="x", pady=(SPACING_400, SPACING_200))

        feat_card = CardFrame(bottom_f, bg=COLOR_SURFACE_1)
        feat_card.pack(fill="x")

        feat_inner = tk.Frame(feat_card.body, bg=COLOR_SURFACE_1, padx=SPACING_300, pady=SPACING_300)
        feat_inner.pack(fill="both")

        feat_inner.columnconfigure(0, weight=1)
        feat_inner.columnconfigure(1, weight=2)

        left_side = tk.Frame(feat_inner, bg=COLOR_SURFACE_1)
        left_side.grid(row=0, column=0, sticky="nw", padx=(0, SPACING_300))

        lbl_feat_title = tk.Label(
            left_side,
            text="The difference is in\nthe execution.",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_HEADING_4,
            justify="left"
        )
        lbl_feat_title.pack(anchor="w")

        lbl_feat_desc = tk.Label(
            left_side,
            text="Designed from the ground up to make algorithms intuitive, beautiful, and interactive.",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY_6,
            wraplength=280,
            justify="left"
        )
        lbl_feat_desc.pack(anchor="w", pady=(8, 0))

        right_side = tk.Frame(feat_inner, bg=COLOR_SURFACE_1)
        right_side.grid(row=0, column=1, sticky="nsew")

        points = [
            ("01  100% Real State Snapshots", "No prewritten animations or faked delays. Every frame comes directly from genuine algorithmic execution."),
            ("02  High-DPI Per-Monitor V2 Crispness", "Subpixel-accurate rendering on modern 4K, 1440p, and multi-monitor setups at 100%, 125%, 150%, and 200%."),
            ("03  Interactive Micro-Laboratories", "Add custom nodes, drag graph vertices, type arbitrary arrays, and watch self-balancing AVL rotations.")
        ]

        for num_title, body_desc in points:
            item_f = tk.Frame(right_side, bg=COLOR_SURFACE_1)
            item_f.pack(fill="x", pady=(0, 12))

            lbl_t = tk.Label(item_f, text=num_title, bg=COLOR_SURFACE_1, fg=COLOR_TEXT_PRIMARY, font=FONT_TITLE_4)
            lbl_t.pack(anchor="w")

            lbl_b = tk.Label(item_f, text=body_desc, bg=COLOR_SURFACE_1, fg=COLOR_TEXT_SECONDARY, font=FONT_BODY_6, wraplength=480, justify="left")
            lbl_b.pack(anchor="w", pady=(2, 0))

    def _create_module_card(self, parent, mod: dict) -> tk.Frame:
        card = CardFrame(parent, bg=COLOR_SURFACE_1)
        p = card.body

        inner = tk.Frame(p, bg=COLOR_SURFACE_1, padx=SPACING_200, pady=SPACING_200)
        inner.pack(fill="both", expand=True)

        # Category Tag (e.g. 01 / ARRAYS)
        lbl_cat = tk.Label(
            inner,
            text=mod["category"],
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_CAPTION_1
        )
        lbl_cat.pack(anchor="w", pady=(0, 6))

        # Title
        lbl_title = tk.Label(
            inner,
            text=mod["title"],
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_TITLE_1
        )
        lbl_title.pack(anchor="w", pady=(0, 8))

        # Description
        lbl_desc = tk.Label(
            inner,
            text=mod["desc"],
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY_6,
            wraplength=260,
            justify="left",
            height=4
        )
        lbl_desc.pack(anchor="w", pady=(0, 16))

        # Explore Button (Rounded Pill Button)
        btn_launch = StyledButton(
            inner,
            text="Explore Laboratory →",
            variant="secondary",
            size="sm",
            command=lambda m_id=mod["id"]: self.on_open_module(m_id)
        )
        btn_launch.pack(anchor="w")

        return card
