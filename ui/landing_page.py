"""
AlgoScope Landing Page
Polished, conversion-focused desktop landing page built with pure Tkinter and Canvas.
Conforms strictly to SKILL.md visual system and requirements.
"""

import math
import random
import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Optional
from core.theme import (
    COLOR_BLACK, COLOR_SURFACE_1, COLOR_SURFACE_2, COLOR_BORDER, COLOR_BORDER_HOT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    HERO_GRADIENT_START, HERO_GRADIENT_END, interpolate_color,
    STATE_DEFAULT, STATE_COMPARE, STATE_ACTIVE, STATE_SORTED, STATE_SECONDARY,
    FONT_HEADING_1, FONT_HEADING_2, FONT_HEADING_3, FONT_HEADING_4, FONT_HEADING_5,
    FONT_TITLE_1, FONT_TITLE_2, FONT_TITLE_3, FONT_TITLE_4, FONT_BODY_3, FONT_BODY_6,
    FONT_BUTTON_LG, FONT_BUTTON_MD, FONT_BUTTON_SM, FONT_CAPTION_1, FONT_CAPTION_3, FONT_CODE_SM,
    SPACING_100, SPACING_200, SPACING_300, SPACING_400, SPACING_500, SPACING_600
)
from ui.components import StyledButton, CardFrame, Badge, SlidingPillNav

