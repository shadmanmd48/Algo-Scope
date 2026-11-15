"""
AlgoScope Sidebar Component
Sidebar navigation adhering strictly to ProFinance modern light design tokens.
Featuring curved navigation buttons with electric lime theme color borders.
"""

import tkinter as tk
from typing import Callable, Optional
from core.theme import (
    COLOR_CONTAINER, COLOR_SURFACE_1, COLOR_SURFACE_2, COLOR_BORDER, COLOR_BORDER_HOT,
    COLOR_LIME, COLOR_INK_BLACK,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    FONT_TITLE_2, FONT_TITLE_4, FONT_BUTTON_SM, FONT_CAPTION_1, FONT_HEADING_6,
    SPACING_50, SPACING_75, SPACING_100, SPACING_200
)
from ui.components import StyledButton

class SidebarNavItem(tk.Canvas):
    """
    Curved navigation button with subtle electric lime theme border:
    - Smooth curved edges (radius 10px, height 38px)
    - Active state: Solid black fill (#000000), white text, and theme border (#DFFF35)
    - Hover state: Soft surface (#F4F4F5), dark text, and theme border (#DFFF35)
    - Idle state: Clean white (#FFFFFF), secondary text (#52525B), subtle border (#E4E4E7)
    """
    def __init__(
        self,
        master,
        label: str,
        route_id: str,
        on_click: Callable[[str], None],
        is_active: bool = False,
        radius: int = 10,
        **kwargs
    ):
        super().__init__(
            master,
            height=38,
            bg="#FFFFFF",
            highlightthickness=0,
            cursor="hand2",
            **kwargs
        )
        self.label = label
        self.route_id = route_id
        self.on_click = on_click
        self.is_active = is_active
        self.is_hover = False
        self.radius = radius

        self.bind("<Configure>", lambda _: self.render())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def set_active(self, active: bool):
        self.is_active = active
        self.render()

    def _on_enter(self, _):
        if not self.is_active:
            self.is_hover = True
            self.render()

    def _on_leave(self, _):
        if not self.is_active:
            self.is_hover = False
            self.render()

    def _on_click(self, _):
        self.on_click(self.route_id)

    def render(self):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 10 or h < 10:
            return

        r = self.radius

        if self.is_active:
            bg = "#000000"
            fg = "#FFFFFF"
            border = COLOR_LIME  # Electric lime theme color border!
            border_w = 1.5
            font = ("Segoe UI", 10, "bold")
        elif self.is_hover:
            bg = "#F4F4F5"
            fg = "#000000"
            border = COLOR_LIME  # Delicate lime border on hover!
            border_w = 1.5
            font = ("Segoe UI", 10, "bold")
        else:
            bg = "#FFFFFF"
            fg = COLOR_TEXT_SECONDARY
            border = "#E4E4E7"
            border_w = 1
            font = FONT_TITLE_4

        # Draw rounded rectangle with curved edges
        x0, y0, x1, y1 = 2, 2, w - 3, h - 3
        self.create_arc(x0, y0, x0 + 2*r, y0 + 2*r, start=90, extent=90, fill=bg, outline="", style="pieslice")
        self.create_arc(x1 - 2*r, y0, x1, y0 + 2*r, start=0, extent=90, fill=bg, outline="", style="pieslice")
        self.create_arc(x1 - 2*r, y1 - 2*r, x1, y1, start=270, extent=90, fill=bg, outline="", style="pieslice")
        self.create_arc(x0, y1 - 2*r, x0 + 2*r, y1, start=180, extent=90, fill=bg, outline="", style="pieslice")
        self.create_rectangle(x0 + r, y0, x1 - r, y1, fill=bg, outline="")
        self.create_rectangle(x0, y0 + r, x1, y1 - r, fill=bg, outline="")

        if border:
            self.create_arc(x0, y0, x0 + 2*r, y0 + 2*r, start=90, extent=90, outline=border, width=border_w, style="arc")
            self.create_arc(x1 - 2*r, y0, x1, y0 + 2*r, start=0, extent=90, outline=border, width=border_w, style="arc")
            self.create_arc(x1 - 2*r, y1 - 2*r, x1, y1, start=270, extent=90, outline=border, width=border_w, style="arc")
            self.create_arc(x0, y1 - 2*r, x0 + 2*r, y1, start=180, extent=90, outline=border, width=border_w, style="arc")
            self.create_line(x0 + r, y0, x1 - r, y0, fill=border, width=border_w)
            self.create_line(x0 + r, y1, x1 - r, y1, fill=border, width=border_w)
            self.create_line(x0, y0 + r, x0, y1 - r, fill=border, width=border_w)
            self.create_line(x1, y0 + r, x1, y1 - r, fill=border, width=border_w)

        # Draw icon & text label aligned to left with comfortable padding
        self.create_text(16, round(h / 2.0), text=self.label, fill=fg, font=font, anchor="w")


