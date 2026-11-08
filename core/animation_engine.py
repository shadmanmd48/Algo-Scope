"""
AlgoScope Animation Engine
Provides non-blocking playback, step-by-step time travel, and timeline management.
"""

from typing import Callable, Generator, List, Optional
from core.base_algorithm import Step

class AnimationEngine:
    """
    Manages algorithm execution steps, playback state, and Tkinter scheduling.
    Allows forward and backward stepping through recorded history.
    """
    def __init__(self, root, on_render_callback: Callable[[Step], None], on_complete_callback: Optional[Callable[[], None]] = None):
        self.root = root
        self.on_render = on_render_callback
        self.on_complete = on_complete_callback

        self.steps: List[Step] = []
        self.current_index: int = -1
        self.generator: Optional[Generator[Step, None, None]] = None
        self.is_playing: bool = False
        self.speed_ms: int = 50  # Delay between steps in milliseconds
        self._scheduled_task = None
        self._is_completed: bool = False

    def load_generator(self, generator: Generator[Step, None, None], initial_step: Optional[Step] = None):
        """Reset and load a new algorithm step generator."""
        self.reset()
        self.generator = generator
        if initial_step:
            self.steps.append(initial_step)
            self.current_index = 0
            self.on_render(initial_step)
        else:
            # Advance to first step
            self.step_forward()

    def load_steps(self, steps: List[Step]):
        """Load pre-generated steps directly."""
        self.reset()
        self.steps = steps
        if self.steps:
            self.current_index = 0
            self.on_render(self.steps[0])

    def set_speed(self, speed_ms: int):
        """Set animation delay in milliseconds (10 to 1000 ms)."""
        self.speed_ms = max(5, int(speed_ms))

    def play(self):
        """Start or resume automatic step playback."""
        if self.is_playing:
            return
        if self._is_completed and self.current_index >= len(self.steps) - 1:
            # Reached end, reset to start or do nothing
            return
        self.is_playing = True
        self._tick()

    def pause(self):
        """Pause automatic playback."""
        self.is_playing = False
        if self._scheduled_task is not None:
            self.root.after_cancel(self._scheduled_task)
            self._scheduled_task = None

    def toggle_play_pause(self) -> bool:
        """Toggle playback and return new playing state."""
        if self.is_playing:
            self.pause()
            return False
        else:
            self.play()
            return True

    def _tick(self):
        """Single playback tick scheduled on Tkinter event loop."""
        if not self.is_playing:
            return

        has_more = self.step_forward()
        if has_more:
            self._scheduled_task = self.root.after(self.speed_ms, self._tick)
        else:
            self.pause()
            self._is_completed = True
            if self.on_complete:
                self.on_complete()

    def step_forward(self) -> bool:
        """Advance one step forward. Returns True if advanced, False if reached end."""
        # If we have buffered steps ahead in history, advance to the next one
        if self.current_index + 1 < len(self.steps):
            self.current_index += 1
            step = self.steps[self.current_index]
            self.on_render(step)
            return True

        # Otherwise pull next step from generator
        if self.generator is not None:
            try:
                next_step = next(self.generator)
                self.steps.append(next_step)
                self.current_index = len(self.steps) - 1
                self.on_render(next_step)
                return True
            except StopIteration:
                self._is_completed = True
                return False

        return False

    def step_backward(self) -> bool:
        """Move one step back in execution history."""
        self.pause()
        if self.current_index > 0:
            self.current_index -= 1
            step = self.steps[self.current_index]
            self.on_render(step)
            return True
        return False

    def reset(self):
        """Cancel scheduling and reset playback state."""
        self.pause()
        self.steps.clear()
        self.current_index = -1
        self.generator = None
        self._is_completed = False

    def jump_to_step(self, index: int):
        """Jump directly to a specific step index in recorded history."""
        self.pause()
        if not self.steps:
            return
        index = max(0, min(index, len(self.steps) - 1))
        self.current_index = index
        self.on_render(self.steps[self.current_index])

    @property
    def current_step(self) -> Optional[Step]:
        if 0 <= self.current_index < len(self.steps):
            return self.steps[self.current_index]
        return None

    @property
    def total_steps(self) -> int:
        return len(self.steps)

