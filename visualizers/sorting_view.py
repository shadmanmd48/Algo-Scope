"""
AlgoScope Sorting Visualizer Module
Interactive Tkinter Canvas displaying real-time sorting execution.
"""

import random
import tkinter as tk
from typing import Callable, List, Optional
from visualizers.base_visualizer import BaseVisualizerView
from core.animation_engine import AnimationEngine
from core.base_algorithm import Step
from core.theme import (
    COLOR_BLACK, COLOR_SURFACE_1, COLOR_SURFACE_2, COLOR_BORDER,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    STATE_DEFAULT, STATE_COMPARE, STATE_ACTIVE, STATE_SORTED, STATE_SECONDARY,
    FONT_BUTTON_SM, FONT_CAPTION_3, FONT_TITLE_4, FONT_BODY_6
)
from ui.components import StyledButton, LabeledEntry
from algorithms.sorting import (
    bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort, heap_sort
)

class SortingView(BaseVisualizerView):
    """Visualizes sorting algorithms on animated Canvas bars."""
    def __init__(self, master, on_back: Callable[[], None]):
        self.algo_functions = {
            "Bubble Sort": bubble_sort,
            "Selection Sort": selection_sort,
            "Insertion Sort": insertion_sort,
            "Merge Sort": merge_sort,
            "Quick Sort": quick_sort,
            "Heap Sort": heap_sort
        }

        super().__init__(
            master=master,
            title="Sorting Visualizer",
            category="Sorting",
            algorithms=list(self.algo_functions.keys()),
            on_algorithm_change=self._on_algorithm_changed,
            on_back_to_dashboard=on_back
        )

        self.array_size = 25
        self.is_ascending = True
        self.raw_data: List[int] = []

        # Setup Canvas
        self.canvas = tk.Canvas(
            self.canvas_card.body,
            bg=COLOR_SURFACE_1,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=12, pady=12)
        self.canvas.bind("<Configure>", lambda _: self._draw_current_state())

        # Top customization bar inside canvas area
        self._add_sorting_controls()

        # Animation Engine
        self.engine = AnimationEngine(
            root=self,
            on_render_callback=self._render_step,
            on_complete_callback=self._on_sorting_completed
        )

        # Generate initial data and load
        self.generate_random_array()

    def _add_sorting_controls(self):
        """Add Array Size slider, Custom input, Asc/Desc toggle, and Randomize button."""
        top_ctrl = tk.Frame(self.canvas_card.body, bg=COLOR_SURFACE_1)
        top_ctrl.pack(fill="x", padx=12, pady=(8, 0), side="top")

        # Randomize button
        btn_rand = StyledButton(top_ctrl, text="🎲 Randomize", size="sm", variant="secondary", command=self.generate_random_array)
        btn_rand.pack(side="left", padx=(0, 10))

        # Array Size
        lbl_size = tk.Label(top_ctrl, text="Size:", bg=COLOR_SURFACE_1, fg=COLOR_TEXT_SECONDARY, font=FONT_BODY_6)
        lbl_size.pack(side="left", padx=(0, 4))

        self.size_scale = tk.Scale(
            top_ctrl,
            from_=8,
            to=50,
            orient="horizontal",
            showvalue=True,
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_PRIMARY,
            troughcolor=COLOR_SURFACE_2,
            highlightthickness=0,
            length=100,
            command=self._on_size_change
        )
        self.size_scale.set(self.array_size)
        self.size_scale.pack(side="left", padx=(0, 14))

        # Asc / Desc Order
        self.order_btn = StyledButton(
            top_ctrl,
            text="Ascending ↑",
            size="sm",
            variant="secondary",
            command=self._toggle_order
        )
        self.order_btn.pack(side="left", padx=(0, 14))

        # Custom Input
        self.custom_entry = LabeledEntry(top_ctrl, label_text="", initial_value="12, 45, 7, 23, 60, 18, 34, 5", width=22)
        self.custom_entry.pack(side="left", padx=(0, 6))

        btn_apply = StyledButton(top_ctrl, text="Set Custom", size="sm", variant="secondary", command=self._apply_custom_array)
        btn_apply.pack(side="left")

    def _toggle_order(self):
        self.is_ascending = not self.is_ascending
        self.order_btn.set_text("Ascending ↑" if self.is_ascending else "Descending ↓")
        self.reload_algorithm()

    def _on_size_change(self, val):
        new_size = int(val)
        if new_size != self.array_size:
            self.array_size = new_size
            self.generate_random_array()

    def _apply_custom_array(self):
        txt = self.custom_entry.get_value()
        try:
            items = [int(x.strip()) for x in txt.split(",") if x.strip()]
            if items:
                self.raw_data = items
                self.array_size = len(items)
                self.size_scale.set(len(items))
                self.reload_algorithm()
        except ValueError:
            self.update_status("Invalid numbers in custom input! Use comma-separated integers.")

    def generate_random_array(self):
        """Generates random integers and reloads current algorithm."""
        self.raw_data = [random.randint(5, 100) for _ in range(self.array_size)]
        self.reload_algorithm()

    def reload_algorithm(self):
        """Resets engine and initializes fresh generator."""
        self.engine.reset()
        algo_fn = self.algo_functions.get(self.current_algo_name, bubble_sort)
        generator = algo_fn(self.raw_data, ascending=self.is_ascending)

        initial_step = Step(
            action="init",
            state=list(self.raw_data),
            indices=[],
            message=f"Initialized {self.current_algo_name} with {len(self.raw_data)} elements.",
            metrics={"comparisons": 0, "swaps": 0}
        )
        self.engine.load_generator(generator, initial_step=initial_step)
        self.btn_play.set_text("▶ Play")
        self.btn_play.command = self.on_play_click

    def _on_algorithm_changed(self, name: str):
        self.reload_algorithm()

    def _render_step(self, step: Step):
        """Callback from AnimationEngine when advancing or stepping back."""
        self._last_step = step
        self.update_status(step.message)
        self.update_metrics(
            comps=step.metrics.get("comparisons", 0),
            swaps=step.metrics.get("swaps", 0),
            step=self.engine.current_index
        )
        self.highlight_pseudocode_line(step.pseudocode_line)
        self._draw_current_state()

    def _draw_current_state(self):
        """Draws the bar chart on Tkinter Canvas representing current array state."""
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

        margin_x = 24
        margin_top = 36
        margin_bottom = 28

        usable_w = w - (margin_x * 2)
        usable_h = h - margin_top - margin_bottom

        n = len(arr)
        bar_w = max(2.0, (usable_w / n) - 3.0)
        gap = 3.0
        max_val = max(arr) if max(arr) > 0 else 1

        for i, val in enumerate(arr):
            x0 = round(margin_x + i * (bar_w + gap))
            x1 = round(x0 + bar_w)
            bar_height = (val / max_val) * usable_h
            y1 = round(h - margin_bottom)
            y0 = round(y1 - bar_height)

            # Determine color
            color = STATE_DEFAULT
            if step.action == "done":
                color = STATE_SORTED
            elif i in step.indices:
                if step.action in ("compare", "probe"):
                    color = STATE_COMPARE
                elif step.action in ("swap", "overwrite", "insert"):
                    color = STATE_ACTIVE
                elif step.action == "pivot":
                    color = STATE_SECONDARY
                elif step.action == "sorted_sub":
                    color = STATE_SORTED
                else:
                    color = STATE_ACTIVE
            elif i in step.secondary_indices:
                color = STATE_SECONDARY

            # Draw bar rectangle with crisp integer coordinates
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                fill=color,
                outline="",
                tags="bar"
            )

            # Draw value text if there's enough space
            if bar_w > 14:
                font = FONT_CAPTION_3 if bar_w < 26 else FONT_BUTTON_SM
                self.canvas.create_text(
                    round((x0 + x1) / 2), round(y0 - 10),
                    text=str(val),
                    fill=COLOR_TEXT_PRIMARY if i in step.indices else COLOR_TEXT_MUTED,
                    font=font
                )

        # Baseline line
        self.canvas.create_line(
            margin_x, h - margin_bottom,
            w - margin_x, h - margin_bottom,
            fill=COLOR_BORDER,
            width=1
        )

    def _on_sorting_completed(self):
        self.btn_play.set_text("✔ Done")
        self.update_status(f"Execution completed! Array is now fully sorted.")

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
        # Convert scale to ms delay (inverted: higher slider = faster = lower delay)
        val_int = int(val)
        delay = max(5, 520 - val_int)
        self.engine.set_speed(delay)

