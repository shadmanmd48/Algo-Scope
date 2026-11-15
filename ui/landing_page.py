"""
AlgoScope Landing Page — ProFinance Reference Edition
A modern, conversion-focused desktop landing page built with pure Tkinter and Canvas.
Faithfully recreates the visual layout, composition, and aesthetic of the ProFinance reference:
- Large white rounded outer website container with generous margins
- Minimal, clean top navbar with logo, links, and rounded CTA button
- Large lime-green/yellow hero section with rounded corners (#DFFF35)
- Bold black typography with oversized headlines ("Make ✦ Algorithms Visible.")
- Minimalistic black & white buttons with subtle hover effects
- Floating, overlapping UI panels that extend beyond the hero section boundary
- Real-time animated sorting visualization inside the front interactive card
- Graph visualization with shortest path highlights inside the back dark card
- Spacious "Get the Most Out of Algorithms" features section and about section below
"""

import math
import random
import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Optional

# ProFinance Reference Color Palette (strictly scoped to this Landing Page)
COLOR_PAGE_BG       = "#E8ECEF"   # Soft neutral light gray window backdrop
COLOR_CONTAINER     = "#FFFFFF"   # Large white website container
COLOR_LIME          = "#DFFF35"   # Vibrant electric lime / chartreuse hero surface
COLOR_LIME_HOVER    = "#D2F52C"   # Subtle hover lime
COLOR_INK_BLACK     = "#000000"   # Bold black typography & primary CTA buttons
COLOR_INK_DARK      = "#18181B"   # Primary text / dark card backgrounds
COLOR_INK_MUTED     = "#52525B"   # Secondary copy / subheadings
COLOR_INK_LIGHT     = "#A1A1AA"   # Captions / metadata / borders
COLOR_CARD_BG       = "#FFFFFF"   # Features card surface
COLOR_CARD_LIGHT    = "#F4F4F5"   # Elevated light surface / search bar mockup
COLOR_CARD_DARK     = "#111115"   # Back dark floating UI device card
COLOR_BORDER_SUBTLE = "#E4E4E7"   # Clean 1px perimeter border
COLOR_BORDER_HOVER  = "#000000"   # Hover state border
COLOR_CORAL_BTN     = "#EF4444"   # Coral red reset button
COLOR_ACCENT_GREEN  = "#10B981"   # Emerald green sorted / optimal path highlight
COLOR_ACCENT_BLUE   = "#3B82F6"   # Sky blue default sorting bars
COLOR_ACCENT_AMBER  = "#F59E0B"   # Amber comparison highlight
COLOR_ACCENT_CYAN   = "#06B6D4"   # Cyan source pointer


