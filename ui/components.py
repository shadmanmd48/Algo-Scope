"""
AlgoScope UI Components
Reusable widgets strictly adhering to SKILL.md:
- Flat surfaces (#000000, #181818, #1F1F1F, #272727, #313131)
- Continuous perimeter borders (no single-sided borders)
- Hover, active, focus, disabled states
- Discrete spacing and padding (8px Y, 12px X for buttons)
"""

import tkinter as tk
from tkinter import ttk, font
from typing import Callable, Optional, List, Dict, Any
from core.theme import (
    COLOR_BLACK, COLOR_SURFACE_1, COLOR_SURFACE_2, COLOR_BORDER, COLOR_BORDER_HOT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    FONT_BUTTON_MD, FONT_BUTTON_SM, FONT_BUTTON_LG, FONT_BODY_6, FONT_TITLE_3,
    FONT_CODE_SM, FONT_CAPTION_1, BTN_PAD_X, BTN_PAD_Y, RADIUS_MD, RADIUS_LG
)

class StyledButton(tk.Frame):
    """
    Polished custom button matching SKILL.md specifications:
    - Flat background
    - Complete perimeter border
    - Distinct Hover and Active states
    - Correct padding (8px Y, 12px X)
    - Fully accessible via keyboard focus and return key
    """
    def __init__(
        self,
        master,
        text: str,
        command: Optional[Callable[[], None]] = None,
        variant: str = "secondary",  # 'primary', 'secondary', 'accent', 'danger'
        size: str = "md",            # 'sm', 'md', 'lg'
        width: Optional[int] = None,
        **kwargs
    ):
        # Choose styling tokens based on variant
        if variant == "primary":
            self.bg_idle = "#FFFFFF"
            self.bg_hover = "#E5E5E5"
            self.bg_active = "#CCCCCC"
            self.fg = "#000000"
            self.border_idle = "#FFFFFF"
            self.border_hover = "#E5E5E5"
        elif variant == "accent":
            self.bg_idle = "#10B981"
            self.bg_hover = "#059669"
            self.bg_active = "#047857"
            self.fg = "#FFFFFF"
            self.border_idle = "#10B981"
            self.border_hover = "#059669"
        elif variant == "danger":
            self.bg_idle = "#EF4444"
            self.bg_hover = "#DC2626"
            self.bg_active = "#B91C1C"
            self.fg = "#FFFFFF"
            self.border_idle = "#EF4444"
            self.border_hover = "#DC2626"
        else:  # secondary (default dark surface button)
            self.bg_idle = COLOR_SURFACE_2
            self.bg_hover = "#272727"
            self.bg_active = "#313131"
            self.fg = COLOR_TEXT_PRIMARY
            self.border_idle = COLOR_BORDER
            self.border_hover = COLOR_BORDER_HOT

        super().__init__(
            master,
            bg=self.border_idle,
            padx=1,
            pady=1,
            cursor="hand2",
            **kwargs
        )

        font = FONT_BUTTON_MD
        padx = BTN_PAD_X
        pady = BTN_PAD_Y
        if size == "sm":
            font = FONT_BUTTON_SM
            padx = 8
            pady = 5
        elif size == "lg":
            font = FONT_BUTTON_LG
            padx = 20
            pady = 10

        self.inner = tk.Label(
            self,
            text=text,
            bg=self.bg_idle,
            fg=self.fg,
            font=font,
            padx=padx,
            pady=pady
        )
        if width is not None:
            self.inner.config(width=width)
        self.inner.pack(fill="both", expand=True)

        self.command = command
        self._disabled = False

        # Bind events for hover and click
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

        self.inner.bind("<Enter>", self._on_enter)
        self.inner.bind("<Leave>", self._on_leave)
        self.inner.bind("<Button-1>", self._on_press)
        self.inner.bind("<ButtonRelease-1>", self._on_release)

    def _on_enter(self, _):
        if not self._disabled:
            self.config(bg=self.border_hover)
            self.inner.config(bg=self.bg_hover)

    def _on_leave(self, _):
        if not self._disabled:
            self.config(bg=self.border_idle)
            self.inner.config(bg=self.bg_idle)

    def _on_press(self, _):
        if not self._disabled:
            self.inner.config(bg=self.bg_active)

    def _on_release(self, _):
        if not self._disabled:
            self.inner.config(bg=self.bg_hover)
            if self.command:
                self.command()

    def set_text(self, text: str):
        self.inner.config(text=text)

    def set_enabled(self, enabled: bool):
        self._disabled = not enabled
        if self._disabled:
            self.inner.config(fg=COLOR_TEXT_MUTED, cursor="arrow")
            self.config(cursor="arrow")
        else:
            self.inner.config(fg=self.fg, cursor="hand2")
            self.config(cursor="hand2")


class CardFrame(tk.Frame):
    """
    Card container adhering to B4:
    - Flat surface #181818
    - Perimeter border #272727 on all 4 sides
    """
    def __init__(self, master, bg: str = COLOR_SURFACE_1, border_color: str = COLOR_BORDER, **kwargs):
        super().__init__(
            master,
            bg=border_color,
            padx=1,
            pady=1,
            **kwargs
        )
        self.body = tk.Frame(self, bg=bg)
        self.body.pack(fill="both", expand=True)


