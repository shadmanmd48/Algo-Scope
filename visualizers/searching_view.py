"""
AlgoScope Searching Visualizer Module
Interactive visualizer for Linear, Binary, Jump, and Interpolation search.
"""

import random
import tkinter as tk
from typing import Callable, List, Optional
from visualizers.base_visualizer import BaseVisualizerView
from core.animation_engine import AnimationEngine
from core.base_algorithm import Step
from core.theme import (
    COLOR_BLACK, COLOR_SURFACE_1, COLOR_SURFACE_2, COLOR_BORDER, COLOR_BORDER_HOT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    STATE_DEFAULT, STATE_COMPARE, STATE_ACTIVE, STATE_SORTED, STATE_SECONDARY,
    FONT_BUTTON_SM, FONT_TITLE_4, FONT_BODY_6, FONT_CAPTION_1
)
from ui.components import StyledButton, LabeledEntry, Badge
from algorithms.searching import (
    linear_search, binary_search, jump_search, interpolation_search
)

class SearchingView(BaseVisualizerView):
    """Visualizes search algorithms with step-by-step pointers and block highlighting."""
    def __init__(self, master, on_back: Callable[[], None]):
        self.algo_functions = {
            "Linear Search": linear_search,
            "Binary Search": binary_search,
            "Jump Search": jump_search,
            "Interpolation Search": interpolation_search
        }

        super().__init__(
            master=master,
            title="Searching Visualizer",
            category="Searching",
            algorithms=list(self.algo_functions.keys()),
            on_algorithm_change=self._on_algorithm_changed,
            on_back_to_dashboard=on_back
        )

        self.array_size = 20
        self.target_val = 42
        self.raw_data: List[int] = []

        # Setup Canvas
        self.canvas = tk.Canvas(
            self.canvas_card.body,
            bg=COLOR_SURFACE_1,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=12, pady=12)
        self.canvas.bind("<Configure>", lambda _: self._draw_current_state())

        self._add_search_controls()

        self.engine = AnimationEngine(
            root=self,
            on_render_callback=self._render_step,
            on_complete_callback=self._on_search_completed
        )

        self.generate_random_array()

    def _add_search_controls(self):
        """Top bar for searching controls: Target input, Sort toggle, and Randomizer."""
        top_ctrl = tk.Frame(self.canvas_card.body, bg=COLOR_SURFACE_1)
        top_ctrl.pack(fill="x", padx=12, pady=(8, 0), side="top")

        # Randomize
        btn_rand = StyledButton(top_ctrl, text="🎲 Randomize", size="sm", variant="secondary", command=self.generate_random_array)
        btn_rand.pack(side="left", padx=(0, 10))

        # Sort Array Button (with notification indicator)
        self.btn_sort = StyledButton(top_ctrl, text="Sort Array (Required for Binary/Jump/Interpolation)", size="sm", variant="secondary", command=self._sort_current_array)
        self.btn_sort.pack(side="left", padx=(0, 14))

        # Target Input
        self.target_entry = LabeledEntry(top_ctrl, label_text="", initial_value=str(self.target_val), width=8)
        self.target_entry.pack(side="left", padx=(0, 6))

        btn_target = StyledButton(top_ctrl, text="Set Target", size="sm", variant="secondary", command=self._apply_target)
        btn_target.pack(side="left", padx=(0, 14))

        # Custom Array Input
        self.custom_entry = LabeledEntry(top_ctrl, label_text="", initial_value="5, 12, 19, 28, 35, 42, 58, 64, 77, 89", width=24)
        self.custom_entry.pack(side="left", padx=(0, 6))

        btn_apply = StyledButton(top_ctrl, text="Set Custom", size="sm", variant="secondary", command=self._apply_custom_array)
        btn_apply.pack(side="left")

    def _apply_target(self):
        val = self.target_entry.get_value()
        try:
            self.target_val = int(val)
            self.reload_algorithm()
        except ValueError:
            self.update_status("Target must be an integer!")

    def _apply_custom_array(self):
        txt = self.custom_entry.get_value()
        try:
            items = [int(x.strip()) for x in txt.split(",") if x.strip()]
            if items:
                self.raw_data = items
                self.array_size = len(items)
                self.reload_algorithm()
        except ValueError:
            self.update_status("Invalid numbers in custom input! Use comma-separated integers.")

    def _sort_current_array(self):
        self.raw_data.sort()
        self.reload_algorithm()
        self.update_status("Array sorted. Binary, Jump, and Interpolation search are now valid.")

    def generate_random_array(self):
        # By default generate sorted array if non-linear search is active
        self.raw_data = sorted([random.randint(5, 120) for _ in range(self.array_size)])
        # Pick one element to guarantee target is frequently in array
        self.target_val = random.choice(self.raw_data)
        self.target_entry.set_value(str(self.target_val))
        self.reload_algorithm()

    def reload_algorithm(self):
        self.engine.reset()

        # Check if algorithm requires sorted array
        needs_sorted = self.current_algo_name in ("Binary Search", "Jump Search", "Interpolation Search")
        is_sorted = (self.raw_data == sorted(self.raw_data))

        if needs_sorted and not is_sorted:
            self.raw_data.sort()
            self.update_status(f"Note: {self.current_algo_name} strictly requires a sorted array. Auto-sorted array.")

        algo_fn = self.algo_functions.get(self.current_algo_name, linear_search)
        generator = algo_fn(self.raw_data, target=self.target_val)

        initial_step = Step(
            action="init",
            state=list(self.raw_data),
            indices=[],
            message=f"Ready to search for target {self.target_val} using {self.current_algo_name}.",
            metrics={"comparisons": 0}
        )
        self.engine.load_generator(generator, initial_step=initial_step)
        self.btn_play.set_text("▶ Play")

    def _on_algorithm_changed(self, name: str):
        self.reload_algorithm()

    def _render_step(self, step: Step):
        self._last_step = step
        self.update_status(step.message)
        self.update_metrics(
            comps=step.metrics.get("comparisons", 0),
            swaps=None,
            step=self.engine.current_index
        )
        self.highlight_pseudocode_line(step.pseudocode_line)
        self._draw_current_state()

    def _draw_current_state(self):
        if not hasattr(self, '_last_step') or not self._last_step:
            return

        step = self._last_step
        arr = step.state
        if not arr:
            return

        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 10 or h <= 10:
            return

        n = len(arr)
        margin_x = 24
        usable_w = w - (margin_x * 2)

        # Draw Target Banner at top
        banner_y = 30
        self.canvas.create_text(
            w / 2, banner_y,
            text=f"Target: {self.target_val}",
            fill=STATE_ACTIVE,
            font=FONT_TITLE_4
        )

        box_w = min(54.0, max(24.0, (usable_w / n) - 4.0))
        box_h = 56.0
        total_span = n * (box_w + 4.0)
        start_x = (w - total_span) / 2
        box_y = h / 2 - 20

        # Draw array cells
        for i, val in enumerate(arr):
            x0 = round(start_x + i * (box_w + 4.0))
            x1 = round(x0 + box_w)
            y0 = round(box_y)
            y1 = round(y0 + box_h)

            # Determine cell color & outline
            bg_color = COLOR_SURFACE_2
            border_col = COLOR_BORDER
            text_col = COLOR_TEXT_PRIMARY

            if step.action == "found" and i in step.indices:
                bg_color = STATE_SORTED
                border_col = "#34D399"
                text_col = "#FFFFFF"
            elif i in step.indices:
                if step.action in ("compare", "probe"):
                    bg_color = STATE_COMPARE
                    border_col = "#FBBF24"
                    text_col = "#000000"
                elif step.action == "jump":
                    bg_color = STATE_SECONDARY
                    border_col = "#22D3EE"
                    text_col = "#000000"
            elif i in step.secondary_indices:
                bg_color = "#272727"
                border_col = COLOR_BORDER_HOT

            # Draw box with crisp pixel coordinates
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                fill=bg_color,
                outline=border_col,
                width=1
            )

            # Draw value
            self.canvas.create_text(
                round((x0 + x1) / 2), round((y0 + y1) / 2),
                text=str(val),
                fill=text_col,
                font=FONT_TITLE_4
            )

            # Draw index underneath
            self.canvas.create_text(
                (x0 + x1) / 2, y1 + 14,
                text=str(i),
                fill=COLOR_TEXT_MUTED,
                font=FONT_CAPTION_1
            )

        # Draw Search Bounds Indicator if applicable (low, high, mid)
        if step.secondary_indices and len(step.secondary_indices) >= 2:
            low_idx = step.secondary_indices[0]
            high_idx = step.secondary_indices[1]
            if 0 <= low_idx < n and 0 <= high_idx < n:
                x_low = start_x + low_idx * (box_w + 4.0) + box_w / 2
                x_high = start_x + high_idx * (box_w + 4.0) + box_w / 2
                self.canvas.create_line(x_low, box_y - 12, x_high, box_y - 12, fill=STATE_SECONDARY, width=2)
                self.canvas.create_text(x_low, box_y - 24, text="Low", fill=STATE_SECONDARY, font=FONT_CAPTION_1)
                self.canvas.create_text(x_high, box_y - 24, text="High", fill=STATE_SECONDARY, font=FONT_CAPTION_1)

    def _on_search_completed(self):
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
        delay = max(5, 520 - val_int)
        self.engine.set_speed(delay)

