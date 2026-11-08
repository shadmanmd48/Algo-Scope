"""
AlgoScope Visual System & Design Tokens
Strictly conforms to SKILL.md (Landing Page Design System).
"""

from core.dpi import setup_high_dpi, configure_root_dpi, get_dpi_scale_factor

# Initialize Windows High-DPI awareness at the earliest possible import
setup_high_dpi()

# B4. Dark Mode Background Colors (strictly these values)
COLOR_BLACK       = "#000000"  # Base background
COLOR_SURFACE_1   = "#181818"  # Card / container surface
COLOR_SURFACE_2   = "#1F1F1F"  # Elevated surface / inputs / navbar
COLOR_BORDER      = "#272727"  # Complete perimeter border
COLOR_BORDER_HOT  = "#313131"  # Active border / hover border
COLOR_WARM_DARK   = "#131209"  # Warm dark accent surface

# Foreground & Text Colors
COLOR_TEXT_PRIMARY   = "#FFFFFF"  # Primary reading text
COLOR_TEXT_SECONDARY = "#9B9B9B"  # Secondary copy / subheadings
COLOR_TEXT_MUTED     = "#666666"  # Captions / metadata / disabled text

# Hero Text Gradient
HERO_GRADIENT_START = "#FFFFFF"
HERO_GRADIENT_END   = "#9B9B9B"

# Algorithmic State Colors (High contrast against dark flat surfaces)
STATE_DEFAULT   = "#3B82F6"  # Sky Blue - idle elements
STATE_COMPARE   = "#F59E0B"  # Amber - comparisons / active checks
STATE_ACTIVE    = "#EF4444"  # Crimson - swaps / current target
STATE_SORTED    = "#10B981"  # Emerald - sorted / found / shortest path
STATE_VISITED   = "#8B5CF6"  # Purple - visited nodes / set members
STATE_SECONDARY = "#06B6D4"  # Cyan - secondary pointer / pivot / boundary
STATE_SPECIAL   = "#EC4899"  # Pink - balancing rotation / special marker

# B2. Spacing Scale Tokens
SPACING_0   = 0
SPACING_25  = 2
SPACING_50  = 4
SPACING_75  = 8
SPACING_100 = 12
SPACING_200 = 16
SPACING_300 = 24
SPACING_400 = 32
SPACING_500 = 40
SPACING_600 = 48
SPACING_700 = 64
SPACING_800 = 80
SPACING_900 = 96

# Main button padding per SKILL.md B2
BTN_PAD_Y = 8
BTN_PAD_X = 12

# B3. Corner Radius
RADIUS_FULL = 9999
RADIUS_2XL  = 24
RADIUS_XL   = 16
RADIUS_LG   = 12
RADIUS_MD   = 8
RADIUS_SM   = 4

def get_nested_radius(outer_radius: int, gap: int) -> int:
    """
    Nested radius formula per SKILL.md B3:
    inner radius = outer radius - gap (when gap < 32px and result > 2)
    """
    if gap < 32:
        inner = outer_radius - gap
        if inner > 2:
            return inner
    return outer_radius

# B1. Typography System
# Available font family: Manrope / Poppins / Segoe UI (Windows fallback)
FONT_PRIMARY = "Segoe UI"
FONT_CODE    = "Consolas"

# Named Text Styles (Exact size and weight per SKILL.md B1)
# Size snapped to Tailwind scale; Line height paired
FONT_HEADING_1 = (FONT_PRIMARY, 44, "bold")    # text-6xl adapted for desktop canvas
FONT_HEADING_2 = (FONT_PRIMARY, 36, "bold")    # text-5xl
FONT_HEADING_3 = (FONT_PRIMARY, 28, "bold")    # text-4xl
FONT_HEADING_4 = (FONT_PRIMARY, 22, "bold")    # text-3xl
FONT_HEADING_5 = (FONT_PRIMARY, 18, "bold")    # text-2xl
FONT_HEADING_6 = (FONT_PRIMARY, 15, "bold")    # text-xl

FONT_TITLE_1 = (FONT_PRIMARY, 15, "bold")      # text-xl Medium
FONT_TITLE_2 = (FONT_PRIMARY, 14, "bold")      # text-lg Medium
FONT_TITLE_3 = (FONT_PRIMARY, 12, "bold")      # text-base Medium
FONT_TITLE_4 = (FONT_PRIMARY, 11, "bold")      # text-sm Medium
FONT_TITLE_5 = (FONT_PRIMARY, 10, "bold")      # text-xs Medium

FONT_BODY_1 = (FONT_PRIMARY, 12, "bold")       # text-base Semibold
FONT_BODY_2 = (FONT_PRIMARY, 12, "bold")       # text-base Medium
FONT_BODY_3 = (FONT_PRIMARY, 12, "normal")     # text-base Regular
FONT_BODY_4 = (FONT_PRIMARY, 11, "bold")       # text-sm Semibold
FONT_BODY_5 = (FONT_PRIMARY, 11, "bold")       # text-sm Medium
FONT_BODY_6 = (FONT_PRIMARY, 11, "normal")     # text-sm Regular

FONT_BUTTON_LG  = (FONT_PRIMARY, 14, "bold")   # Button-lg
FONT_BUTTON_MD  = (FONT_PRIMARY, 12, "bold")   # Button-md
FONT_BUTTON_SM  = (FONT_PRIMARY, 11, "bold")   # Button-sm
FONT_BUTTON_XSM = (FONT_PRIMARY, 10, "bold")   # Button-Xsm

FONT_CAPTION_1 = (FONT_PRIMARY, 11, "bold")    # Caption 1
FONT_CAPTION_2 = (FONT_PRIMARY, 11, "normal")  # Caption 2
FONT_CAPTION_3 = (FONT_PRIMARY, 10, "bold")    # Caption 3
FONT_CAPTION_4 = (FONT_PRIMARY, 10, "bold")    # Caption 4
FONT_CAPTION_5 = (FONT_PRIMARY, 10, "normal")  # Caption 5

FONT_CODE_MD = (FONT_CODE, 11, "normal")
FONT_CODE_SM = (FONT_CODE, 10, "normal")

def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    clean = hex_str.lstrip("#")
    if len(clean) == 3:
        clean = "".join([c * 2 for c in clean])
    return int(clean[0:2], 16), int(clean[2:4], 16), int(clean[4:6], 16)

def interpolate_color(c1: str, c2: str, t: float) -> str:
    """Interpolate between two hex colors."""
    t = max(0.0, min(1.0, t))
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"