class Badge(tk.Frame):
    """Small status or metric tag."""
    def __init__(self, master, text: str, bg_color: str = COLOR_SURFACE_2, fg_color: str = COLOR_TEXT_PRIMARY, **kwargs):
        super().__init__(master, bg=COLOR_BORDER, padx=1, pady=1, **kwargs)
        self.label = tk.Label(
            self,
            text=text,
            bg=bg_color,
            fg=fg_color,
            font=FONT_CAPTION_1,
            padx=6,
            pady=2
        )
        self.label.pack()

    def set_text(self, text: str):
        self.label.config(text=text)


class LabeledEntry(tk.Frame):
    """A clean dark-themed text entry with label."""
    def __init__(self, master, label_text: str, initial_value: str = "", width: int = 15, **kwargs):
        super().__init__(master, bg=COLOR_SURFACE_1, **kwargs)

        self.label = tk.Label(
            self,
            text=label_text,
            bg=COLOR_SURFACE_1,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_BODY_6
        )
        self.label.pack(anchor="w", pady=(0, 4))

        self.entry_frame = tk.Frame(self, bg=COLOR_BORDER, padx=1, pady=1)
        self.entry_frame.pack(fill="x")

        self.entry = tk.Entry(
            self.entry_frame,
            bg=COLOR_SURFACE_2,
            fg=COLOR_TEXT_PRIMARY,
            insertbackground=COLOR_TEXT_PRIMARY,
            font=FONT_TITLE_3,
            relief="flat",
            width=width
        )
        self.entry.insert(0, initial_value)
        self.entry.pack(fill="x", ipady=4, padx=4)

        self.entry.bind("<FocusIn>", lambda _: self.entry_frame.config(bg=COLOR_BORDER_HOT))
        self.entry.bind("<FocusOut>", lambda _: self.entry_frame.config(bg=COLOR_BORDER))

    def get_value(self) -> str:
        return self.entry.get().strip()

    def set_value(self, val: str):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(val))


class CanvasHelper:
    """Helper utilities for manual drawing on Tkinter Canvas."""
    @staticmethod
    def draw_rounded_rect(
        canvas: tk.Canvas,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        radius: float = 8,
        fill: str = "",
        outline: str = "",
        width: int = 1,
        tags: str = ""
    ):
        """Draw smooth rounded rectangle polygon."""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return canvas.create_polygon(
            points,
            smooth=True,
            fill=fill,
            outline=outline,
            width=width,
            tags=tags
        )


