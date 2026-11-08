"""
AlgoScope Sidebar Component
Sidebar navigation adhering strictly to SKILL.md flat dark design tokens.
"""

import tkinter as tk
from typing import Callable, Optional
from core.theme import (
    COLOR_BLACK, COLOR_SURFACE_1, COLOR_SURFACE_2, COLOR_BORDER, COLOR_BORDER_HOT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    FONT_TITLE_2, FONT_TITLE_4, FONT_BUTTON_SM, FONT_CAPTION_1, FONT_HEADING_6,
    SPACING_75, SPACING_100, SPACING_200
)
from ui.components import CardFrame

class Sidebar(tk.Frame):
    """Sidebar containing AlgoScope branding, navigation links, and summary stats."""
    def __init__(
        self,
        master,
        on_navigate: Callable[[str], None],
        on_go_home: Callable[[], None],
        active_route: str = "Dashboard",
        **kwargs
    ):
        super().__init__(master, bg=COLOR_SURFACE_1, width=240, **kwargs)
        self.pack_propagate(False)
        self.on_navigate = on_navigate
        self.on_go_home = on_go_home
        self.active_route = active_route
        self.nav_buttons: dict[str, tk.Label] = {}

        self._build_sidebar()

    def _build_sidebar(self):
        # 1. Branding Header
        brand_box = tk.Frame(self, bg=COLOR_SURFACE_1, height=64)
        brand_box.pack(fill="x", padx=SPACING_200, pady=SPACING_200)

        lbl_logo = tk.Label(
            brand_box,
            text="◈ AlgoScope",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_HEADING_6,
            cursor="hand2"
        )
        lbl_logo.pack(anchor="w")
        lbl_logo.bind("<Button-1>", lambda _: self.on_go_home())

        lbl_tag = tk.Label(
            brand_box,
            text="DSA Visualizer & Analyzer",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_MUTED,
            font=FONT_CAPTION_1
        )
        lbl_tag.pack(anchor="w", pady=(2, 0))

        # Divider
        tk.Frame(self, bg=COLOR_BORDER, height=1).pack(fill="x", pady=(0, SPACING_100))

        # 2. Main Navigation Links
        nav_container = tk.Frame(self, bg=COLOR_SURFACE_1)
        nav_container.pack(fill="x", padx=SPACING_100)

        nav_items = [
            ("Dashboard", "▦ Overview"),
            ("Sorting", "⇅ Sorting"),
            ("Searching", "⌕ Searching"),
            ("Graphs", "☊ Graphs"),
            ("Trees", "⚯ Trees"),
            ("Data Structures", "☵ Data Structures"),
            ("Performance", "⚡ Performance")
        ]

        for route_id, label in nav_items:
            btn = self._create_nav_item(nav_container, route_id, label)
            btn.pack(fill="x", pady=2)

        # Divider
        tk.Frame(self, bg=COLOR_BORDER, height=1).pack(fill="x", pady=SPACING_200)

        # 3. Quick Stats Card at bottom
        stats_card = CardFrame(self, bg=COLOR_SURFACE_2)
        stats_card.pack(side="bottom", fill="x", padx=SPACING_100, pady=SPACING_200)

        p = stats_card.body
        lbl_st_title = tk.Label(p, text="Learning Metrics", bg=COLOR_SURFACE_2, fg=COLOR_TEXT_PRIMARY, font=FONT_TITLE_4)
        lbl_st_title.pack(anchor="w", padx=10, pady=(8, 4))

        def add_stat_row(label, val):
            row = tk.Frame(p, bg=COLOR_SURFACE_2)
            row.pack(fill="x", padx=10, pady=2)
            tk.Label(row, text=label, bg=COLOR_SURFACE_2, fg=COLOR_TEXT_SECONDARY, font=FONT_CAPTION_1).pack(side="left")
            tk.Label(row, text=val, bg=COLOR_SURFACE_2, fg=COLOR_TEXT_PRIMARY, font=FONT_CAPTION_1).pack(side="right")

        add_stat_row("Modules:", "6 Active")
        add_stat_row("Algorithms:", "24 Total")
        add_stat_row("Execution:", "100% Real")
        add_stat_row("Engine:", "Local Tkinter")

        # Home button at very bottom of sidebar
        btn_home = tk.Label(
            self,
            text="⌂ Return to Landing Page",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BUTTON_SM,
            cursor="hand2",
            pady=8
        )
        btn_home.pack(side="bottom", fill="x", padx=SPACING_100, pady=(0, 6))
        btn_home.bind("<Button-1>", lambda _: self.on_go_home())
        btn_home.bind("<Enter>", lambda _: btn_home.config(fg=COLOR_TEXT_PRIMARY))
        btn_home.bind("<Leave>", lambda _: btn_home.config(fg=COLOR_TEXT_SECONDARY))

    def _create_nav_item(self, parent, route_id: str, label: str) -> tk.Frame:
        f = tk.Frame(parent, bg=COLOR_SURFACE_1, cursor="hand2")

        is_active = (self.active_route == route_id)
        bg_col = COLOR_SURFACE_2 if is_active else COLOR_SURFACE_1
        fg_col = COLOR_TEXT_PRIMARY if is_active else COLOR_TEXT_SECONDARY

        lbl = tk.Label(
            f,
            text=f"  {label}",
            bg=bg_col,
            fg=fg_col,
            font=FONT_TITLE_4,
            anchor="w",
            padx=10,
            pady=7
        )
        lbl.pack(fill="both", expand=True)

        self.nav_buttons[route_id] = lbl

        def on_click(_):
            self.set_active_route(route_id)
            self.on_navigate(route_id)

        def on_enter(_):
            if self.active_route != route_id:
                lbl.config(bg="#222222", fg=COLOR_TEXT_PRIMARY)

        def on_leave(_):
            if self.active_route != route_id:
                lbl.config(bg=COLOR_SURFACE_1, fg=COLOR_TEXT_SECONDARY)

        f.bind("<Button-1>", on_click)
        lbl.bind("<Button-1>", on_click)
        lbl.bind("<Enter>", on_enter)
        lbl.bind("<Leave>", on_leave)

        return f

    def set_active_route(self, route_id: str):
        self.active_route = route_id
        for r_id, lbl in self.nav_buttons.items():
            if r_id == route_id:
                lbl.config(bg=COLOR_SURFACE_2, fg=COLOR_TEXT_PRIMARY)
            else:
                lbl.config(bg=COLOR_SURFACE_1, fg=COLOR_TEXT_SECONDARY)

