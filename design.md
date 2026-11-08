# AlgoScope Design System & Specifications

This document defines the visual design system, color palette, typography, spacing tokens, component specifications, and interaction guidelines for **AlgoScope – Interactive DSA & Algorithm Visualizer**.

---

## 1. Design Philosophy & Direction

- **Theme**: Refined Dark Mode — Modern, professional, sleek, and focused on educational clarity.
- **Surface Architecture**: Pure flat dark surfaces (`#000000`, `#181818`, `#1F1F1F`, `#272727`, `#313131`) with complete perimeter borders. No partial borders, no background gradients.
- **Visual Hierarchy**: High contrast between background, structural containers, and algorithmic visualization states.
- **Clarity First**: Every data structure and algorithm visualization is clean, well-spaced, and driven by real execution data.

---

## 2. Color Palette

### Base & Surface Colors
| Token | Hex Value | Usage |
|---|---|---|
| `BG_BASE` | `#000000` | Deep application background |
| `BG_SURFACE` | `#181818` | Primary surface: cards, sidebars, main panels |
| `BG_ELEVATED` | `#1F1F1F` | Elevated cards, modal dialogs, top nav |
| `BORDER_MUTED` | `#272727` | Subtle card borders, dividers, grid lines |
| `BORDER_HOVER` | `#313131` | Hover states, active borders, focused outlines |
| `BG_WARM_DARK` | `#131209` | Accent highlight background container |

### Typography & Foreground Colors
| Token | Hex Value | Usage |
|---|---|---|
| `TEXT_PRIMARY` | `#FFFFFF` | Primary headings, active labels, critical values |
| `TEXT_SECONDARY` | `#9B9B9B` | Subheadings, descriptions, metrics labels |
| `TEXT_MUTED` | `#666666` | Helper text, disabled states, timestamps |
| `HERO_TEXT_GRADIENT_START` | `#FFFFFF` | Hero heading text gradient start |
| `HERO_TEXT_GRADIENT_END` | `#9B9B9B` | Hero heading text gradient end |

### Algorithmic Visualization Palette
| State | Hex Value | Meaning |
|---|---|---|
| `STATE_DEFAULT` | `#3B82F6` | Default elements, unvisited nodes/bars (Sky Blue) |
| `STATE_COMPARE` | `#F59E0B` | Active comparison / inspection (Amber) |
| `STATE_ACTIVE` | `#EF4444` | Current swap / write / target match (Crimson Red) |
| `STATE_SORTED` | `#10B981` | Fully sorted / found / confirmed shortest path (Emerald Green) |
| `STATE_VISITED` | `#8B5CF6` | Visited nodes / explored boundary (Purple) |
| `STATE_SECONDARY` | `#06B6D4` | Secondary pointer / pivot element (Cyan) |

---

## 3. Typography Scale & Named Styles

Default family: `"Segoe UI"`, `"Manrope"`, `"DejaVu Sans"`, sans-serif.  
Code / Monospace: `"Consolas"`, `"Courier New"`, monospace.  
*Rule: No italics anywhere in the interface. Cap font weight at bold/semibold.*

| Style Name | Font Size | Weight | Line Height | Usage |
|---|---|---|---|---|
| `Heading 1` | 36px (or 40px) | Bold | 1.2 | Landing hero main heading |
| `Heading 2` | 28px | Bold | 1.2 | Major section headers, module titles |
| `Heading 3` | 22px | Bold | 1.25 | Subsection titles, card group headers |
| `Heading 4` | 18px | Semibold | 1.3 | Panel titles, modal headings |
| `Title 1` | 16px | Bold | 1.3 | Card titles, primary navigation |
| `Title 2` | 14px | Bold | 1.4 | Metric headers, control labels |
| `Body 1` | 14px | Regular | 1.5 | Explanations, descriptive copy |
| `Body 2` | 12px | Regular | 1.5 | Secondary copy, instructions |
| `Button-lg` | 15px | Bold | 1.0 | Primary CTA buttons |
| `Button-md` | 13px | Semibold | 1.0 | Standard controls (Play, Pause, Step) |
| `Button-sm` | 11px | Semibold | 1.0 | Compact toolbar buttons, badges |
| `Caption` | 10px / 11px | Regular | 1.4 | Badges, footnotes, status tags |
| `Code` | 12px | Regular | 1.4 | Pseudocode viewer, complexity notation |

---

## 4. Spacing System

Only use the following discrete spacing values:
- `Spacing-0`: 0px
- `Spacing-25`: 2px
- `Spacing-50`: 4px
- `Spacing-75`: 8px
- `Spacing-100`: 12px
- `Spacing-200`: 16px
- `Spacing-300`: 24px
- `Spacing-400`: 32px
- `Spacing-500`: 40px
- `Spacing-600`: 48px
- `Spacing-700`: 64px
- `Spacing-800`: 80px
- `Spacing-900`: 96px

**Button Padding**:
- Main CTA Button: 10px vertical, 20px horizontal
- Standard Control Button: 8px vertical, 14px horizontal
- Compact Button: 6px vertical, 10px horizontal

---

## 5. Corner Radii & Borders

- **Outer Cards**: 12px radius (`rounded-xl`)
- **Inner Elements**: $\text{inner radius} = \text{outer radius} - \text{gap}$ when gap $< 32\text{px}$ and result $> 2\text{px}$.
- **Pill Badges**: Full radius (16px)
- **Borders**: Continuous 1px perimeter border (`#272727` resting, `#313131` hover/active). Never single-sided borders.

---

## 6. Component Specs

### Primary Button
- Background: `#FFFFFF`
- Foreground: `#000000`
- Hover: `#E0E0E0`
- Active: `#C8C8C8`
- Font: Semibold / Bold

### Secondary / Ghost Button
- Background: `#1F1F1F`
- Border: `#272727`
- Foreground: `#FFFFFF`
- Hover: Background `#272727`, Border `#313131`
- Active: Background `#313131`

### Accent / Action Button (Play / Execute)
- Background: `#10B981` (Emerald) or `#3B82F6` (Sky Blue)
- Foreground: `#FFFFFF`
- Hover: Brightness +10%

### Cards
- Background: `#181818`
- Border: 1px `#272727`
- Hover: Border `#3B82F6` or `#313131` with subtle lift

---

## 7. Layout Hierarchy

1. **Landing Page**:
   - Floating Navbar (Logo, Links, "Get Started" CTA)
   - Hero Section (Outcome heading, Subtitle, 2 CTAs, Live Tkinter Canvas sorting preview)
   - Live Preview Section (Interactive preview cards for Sorting, Graphs, Trees)
   - Features Grid (6 Core Modules)
   - "Why AlgoScope" Value Section
   - Final CTA Banner ("Ready to Explore Algorithms?")
2. **Dashboard**:
   - Left Sidebar (Branding, Module Navigation, Home link, Stats)
   - Main Canvas Area (Breadcrumb header, module cards with quick launch, metrics)
3. **Module Visualizer**:
   - Header Bar (Module Title, Algorithm Selector, Preset Buttons)
   - Visualization Canvas (Responsive, high-frame-rate rendering)
   - Control Bar (Play, Pause, Step Back, Step Forward, Reset, Speed Slider, Custom Input)
   - Information Drawer (Status indicator, Comparison/Swap counters, Pseudocode step-highlighter, Time & Space Complexity cards)