class SlidingPillNav(tk.Canvas):
    """
    Floating segmented capsule navigation with smooth sliding pill animation.
    Accurately reproduces modern capsule pill tabs (e.g. Apple, Vercel, Linear).
    - Dark capsule background with 1px continuous perimeter border.
    - Pure white active pill that smoothly glides with ease-out interpolation.
    - Active text turns deep black (#0A0A0A) as the pill slides under it.
    - Inactive text is muted cool gray (#8E8E93), with hover highlight (#FFFFFF).
    """
    def __init__(
        self,
        master,
        items: List[str],
        initial_index: int = 0,
        on_select: Optional[Callable[[int, str], None]] = None,
        height: int = 40,
        bg_parent: str = COLOR_SURFACE_1,
        bg_container: str = "#141414",
        border_color: str = "#2C2C2C",
        pill_color: str = "#FFFFFF",
        text_active_color: str = "#0A0A0A",
        text_inactive_color: str = "#8E8E93",
        text_hover_color: str = "#FFFFFF",
        padding_x: int = 18,
        font_size: int = 10,
        **kwargs
    ):
        self.items = items
        self.on_select = on_select
        self.height = height
        self.bg_parent = bg_parent
        self.bg_container = bg_container
        self.border_color = border_color
        self.pill_color = pill_color
        self.text_active_color = text_active_color
        self.text_inactive_color = text_inactive_color
        self.text_hover_color = text_hover_color
        self.padding_x = padding_x

        self.f_bold = font.Font(family="Segoe UI", size=font_size, weight="bold")
        self.f_norm = font.Font(family="Segoe UI", size=font_size, weight="normal")

        # Compute slot widths
        self.slots: List[Dict[str, Any]] = []
        cur_x = 4.0
        for it in items:
            tw = self.f_norm.measure(it)
            w = max(tw + 2 * padding_x, 46.0)
            self.slots.append({
                "name": it,
                "x1": cur_x,
                "x2": cur_x + w,
                "w": w,
                "cx": cur_x + w / 2.0
            })
            cur_x += w + 2.0
        self.total_w = int(cur_x + 2.0)

        super().__init__(
            master,
            width=self.total_w,
            height=self.height,
            bg=self.bg_parent,
            highlightthickness=0,
            **kwargs
        )

        self.selected_idx = max(0, min(initial_index, len(items) - 1)) if items else 0
        self.hovered_idx: Optional[int] = None

        if self.slots:
            self.cur_x = float(self.slots[self.selected_idx]["x1"])
            self.cur_w = float(self.slots[self.selected_idx]["w"])
        else:
            self.cur_x = 4.0
            self.cur_w = 40.0

        self.target_x = self.cur_x
        self.target_w = self.cur_w
        self.is_animating = False
        self._anim_id: Optional[str] = None

        # Bindings
        self.bind("<Motion>", self._on_motion)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

        self._render()

    def _get_slot_at_x(self, x: float) -> Optional[int]:
        for idx, s in enumerate(self.slots):
            if s["x1"] <= x <= s["x2"]:
                return idx
        return None

    def _on_motion(self, event):
        idx = self._get_slot_at_x(event.x)
        if idx != self.hovered_idx:
            self.hovered_idx = idx
            self.config(cursor="hand2" if idx is not None else "arrow")
            self._render()

    def _on_leave(self, event):
        if self.hovered_idx is not None:
            self.hovered_idx = None
            self._render()

    def _on_click(self, event):
        idx = self._get_slot_at_x(event.x)
        if idx is not None:
            self.set_selected_index(idx, trigger_callback=True, animate=True)

    def set_selected_index(self, idx: int, trigger_callback: bool = False, animate: bool = True):
        if 0 <= idx < len(self.slots):
            if idx == self.selected_idx and not self.is_animating:
                return
            self.selected_idx = idx
            self.target_x = float(self.slots[idx]["x1"])
            self.target_w = float(self.slots[idx]["w"])

            if not animate:
                self.cur_x = self.target_x
                self.cur_w = self.target_w
                self._render()
            else:
                self._start_animation()

            if trigger_callback and self.on_select:
                self.on_select(idx, self.slots[idx]["name"])

    def select_by_name(self, name: str, trigger_callback: bool = False, animate: bool = True):
        for idx, s in enumerate(self.slots):
            if s["name"].lower() == name.lower():
                self.set_selected_index(idx, trigger_callback=trigger_callback, animate=animate)
                break

    def _start_animation(self):
        if self._anim_id is not None:
            try:
                self.after_cancel(self._anim_id)
            except Exception:
                pass
            self._anim_id = None
        self.is_animating = True
        self._step_animation()

    def _step_animation(self):
        if not self.winfo_exists():
            return

        dx = self.target_x - self.cur_x
        dw = self.target_w - self.cur_w

        if abs(dx) < 0.6 and abs(dw) < 0.6:
            self.cur_x = self.target_x
            self.cur_w = self.target_w
            self.is_animating = False
            self._anim_id = None
            self._render()
        else:
            self.cur_x += dx * 0.32
            self.cur_w += dw * 0.32
            self._render()
            self._anim_id = self.after(16, self._step_animation)

    def _render(self):
        self.delete("all")
        h = self.height
        w = self.total_w
        r = (h - 4) / 2.0

        # Outer capsule container fill
        self.create_arc(2, 2, 2 + 2 * r, h - 2, start=90, extent=180, fill=self.bg_container, outline="", style="pieslice")
        self.create_arc(w - 2 - 2 * r, 2, w - 2, h - 2, start=270, extent=180, fill=self.bg_container, outline="", style="pieslice")
        self.create_rectangle(2 + r - 0.5, 2, w - 2 - r + 0.5, h - 2, fill=self.bg_container, outline="")

        # 1px perimeter outline without internal seam lines
        if self.border_color:
            self.create_arc(2, 2, 2 + 2 * r, h - 2, start=90, extent=180, outline=self.border_color, width=1, style="arc")
            self.create_arc(w - 2 - 2 * r, 2, w - 2, h - 2, start=270, extent=180, outline=self.border_color, width=1, style="arc")
            self.create_line(2 + r, 2, w - 2 - r, 2, fill=self.border_color, width=1)
            self.create_line(2 + r, h - 2, w - 2 - r, h - 2, fill=self.border_color, width=1)

        # Sliding white active pill snapped to integer pixel grid
        pr = (h - 8) / 2.0
        px1 = round(self.cur_x)
        px2 = round(self.cur_x + self.cur_w)
        if px2 - px1 >= 2 * pr:
            self.create_arc(px1, 4, px1 + 2 * pr, h - 4, start=90, extent=180, fill=self.pill_color, outline="", style="pieslice")
            self.create_arc(px2 - 2 * pr, 4, px2, h - 4, start=270, extent=180, fill=self.pill_color, outline="", style="pieslice")
            self.create_rectangle(px1 + pr - 0.5, 4, px2 - pr + 0.5, h - 4, fill=self.pill_color, outline="")

        # Crisp centered text labels snapped to integer coordinates
        center_y = round(h / 2.0)
        for idx, s in enumerate(self.slots):
            is_active = (px1 <= s["cx"] <= px2)
            if is_active:
                fg = self.text_active_color
                f = self.f_bold
            else:
                if idx == self.hovered_idx:
                    fg = self.text_hover_color
                else:
                    fg = self.text_inactive_color
                f = self.f_norm

            self.create_text(round(s["cx"]), center_y, text=s["name"], fill=fg, font=f, anchor="center")


