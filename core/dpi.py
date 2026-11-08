"""
AlgoScope High-DPI & Display Scaling Subsystem
Configures Windows High-DPI awareness and synchronizes Tkinter internal scaling
to ensure razor-sharp DirectWrite/ClearType font rendering and crisp 1:1 hardware pixel mapping.
"""

import sys
import os
import tkinter as tk
from typing import Tuple

_DPI_SCALE_FACTOR: float = 1.0
_DPI_AWARENESS_MODE: str = "unaware"

def setup_high_dpi() -> str:
    """
    Activates modern Windows High-DPI awareness BEFORE the Tkinter root window is instantiated.
    Completely eliminates Windows DWM bilinear bitmap stretching on 125%, 150%, 175%, and 200% displays.
    """
    global _DPI_AWARENESS_MODE
    if sys.platform != "win32":
        _DPI_AWARENESS_MODE = "non-windows"
        return _DPI_AWARENESS_MODE

    import ctypes

    # 1. Attempt Per-Monitor V2 (Windows 10 version 1703+ and Windows 11)
    # DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = -4
    try:
        user32 = ctypes.windll.user32
        if hasattr(user32, "SetProcessDpiAwarenessContext"):
            result = user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
            if result:
                _DPI_AWARENESS_MODE = "per_monitor_v2"
                return _DPI_AWARENESS_MODE
    except Exception:
        pass

    # 2. Attempt Per-Monitor V1 via Shcore (Windows 8.1 / Windows 10)
    try:
        shcore = ctypes.windll.shcore
        if hasattr(shcore, "SetProcessDpiAwareness"):
            # PROCESS_PER_MONITOR_DPI_AWARE = 2
            hr = shcore.SetProcessDpiAwareness(2)
            if hr == 0:
                _DPI_AWARENESS_MODE = "per_monitor_v1"
                return _DPI_AWARENESS_MODE
            # Fallback to PROCESS_SYSTEM_DPI_AWARE = 1
            hr = shcore.SetProcessDpiAwareness(1)
            if hr == 0:
                _DPI_AWARENESS_MODE = "system_aware"
                return _DPI_AWARENESS_MODE
    except Exception:
        pass

    # 3. Fallback to Windows Vista / 7 User32 API
    try:
        user32 = ctypes.windll.user32
        if hasattr(user32, "SetProcessDPIAware"):
            user32.SetProcessDPIAware()
            _DPI_AWARENESS_MODE = "system_legacy"
            return _DPI_AWARENESS_MODE
    except Exception:
        pass

    _DPI_AWARENESS_MODE = "unaware"
    return _DPI_AWARENESS_MODE


def configure_root_dpi(root: tk.Tk) -> float:
    """
    Synchronizes Tkinter's internal font points-to-pixels ratio with the hardware display DPI.
    Ensures that DirectWrite/ClearType font rasterization happens at the native pixel grid.
    Returns the display scale factor (1.0 = 100%, 1.25 = 125%, 1.5 = 150%, 2.0 = 200%).
    """
    global _DPI_SCALE_FACTOR
    if sys.platform != "win32":
        _DPI_SCALE_FACTOR = 1.0
        return _DPI_SCALE_FACTOR

    import ctypes

    try:
        # Determine physical screen DPI
        hdc = ctypes.windll.user32.GetDC(0)
        dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # 88 = LOGPIXELSX
        ctypes.windll.user32.ReleaseDC(0, hdc)

        if dpi > 0:
            _DPI_SCALE_FACTOR = dpi / 96.0
            target_tk_scaling = dpi / 72.0

            try:
                current_scaling = float(root.tk.call("tk", "scaling"))
                if abs(current_scaling - target_tk_scaling) > 0.05:
                    root.tk.call("tk", "scaling", target_tk_scaling)
            except Exception:
                root.tk.call("tk", "scaling", target_tk_scaling)
    except Exception:
        _DPI_SCALE_FACTOR = 1.0

    return _DPI_SCALE_FACTOR


def get_dpi_scale_factor() -> float:
    """Returns the active display scale factor relative to standard 96 DPI."""
    return _DPI_SCALE_FACTOR

