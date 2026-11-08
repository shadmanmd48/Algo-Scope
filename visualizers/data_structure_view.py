"""
AlgoScope Data Structures Visualizer Module
Interactive Canvas for Stack, Queue, Circular Queue, Linked Lists, and Hash Table.
"""

import math
import tkinter as tk
from typing import Any, Callable, Dict, List, Optional
from visualizers.base_visualizer import BaseVisualizerView
from core.animation_engine import AnimationEngine
from core.base_algorithm import Step
from core.theme import (
    COLOR_BLACK, COLOR_SURFACE_1, COLOR_SURFACE_2, COLOR_BORDER, COLOR_BORDER_HOT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    STATE_DEFAULT, STATE_COMPARE, STATE_ACTIVE, STATE_SORTED, STATE_SECONDARY,
    FONT_BUTTON_SM, FONT_TITLE_4, FONT_TITLE_3, FONT_CAPTION_1, FONT_BODY_6
)
from ui.components import StyledButton, LabeledEntry
from algorithms.data_structures import (
    VisualStack, VisualQueue, VisualCircularQueue, VisualLinkedList, VisualHashTable
)

class DataStructureView(BaseVisualizerView):
    """Visualizes foundational data structures with real memory representations."""
    def __init__(self, master, on_back: Callable[[], None]):
        self.structures = ["Stack", "Queue", "Circular Queue", "Linked List", "Hash Table"]

        super().__init__(
            master=master,
            title="Data Structure Visualizer",
            category="Data Structures",
            algorithms=self.structures,
            on_algorithm_change=self._on_structure_changed,
            on_back_to_dashboard=on_back
        )

        # Active Data Structure Models
        self.stack = VisualStack(capacity=7)
        self.queue = VisualQueue(capacity=7)
        self.circ_queue = VisualCircularQueue(capacity=8)
        self.linked_list = VisualLinkedList(is_doubly=False)
        self.hash_table = VisualHashTable(capacity=7, mode="chaining")

        # Canvas
        self.canvas = tk.Canvas(
            self.canvas_card.body,
            bg=COLOR_SURFACE_1,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=12, pady=12)
        self.canvas.bind("<Configure>", lambda _: self._draw_current_state())

        # Operations Bar
        self.ops_bar = tk.Frame(self.canvas_card.body, bg=COLOR_SURFACE_1)
        self.ops_bar.pack(fill="x", padx=12, pady=(8, 0), side="top")

        self.engine = AnimationEngine(
            root=self,
            on_render_callback=self._render_step,
            on_complete_callback=self._on_ds_completed
        )

        self._build_active_structure_controls()
        self._load_initial_data()

    def _on_structure_changed(self, name: str):
        self._build_active_structure_controls()
        self._load_initial_data()

    def _build_active_structure_controls(self):
        """Rebuild top controls depending on which data structure is active."""
        for w in self.ops_bar.winfo_children():
            w.destroy()

        mode = self.current_algo_name

        if mode == "Stack":
            self.entry_val = LabeledEntry(self.ops_bar, label_text="", initial_value="42", width=6)
            self.entry_val.pack(side="left", padx=(0, 6))

            btn_push = StyledButton(self.ops_bar, text="Push", size="sm", variant="secondary", command=self._stack_push)
            btn_push.pack(side="left", padx=(0, 6))

            btn_pop = StyledButton(self.ops_bar, text="Pop", size="sm", variant="secondary", command=self._stack_pop)
            btn_pop.pack(side="left", padx=(0, 6))

            btn_peek = StyledButton(self.ops_bar, text="Peek", size="sm", variant="secondary", command=self._stack_peek)
            btn_peek.pack(side="left", padx=(0, 6))

        elif mode == "Queue":
            self.entry_val = LabeledEntry(self.ops_bar, label_text="", initial_value="15", width=6)
            self.entry_val.pack(side="left", padx=(0, 6))

            btn_enq = StyledButton(self.ops_bar, text="Enqueue", size="sm", variant="secondary", command=self._queue_enq)
            btn_enq.pack(side="left", padx=(0, 6))

            btn_deq = StyledButton(self.ops_bar, text="Dequeue", size="sm", variant="secondary", command=self._queue_deq)
            btn_deq.pack(side="left", padx=(0, 6))

        elif mode == "Circular Queue":
            self.entry_val = LabeledEntry(self.ops_bar, label_text="", initial_value="88", width=6)
            self.entry_val.pack(side="left", padx=(0, 6))

            btn_enq = StyledButton(self.ops_bar, text="Enqueue", size="sm", variant="secondary", command=self._cq_enq)
            btn_enq.pack(side="left", padx=(0, 6))

            btn_deq = StyledButton(self.ops_bar, text="Dequeue", size="sm", variant="secondary", command=self._cq_deq)
            btn_deq.pack(side="left", padx=(0, 6))

        elif mode == "Linked List":
            self.entry_val = LabeledEntry(self.ops_bar, label_text="", initial_value="99", width=6)
            self.entry_val.pack(side="left", padx=(0, 6))

            btn_head = StyledButton(self.ops_bar, text="Insert Head", size="sm", variant="secondary", command=self._ll_insert_head)
            btn_head.pack(side="left", padx=(0, 4))

            btn_tail = StyledButton(self.ops_bar, text="Insert Tail", size="sm", variant="secondary", command=self._ll_insert_tail)
            btn_tail.pack(side="left", padx=(0, 4))

            btn_del = StyledButton(self.ops_bar, text="Delete", size="sm", variant="secondary", command=self._ll_delete)
            btn_del.pack(side="left", padx=(0, 4))

            btn_search = StyledButton(self.ops_bar, text="Search", size="sm", variant="secondary", command=self._ll_search)
            btn_search.pack(side="left", padx=(0, 10))

            self.btn_toggle_doubly = StyledButton(
                self.ops_bar,
                text="Mode: Singly",
                size="sm",
                variant="secondary",
                command=self._ll_toggle_mode
            )
            self.btn_toggle_doubly.pack(side="left")

        elif mode == "Hash Table":
            self.entry_key = LabeledEntry(self.ops_bar, label_text="", initial_value="apple", width=8)
            self.entry_key.pack(side="left", padx=(0, 4))

            self.entry_val = LabeledEntry(self.ops_bar, label_text="", initial_value="100", width=6)
            self.entry_val.pack(side="left", padx=(0, 6))

            btn_ins = StyledButton(self.ops_bar, text="Insert", size="sm", variant="secondary", command=self._ht_insert)
            btn_ins.pack(side="left", padx=(0, 4))

            btn_find = StyledButton(self.ops_bar, text="Search", size="sm", variant="secondary", command=self._ht_search)
            btn_find.pack(side="left", padx=(0, 4))

            btn_del = StyledButton(self.ops_bar, text="Delete", size="sm", variant="secondary", command=self._ht_delete)
            btn_del.pack(side="left", padx=(0, 10))

            self.btn_ht_mode = StyledButton(
                self.ops_bar,
                text="Resolution: Chaining",
                size="sm",
                variant="secondary",
                command=self._ht_toggle_mode
            )
            self.btn_ht_mode.pack(side="left")

    def _load_initial_data(self):
        """Populate initial sample items for the active data structure."""
        mode = self.current_algo_name
        if mode == "Stack":
            self.stack = VisualStack(capacity=7)
            for v in [10, 20, 30]:
                self.stack.items.append(v)
            step = Step(action="init", state=list(self.stack.items), message="Stack ready with 3 initial items.")
            self.engine.load_steps([step])

        elif mode == "Queue":
            self.queue = VisualQueue(capacity=7)
            for v in [5, 15, 25]:
                self.queue.items.append(v)
            step = Step(action="init", state=list(self.queue.items), message="Queue ready with 3 initial items.")
            self.engine.load_steps([step])

        elif mode == "Circular Queue":
            self.circ_queue = VisualCircularQueue(capacity=8)
            for v in [10, 20, 30, 40]:
                self.circ_queue.enqueue(v)
                # drain generator
            step = Step(action="init", state=self.circ_queue.snapshot(), message="Circular Queue ring buffer ready.")
            self.engine.load_steps([step])

        elif mode == "Linked List":
            self.linked_list = VisualLinkedList(is_doubly=False)
            self.linked_list.nodes = [12, 24, 36, 48]
            step = Step(action="init", state=self.linked_list.snapshot(), message="Linked List ready with 4 nodes.")
            self.engine.load_steps([step])

        elif mode == "Hash Table":
            self.hash_table = VisualHashTable(capacity=7, mode="chaining")
            for k, v in [("cat", 10), ("dog", 20), ("bird", 30)]:
                # run insert silently
                gen = self.hash_table.insert(k, v)
                try:
                    while True: next(gen)
                except StopIteration: pass
            step = Step(action="init", state=self.hash_table.snapshot(), message="Hash Table ready with sample keys.")
            self.engine.load_steps([step])

    # Stack Actions
    def _stack_push(self):
        v = self.entry_val.get_value()
        gen = self.stack.push(v)
        self.engine.load_generator(gen)

    def _stack_pop(self):
        gen = self.stack.pop()
        self.engine.load_generator(gen)

    def _stack_peek(self):
        gen = self.stack.peek()
        self.engine.load_generator(gen)

    # Queue Actions
    def _queue_enq(self):
        v = self.entry_val.get_value()
        gen = self.queue.enqueue(v)
        self.engine.load_generator(gen)

    def _queue_deq(self):
        gen = self.queue.dequeue()
        self.engine.load_generator(gen)

    # Circular Queue Actions
    def _cq_enq(self):
        v = self.entry_val.get_value()
        gen = self.circ_queue.enqueue(v)
        self.engine.load_generator(gen)

    def _cq_deq(self):
        gen = self.circ_queue.dequeue()
        self.engine.load_generator(gen)

    # Linked List Actions
    def _ll_insert_head(self):
        v = self.entry_val.get_value()
        gen = self.linked_list.insert_head(v)
        self.engine.load_generator(gen)

    def _ll_insert_tail(self):
        v = self.entry_val.get_value()
        gen = self.linked_list.insert_tail(v)
        self.engine.load_generator(gen)

    def _ll_delete(self):
        v = self.entry_val.get_value()
        # Parse int if possible
        val = int(v) if v.isdigit() else v
        gen = self.linked_list.delete(val)
        self.engine.load_generator(gen)

    def _ll_search(self):
        v = self.entry_val.get_value()
        val = int(v) if v.isdigit() else v
        gen = self.linked_list.search(val)
        self.engine.load_generator(gen)

    def _ll_toggle_mode(self):
        self.linked_list.is_doubly = not self.linked_list.is_doubly
        self.btn_toggle_doubly.set_text("Mode: Doubly" if self.linked_list.is_doubly else "Mode: Singly")
        self._load_initial_data()

    # Hash Table Actions
    def _ht_insert(self):
        k = self.entry_key.get_value()
        v = self.entry_val.get_value()
        gen = self.hash_table.insert(k, v)
        self.engine.load_generator(gen)

    def _ht_search(self):
        k = self.entry_key.get_value()
        gen = self.hash_table.search(k)
        self.engine.load_generator(gen)

    def _ht_delete(self):
        k = self.entry_key.get_value()
        gen = self.hash_table.delete(k)
        self.engine.load_generator(gen)

    def _ht_toggle_mode(self):
        new_mode = "linear_probing" if self.hash_table.mode == "chaining" else "chaining"
        self.hash_table = VisualHashTable(capacity=7, mode=new_mode)
        self.btn_ht_mode.set_text("Resolution: Linear Probing" if new_mode == "linear_probing" else "Resolution: Chaining")
        self._load_initial_data()

    def _render_step(self, step: Step):
        self._last_step = step
        self.update_status(step.message)
        self._draw_current_state()

    def _draw_current_state(self):
        """Renders graphical data structures directly on Tkinter Canvas."""
        self.canvas.delete("all")
        if not hasattr(self, '_last_step') or not self._last_step:
            return

        step = self._last_step
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 10 or h <= 10:
            return

        mode = self.current_algo_name

        if mode == "Stack":
            self._draw_stack(step, w, h)
        elif mode == "Queue":
            self._draw_queue(step, w, h)
        elif mode == "Circular Queue":
            self._draw_circular_queue(step, w, h)
        elif mode == "Linked List":
            self._draw_linked_list(step, w, h)
        elif mode == "Hash Table":
            self._draw_hash_table(step, w, h)

    def _draw_stack(self, step: Step, w: float, h: float):
        items = step.state if isinstance(step.state, list) else []
        box_w = 140
        box_h = 36
        cx = w / 2
        bottom_y = h - 60

        # Draw container walls
        wall_h = 7 * (box_h + 4) + 16
        self.canvas.create_line(cx - box_w/2 - 8, bottom_y + 8, cx - box_w/2 - 8, bottom_y - wall_h, fill=COLOR_BORDER, width=3)
        self.canvas.create_line(cx + box_w/2 + 8, bottom_y + 8, cx + box_w/2 + 8, bottom_y - wall_h, fill=COLOR_BORDER, width=3)
        self.canvas.create_line(cx - box_w/2 - 8, bottom_y + 8, cx + box_w/2 + 8, bottom_y + 8, fill=COLOR_BORDER, width=3)

        for i, val in enumerate(items):
            y1 = bottom_y - i * (box_h + 4)
            y0 = y1 - box_h

            bg_col = COLOR_SURFACE_2
            border_col = COLOR_BORDER
            if i in step.indices:
                bg_col = STATE_ACTIVE if step.action == "push" else STATE_COMPARE
                border_col = "#F87171"

            self.canvas.create_rectangle(
                cx - box_w/2, y0, cx + box_w/2, y1,
                fill=bg_col, outline=border_col, width=2
            )
            self.canvas.create_text(
                cx, (y0 + y1) / 2,
                text=str(val), fill=COLOR_TEXT_PRIMARY, font=FONT_TITLE_4
            )

        if items:
            top_idx = len(items) - 1
            top_y = bottom_y - top_idx * (box_h + 4) - box_h / 2
            self.canvas.create_text(
                cx + box_w/2 + 40, top_y,
                text="← TOP", fill=STATE_ACTIVE, font=FONT_TITLE_4
            )

    def _draw_queue(self, step: Step, w: float, h: float):
        items = step.state if isinstance(step.state, list) else []
        box_w = 64
        box_h = 56
        cy = h / 2
        start_x = (w - (len(items) * (box_w + 6))) / 2 if items else w / 2

        for i, val in enumerate(items):
            x0 = start_x + i * (box_w + 6)
            x1 = x0 + box_w
            y0 = cy - box_h / 2
            y1 = cy + box_h / 2

            bg_col = COLOR_SURFACE_2
            border_col = COLOR_BORDER
            if i in step.indices:
                bg_col = STATE_ACTIVE if step.action == "enqueue" else STATE_SORTED
                border_col = "#34D399"

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg_col, outline=border_col, width=2)
            self.canvas.create_text((x0 + x1)/2, cy, text=str(val), fill=COLOR_TEXT_PRIMARY, font=FONT_TITLE_4)

        if items:
            # Front pointer
            fx = start_x + box_w / 2
            self.canvas.create_text(fx, cy - box_h/2 - 16, text="FRONT (Exit) ↓", fill=STATE_SECONDARY, font=FONT_CAPTION_1)

            # Rear pointer
            rx = start_x + (len(items) - 1) * (box_w + 6) + box_w / 2
            self.canvas.create_text(rx, cy + box_h/2 + 16, text="↑ REAR (Entry)", fill=STATE_ACTIVE, font=FONT_CAPTION_1)

    def _draw_circular_queue(self, step: Step, w: float, h: float):
        info = step.state if isinstance(step.state, dict) else {}
        buf = info.get("buffer", [None]*8)
        front = info.get("front", -1)
        rear = info.get("rear", -1)
        cap = info.get("capacity", 8)

        cx = w / 2
        cy = h / 2
        radius = min(w, h) / 3.2

        for i in range(cap):
            angle = (2 * math.pi * i) / cap - math.pi / 2
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)

            val = buf[i]
            bg_col = COLOR_SURFACE_2
            border_col = COLOR_BORDER
            text_val = "-" if val is None else str(val)

            if i in step.indices:
                bg_col = STATE_ACTIVE
                border_col = "#F87171"
            elif i in step.secondary_indices:
                bg_col = STATE_SECONDARY
                border_col = "#22D3EE"

            # Draw circle slot
            r_slot = 24
            self.canvas.create_oval(x - r_slot, y - r_slot, x + r_slot, y + r_slot, fill=bg_col, outline=border_col, width=2)
            self.canvas.create_text(x, y, text=text_val, fill=COLOR_TEXT_PRIMARY, font=FONT_TITLE_4)

            # Draw slot index
            idx_x = cx + (radius + 36) * math.cos(angle)
            idx_y = cy + (radius + 36) * math.sin(angle)
            label = f"[{i}]"
            if i == front:
                label += " F"
            if i == rear:
                label += " R"
            self.canvas.create_text(idx_x, idx_y, text=label, fill=STATE_SECONDARY if i == front else (STATE_ACTIVE if i == rear else COLOR_TEXT_MUTED), font=FONT_CAPTION_1)

    def _draw_linked_list(self, step: Step, w: float, h: float):
        info = step.state if isinstance(step.state, dict) else {}
        nodes = info.get("nodes", [])
        is_doubly = info.get("is_doubly", False)

        node_w = 76
        node_h = 44
        cy = h / 2
        start_x = 40

        for i, val in enumerate(nodes):
            x0 = start_x + i * (node_w + 44)
            x1 = x0 + node_w
            y0 = cy - node_h / 2
            y1 = cy + node_h / 2

            bg_col = COLOR_SURFACE_2
            border_col = COLOR_BORDER
            if i in step.indices:
                bg_col = STATE_ACTIVE if step.action in ("insert_head", "insert_tail", "deleted") else STATE_SORTED
                border_col = "#34D399"

            # Data container
            self.canvas.create_rectangle(x0, y0, x1 - 22, y1, fill=bg_col, outline=border_col, width=2)
            self.canvas.create_text((x0 + x1 - 22)/2, cy, text=str(val), fill=COLOR_TEXT_PRIMARY, font=FONT_TITLE_4)

            # Pointer box
            self.canvas.create_rectangle(x1 - 22, y0, x1, y1, fill=COLOR_SURFACE_1, outline=border_col, width=2)
            self.canvas.create_text(x1 - 11, cy, text="•", fill=COLOR_TEXT_SECONDARY, font=FONT_TITLE_3)

            # Next arrow
            if i < len(nodes) - 1:
                next_x0 = x1
                next_x1 = x1 + 44
                self.canvas.create_line(next_x0, cy - (4 if is_doubly else 0), next_x1, cy - (4 if is_doubly else 0), fill=STATE_DEFAULT, width=2, arrow=tk.LAST)
                if is_doubly:
                    self.canvas.create_line(next_x1, cy + 4, next_x0, cy + 4, fill=STATE_SECONDARY, width=2, arrow=tk.LAST)
            else:
                self.canvas.create_text(x1 + 22, cy, text="NULL", fill=COLOR_TEXT_MUTED, font=FONT_CAPTION_1)

    def _draw_hash_table(self, step: Step, w: float, h: float):
        info = step.state if isinstance(step.state, dict) else {}
        cap = info.get("capacity", 7)
        table = info.get("table", [])
        mode = info.get("mode", "chaining")

        start_x = 80
        start_y = 50
        slot_w = 70
        slot_h = 36

        for i in range(cap):
            y0 = start_y + i * (slot_h + 8)
            y1 = y0 + slot_h

            bg_col = COLOR_SURFACE_2
            border_col = COLOR_BORDER
            if i in step.indices:
                bg_col = STATE_ACTIVE if step.action in ("chain_insert", "probe_insert") else STATE_COMPARE
                border_col = "#FBBF24"

            # Slot box
            self.canvas.create_rectangle(start_x, y0, start_x + slot_w, y1, fill=bg_col, outline=border_col, width=2)
            self.canvas.create_text(start_x + slot_w / 2, (y0 + y1) / 2, text=f"[{i}]", fill=COLOR_TEXT_PRIMARY, font=FONT_TITLE_4)

            # Render bucket items
            if i < len(table) and table[i] is not None:
                if mode == "chaining" and isinstance(table[i], list):
                    chain_x = start_x + slot_w + 24
                    for k, v in table[i]:
                        self.canvas.create_line(chain_x - 24, (y0 + y1)/2, chain_x, (y0 + y1)/2, fill=STATE_DEFAULT, width=2, arrow=tk.LAST)
                        bw = 90
                        self.canvas.create_rectangle(chain_x, y0, chain_x + bw, y1, fill=COLOR_SURFACE_1, outline=COLOR_BORDER)
                        self.canvas.create_text(chain_x + bw/2, (y0 + y1)/2, text=f"{k}: {v}", fill=COLOR_TEXT_PRIMARY, font=FONT_CAPTION_1)
                        chain_x += bw + 24
                elif mode == "linear_probing":
                    k, v = table[i]
                    self.canvas.create_text(start_x + slot_w + 60, (y0 + y1)/2, text=f"→ ({k}: {v})", fill=STATE_SORTED, font=FONT_TITLE_4)

    def _on_ds_completed(self):
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
        self._load_initial_data()

    def _on_speed_change(self, val):
        val_int = int(val)
        delay = max(10, 520 - val_int)
        self.engine.set_speed(delay)

