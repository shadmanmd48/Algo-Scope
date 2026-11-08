"""
AlgoScope Performance Analyzer Module
Runs real benchmark profiling on sorting algorithms and graphs live runtime and operation charts on Tkinter Canvas.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, List
from core.theme import (
    COLOR_BLACK, COLOR_SURFACE_1, COLOR_SURFACE_2, COLOR_BORDER, COLOR_BORDER_HOT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    STATE_DEFAULT, STATE_COMPARE, STATE_ACTIVE, STATE_SORTED, STATE_SECONDARY,
    FONT_HEADING_4, FONT_TITLE_2, FONT_TITLE_3, FONT_TITLE_4, FONT_BODY_6,
    FONT_BUTTON_SM, FONT_CAPTION_1, SPACING_100, SPACING_200
)
from ui.components import StyledButton, CardFrame, LabeledEntry
from algorithms.benchmarks import BENCHMARK_FUNCTIONS, run_benchmark
from data.algorithm_info import ALGORITHM_DATA

class PerformanceView(tk.Frame):
    """Executes real-time benchmark profiling and renders comparative Canvas charts."""
    def __init__(self, master, on_back: Callable[[], None]):
        super().__init__(master, bg=COLOR_BLACK)
        self.on_back_to_dashboard = on_back

        self.available_algos = list(BENCHMARK_FUNCTIONS.keys())
        self.selected_algos = {name: tk.BooleanVar(value=True) for name in self.available_algos}
        self.input_size = 500
        self.last_results: Dict[str, Dict[str, float]] = {}

        self._build_header()
        self._build_content()

        # Run an initial benchmark
        self.after(200, self.execute_benchmark)

    def _build_header(self):
        header = tk.Frame(self, bg=COLOR_SURFACE_1, height=56)
        header.pack(fill="x", side="top")

        border = tk.Frame(self, bg=COLOR_BORDER, height=1)
        border.pack(fill="x", side="top")

        box = tk.Frame(header, bg=COLOR_SURFACE_1)
        box.pack(side="left", padx=SPACING_200, pady=SPACING_100)

        btn_back = StyledButton(
            box,
            text="← Dashboard",
            command=self.on_back_to_dashboard,
            variant="secondary",
            size="sm"
        )
        btn_back.pack(side="left", padx=(0, SPACING_200))

        lbl = tk.Label(
            box,
            text="Performance Analyzer & Benchmarking",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_HEADING_4
        )
        lbl.pack(side="left")

    def _build_content(self):
        body = tk.Frame(self, bg=COLOR_BLACK)
        body.pack(fill="both", expand=True, padx=SPACING_100, pady=SPACING_100)

        # Left Settings & Controls Card
        self.left_card = CardFrame(body, bg=COLOR_SURFACE_1, width=320)
        self.left_card.pack(side="left", fill="y", padx=(0, SPACING_100))
        self.left_card.pack_propagate(False)

        # Right Visualization Canvas Card
        self.canvas_card = CardFrame(body, bg=COLOR_SURFACE_1)
        self.canvas_card.pack(side="right", fill="both", expand=True)

        self._build_settings_panel(self.left_card.body)
        self._build_canvas_panel(self.canvas_card.body)

    def _build_settings_panel(self, parent):
        lbl_cfg = tk.Label(parent, text="Benchmark Configuration", bg=COLOR_SURFACE_1, fg=COLOR_TEXT_PRIMARY, font=FONT_TITLE_2)
        lbl_cfg.pack(anchor="w", padx=14, pady=(14, 8))

        lbl_inst = tk.Label(
            parent,
            text="Executes actual algorithms on real arrays. Execution times (ms), comparisons, and swaps are measured live.",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY_6,
            wraplength=280,
            justify="left"
        )
        lbl_inst.pack(anchor="w", padx=14, pady=(0, 12))

        # Array Size options
        lbl_sz = tk.Label(parent, text="Test Array Size:", bg=COLOR_SURFACE_1, fg=COLOR_TEXT_PRIMARY, font=FONT_TITLE_4)
        lbl_sz.pack(anchor="w", padx=14, pady=(4, 4))

        sizes_f = tk.Frame(parent, bg=COLOR_SURFACE_1)
        sizes_f.pack(fill="x", padx=14, pady=(0, 12))

        self.size_var = tk.IntVar(value=self.input_size)
        for s in [50, 100, 250, 500, 1000]:
            r = tk.Radiobutton(
                sizes_f,
                text=str(s),
                variable=self.size_var,
                value=s,
                bg=COLOR_SURFACE_1,
                fg=COLOR_TEXT_PRIMARY,
                selectcolor=COLOR_SURFACE_2,
                activebackground=COLOR_SURFACE_1,
                activeforeground=COLOR_TEXT_PRIMARY,
                font=FONT_BODY_6,
                command=self._on_size_selected
            )
            r.pack(side="left", padx=(0, 8))

        # Algorithm Selection Checkboxes
        lbl_algos = tk.Label(parent, text="Select Algorithms:", bg=COLOR_SURFACE_1, fg=COLOR_TEXT_PRIMARY, font=FONT_TITLE_4)
        lbl_algos.pack(anchor="w", padx=14, pady=(8, 4))

        for name in self.available_algos:
            cb = tk.Checkbutton(
                parent,
                text=name,
                variable=self.selected_algos[name],
                bg=COLOR_SURFACE_1,
                fg=COLOR_TEXT_PRIMARY,
                selectcolor=COLOR_SURFACE_2,
                activebackground=COLOR_SURFACE_1,
                activeforeground=COLOR_TEXT_PRIMARY,
                font=FONT_BODY_6
            )
            cb.pack(anchor="w", padx=14, pady=2)

        # Run Button
        btn_run = StyledButton(
            parent,
            text="⚡ Run Live Benchmark",
            variant="accent",
            size="md",
            command=self.execute_benchmark
        )
        btn_run.pack(fill="x", padx=14, pady=(16, 8))

        # Status readout
        self.lbl_status = tk.Label(
            parent,
            text="Ready.",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_CAPTION_1,
            wraplength=280
        )
        self.lbl_status.pack(anchor="w", padx=14)

    def _build_canvas_panel(self, parent):
        top_bar = tk.Frame(parent, bg=COLOR_SURFACE_1)
        top_bar.pack(fill="x", padx=14, pady=(10, 4))

        self.lbl_chart_title = tk.Label(
            top_bar,
            text="Execution Time Comparison (Milliseconds)",
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_PRIMARY,
            font=FONT_TITLE_2
        )
        self.lbl_chart_title.pack(side="left")

        # Metric toggle: Time vs Comparisons
        self.metric_mode = "time"
        btn_toggle = StyledButton(
            top_bar,
            text="Toggle Time / Comparisons",
            size="sm",
            variant="secondary",
            command=self._toggle_metric_mode
        )
        btn_toggle.pack(side="right")

        self.canvas = tk.Canvas(parent, bg=COLOR_SURFACE_1, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=14, pady=10)
        self.canvas.bind("<Configure>", lambda _: self._draw_charts())

    def _toggle_metric_mode(self):
        self.metric_mode = "comparisons" if self.metric_mode == "time" else "time"
        self.lbl_chart_title.config(
            text="Comparison & Swap Count Comparison" if self.metric_mode == "comparisons" else "Execution Time Comparison (Milliseconds)"
        )
        self._draw_charts()

    def _on_size_selected(self):
        self.input_size = self.size_var.get()
        self.execute_benchmark()

    def execute_benchmark(self):
        """Runs real algorithms on random data and measures exact metrics."""
        chosen = [name for name, var in self.selected_algos.items() if var.get()]
        if not chosen:
            self.lbl_status.config(text="Please select at least one algorithm.")
            return

        self.lbl_status.config(text=f"Running live benchmarks on {len(chosen)} algorithms (N={self.input_size})...")
        self.update_idletasks()

        # Run real benchmark
        self.last_results = run_benchmark(chosen, self.input_size)
        self.lbl_status.config(text=f"Benchmark completed successfully for N={self.input_size}!")
        self._draw_charts()

    def _draw_charts(self):
        """Draws clean high-contrast comparative bar chart directly on Tkinter Canvas."""
        self.canvas.delete("all")
        if not self.last_results:
            return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 10 or h <= 10:
            return

        margin_left = 130
        margin_right = 40
        margin_top = 40
        margin_bottom = 50

        usable_w = w - margin_left - margin_right
        usable_h = h - margin_top - margin_bottom

        names = list(self.last_results.keys())
        if not names:
            return

        # Determine metric values
        if self.metric_mode == "time":
            values = [self.last_results[n]["time_ms"] for n in names]
            val_format = lambda v: f"{v:.2f} ms"
        else:
            values = [self.last_results[n]["comparisons"] for n in names]
            val_format = lambda v: f"{int(v):,} comps"

        max_val = max(values) if max(values) > 0 else 1.0

        bar_h = min(44.0, (usable_h / len(names)) - 14.0)
        gap = 14.0

        colors = [
            "#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EC4899", "#06B6D4"
        ]

        for i, name in enumerate(names):
            val = values[i]
            y0 = round(margin_top + i * (bar_h + gap))
            y1 = round(y0 + bar_h)

            bar_len = (val / max_val) * usable_w if max_val > 0 else 0
            x0 = round(margin_left)
            x1 = round(x0 + max(4.0, bar_len))

            color = colors[i % len(colors)]

            # Draw label with crisp coordinates
            self.canvas.create_text(
                margin_left - 14, round((y0 + y1) / 2),
                text=name,
                fill=COLOR_TEXT_PRIMARY,
                font=FONT_TITLE_4,
                anchor="e"
            )

            # Draw bar
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                fill=color,
                outline="",
                tags="chart_bar"
            )

            # Draw value readout at end of bar
            info = ALGORITHM_DATA.get(name)
            comp_tag = f"[{info.avg_time}]" if info else ""
            self.canvas.create_text(
                x1 + 10, round((y0 + y1) / 2),
                text=f"{val_format(val)}  {comp_tag}",
                fill=COLOR_TEXT_SECONDARY,
                font=FONT_BODY_6,
                anchor="w"
            )

        # Baseline axis line
        self.canvas.create_line(
            margin_left, margin_top - 10,
            margin_left, margin_top + len(names) * (bar_h + gap),
            fill=COLOR_BORDER,
            width=2
        )