class Sidebar(tk.Frame):
    """Sidebar containing AlgoScope branding, navigation links, and quick launches."""
    def __init__(
        self,
        master,
        on_navigate: Callable[[str], None],
        on_go_home: Callable[[], None],
        active_route: str = "Dashboard",
        **kwargs
    ):
        super().__init__(master, bg="#FFFFFF", width=260, highlightthickness=1, highlightbackground=COLOR_BORDER, **kwargs)
        self.pack_propagate(False)
        self.on_navigate = on_navigate
        self.on_go_home = on_go_home
        self.active_route = active_route
        self.nav_buttons: dict[str, SidebarNavItem] = {}

        self._build_sidebar()

    def _build_sidebar(self):
        # 1. Branding Header
        brand_box = tk.Frame(self, bg="#FFFFFF", height=64)
        brand_box.pack(fill="x", padx=SPACING_200, pady=(SPACING_200, SPACING_100))

        brand_row = tk.Frame(brand_box, bg="#FFFFFF", cursor="hand2")
        brand_row.pack(anchor="w")

        lbl_logo = tk.Label(
            brand_row,
            text="AlgoScope",
            bg="#FFFFFF",
            fg=COLOR_INK_BLACK,
            font=("Segoe UI", 16, "bold"),
            cursor="hand2"
        )
        lbl_logo.pack(side="left")

        # Electric lime accent dot
        dot = tk.Canvas(brand_row, width=14, height=14, bg="#FFFFFF", highlightthickness=0)
        dot.pack(side="left", padx=(4, 0))
        dot.create_oval(1, 1, 13, 13, fill=COLOR_LIME, outline="")

        brand_row.bind("<Button-1>", lambda _: self.on_go_home())
        lbl_logo.bind("<Button-1>", lambda _: self.on_go_home())

        lbl_tag = tk.Label(
            brand_box,
            text="DSA Visualizer & Analyzer",
            bg="#FFFFFF",
            fg=COLOR_TEXT_MUTED,
            font=FONT_CAPTION_1
        )
        lbl_tag.pack(anchor="w", pady=(2, 0))

        # Divider
        tk.Frame(self, bg=COLOR_BORDER, height=1).pack(fill="x", pady=(SPACING_100, SPACING_100))

        # 2. Main Navigation Links
        nav_container = tk.Frame(self, bg="#FFFFFF")
        nav_container.pack(fill="x", padx=SPACING_100)

        nav_items = [
            ("Dashboard", "▦  Overview"),
            ("Sorting", "⇅  Sorting Visualizer"),
            ("Searching", "⌕  Searching Visualizer"),
            ("Graphs", "☊  Graph Visualizer"),
            ("Trees", "⚯  Tree Visualizer"),
            ("Data Structures", "☵  Data Structures"),
            ("Performance", "⚡  Performance Analyzer")
        ]

        for route_id, label in nav_items:
            is_act = (self.active_route == route_id)
            btn = SidebarNavItem(
                nav_container,
                label=label,
                route_id=route_id,
                on_click=self._on_item_clicked,
                is_active=is_act,
                radius=10
            )
            btn.pack(fill="x", pady=3)
            self.nav_buttons[route_id] = btn

        # 3. Small Return to Landing Page button in theme color (Electric Lime)
        bottom_box = tk.Frame(self, bg="#FFFFFF")
        bottom_box.pack(side="bottom", fill="x", padx=SPACING_100, pady=SPACING_200)

        # Subtle divider above button
        tk.Frame(bottom_box, bg=COLOR_BORDER, height=1).pack(fill="x", pady=(0, SPACING_100))

        btn_home = StyledButton(
            bottom_box,
            text="⌂ Return to Landing Page",
            variant="accent",  # Electric lime theme color
            size="sm",
            command=self.on_go_home
        )
        btn_home.pack(anchor="center", pady=(4, 0))

    def _on_item_clicked(self, route_id: str):
        self.set_active_route(route_id)
        self.on_navigate(route_id)

    def set_active_route(self, route_id: str):
        self.active_route = route_id
        for r_id, btn in self.nav_buttons.items():
            btn.set_active(r_id == route_id)
