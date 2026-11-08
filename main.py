"""
AlgoScope – Interactive DSA & Algorithm Visualizer
Main Application Orchestrator & Screen Switcher
"""

import sys
from core.dpi import setup_high_dpi, configure_root_dpi, get_dpi_scale_factor

# Establish Windows High-DPI awareness before creating any Tkinter window
setup_high_dpi()

import tkinter as tk
from tkinter import ttk
from typing import Optional

from core.theme import (
    COLOR_BLACK, COLOR_SURFACE_1, COLOR_SURFACE_2, COLOR_BORDER, COLOR_BORDER_HOT,
    COLOR_TEXT_SECONDARY
)
from ui.landing_page import LandingPage
from ui.sidebar import Sidebar
from ui.dashboard import DashboardView
from visualizers.sorting_view import SortingView
from visualizers.searching_view import SearchingView
from visualizers.graph_view import GraphView
from visualizers.tree_view import TreeView
from visualizers.data_structure_view import DataStructureView
from visualizers.performance_view import PerformanceView

class AlgoScopeApp:
    """Master application controller managing navigation and screen state."""
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AlgoScope – Interactive DSA & Algorithm Visualizer")

        # Synchronize Tk font and physical pixel scaling with active screen DPI
        scale_factor = configure_root_dpi(self.root)

        # Scale window geometry appropriately for display DPI
        base_w = int(1280 * min(scale_factor, 1.25))
        base_h = int(820 * min(scale_factor, 1.25))

        # Check screen resolution to ensure comfortable desktop framing
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        target_w = min(base_w, int(screen_w * 0.94))
        target_h = min(base_h, int(screen_h * 0.92))

        self.root.geometry(f"{target_w}x{target_h}")
        self.root.minsize(int(1024 * min(scale_factor, 1.15)), int(680 * min(scale_factor, 1.15)))
        self.root.configure(bg=COLOR_BLACK)

        # Style standard ttk widgets for dark mode
        self._configure_ttk_styles()

        # Master Container
        self.main_container = tk.Frame(self.root, bg=COLOR_BLACK)
        self.main_container.pack(fill="both", expand=True)

        # App Layout Components
        self.landing_page: Optional[LandingPage] = None
        self.app_frame: Optional[tk.Frame] = None
        self.sidebar: Optional[Sidebar] = None
        self.content_area: Optional[tk.Frame] = None
        self.current_view: Optional[tk.Frame] = None

        # Bind Global Keyboard Shortcuts
        self.root.bind("<space>", self._on_space_pressed)
        self.root.bind("<Right>", self._on_right_pressed)
        self.root.bind("<Left>", self._on_left_pressed)

        # Initially open the Landing Page
        self.show_landing_page()

    def _configure_ttk_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(".", font=("Segoe UI", 10))
        style.configure(
            "TCombobox",
            fieldbackground=COLOR_SURFACE_2,
            background=COLOR_SURFACE_1,
            foreground="#FFFFFF",
            arrowcolor="#FFFFFF",
            bordercolor=COLOR_BORDER,
            lightcolor=COLOR_BORDER,
            darkcolor=COLOR_BORDER
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", COLOR_SURFACE_2)],
            selectbackground=[("readonly", COLOR_SURFACE_2)],
            selectforeground=[("readonly", "#FFFFFF")]
        )
        # Custom dark flat scrollbar with crisp perimeter border
        style.configure(
            "Vertical.TScrollbar",
            gripcount=0,
            background=COLOR_SURFACE_2,
            darkcolor=COLOR_SURFACE_1,
            lightcolor=COLOR_SURFACE_1,
            troughcolor=COLOR_BLACK,
            bordercolor=COLOR_BORDER,
            arrowcolor=COLOR_TEXT_SECONDARY
        )
        style.map(
            "Vertical.TScrollbar",
            background=[("active", COLOR_BORDER_HOT), ("disabled", COLOR_BLACK)]
        )

    # ------------------ NAVIGATION FLOW ------------------

    def show_landing_page(self):
        """Displays the landing page as the first screen."""
        self._cleanup_current_views()

        self.landing_page = LandingPage(
            self.main_container,
            on_get_started=self.show_dashboard,
            on_explore_algorithms=self.show_dashboard
        )
        self.landing_page.pack(fill="both", expand=True)

    def _ensure_app_shell(self):
        """Ensures the persistent application frame with sidebar is mounted."""
        if self.app_frame is None or not self.app_frame.winfo_exists():
            self.app_frame = tk.Frame(self.main_container, bg=COLOR_BLACK)
            self.app_frame.pack(fill="both", expand=True)

            self.sidebar = Sidebar(
                self.app_frame,
                on_navigate=self.navigate_to_module,
                on_go_home=self.show_landing_page
            )
            self.sidebar.pack(side="left", fill="y")

            self.content_area = tk.Frame(self.app_frame, bg=COLOR_BLACK)
            self.content_area.pack(side="right", fill="both", expand=True)

    def show_dashboard(self):
        """Navigates to the main dashboard."""
        self._cleanup_landing_page()
        self._ensure_app_shell()

        if self.current_view:
            self.current_view.destroy()

        self.sidebar.set_active_route("Dashboard")
        self.current_view = DashboardView(
            self.content_area,
            on_open_module=self.navigate_to_module
        )
        self.current_view.pack(fill="both", expand=True)

    def navigate_to_module(self, module_name: str):
        """Switches the active content view to the selected module visualizer."""
        if module_name == "Dashboard":
            self.show_dashboard()
            return

        self._cleanup_landing_page()
        self._ensure_app_shell()

        if self.current_view:
            self.current_view.destroy()

        self.sidebar.set_active_route(module_name)

        if module_name == "Sorting":
            self.current_view = SortingView(self.content_area, on_back=self.show_dashboard)
        elif module_name == "Searching":
            self.current_view = SearchingView(self.content_area, on_back=self.show_dashboard)
        elif module_name == "Graphs":
            self.current_view = GraphView(self.content_area, on_back=self.show_dashboard)
        elif module_name == "Trees":
            self.current_view = TreeView(self.content_area, on_back=self.show_dashboard)
        elif module_name == "Data Structures":
            self.current_view = DataStructureView(self.content_area, on_back=self.show_dashboard)
        elif module_name == "Performance":
            self.current_view = PerformanceView(self.content_area, on_back=self.show_dashboard)

        if self.current_view:
            self.current_view.pack(fill="both", expand=True)

    def _cleanup_landing_page(self):
        if self.landing_page and self.landing_page.winfo_exists():
            self.landing_page.destroy()
            self.landing_page = None

    def _cleanup_current_views(self):
        if self.current_view and self.current_view.winfo_exists():
            self.current_view.destroy()
            self.current_view = None
        if self.app_frame and self.app_frame.winfo_exists():
            self.app_frame.destroy()
            self.app_frame = None
            self.sidebar = None
            self.content_area = None

    # Keyboard shortcut hooks
    def _on_space_pressed(self, _):
        if self.current_view and hasattr(self.current_view, 'on_play_click'):
            self.current_view.on_play_click()

    def _on_right_pressed(self, _):
        if self.current_view and hasattr(self.current_view, 'on_next_click'):
            self.current_view.on_next_click()

    def _on_left_pressed(self, _):
        if self.current_view and hasattr(self.current_view, 'on_prev_click'):
            self.current_view.on_prev_click()


def main():
    root = tk.Tk()
    app = AlgoScopeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