def draw_smooth_rounded_rect(
    canvas: tk.Canvas,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    radius: float = 24,
    **kwargs
) -> int:
    """
    Draws a precision rounded rectangle on a Tkinter Canvas using double-edge points
    to ensure perfectly straight edges and smooth antialiased corners.
    """
    r = min(radius, abs(x2 - x1) / 2, abs(y2 - y1) / 2)
    points = [
        x1 + r, y1,
        x1 + r, y1,
        x2 - r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1 + r,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


class LandingPage(tk.Frame):
    """
    Main landing screen strictly following the ProFinance reference aesthetic:
    - Large white rounded container centered on light gray backdrop
    - Clean top navigation bar with lime accent
    - Large rounded lime-green hero section (#DFFF35)
    - Bold black headline with 4-point star 'Make ✦ Algorithms Visible.'
    - Floating overlapping UI panels extending past hero boundaries
    - Real-time animated sorting visualization and graph path highlights
    - 'Get the Most Out of Algorithms' features section below
    """
    def __init__(
        self,
        master,
        on_get_started: Callable[[], None],
        on_explore_algorithms: Callable[[], None],
        on_open_module: Optional[Callable[[str], None]] = None,
        **kwargs
    ):
        super().__init__(master, bg=COLOR_PAGE_BG, **kwargs)
        self.on_get_started = on_get_started
        self.on_explore_algorithms = on_explore_algorithms
        self.on_open_module = on_open_module or (lambda _: on_get_started())

        # Section targets for smooth in-page jumping
        self.section_anchors = {}

        # Sorting animation state
        self.hero_sort_data = [24, 78, 45, 92, 18, 63, 85, 34, 56, 99, 12, 68, 41, 88, 30, 74, 52, 95]
        self.hero_sort_i = 0
        self.hero_sort_j = 0
        self.hero_sort_active = True
        self.hero_sort_comps = 0
        self.hero_sort_swaps = 0

        # Primary scrollable Canvas
        self.canvas = tk.Canvas(self, bg=COLOR_PAGE_BG, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=COLOR_PAGE_BG)

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
            lambda e: self._on_canvas_resize(e.width)
        )
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Assemble the page structure
        self._build_page_layout()

        # Start background sorting animation
        self._step_hero_sorting()

    def _on_canvas_resize(self, width: int):
        self.canvas.itemconfig(self.window_id, width=width)
        if hasattr(self, 'site_wrapper'):
            site_w = max(940, width - 48)
            self.site_wrapper.config(width=site_w)
        if hasattr(self, 'hero_canvas'):
            self._redraw_hero_canvas()

    def _on_mousewheel(self, event):
        if self.winfo_ismapped():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _scroll_to_section(self, section_name: str):
        if section_name in self.section_anchors:
            widget = self.section_anchors[section_name]
            self.update_idletasks()
            y = widget.winfo_y()
            total_h = self.scroll_frame.winfo_height()
            if total_h > 0:
                fraction = max(0.0, min(1.0, (y - 30) / total_h))
                self.canvas.yview_moveto(fraction)

    # -------------------------------------------------------------
    # PAGE LAYOUT & CONTAINER
    # -------------------------------------------------------------

    def _build_page_layout(self):
        # Outer framing padding (soft neutral background visible around website container)
        self.outer_box = tk.Frame(self.scroll_frame, bg=COLOR_PAGE_BG, padx=24, pady=24)
        self.outer_box.pack(fill="x", expand=True)

        # Large White Website Container (with crisp rounded appearance and perimeter border)
        self.site_wrapper = tk.Frame(self.outer_box, bg=COLOR_CONTAINER)
        self.site_wrapper.pack(fill="x", expand=True)

        # Top 1px perimeter border
        tk.Frame(self.site_wrapper, bg=COLOR_BORDER_SUBTLE, height=1).pack(fill="x")

        # 1. Navigation Bar
        self._build_navbar()

        # 2. Hero Section with Lime Background & Overlapping Panels
        self._build_hero_section()

        # 3. Features Section ("Get the Most Out of Algorithms")
        self._build_features_section()

        # 4. About / Value Section ("Why AlgoScope")
        self._build_why_section()

        # 5. Final Call-to-Action Banner
        self._build_final_cta()

        # 6. Minimalist Footer
        self._build_footer()

        # Bottom 1px perimeter border
        tk.Frame(self.site_wrapper, bg=COLOR_BORDER_SUBTLE, height=1).pack(fill="x")

    # -------------------------------------------------------------
    # 1. NAVIGATION BAR
    # -------------------------------------------------------------

    def _build_navbar(self):
        nav_frame = tk.Frame(self.site_wrapper, bg=COLOR_CONTAINER, height=72)
        nav_frame.pack(fill="x", padx=36, pady=(16, 8))

        # Left: AlgoScope Logo + Lime Circle Accent (mirrors ProFinance brand)
        left_box = tk.Frame(nav_frame, bg=COLOR_CONTAINER, cursor="hand2")
        left_box.pack(side="left")

        # Logo text
        lbl_brand = tk.Label(
            left_box,
            text="AlgoScope",
            bg=COLOR_CONTAINER,
            fg=COLOR_INK_BLACK,
            font=("Segoe UI", 18, "bold")
        )
        lbl_brand.pack(side="left")

        # Lime Accent Badge (matches yellow circle beside 'Pro Finance')
        lime_dot_frame = tk.Canvas(left_box, width=18, height=18, bg=COLOR_CONTAINER, highlightthickness=0)
        lime_dot_frame.pack(side="left", padx=(6, 0))
        lime_dot_frame.create_oval(2, 2, 16, 16, fill=COLOR_LIME, outline="")

        left_box.bind("<Button-1>", lambda _: self.canvas.yview_moveto(0.0))
        lbl_brand.bind("<Button-1>", lambda _: self.canvas.yview_moveto(0.0))

        # Right CTA Button: Rounded Black Button ("Get Started")
        right_box = tk.Frame(nav_frame, bg=COLOR_CONTAINER)
        right_box.pack(side="right")

        btn_cta = tk.Label(
            right_box,
            text="Get Started",
            bg=COLOR_INK_BLACK,
            fg="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            padx=18,
            pady=8,
            cursor="hand2"
        )
        btn_cta.pack(side="right")
        btn_cta.bind("<Button-1>", lambda _: self.on_get_started())
        btn_cta.bind("<Enter>", lambda _: btn_cta.config(bg="#27272A"))
        btn_cta.bind("<Leave>", lambda _: btn_cta.config(bg=COLOR_INK_BLACK))

        # Sign Up Button
        btn_signup = tk.Label(
            right_box,
            text="Sign Up",
            bg=COLOR_CONTAINER,
            fg=COLOR_INK_BLACK,
            font=("Segoe UI", 11, "bold"),
            padx=16,
            pady=7,
            cursor="hand2",
            highlightthickness=1,
            highlightbackground=COLOR_BORDER_SUBTLE
        )
        btn_signup.pack(side="right", padx=(0, 10))
        btn_signup.bind("<Button-1>", lambda _: self._open_signup_modal())
        btn_signup.bind("<Enter>", lambda _: btn_signup.config(bg=COLOR_CARD_LIGHT))
        btn_signup.bind("<Leave>", lambda _: btn_signup.config(bg=COLOR_CONTAINER))

        # Subtle "Explore" ghost link next to CTA
        btn_explore_link = tk.Label(
            right_box,
            text="Overview",
            bg=COLOR_CONTAINER,
            fg=COLOR_INK_MUTED,
            font=("Segoe UI", 11, "bold"),
            padx=14,
            pady=8,
            cursor="hand2"
        )
        btn_explore_link.pack(side="right", padx=(0, 10))
        btn_explore_link.bind("<Button-1>", lambda _: self.on_explore_algorithms())
        btn_explore_link.bind("<Enter>", lambda _: btn_explore_link.config(fg=COLOR_INK_BLACK))
        btn_explore_link.bind("<Leave>", lambda _: btn_explore_link.config(fg=COLOR_INK_MUTED))

        # Center Navigation Links: Home, Explore, Features, About
        center_box = tk.Frame(nav_frame, bg=COLOR_CONTAINER)
        center_box.pack(side="left", fill="both", expand=True)

        nav_items = [
            ("Home", lambda: self.canvas.yview_moveto(0.0)),
            ("Explore", lambda: self.on_explore_algorithms()),
            ("Features", lambda: self._scroll_to_section("features")),
            ("About", lambda: self._scroll_to_section("about"))
        ]

        links_inner = tk.Frame(center_box, bg=COLOR_CONTAINER)
        links_inner.pack(expand=True)

        for text, cmd in nav_items:
            lbl_link = tk.Label(
                links_inner,
                text=text,
                bg=COLOR_CONTAINER,
                fg=COLOR_INK_DARK,
                font=("Segoe UI", 12, "bold"),
                padx=16,
                cursor="hand2"
            )
            lbl_link.pack(side="left")
            lbl_link.bind("<Button-1>", lambda _e, action=cmd: action())
            lbl_link.bind("<Enter>", lambda _e, w=lbl_link: w.config(fg=COLOR_INK_BLACK))
            lbl_link.bind("<Leave>", lambda _e, w=lbl_link: w.config(fg=COLOR_INK_DARK))

    # -------------------------------------------------------------
    # SIGNUP MODAL OVERLAY
    # -------------------------------------------------------------

    def _open_signup_modal(self):
        """Displays a sleek, modern signup modal directly inside the landing page."""
        if hasattr(self, 'signup_overlay') and self.signup_overlay.winfo_exists():
            return

        # Dimmed backdrop overlay covering the entire LandingPage frame
        self.signup_overlay = tk.Frame(self, bg="#0F172A")
        self.signup_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Centered Modal Card (White, subtle rounded appearance with 1px border)
        card = tk.Frame(self.signup_overlay, bg="#FFFFFF", padx=32, pady=28, highlightthickness=1, highlightbackground=COLOR_BORDER_SUBTLE)
        card.place(relx=0.5, rely=0.5, anchor="center", width=460)

        # Header with Logo & Close button
        top_bar = tk.Frame(card, bg="#FFFFFF")
        top_bar.pack(fill="x", pady=(0, 16))

        brand_box = tk.Frame(top_bar, bg="#FFFFFF")
        brand_box.pack(side="left")

        lbl_logo = tk.Label(brand_box, text="AlgoScope", bg="#FFFFFF", fg=COLOR_INK_BLACK, font=("Segoe UI", 16, "bold"))
        lbl_logo.pack(side="left")

        dot = tk.Canvas(brand_box, width=14, height=14, bg="#FFFFFF", highlightthickness=0)
        dot.pack(side="left", padx=(4, 0))
        dot.create_oval(1, 1, 13, 13, fill=COLOR_LIME, outline="")

        btn_close = tk.Label(top_bar, text="✕", bg="#FFFFFF", fg=COLOR_INK_MUTED, font=("Segoe UI", 13, "bold"), cursor="hand2")
        btn_close.pack(side="right")
        btn_close.bind("<Button-1>", lambda _: self._close_signup_modal())
        btn_close.bind("<Enter>", lambda _: btn_close.config(fg=COLOR_INK_BLACK))
        btn_close.bind("<Leave>", lambda _: btn_close.config(fg=COLOR_INK_MUTED))

        # Title & Subtitle
        lbl_title = tk.Label(card, text="Create your Account", bg="#FFFFFF", fg=COLOR_INK_BLACK, font=("Segoe UI", 18, "bold"))
        lbl_title.pack(anchor="w", pady=(0, 4))

        lbl_sub = tk.Label(card, text="Join AlgoScope to save visualizer presets and analyze DSA performance.", bg="#FFFFFF", fg=COLOR_INK_MUTED, font=("Segoe UI", 10), wraplength=390, justify="left")
        lbl_sub.pack(anchor="w", pady=(0, 20))

        # Input fields helper
        def make_field(label_text, is_password=False, default_val=""):
            tk.Label(card, text=label_text, bg="#FFFFFF", fg=COLOR_INK_DARK, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
            f_frame = tk.Frame(card, bg=COLOR_CARD_LIGHT, padx=12, pady=8, highlightthickness=1, highlightbackground=COLOR_BORDER_SUBTLE)
            f_frame.pack(fill="x", pady=(0, 14))
            entry = tk.Entry(f_frame, bg=COLOR_CARD_LIGHT, fg=COLOR_INK_BLACK, font=("Segoe UI", 11), relief="flat", insertbackground=COLOR_INK_BLACK)
            if is_password:
                entry.config(show="•")
            if default_val:
                entry.insert(0, default_val)
            entry.pack(fill="x")
            return entry

        entry_name = make_field("Full Name", default_val="Student Developer")
        entry_email = make_field("Email Address", default_val="student@algoscope.io")
        entry_password = make_field("Password", is_password=True, default_val="password123")

        # Status / Feedback label
        lbl_feedback = tk.Label(card, text="", bg="#FFFFFF", fg="#EF4444", font=("Segoe UI", 10, "bold"))
        lbl_feedback.pack(anchor="w", pady=(0, 8))

        # Submit Button (Solid Black Pill Button)
        def on_submit():
            name = entry_name.get().strip()
            email = entry_email.get().strip()
            if not name:
                lbl_feedback.config(text="Please enter your name.", fg="#EF4444")
                return
            if not email or "@" not in email:
                lbl_feedback.config(text="Please enter a valid email address.", fg="#EF4444")
                return

            lbl_feedback.config(text=f"✔ Welcome aboard, {name}! Account created.", fg="#10B981")
            self.after(700, lambda: (self._close_signup_modal(), self.on_get_started()))

        btn_submit = tk.Label(
            card,
            text="Sign Up & Get Started →",
            bg=COLOR_INK_BLACK,
            fg="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        btn_submit.pack(fill="x", pady=(4, 12))
        btn_submit.bind("<Button-1>", lambda _: on_submit())
        btn_submit.bind("<Enter>", lambda _: btn_submit.config(bg="#27272A"))
        btn_submit.bind("<Leave>", lambda _: btn_submit.config(bg=COLOR_INK_BLACK))

        # Bottom text
        lbl_terms = tk.Label(card, text="100% Free & Open Source • Runs locally on your machine", bg="#FFFFFF", fg=COLOR_INK_LIGHT, font=("Segoe UI", 9))
        lbl_terms.pack(anchor="center")

        # Close on Escape
        self.signup_overlay.bind_all("<Escape>", lambda _: self._close_signup_modal())

    def _close_signup_modal(self):
        if hasattr(self, 'signup_overlay') and self.signup_overlay.winfo_exists():
            self.signup_overlay.destroy()

    # -------------------------------------------------------------
    # 2. HERO SECTION — THE PROFINANCE COMPOSITION
    # -------------------------------------------------------------

    def _build_hero_section(self):
        """
        Builds the hero canvas which draws the large lime-green rounded container
        and hosts the floating overlapping cards that extend beyond its bottom edge.
        """
        hero_wrapper = tk.Frame(self.site_wrapper, bg=COLOR_CONTAINER)
        hero_wrapper.pack(fill="x", padx=28, pady=(8, 36))

        # Canvas with generous height so the overlapping cards extend onto the white space below
        self.hero_canvas_height = 620
        self.hero_canvas = tk.Canvas(
            hero_wrapper,
            bg=COLOR_CONTAINER,
            height=self.hero_canvas_height,
            highlightthickness=0
        )
        self.hero_canvas.pack(fill="x", expand=True)

        # Interactive click bindings on hero canvas
        self.hero_canvas.bind("<Button-1>", self._on_hero_canvas_click)

    def _redraw_hero_canvas(self):
        """Redraws the entire hero composition responsively."""
        if not hasattr(self, 'hero_canvas') or not self.hero_canvas.winfo_exists():
            return

        w = self.hero_canvas.winfo_width()
        if w < 100:
            w = 1100

        self.hero_canvas.delete("all")

        # 1. Draw Large Lime-Green Rounded Rectangle (Hero Container)
        # Ends at y = 480 so the floating cards extending to y = 575 cross the boundary!
        lime_h = 480
        draw_smooth_rounded_rect(
            self.hero_canvas,
            x1=0,
            y1=0,
            x2=w,
            y2=lime_h,
            radius=32,
            fill=COLOR_LIME,
            outline=""
        )

        # ------------------ LEFT SIDE: HEADLINE & CTAs ------------------
        # Headline: "Make ✦\nAlgorithms Visible."
        self.hero_canvas.create_text(
            48, 86,
            text="Make  ✦",
            anchor="w",
            fill=COLOR_INK_BLACK,
            font=("Segoe UI", 44, "bold")
        )
        self.hero_canvas.create_text(
            48, 146,
            text="Algorithms Visible.",
            anchor="w",
            fill=COLOR_INK_BLACK,
            font=("Segoe UI", 44, "bold")
        )

        # Description: "Explore, understand, and visualize algorithms through interactive step-by-step execution."
        desc_text = (
            "Explore, understand, and visualize algorithms through\n"
            "interactive step-by-step execution and real memory traces."
        )
        self.hero_canvas.create_text(
            48, 224,
            text=desc_text,
            anchor="w",
            fill=COLOR_INK_DARK,
            font=("Segoe UI", 13, "bold"),
            justify="left"
        )

        # Primary Button: "Get Started" (Black rounded pill)
        btn_w, btn_h = 160, 48
        bx1, by1 = 48, 290
        bx2, by2 = bx1 + btn_w, by1 + btn_h
        draw_smooth_rounded_rect(
            self.hero_canvas,
            bx1, by1, bx2, by2,
            radius=24,
            fill=COLOR_INK_BLACK,
            outline="",
            tags=("btn_get_started",)
        )
        self.hero_canvas.create_text(
            bx1 + btn_w / 2, by1 + btn_h / 2,
            text="▶  Get Started",
            fill="#FFFFFF",
            font=("Segoe UI", 12, "bold"),
            tags=("btn_get_started",)
        )

        # Secondary Link: "Explore Features ↓"
        self.hero_canvas.create_text(
            48, 385,
            text="Find Out More  ↓",
            anchor="w",
            fill=COLOR_INK_BLACK,
            font=("Segoe UI", 12, "bold"),
            tags=("link_features",)
        )

        # Hand-drawn curved arrow swooping from below the button towards the floating cards
        # Exactly mirrors the playful curved arrow in the reference image
        arrow_card_x = w - 480
        arrow_start_x = bx2 + 18
        arrow_start_y = by1 + 24
        mid_x = (arrow_start_x + arrow_card_x) / 2
        arrow_pts = [
            arrow_start_x, arrow_start_y,
            arrow_start_x + 50, arrow_start_y + 60,
            mid_x - 20, arrow_start_y + 80,
            arrow_card_x - 12, arrow_start_y + 40
        ]
        self.hero_canvas.create_line(
            arrow_pts,
            smooth=True,
            arrow=tk.LAST,
            arrowshape=(11, 14, 5),
            width=2.5,
            fill=COLOR_INK_BLACK
        )

        # ------------------ RIGHT SIDE: FLOATING OVERLAPPING CARDS ------------------
        # Positioning:
        # Card 1 (Back Dark Card): positioned top-right, touches the bottom boundary (y=475)
        # Card 2 (Front White Card): overlaps Card 1, extends PAST the boundary to y=575!

        card1_w, card1_h = 320, 430
        card1_x2 = w - 30
        card1_x1 = card1_x2 - card1_w
        card1_y1 = 35
        card1_y2 = card1_y1 + card1_h

        card2_w, card2_h = 340, 480
        card2_x2 = card1_x1 + 185
        card2_x1 = card2_x2 - card2_w
        card2_y1 = 75
        card2_y2 = card2_y1 + card2_h  # Reaches y = 555 (75px below lime green boundary!)

        # Store coordinates for interaction
        self.card1_bounds = (card1_x1, card1_y1, card1_x2, card1_y2)
        self.card2_bounds = (card2_x1, card2_y1, card2_x2, card2_y2)

        # Draw Back Card (Dark Mode Graph & Shortest Path Panel)
        self._draw_back_dark_card(card1_x1, card1_y1, card1_x2, card1_y2)

        # Draw Front Card (Light Mode Live Sorting Visualizer Card)
        self._draw_front_white_card(card2_x1, card2_y1, card2_x2, card2_y2)

    def _draw_back_dark_card(self, x1, y1, x2, y2):
        """Draws the dark device panel with graph visualization & trading-style buttons."""
        # Main dark body
        draw_smooth_rounded_rect(
            self.hero_canvas,
            x1, y1, x2, y2,
            radius=24,
            fill=COLOR_CARD_DARK,
            outline="#27272A",
            width=1.5
        )

        # Top Bar: "← Graph Network  ☆"
        self.hero_canvas.create_text(
            x1 + 20, y1 + 22,
            text="←  Graph Network",
            anchor="w",
            fill="#FFFFFF",
            font=("Segoe UI", 11, "bold")
        )
        self.hero_canvas.create_text(
            x2 - 20, y1 + 22,
            text="☆",
            anchor="e",
            fill=COLOR_ACCENT_AMBER,
            font=("Segoe UI", 12, "bold")
        )

        # Metrics Bar: "$142.15  +1.25%  /  Cost: 14.2"
        self.hero_canvas.create_text(
            x1 + 20, y1 + 52,
            text="Shortest Path: Cost 14.2",
            anchor="w",
            fill="#FFFFFF",
            font=("Segoe UI", 12, "bold")
        )
        self.hero_canvas.create_text(
            x2 - 20, y1 + 52,
            text="● OPTIMAL",
            anchor="e",
            fill=COLOR_ACCENT_GREEN,
            font=("Segoe UI", 9, "bold")
        )

        # Graph Visualization Canvas inside dark card
        # Nodes & Glowing Weighted Edges
        gx1, gy1 = x1 + 18, y1 + 80
        gx2, gy2 = x2 - 18, y1 + 270

        # Draw dark canvas background
        draw_smooth_rounded_rect(
            self.hero_canvas,
            gx1, gy1, gx2, gy2,
            radius=12,
            fill="#18181B",
            outline="#27272A"
        )

        # Node coordinates
        nodes = {
            "A": (gx1 + 35, gy1 + 90),
            "B": (gx1 + 110, gy1 + 35),
            "C": (gx1 + 110, gy1 + 145),
            "D": (gx1 + 195, gy1 + 90),
            "E": (gx1 + 255, gy1 + 45),
            "F": (gx1 + 255, gy1 + 135)
        }

        # Edges: (u, v, weight, is_shortest_path)
        edges = [
            ("A", "C", "2", True),
            ("C", "B", "1", True),
            ("B", "D", "5", True),
            ("D", "F", "3", True),
            ("A", "B", "4", False),
            ("C", "D", "8", False),
            ("B", "E", "6", False),
            ("E", "F", "7", False)
        ]

        # Draw edges
        for u, v, weight, is_path in edges:
            p1, p2 = nodes[u], nodes[v]
            color = COLOR_ACCENT_GREEN if is_path else "#3F3F46"
            width = 2.5 if is_path else 1.2
            self.hero_canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=width)

            # Weight badge at midpoint
            mx = (p1[0] + p2[0]) / 2
            my = (p1[1] + p2[1]) / 2
            draw_smooth_rounded_rect(
                self.hero_canvas,
                mx - 7, my - 6, mx + 7, my + 6,
                radius=4,
                fill="#27272A",
                outline=""
            )
            self.hero_canvas.create_text(
                mx, my,
                text=weight,
                fill="#A1A1AA" if not is_path else "#FFFFFF",
                font=("Segoe UI", 7, "bold")
            )

        # Draw nodes
        for name, (nx, ny) in nodes.items():
            is_source = (name == "A")
            is_dest = (name == "F")
            is_path = name in ("A", "C", "B", "D", "F")

            n_fill = COLOR_ACCENT_CYAN if is_source else (COLOR_ACCENT_GREEN if is_path else "#27272A")
            n_outline = "#FFFFFF" if (is_source or is_dest) else "#3F3F46"
            self.hero_canvas.create_oval(nx - 11, ny - 11, nx + 11, ny + 11, fill=n_fill, outline=n_outline, width=1.5)
            self.hero_canvas.create_text(nx, ny, text=name, fill="#FFFFFF" if is_path else "#A1A1AA", font=("Segoe UI", 8, "bold"))

        # Algorithm Selection Pills (1H, 4H, Day, Week equivalent from reference image)
        tabs = ["BFS", "DFS", "Dijkstra", "A*", "MST"]
        tab_y = y1 + 295
        tab_w = (x2 - x1 - 36) / len(tabs)
        for i, t in enumerate(tabs):
            tx1 = x1 + 18 + i * tab_w
            tx2 = tx1 + tab_w - 4
            is_active = (t == "Dijkstra")
            draw_smooth_rounded_rect(
                self.hero_canvas,
                tx1, tab_y, tx2, tab_y + 22,
                radius=6,
                fill="#27272A" if is_active else "#18181B",
                outline=COLOR_ACCENT_AMBER if is_active else ""
            )
            self.hero_canvas.create_text(
                (tx1 + tx2) / 2, tab_y + 11,
                text=t,
                fill="#FFFFFF" if is_active else "#71717A",
                font=("Segoe UI", 8, "bold")
            )

        # Metrics rows: Total Cost $14.2, Visited Nodes: 5/6
        row_y = y1 + 335
        self.hero_canvas.create_text(x1 + 22, row_y, text="Dijkstra Heuristic", anchor="w", fill="#71717A", font=("Segoe UI", 9, "bold"))
        self.hero_canvas.create_text(x2 - 22, row_y, text="0.42 ms", anchor="e", fill="#FFFFFF", font=("Segoe UI", 9, "bold"))

        self.hero_canvas.create_text(x1 + 22, row_y + 22, text="Path Complexity", anchor="w", fill="#71717A", font=("Segoe UI", 9, "bold"))
        self.hero_canvas.create_text(x2 - 22, row_y + 22, text="O((V + E) log V)", anchor="e", fill=COLOR_ACCENT_GREEN, font=("Segoe UI", 9, "bold"))

        # Bottom Buttons (Coral Red "Reset" and Electric Lime "Run Path", mirroring Sell/Buy!)
        btn_y = y1 + 382
        bw = (x2 - x1 - 44) / 2

        # Reset button (Coral)
        draw_smooth_rounded_rect(
            self.hero_canvas,
            x1 + 18, btn_y, x1 + 18 + bw, btn_y + 36,
            radius=12,
            fill=COLOR_CORAL_BTN,
            outline="",
            tags=("graph_reset_btn",)
        )
        self.hero_canvas.create_text(
            x1 + 18 + bw / 2, btn_y + 18,
            text="Reset",
            fill="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            tags=("graph_reset_btn",)
        )

        # Run Path button (Electric Lime)
        draw_smooth_rounded_rect(
            self.hero_canvas,
            x2 - 18 - bw, btn_y, x2 - 18, btn_y + 36,
            radius=12,
            fill=COLOR_LIME,
            outline="",
            tags=("graph_run_btn",)
        )
        self.hero_canvas.create_text(
            x2 - 18 - bw / 2, btn_y + 18,
            text="Run Path",
            fill=COLOR_INK_BLACK,
            font=("Segoe UI", 10, "bold"),
            tags=("graph_run_btn",)
        )

    def _draw_front_white_card(self, x1, y1, x2, y2):
        """Draws the crisp white interactive card featuring live sorting visualization."""
        # Shadow / depth lift behind card
        draw_smooth_rounded_rect(
            self.hero_canvas,
            x1 + 4, y1 + 6, x2 + 4, y2 + 6,
            radius=26,
            fill="#E4E4E7",
            outline=""
        )

        # Main crisp white surface with rounded corners
        draw_smooth_rounded_rect(
            self.hero_canvas,
            x1, y1, x2, y2,
            radius=24,
            fill="#FFFFFF",
            outline=COLOR_BORDER_SUBTLE,
            width=1.5
        )

        # Card Title: "Market" -> "Algorithm Lab"
        self.hero_canvas.create_text(
            x1 + 22, y1 + 28,
            text="Algorithm Lab",
            anchor="w",
            fill=COLOR_INK_BLACK,
            font=("Segoe UI", 16, "bold")
        )

        # Search / Filter Mockup Bar (mirrors "Find stocks, funds, bonds...")
        search_y = y1 + 54
        draw_smooth_rounded_rect(
            self.hero_canvas,
            x1 + 20, search_y, x2 - 20, search_y + 32,
            radius=16,
            fill="#F4F4F5",
            outline="#E4E4E7"
        )
        self.hero_canvas.create_text(
            x1 + 34, search_y + 16,
            text="🔍  Search algorithm, array...",
            anchor="w",
            fill="#71717A",
            font=("Segoe UI", 9, "bold")
        )

        # Filter Pills: Sorting (Active Black), Searching, Graphs, Trees
        pill_y = y1 + 96
        chips = [("Sorting", True), ("Searching", False), ("Graphs", False), ("Trees", False)]
        cx = x1 + 20
        for name, active in chips:
            cw = len(name) * 7 + 22
            fill_c = COLOR_INK_BLACK if active else "#F4F4F5"
            text_c = "#FFFFFF" if active else "#52525B"
            draw_smooth_rounded_rect(
                self.hero_canvas,
                cx, pill_y, cx + cw, pill_y + 24,
                radius=12,
                fill=fill_c,
                outline=""
            )
            self.hero_canvas.create_text(
                cx + cw / 2, pill_y + 12,
                text=name,
                fill=text_c,
                font=("Segoe UI", 8, "bold")
            )
            cx += cw + 6

        # Featured Collection Card (mirrors "Dividend Strategy" dark collection card!)
        card_mini_y = y1 + 132
        draw_smooth_rounded_rect(
            self.hero_canvas,
            x1 + 20, card_mini_y, x2 - 20, card_mini_y + 64,
            radius=14,
            fill="#18181B",
            outline=""
        )
        self.hero_canvas.create_text(
            x1 + 32, card_mini_y + 18,
            text="Bubble Sort Engine",
            anchor="w",
            fill="#FFFFFF",
            font=("Segoe UI", 11, "bold")
        )
        self.hero_canvas.create_text(
            x1 + 32, card_mini_y + 36,
            text="Real-time adjacent comparison & swaps",
            anchor="w",
            fill="#A1A1AA",
            font=("Segoe UI", 8, "normal")
        )
        self.hero_canvas.create_text(
            x1 + 32, card_mini_y + 52,
            text="+100% Real Time Execution",
            anchor="w",
            fill=COLOR_ACCENT_GREEN,
            font=("Segoe UI", 8, "bold")
        )
        self.hero_canvas.create_text(
            x2 - 32, card_mini_y + 52,
            text="O(N log N)",
            anchor="e",
            fill=COLOR_LIME,
            font=("Segoe UI", 8, "bold")
        )

        # ------------------ LIVE SORTING VISUALIZATION BARS ------------------
        # Section Header: "LIVE EXECUTION"
        self.hero_canvas.create_text(
            x1 + 22, y1 + 214,
            text="LIVE MEMORY STATE",
            anchor="w",
            fill="#71717A",
            font=("Segoe UI", 8, "bold")
        )

        # Sorting Canvas Area
        sx1, sy1 = x1 + 20, y1 + 228
        sx2, sy2 = x2 - 20, y1 + 360
        draw_smooth_rounded_rect(
            self.hero_canvas,
            sx1, sy1, sx2, sy2,
            radius=12,
            fill="#FAFAFA",
            outline="#E4E4E7"
        )

        # Render sorting bars
        n = len(self.hero_sort_data)
        bar_w = (sx2 - sx1 - 16) / n
        max_val = max(self.hero_sort_data) if max(self.hero_sort_data) > 0 else 1
        comparing_pair = (self.hero_sort_j, self.hero_sort_j + 1)

        for idx, val in enumerate(self.hero_sort_data):
            bx0 = sx1 + 8 + idx * bar_w
            bx1 = bx0 + bar_w - 2.5
            bh = (val / max_val) * (sy2 - sy1 - 24)
            by1 = sy2 - 8
            by0 = by1 - bh

            # Determine color state
            bar_color = COLOR_ACCENT_BLUE
            if idx >= n - self.hero_sort_i:
                bar_color = COLOR_ACCENT_GREEN
            elif idx in comparing_pair:
                bar_color = COLOR_ACCENT_AMBER
            if idx == comparing_pair[0] and self.hero_sort_i < n:
                bar_color = COLOR_CORAL_BTN

            self.hero_canvas.create_rectangle(
                bx0, by0, bx1, by1,
                fill=bar_color,
                outline="",
                tags=("sorting_bars",)
            )

        # Metrics below live bars
        lbl_metrics = f"Comparisons: {self.hero_sort_comps}    Swaps: {self.hero_sort_swaps}"
        self.hero_canvas.create_text(
            x1 + 24, y1 + 378,
            text=lbl_metrics,
            anchor="w",
            fill=COLOR_INK_DARK,
            font=("Segoe UI", 9, "bold"),
            tags=("sort_metrics_text",)
        )
        self.hero_canvas.create_text(
            x2 - 24, y1 + 378,
            text="● ACTIVE",
            anchor="e",
            fill=COLOR_ACCENT_GREEN,
            font=("Segoe UI", 8, "bold")
        )

        # Interactive Controls Pill Row at bottom
        ctrl_y = y1 + 410
        btn_step_w = 90

        # Play/Pause Pill
        play_label = "⏸ Pause" if self.hero_sort_active else "▶ Play"
        draw_smooth_rounded_rect(
            self.hero_canvas,
            x1 + 20, ctrl_y, x1 + 20 + btn_step_w, ctrl_y + 34,
            radius=12,
            fill=COLOR_INK_BLACK,
            outline="",
            tags=("sort_play_btn",)
        )
        self.hero_canvas.create_text(
            x1 + 20 + btn_step_w / 2, ctrl_y + 17,
            text=play_label,
            fill="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            tags=("sort_play_btn",)
        )

        # Step Pill
        draw_smooth_rounded_rect(
            self.hero_canvas,
            x1 + 26 + btn_step_w, ctrl_y, x1 + 26 + btn_step_w * 2, ctrl_y + 34,
            radius=12,
            fill="#F4F4F5",
            outline="#E4E4E7",
            tags=("sort_step_btn",)
        )
        self.hero_canvas.create_text(
            x1 + 26 + btn_step_w * 1.5, ctrl_y + 17,
            text="⏭ Step",
            fill=COLOR_INK_BLACK,
            font=("Segoe UI", 9, "bold"),
            tags=("sort_step_btn",)
        )

        # Shuffle Pill
        draw_smooth_rounded_rect(
            self.hero_canvas,
            x2 - 20 - btn_step_w, ctrl_y, x2 - 20, ctrl_y + 34,
            radius=12,
            fill="#F4F4F5",
            outline="#E4E4E7",
            tags=("sort_shuffle_btn",)
        )
        self.hero_canvas.create_text(
            x2 - 20 - btn_step_w / 2, ctrl_y + 17,
            text="↺ Reset",
            fill=COLOR_INK_BLACK,
            font=("Segoe UI", 9, "bold"),
            tags=("sort_shuffle_btn",)
        )

    # ------------------ HERO SORTING ANIMATION STEP ------------------

    def _step_hero_sorting(self):
        """Advances bubble sort by one atomic step and updates the live canvas."""
        if not self.winfo_exists():
            return

        if self.hero_sort_active:
            n = len(self.hero_sort_data)
            if self.hero_sort_i < n:
                if self.hero_sort_j < n - self.hero_sort_i - 1:
                    self.hero_sort_comps += 1
                    if self.hero_sort_data[self.hero_sort_j] > self.hero_sort_data[self.hero_sort_j + 1]:
                        self.hero_sort_data[self.hero_sort_j], self.hero_sort_data[self.hero_sort_j + 1] = (
                            self.hero_sort_data[self.hero_sort_j + 1], self.hero_sort_data[self.hero_sort_j]
                        )
                        self.hero_sort_swaps += 1
                    self.hero_sort_j += 1
                else:
                    self.hero_sort_j = 0
                    self.hero_sort_i += 1
            else:
                # Reset array after full completion
                self.hero_sort_data = [random.randint(12, 98) for _ in range(18)]
                self.hero_sort_i = 0
                self.hero_sort_j = 0
                self.hero_sort_comps = 0
                self.hero_sort_swaps = 0

            if hasattr(self, 'hero_canvas') and self.hero_canvas.winfo_exists():
                self._redraw_hero_canvas()

        self.after(110, self._step_hero_sorting)

    def _on_hero_canvas_click(self, event):
        """Dispatches clicks on buttons rendered on the hero canvas."""
        x, y = event.x, event.y
        current_tags = self.hero_canvas.gettags("current")

        if "btn_get_started" in current_tags or "link_features" in current_tags:
            if "link_features" in current_tags:
                self._scroll_to_section("features")
            else:
                self.on_get_started()
            return

        if "sort_play_btn" in current_tags:
            self.hero_sort_active = not self.hero_sort_active
            self._redraw_hero_canvas()
            return

        if "sort_step_btn" in current_tags:
            # Single manual step
            self.hero_sort_active = False
            n = len(self.hero_sort_data)
            if self.hero_sort_i < n:
                if self.hero_sort_j < n - self.hero_sort_i - 1:
                    self.hero_sort_comps += 1
                    if self.hero_sort_data[self.hero_sort_j] > self.hero_sort_data[self.hero_sort_j + 1]:
                        self.hero_sort_data[self.hero_sort_j], self.hero_sort_data[self.hero_sort_j + 1] = (
                            self.hero_sort_data[self.hero_sort_j + 1], self.hero_sort_data[self.hero_sort_j]
                        )
                        self.hero_sort_swaps += 1
                    self.hero_sort_j += 1
                else:
                    self.hero_sort_j = 0
                    self.hero_sort_i += 1
            self._redraw_hero_canvas()
            return

        if "sort_shuffle_btn" in current_tags or "graph_reset_btn" in current_tags:
            self.hero_sort_data = [random.randint(12, 98) for _ in range(18)]
            self.hero_sort_i = 0
            self.hero_sort_j = 0
            self.hero_sort_comps = 0
            self.hero_sort_swaps = 0
            self._redraw_hero_canvas()
            return

        if "graph_run_btn" in current_tags:
            self.on_open_module("Graphs")
            return

        # Check if user clicked inside front card -> open sorting
        if hasattr(self, 'card2_bounds'):
            x1, y1, x2, y2 = self.card2_bounds
            if x1 <= x <= x2 and y1 <= y <= y2:
                # If clicked outside control buttons, navigate to Sorting
                if not ("sort_play_btn" in current_tags or "sort_step_btn" in current_tags or "sort_shuffle_btn" in current_tags):
                    self.on_open_module("Sorting")
                return

        # Check if user clicked inside back card -> open graphs
        if hasattr(self, 'card1_bounds'):
            x1, y1, x2, y2 = self.card1_bounds
            if x1 <= x <= x2 and y1 <= y <= y2:
                self.on_open_module("Graphs")
                return

    # -------------------------------------------------------------
    # 3. FEATURES SECTION ("Get the Most Out of Algorithms")
    # -------------------------------------------------------------

    def _build_features_section(self):
        """
        Builds the spacious features section below the hero, inspired directly by
        'Get the Most Out' in the ProFinance reference image.
        """
        sec = tk.Frame(self.site_wrapper, bg=COLOR_CONTAINER)
        sec.pack(fill="x", padx=36, pady=(32, 48))
        self.section_anchors["features"] = sec

        # Section Header: "Get the Most Out of Algorithms"
        lbl_head = tk.Label(
            sec,
            text="Get the Most Out of Algorithms",
            bg=COLOR_CONTAINER,
            fg=COLOR_INK_BLACK,
            font=("Segoe UI", 32, "bold")
        )
        lbl_head.pack(anchor="w", pady=(0, 6))

        lbl_sub = tk.Label(
            sec,
            text="Six comprehensive visual laboratories designed to build deep algorithmic intuition through genuine execution.",
            bg=COLOR_CONTAINER,
            fg=COLOR_INK_MUTED,
            font=("Segoe UI", 13, "normal")
        )
        lbl_sub.pack(anchor="w", pady=(0, 32))

        # 6 Modern Features Grid (3 Columns x 2 Rows)
        grid = tk.Frame(sec, bg=COLOR_CONTAINER)
        grid.pack(fill="x")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.columnconfigure(2, weight=1)

        features = [
            (
                "01 / ARRAYS",
                "Sorting Visualizer",
                "Bubble, Selection, Insertion, Merge, Quick, and Heap Sort with dynamic bar animations, pivot indicators, and live swap counters.",
                "Sorting"
            ),
            (
                "02 / NETWORKS",
                "Graph Visualizer",
                "Interactive topology builder. Test BFS, DFS, Dijkstra's shortest path, A* search, and Prim's & Kruskal's Minimum Spanning Trees.",
                "Graphs"
            ),
            (
                "03 / SEARCH",
                "Searching Visualizer",
                "Step-by-step element probing with Linear, Binary, and Jump search boundary tracking on sorted and unsorted sets.",
                "Searching"
            ),
            (
                "04 / HIERARCHY",
                "Tree Visualizer",
                "Dynamic BST and self-balancing AVL trees. Follow balance factor computations, LL/RR/LR/RL rotation mechanics, and 4 traversals.",
                "Trees"
            ),
            (
                "05 / MEMORY",
                "Data Structures",
                "Watch Stacks (LIFO), Queues (FIFO), Circular Buffers, Singly & Doubly Linked Lists, and Hash Table collision resolution mutate in memory.",
                "Data Structures"
            ),
            (
                "06 / BENCHMARKS",
                "Performance Analyzer",
                "Benchmark actual CPU wall-clock runtime in milliseconds with time.perf_counter(). Compare operations against Big-O bounds.",
                "Performance"
            )
        ]

        for i, (badge, title, desc, mod_name) in enumerate(features):
            row = i // 3
            col = i % 3

            card = tk.Frame(grid, bg=COLOR_CONTAINER, highlightthickness=1, highlightbackground=COLOR_BORDER_SUBTLE, padx=24, pady=24, cursor="hand2")
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

            # Eyebrow tag
            lbl_tag = tk.Label(
                card,
                text=badge,
                bg=COLOR_CONTAINER,
                fg=COLOR_INK_MUTED,
                font=("Segoe UI", 9, "bold")
            )
            lbl_tag.pack(anchor="w", pady=(0, 8))

            # Title
            lbl_title = tk.Label(
                card,
                text=title,
                bg=COLOR_CONTAINER,
                fg=COLOR_INK_BLACK,
                font=("Segoe UI", 16, "bold")
            )
            lbl_title.pack(anchor="w", pady=(0, 6))

            # Description
            lbl_desc = tk.Label(
                card,
                text=desc,
                bg=COLOR_CONTAINER,
                fg=COLOR_INK_MUTED,
                font=("Segoe UI", 11, "normal"),
                wraplength=270,
                justify="left"
            )
            lbl_desc.pack(anchor="w", pady=(0, 16))

            # Action link
            lbl_action = tk.Label(
                card,
                text="Explore Laboratory  →",
                bg=COLOR_CONTAINER,
                fg=COLOR_INK_BLACK,
                font=("Segoe UI", 10, "bold")
            )
            lbl_action.pack(anchor="w")

            # Bind clicks
            for w in (card, lbl_tag, lbl_title, lbl_desc, lbl_action):
                w.bind("<Button-1>", lambda _e, name=mod_name: self.on_open_module(name))
                w.bind("<Enter>", lambda _e, c=card, a=lbl_action: self._on_card_hover(c, a, True))
                w.bind("<Leave>", lambda _e, c=card, a=lbl_action: self._on_card_hover(c, a, False))

    def _on_card_hover(self, card, action_label, is_hover: bool):
        if is_hover:
            card.config(highlightbackground=COLOR_INK_BLACK)
            action_label.config(fg="#2563EB")
        else:
            card.config(highlightbackground=COLOR_BORDER_SUBTLE)
            action_label.config(fg=COLOR_INK_BLACK)

    # -------------------------------------------------------------
    # 4. ABOUT / "WHY ALGOSCOPE" SECTION
    # -------------------------------------------------------------

    def _build_why_section(self):
        sec = tk.Frame(self.site_wrapper, bg=COLOR_CONTAINER)
        sec.pack(fill="x", padx=36, pady=(16, 48))
        self.section_anchors["about"] = sec

        story = tk.Frame(sec, bg=COLOR_CONTAINER)
        story.pack(fill="x")
        story.columnconfigure(0, weight=1)
        story.columnconfigure(1, weight=1)

        # Left Column: Heading and narrative
        left = tk.Frame(story, bg=COLOR_CONTAINER)
        left.grid(row=0, column=0, sticky="nw", padx=(0, 48))

        lbl_why_head = tk.Label(
            left,
            text="The difference is in\nthe execution.",
            bg=COLOR_CONTAINER,
            fg=COLOR_INK_BLACK,
            font=("Segoe UI", 28, "bold"),
            justify="left"
        )
        lbl_why_head.pack(anchor="w", pady=(0, 14))

        lbl_why_sub = tk.Label(
            left,
            text="Traditional textbooks force students to imagine abstract state changes. AlgoScope executes genuine Python algorithm generators, providing 100% authentic state snapshots at every single transition.",
            bg=COLOR_CONTAINER,
            fg=COLOR_INK_MUTED,
            font=("Segoe UI", 12, "normal"),
            wraplength=440,
            justify="left"
        )
        lbl_why_sub.pack(anchor="w")

        # Right Column: 3 Value Pillars
        pillars = [
            ("01", "100% Real State Snapshots", "No prewritten animations or faked delays. Every frame comes directly from genuine algorithmic generators."),
            ("02", "Bidirectional Time-Travel", "Scrub back and forth through execution history. Pause, step forward, rewind, and inspect active pseudocode."),
            ("03", "Hardware CPU Profiler", "Measure real wall-clock microsecond timing without artificial simulation pauses. Compare theory with reality.")
        ]

        right = tk.Frame(story, bg=COLOR_CONTAINER)
        right.grid(row=0, column=1, sticky="nsew")

        for num, title, text in pillars:
            row = tk.Frame(right, bg=COLOR_CONTAINER, highlightthickness=1, highlightbackground=COLOR_BORDER_SUBTLE, padx=20, pady=16)
            row.pack(fill="x", pady=6)

            lbl_num = tk.Label(row, text=num, bg=COLOR_CONTAINER, fg=COLOR_INK_BLACK, font=("Segoe UI", 11, "bold"), width=3, anchor="w")
            lbl_num.pack(side="left", anchor="n")

            content = tk.Frame(row, bg=COLOR_CONTAINER)
            content.pack(side="left", fill="x", expand=True)

            lbl_t = tk.Label(content, text=title, bg=COLOR_CONTAINER, fg=COLOR_INK_BLACK, font=("Segoe UI", 13, "bold"))
            lbl_t.pack(anchor="w")

            lbl_d = tk.Label(content, text=text, bg=COLOR_CONTAINER, fg=COLOR_INK_MUTED, font=("Segoe UI", 10, "normal"), wraplength=400, justify="left")
            lbl_d.pack(anchor="w", pady=(2, 0))

    # -------------------------------------------------------------
    # 5. FINAL CALL TO ACTION BANNER
    # -------------------------------------------------------------

    def _build_final_cta(self):
        sec = tk.Frame(self.site_wrapper, bg=COLOR_CONTAINER)
        sec.pack(fill="x", padx=36, pady=(16, 48))

        cta_card = tk.Frame(sec, bg="#F9FAFB", highlightthickness=1, highlightbackground=COLOR_BORDER_SUBTLE, padx=48, pady=48)
        cta_card.pack(fill="x")

        # Badge
        lbl_badge = tk.Label(
            cta_card,
            text="✦  MAKE ALGORITHMS VISIBLE",
            bg="#F9FAFB",
            fg=COLOR_INK_MUTED,
            font=("Segoe UI", 9, "bold")
        )
        lbl_badge.pack(anchor="center", pady=(0, 8))

        # Heading
        lbl_head = tk.Label(
            cta_card,
            text="Ready to Explore How Algorithms Work?",
            bg="#F9FAFB",
            fg=COLOR_INK_BLACK,
            font=("Segoe UI", 26, "bold")
        )
        lbl_head.pack(anchor="center", pady=(0, 8))

        # Subhead
        lbl_sub = tk.Label(
            cta_card,
            text="Launch the AlgoScope workspace to trace sorting, graphs, trees, and data structures in real time.",
            bg="#F9FAFB",
            fg=COLOR_INK_MUTED,
            font=("Segoe UI", 12, "normal")
        )
        lbl_sub.pack(anchor="center", pady=(0, 24))

        # Button
        btn_launch = tk.Label(
            cta_card,
            text="Get Started Now  →",
            bg=COLOR_INK_BLACK,
            fg="#FFFFFF",
            font=("Segoe UI", 12, "bold"),
            padx=28,
            pady=12,
            cursor="hand2"
        )
        btn_launch.pack(anchor="center")
        btn_launch.bind("<Button-1>", lambda _: self.on_get_started())
        btn_launch.bind("<Enter>", lambda _: btn_launch.config(bg="#27272A"))
        btn_launch.bind("<Leave>", lambda _: btn_launch.config(bg=COLOR_INK_BLACK))

    # -------------------------------------------------------------
    # 6. MINIMALIST FOOTER
    # -------------------------------------------------------------

    def _build_footer(self):
        tk.Frame(self.site_wrapper, bg=COLOR_BORDER_SUBTLE, height=1).pack(fill="x")

        footer = tk.Frame(self.site_wrapper, bg=COLOR_CONTAINER, padx=36, pady=24)
        footer.pack(fill="x")

        # Left branding
        left = tk.Frame(footer, bg=COLOR_CONTAINER)
        left.pack(side="left")

        lbl_logo = tk.Label(left, text="◈ AlgoScope", bg=COLOR_CONTAINER, fg=COLOR_INK_BLACK, font=("Segoe UI", 11, "bold"))
        lbl_logo.pack(side="left")

        lbl_desc = tk.Label(left, text="— Interactive DSA & Algorithm Visualizer", bg=COLOR_CONTAINER, fg=COLOR_INK_MUTED, font=("Segoe UI", 10, "normal"))
        lbl_desc.pack(side="left", padx=(8, 0))

        # Center links
        center = tk.Frame(footer, bg=COLOR_CONTAINER)
        center.pack(side="left", fill="x", expand=True)

        # Right metadata
        right = tk.Frame(footer, bg=COLOR_CONTAINER)
        right.pack(side="right")

        lbl_meta = tk.Label(
            right,
            text="Pure Python & Tkinter  ·  MIT License",
            bg=COLOR_CONTAINER,
            fg=COLOR_INK_MUTED,
            font=("Segoe UI", 9, "normal")
        )
        lbl_meta.pack(side="right")
