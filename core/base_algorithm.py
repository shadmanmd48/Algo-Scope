"""
AlgoScope Base Algorithm & Step Model
Defines the core contracts for real algorithm execution and snapshot generation.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class Step:
    """Represents an atomic execution step in an algorithm."""
    action: str                        # 'compare', 'swap', 'visit', 'highlight', 'rotate', etc.
    state: Any                         # Snapshot of the underlying data structure
    indices: List[Any] = field(default_factory=list) # Active indices or node IDs
    secondary_indices: List[Any] = field(default_factory=list) # Auxiliary pointers
    pseudocode_line: int = -1          # 0-indexed line to highlight in pseudocode viewer
    message: str = ""                  # Human-readable explanation of current operation
    metrics: Dict[str, Any] = field(default_factory=dict) # e.g. comparisons, swaps, height
    custom_colors: Dict[Any, str] = field(default_factory=dict) # Key -> Hex color override

@dataclass
class AlgorithmInfo:
    """Metadata, complexities, and pseudocode for an algorithm."""
    name: str
    category: str
    description: str
    best_time: str
    avg_time: str
    worst_time: str
    space_complexity: str
    pseudocode: List[str]
    use_cases: List[str]