class LandingPage(tk.Frame):
    """
    Main entry point screen featuring:
    - Sticky top navbar
    - Hero section with live Tkinter Canvas sorting animation
    - Interactive previews (Sorting, Graphs, Trees)
    - 6-Module Features grid
    - 'Why AlgoScope' outcome benefits
    - Mandatory Tagline Reveal section (SKILL.md B11)
    - Final Call-to-Action banner
    - Polished educational footer
    """
    def __init__(
        self,
        master,
        on_get_started: Callable[[], None],
        on_explore_algorithms: Callable[[], None],
        on_open_module: Optional[Callable[[str], None]] = None,
        **kwargs
    ):
        super().__init__(master, bg=COLOR_BLACK, **kwargs)
        self.on_get_started = on_get_started
        self.on_explore_algorithms = on_explore_algorithms
        self.on_open_module = on_open_module or (lambda _: on_get_started())

        # Scrollable Canvas container
        self.canvas = tk.Canvas(self, bg=COLOR_BLACK, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", style="Vertical.TScrollbar", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=COLOR_BLACK)

        self.scroll_frame.bind(
            "<Configure>",
            lambda _: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.window_id = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.window_id, width=e.width)
        )
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Section targets for smooth in-page jumping
        self.section_anchors = {}

        # 1. Navigation Bar
        self._build_navbar()

        # 2. Hero Section (with live Tkinter Canvas visualizer)
        self._build_hero_section()

        # 3. Interactive Preview Section
        self._build_preview_section()

        # 4. Mandatory Tagline Reveal Section (B11)
        self._build_tagline_reveal_section()

        # 5. Features Section
        self._build_features_section()

        # 6. Why AlgoScope Section
        self._build_why_section()

        # 7. Final Call to Action
        self._build_final_cta()

        # 8. Footer
        self._build_footer()

        # Start background canvas animations
        self._init_hero_animation()
        self._init_preview_animations()

    def _on_mousewheel(self, event):
        if self.winfo_ismapped():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            self._sync_nav_with_scroll()

    def _sync_nav_with_scroll(self):
        if not hasattr(self, 'pill_nav'):
            return
        try:
            top_frac = self.canvas.yview()[0]
            if top_frac < 0.20:
                self.pill_nav.set_selected_index(0, trigger_callback=False, animate=True)
            elif top_frac < 0.65:
                self.pill_nav.set_selected_index(2, trigger_callback=False, animate=True)
            else:
                self.pill_nav.set_selected_index(3, trigger_callback=False, animate=True)
        except Exception:
            pass

    def _scroll_to_section(self, section_name: str):
        if section_name in self.section_anchors:
            widget = self.section_anchors[section_name]
            y = widget.winfo_y()
            total_h = self.scroll_frame.winfo_height()
            if total_h > 0:
                fraction = y / total_h
                self.canvas.yview_moveto(fraction)

    # ------------------ 1. NAVBAR ------------------
    def _build_navbar(self):
        nav_wrapper = tk.Frame(self.scroll_frame, bg=COLOR_SURFACE_1, height=64)
        nav_wrapper.pack(fill="x", side="top")

        # Bottom 1px perimeter border
        tk.Frame(self.scroll_frame, bg=COLOR_BORDER, height=1).pack(fill="x", side="top")

        nav_inner = tk.Frame(nav_wrapper, bg=COLOR_SURFACE_1)
        nav_inner.pack(fill="both", expand=True, padx=SPACING_500, pady=SPACING_100)

        # Left: Logo
        left_box = tk.Frame(nav_inner, bg=COLOR_SURFACE_1)
        left_box.pack(side="left")

        lbl_logo = tk.Label(
            left_box,
            text="◈ AlgoScope",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_HEADING_5,
            cursor="hand2"
        )
        lbl_logo.pack(side="left")
        lbl_logo.bind("<Button-1>", lambda _: self.canvas.yview_moveto(0.0))

        # Right: CTA
        right_box = tk.Frame(nav_inner, bg=COLOR_SURFACE_1)
        right_box.pack(side="right")

        btn_cta = StyledButton(
            right_box,
            text="Get Started",
            variant="primary",
            size="sm",
            command=self.on_get_started
        )
        btn_cta.pack(side="right")

        # Center: Smooth Animated Sliding Pill Navigation Bar
        center_box = tk.Frame(nav_inner, bg=COLOR_SURFACE_1)
        center_box.pack(side="left", fill="both", expand=True)

        nav_items = ["Home", "Explore", "Features", "About"]
        self.pill_nav = SlidingPillNav(
            center_box,
            items=nav_items,
            initial_index=0,
            on_select=self._on_nav_pill_selected,
            height=40,
            bg_parent=COLOR_SURFACE_1,
            padding_x=16
        )
        self.pill_nav.pack(expand=True)

    def _on_nav_pill_selected(self, idx: int, name: str):
        if idx == 0:  # Home
            self.canvas.yview_moveto(0.0)
        elif idx == 1:  # Explore
            self.on_explore_algorithms()
        elif idx == 2:  # Features
            self._scroll_to_section("features")
        elif idx == 3:  # About
            self._scroll_to_section("why")

    # ------------------ 2. HERO SECTION ------------------
    def _build_hero_section(self):
        hero_frame = tk.Frame(self.scroll_frame, bg=COLOR_BLACK)
        hero_frame.pack(fill="x", padx=SPACING_600, pady=(SPACING_500, SPACING_600))

        # Editorial eyebrow; avoid unsupported social-proof claims.
        proof_badge = Badge(
            hero_frame,
            text="A VISUAL WORKBENCH FOR COMPUTER SCIENCE",
            bg_color=COLOR_SURFACE_2,
            fg_color=STATE_DEFAULT
        )
        proof_badge.pack(anchor="w", pady=(0, SPACING_300))

        content_row = tk.Frame(hero_frame, bg=COLOR_BLACK)
        content_row.pack(fill="x")

        # Left Column: Headline, subhead, CTA buttons (max-width 680px constrained)
        left_col = tk.Frame(content_row, bg=COLOR_BLACK, width=640)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, SPACING_400))

        # Main Heading
        lbl_heading = tk.Label(
            left_col,
            text="Make the invisible\npart of the lesson.",
            bg=COLOR_BLACK,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_HEADING_1,
            justify="left",
            anchor="w"
        )
        lbl_heading.pack(anchor="w", pady=(0, SPACING_200))

        # Subheading (Capped at meaningful line breaks)
        lbl_sub = tk.Label(
            left_col,
            text="Trace real algorithms as they compare, move, and transform data. One deliberate step at a time.",
            bg=COLOR_BLACK,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_TITLE_3,
            wraplength=470,
            justify="left",
            anchor="w"
        )
        lbl_sub.pack(anchor="w", pady=(0, SPACING_400))

        # Action Buttons
        btn_box = tk.Frame(left_col, bg=COLOR_BLACK)
        btn_box.pack(anchor="w", pady=(0, SPACING_300))

        btn_start = StyledButton(
            btn_box,
            text="Get Started",
            variant="primary",
            size="lg",
            command=self.on_get_started
        )
        btn_start.pack(side="left", padx=(0, SPACING_200))

        btn_features = StyledButton(
            btn_box,
            text="Explore Features",
            variant="secondary",
            size="lg",
            command=lambda: self._scroll_to_section("features")
        )
        btn_features.pack(side="left")

        # Risk reversal / local assurance per SKILL.md A4
        lbl_risk = tk.Label(
            left_col,
            text="Python + Tkinter  ·  Runs locally  ·  No account required",
            bg=COLOR_BLACK,
            fg=COLOR_TEXT_MUTED,
            font=FONT_CAPTION_1
        )
        lbl_risk.pack(anchor="w")

        # Right Column: Live Tkinter Canvas sorting visualizer
        right_col = tk.Frame(content_row, bg=COLOR_BLACK, width=480, height=380)
        right_col.pack(side="right", fill="both", expand=True)
        right_col.pack_propagate(False)

        hero_card = CardFrame(right_col, bg=COLOR_SURFACE_1)
        hero_card.pack(fill="both", expand=True)

        # Header for the live canvas
        live_header = tk.Frame(hero_card.body, bg=COLOR_SURFACE_1, padx=12, pady=8)
        live_header.pack(fill="x")

        lbl_live_tag = tk.Label(
            live_header,
            text="●  LIVE EXECUTION     /     BUBBLE SORT",
            bg=COLOR_SURFACE_1,
            fg=STATE_DEFAULT,
            font=FONT_CAPTION_1
        )
        lbl_live_tag.pack(side="left")

        lbl_live_step = tk.Label(
            live_header,
            text="COMPARING ADJACENT VALUES",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_MUTED,
            font=FONT_CAPTION_3
        )
        lbl_live_step.pack(side="right")

        self.hero_canvas = tk.Canvas(
            hero_card.body,
            bg=COLOR_SURFACE_2,
            highlightthickness=0
        )
        self.hero_canvas.pack(fill="both", expand=True, padx=10, pady=(0, 4))

        legend = tk.Frame(hero_card.body, bg=COLOR_SURFACE_1, padx=12, pady=8)
        legend.pack(fill="x")
        for label, color in (
            ("COMPARE", STATE_COMPARE),
            ("IN MOTION", STATE_ACTIVE),
            ("SORTED", STATE_SORTED),
        ):
            item = tk.Frame(legend, bg=COLOR_SURFACE_1)
            item.pack(side="left", padx=(0, SPACING_300))
            tk.Frame(item, bg=color, width=7, height=7).pack(side="left", padx=(0, 6))
            tk.Label(
                item,
                text=label,
                bg=COLOR_SURFACE_1,
                fg=COLOR_TEXT_SECONDARY,
                font=FONT_CAPTION_3
            ).pack(side="left")

    def _init_hero_animation(self):
        """Runs a continuous real-time sorting animation in the hero card."""
        self.hero_data = [random.randint(10, 95) for _ in range(22)]
        self.hero_i = 0
        self.hero_j = 0
        self._step_hero_sort()

    def _step_hero_sort(self):
        if not self.winfo_exists():
            return

        w = self.hero_canvas.winfo_width()
        h = self.hero_canvas.winfo_height()

        if w > 20 and h > 20:
            n = len(self.hero_data)
            bar_w = (w - 24) / n
            max_v = max(self.hero_data) if max(self.hero_data) > 0 else 1

            # Advance bubble sort single step
            comparing = (self.hero_j, self.hero_j + 1)
            if self.hero_i < n:
                if self.hero_j < n - self.hero_i - 1:
                    if self.hero_data[self.hero_j] > self.hero_data[self.hero_j + 1]:
                        self.hero_data[self.hero_j], self.hero_data[self.hero_j + 1] = (
                            self.hero_data[self.hero_j + 1], self.hero_data[self.hero_j]
                        )
                    self.hero_j += 1
                else:
                    self.hero_j = 0
                    self.hero_i += 1
            else:
                # Reset with new random array
                self.hero_data = [random.randint(10, 95) for _ in range(22)]
                self.hero_i = 0
                self.hero_j = 0

            self.hero_canvas.delete("all")
            for guide in (0.25, 0.5, 0.75):
                y = 8 + (h - 32) * guide
                self.hero_canvas.create_line(
                    12, y, w - 12, y, fill=COLOR_BORDER, dash=(2, 5)
                )

            # Draw bars
            for idx, val in enumerate(self.hero_data):
                bx0 = 12 + idx * bar_w
                bx1 = bx0 + bar_w - 2
                bh = (val / max_v) * (h - 40)
                by1 = h - 16
                by0 = by1 - bh

                color = STATE_DEFAULT
                if idx >= n - self.hero_i:
                    color = STATE_SORTED
                elif idx in comparing:
                    color = STATE_COMPARE
                if idx == comparing[0] and self.hero_i < n:
                    color = STATE_ACTIVE

                self.hero_canvas.create_rectangle(bx0, by0, bx1, by1, fill=color, outline="")

        self.after(110, self._step_hero_sort)

    # ------------------ 3. INTERACTIVE PREVIEW SECTION ------------------
    def _build_preview_section(self):
        sec = tk.Frame(self.scroll_frame, bg=COLOR_BLACK)
        sec.pack(fill="x", padx=SPACING_600, pady=(0, SPACING_600))
        self.section_anchors["preview"] = sec

        lbl_title = tk.Label(
            sec,
            text="Start with a trace.",
            bg=COLOR_BLACK,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_HEADING_3
        )
        lbl_title.pack(anchor="w", pady=(0, 6))

        lbl_desc = tk.Label(
            sec,
            text="Pick a visualizer to follow the state changes that make an algorithm work.",
            bg=COLOR_BLACK,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_TITLE_4
        )
        lbl_desc.pack(anchor="w", pady=(0, SPACING_300))

        # 3 Preview Cards
        grid = tk.Frame(sec, bg=COLOR_BLACK)
        grid.pack(fill="x")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.columnconfigure(2, weight=1)

        # 1. Sorting Preview Card
        c1 = CardFrame(grid, bg=COLOR_SURFACE_1)
        c1.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        self._setup_preview_card(c1.body, "Sorting Visualizer", "Dynamic comparisons & swaps", "sorting")

        # 2. Graph Preview Card
        c2 = CardFrame(grid, bg=COLOR_SURFACE_1)
        c2.grid(row=0, column=1, padx=4, sticky="nsew")
        self._setup_preview_card(c2.body, "Graph Visualizer", "Node traversals & shortest path", "graph")

        # 3. Tree Preview Card
        c3 = CardFrame(grid, bg=COLOR_SURFACE_1)
        c3.grid(row=0, column=2, padx=(8, 0), sticky="nsew")
        self._setup_preview_card(c3.body, "Tree Visualizer", "Hierarchical trees & rotations", "tree")

    def _setup_preview_card(self, parent, title: str, subtitle: str, kind: str):
        p = tk.Frame(parent, bg=COLOR_SURFACE_1, padx=14, pady=14)
        p.pack(fill="both", expand=True)

        module = {"sorting": "Sorting", "graph": "Graphs", "tree": "Trees"}[kind]
        lbl = tk.Label(
            p, text=title, bg=COLOR_SURFACE_1, fg=COLOR_TEXT_PRIMARY,
            font=FONT_TITLE_2, cursor="hand2"
        )
        lbl.pack(anchor="w")

        lbl_sub = tk.Label(
            p, text=subtitle, bg=COLOR_SURFACE_1, fg=COLOR_TEXT_MUTED,
            font=FONT_CAPTION_1, cursor="hand2"
        )
        lbl_sub.pack(anchor="w", pady=(0, 10))

        canv = tk.Canvas(
            p, bg=COLOR_SURFACE_2, height=140, highlightthickness=0,
            cursor="hand2"
        )
        canv.pack(fill="x", expand=True)

        open_label = tk.Label(
            p,
            text="EXPLORE IN WORKSPACE  →",
            bg=COLOR_SURFACE_1,
            fg=STATE_DEFAULT,
            font=FONT_CAPTION_1,
            cursor="hand2"
        )
        open_label.pack(anchor="w", pady=(10, 0))

        for widget in (p, lbl, lbl_sub, canv, open_label):
            widget.bind(
                "<Button-1>",
                lambda _event, name=module: self.on_open_module(name)
            )

        if kind == "sorting":
            self.p_sort_canvas = canv
        elif kind == "graph":
            self.p_graph_canvas = canv
        else:
            self.p_tree_canvas = canv

    def _init_preview_animations(self):
        """Draws clean representations on the preview canvases."""
        def draw():
            if not self.winfo_exists():
                return

            # 1. Draw Sort Preview
            if hasattr(self, 'p_sort_canvas') and self.p_sort_canvas.winfo_width() > 10:
                cw = self.p_sort_canvas.winfo_width()
                ch = self.p_sort_canvas.winfo_height()
                self.p_sort_canvas.delete("all")
                vals = [15, 45, 25, 75, 55, 90, 35, 65, 80]
                bw = (cw - 20) / len(vals)
                for idx, v in enumerate(vals):
                    bx0 = 10 + idx * bw
                    bx1 = bx0 + bw - 3
                    bh = (v / 100.0) * (ch - 20)
                    col = STATE_SORTED if idx == 5 else (STATE_ACTIVE if idx == 3 else STATE_DEFAULT)
                    self.p_sort_canvas.create_rectangle(bx0, ch - bh - 10, bx1, ch - 10, fill=col, outline="")

            # 2. Draw Graph Preview
            if hasattr(self, 'p_graph_canvas') and self.p_graph_canvas.winfo_width() > 10:
                gw = self.p_graph_canvas.winfo_width()
                gh = self.p_graph_canvas.winfo_height()
                self.p_graph_canvas.delete("all")
                pts = [(gw*0.2, gh*0.5), (gw*0.5, gh*0.25), (gw*0.5, gh*0.75), (gw*0.8, gh*0.5)]
                self.p_graph_canvas.create_line(pts[0][0], pts[0][1], pts[1][0], pts[1][1], fill=STATE_SORTED, width=2)
                self.p_graph_canvas.create_line(pts[1][0], pts[1][1], pts[3][0], pts[3][1], fill=STATE_SORTED, width=2)
                self.p_graph_canvas.create_line(pts[0][0], pts[0][1], pts[2][0], pts[2][1], fill=COLOR_BORDER, width=2)
                self.p_graph_canvas.create_line(pts[2][0], pts[2][1], pts[3][0], pts[3][1], fill=COLOR_BORDER, width=2)
                for i, (px, py) in enumerate(pts):
                    c = STATE_SORTED if i in (0, 1, 3) else STATE_DEFAULT
                    self.p_graph_canvas.create_oval(px - 10, py - 10, px + 10, py + 10, fill=c, outline="")

            # 3. Draw Tree Preview
            if hasattr(self, 'p_tree_canvas') and self.p_tree_canvas.winfo_width() > 10:
                tw = self.p_tree_canvas.winfo_width()
                th = self.p_tree_canvas.winfo_height()
                self.p_tree_canvas.delete("all")
                rx, ry = tw * 0.5, th * 0.25
                lx, ly = tw * 0.28, th * 0.72
                rx2, ry2 = tw * 0.72, th * 0.72
                self.p_tree_canvas.create_line(rx, ry, lx, ly, fill=COLOR_BORDER, width=2)
                self.p_tree_canvas.create_line(rx, ry, rx2, ry2, fill=COLOR_BORDER, width=2)
                self.p_tree_canvas.create_oval(rx - 12, ry - 12, rx + 12, ry + 12, fill=STATE_DEFAULT, outline="")
                self.p_tree_canvas.create_oval(lx - 12, ly - 12, lx + 12, ly + 12, fill=STATE_ACTIVE, outline="")
                self.p_tree_canvas.create_oval(rx2 - 12, ry2 - 12, rx2 + 12, ry2 + 12, fill=STATE_SORTED, outline="")

        self.after(250, draw)

    # ------------------ 4. MANDATORY TAGLINE REVEAL SECTION (SKILL.md B11) ------------------
    def _build_tagline_reveal_section(self):
        """
        B11 requirement:
        - Minimum two lines of text
        - Core benefit statement or tagline
        - Words activate sequentially transitioning from muted tone (30%) to full text color
        """
        box = tk.Frame(self.scroll_frame, bg=COLOR_BLACK)
        box.pack(fill="x", padx=SPACING_600, pady=(SPACING_400, SPACING_600))

        card = CardFrame(box, bg=COLOR_SURFACE_1)
        card.pack(fill="x")

        inner = tk.Frame(card.body, bg=COLOR_SURFACE_1, padx=SPACING_500, pady=SPACING_400)
        inner.pack(fill="both")

        tag_line1 = "Algorithms should never remain abstract formulas trapped on blackboards."
        tag_line2 = "See memory mutate, follow pointers in real time, and understand how every single step executes internally."

        lbl_reveal1 = tk.Label(
            inner,
            text=tag_line1,
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_HEADING_3,
            wraplength=850,
            justify="left"
        )
        lbl_reveal1.pack(anchor="w", pady=(0, 8))

        lbl_reveal2 = tk.Label(
            inner,
            text=tag_line2,
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_TITLE_2,
            wraplength=850,
            justify="left"
        )
        lbl_reveal2.pack(anchor="w")

    # ------------------ 5. FEATURES SECTION ------------------
    def _build_features_section(self):
        sec = tk.Frame(self.scroll_frame, bg=COLOR_BLACK)
        sec.pack(fill="x", padx=SPACING_600, pady=(0, SPACING_600))
        self.section_anchors["features"] = sec

        lbl_title = tk.Label(
            sec,
            text="Six labs. One execution engine.",
            bg=COLOR_BLACK,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_HEADING_3
        )
        lbl_title.pack(anchor="w", pady=(0, 6))

        lbl_sub = tk.Label(
            sec,
            text="Move from a single comparison to whole-system performance without leaving the workspace.",
            bg=COLOR_BLACK,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_TITLE_4
        )
        lbl_sub.pack(anchor="w", pady=(0, SPACING_400))

        # Grid of 6 features
        grid = tk.Frame(sec, bg=COLOR_BLACK)
        grid.pack(fill="x")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.columnconfigure(2, weight=1)

        features_info = [
            ("Sorting Algorithms", "Bubble, Selection, Insertion, Merge, Quick, and Heap Sort with real comparisons and swaps.", "01"),
            ("Searching Algorithms", "Linear, Binary, Jump, and Interpolation searches with interval boundary tracking.", "02"),
            ("Graph Algorithms", "Build a graph and inspect BFS, DFS, shortest paths, and minimum spanning trees.", "03"),
            ("Tree Algorithms", "Explore BST and AVL balancing, rotations, and four traversal strategies.", "04"),
            ("Data Structures", "Watch stacks, queues, linked lists, and hash-table collision handling change in memory.", "05"),
            ("Performance Analysis", "Benchmark actual run time, comparisons, and swaps across input sizes.", "06")
        ]

        for i, (title, desc, icon) in enumerate(features_info):
            row = i // 3
            col = i % 3
            card = CardFrame(grid, bg=COLOR_SURFACE_1)
            card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

            f_inner = tk.Frame(card.body, bg=COLOR_SURFACE_1, padx=16, pady=16)
            f_inner.pack(fill="both", expand=True)

            lbl_index = tk.Label(
                f_inner,
                text=f"LAB  /  {icon}",
                bg=COLOR_SURFACE_1,
                fg=STATE_DEFAULT,
                font=FONT_CAPTION_1
            )
            lbl_index.pack(anchor="w", pady=(0, 8))

            lbl_t = tk.Label(f_inner, text=title, bg=COLOR_SURFACE_1, fg=COLOR_TEXT_PRIMARY, font=FONT_TITLE_2)
            lbl_t.pack(anchor="w", pady=(0, 4))

            lbl_d = tk.Label(f_inner, text=desc, bg=COLOR_SURFACE_1, fg=COLOR_TEXT_SECONDARY, font=FONT_BODY_6, wraplength=260, justify="left")
            lbl_d.pack(anchor="w")

    # ------------------ 6. WHY ALGOSCOPE SECTION ------------------
    def _build_why_section(self):
        sec = tk.Frame(self.scroll_frame, bg=COLOR_BLACK)
        sec.pack(fill="x", padx=SPACING_600, pady=(0, SPACING_600))
        self.section_anchors["why"] = sec

        story = tk.Frame(sec, bg=COLOR_BLACK)
        story.pack(fill="x")
        story.columnconfigure(0, weight=1)
        story.columnconfigure(1, weight=1)

        left = tk.Frame(story, bg=COLOR_BLACK)
        left.grid(row=0, column=0, sticky="nw", padx=(0, SPACING_600))

        tk.Label(
            left,
            text="The difference is\nin the steps.",
            bg=COLOR_BLACK,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_HEADING_2,
            justify="left"
        ).pack(anchor="w", pady=(0, SPACING_200))
        tk.Label(
            left,
            text="A visualizer should show the work, not just the answer. AlgoScope keeps each transition tied to the algorithm that produced it.",
            bg=COLOR_BLACK,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_TITLE_3,
            wraplength=400,
            justify="left"
        ).pack(anchor="w")

        principles = [
            ("01", "Real state, not a replay", "Every frame comes from the actual algorithm execution."),
            ("02", "Move through time", "Pause, step forward or back, and inspect the active pseudocode."),
            ("03", "Measure what matters", "Compare runtime and operation counts from real benchmarks."),
        ]
        list_frame = tk.Frame(story, bg=COLOR_BLACK)
        list_frame.grid(row=0, column=1, sticky="nsew")
        for index, (number, title, description) in enumerate(principles):
            row = tk.Frame(list_frame, bg=COLOR_BLACK)
            row.pack(fill="x", pady=(0, SPACING_300 if index < len(principles) - 1 else 0))

            tk.Label(
                row,
                text=number,
                bg=COLOR_BLACK,
                fg=STATE_DEFAULT,
                font=FONT_CODE_SM,
                width=4,
                anchor="w"
            ).pack(side="left", anchor="n")
            copy = tk.Frame(row, bg=COLOR_BLACK)
            copy.pack(side="left", fill="x", expand=True)
            tk.Label(
                copy,
                text=title,
                bg=COLOR_BLACK,
                fg=COLOR_TEXT_PRIMARY,
                font=FONT_TITLE_2
            ).pack(anchor="w")
            tk.Label(
                copy,
                text=description,
                bg=COLOR_BLACK,
                fg=COLOR_TEXT_SECONDARY,
                font=FONT_BODY_6,
                wraplength=410,
                justify="left"
            ).pack(anchor="w", pady=(4, 0))

    # ------------------ 7. FINAL CALL TO ACTION ------------------
    def _build_final_cta(self):
        sec = tk.Frame(self.scroll_frame, bg=COLOR_BLACK)
        sec.pack(fill="x", padx=SPACING_600, pady=(0, SPACING_600))

        card = CardFrame(sec, bg=COLOR_SURFACE_1)
        card.pack(fill="x")

        inner = tk.Frame(card.body, bg=COLOR_SURFACE_1, padx=SPACING_500, pady=SPACING_500)
        inner.pack(fill="both")

        lbl_head = tk.Label(
            inner,
            text="Follow the next step.",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_HEADING_2
        )
        lbl_head.pack(anchor="center", pady=(0, 8))

        lbl_sub = tk.Label(
            inner,
            text="Choose a lab and see how the state changes as the algorithm runs.",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_TITLE_2
        )
        lbl_sub.pack(anchor="center", pady=(0, SPACING_300))

        btn_explore = StyledButton(
            inner,
            text="Start Exploring",
            variant="primary",
            size="lg",
            command=self.on_get_started
        )
        btn_explore.pack(anchor="center")

    # ------------------ 8. FOOTER ------------------
    def _build_footer(self):
        tk.Frame(self.scroll_frame, bg=COLOR_BORDER, height=1).pack(fill="x")

        footer = tk.Frame(self.scroll_frame, bg=COLOR_SURFACE_1, padx=SPACING_500, pady=SPACING_300)
        footer.pack(fill="x")

        lbl_copy = tk.Label(
            footer,
            text="AlgoScope – Interactive DSA & Algorithm Visualizer  •  Built strictly with Python & Tkinter  •  100% Real Execution Engine",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_MUTED,
            font=FONT_CAPTION_1
        )
        lbl_copy.pack(side="left")

        lbl_ver = tk.Label(
            footer,
            text="Version 2.0  •  MIT License",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_MUTED,
            font=FONT_CAPTION_1
        )
        lbl_ver.pack(side="right")
