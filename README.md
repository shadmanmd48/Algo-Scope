# AlgoScope – Interactive DSA & Algorithm Visualizer

A professional desktop application built with Python and Tkinter designed to help students, educators, and engineers understand how Data Structures and Algorithms work internally through real-time, step-by-step visualizations driven by actual algorithm execution.

---

## Highlights & Capabilities

- **100% Real Algorithm Execution**: No prewritten or fake animations. Every visual state is driven by genuine algorithmic generators yielding snapshots of memory, pointers, and comparisons.
- **Strict Visual Design System**: Adheres strictly to the dark mode design tokens:
  - Base flat surfaces: `#000000`, `#181818`, `#1F1F1F`, `#272727`, `#313131`, `#131209`
  - Strict type scale and discrete spacing tokens
  - Perimeter borders (continuous 1px all the way around)
  - Interactive states for every button and card
- **Zero External Dependencies**: Built entirely with Python's standard library and native Tkinter (no PyQt, no Matplotlib, no Pygame, no Pillow). Runs 100% locally and offline.
- **Time Travel & Timeline Scrubbing**: Full Play, Pause, Resume, Step Forward, Step Backward, and dynamic Speed Control.
- **Synchronized Pseudocode Highlighter**: Follows the active executing line of pseudocode with explanation banners and asymptotic complexities (Best, Average, Worst, and Space).

---

## Application Navigation Flow

```
Landing Page
   │
   ▼
[Get Started / Start Exploring]
   │
   ▼
Main Dashboard
   │
   ├── Module 1: Sorting Visualizer
   ├── Module 2: Searching Visualizer
   ├── Module 3: Graph Visualizer
   ├── Module 4: Tree Visualizer
   ├── Module 5: Data Structure Visualizer
   └── Module 6: Performance Analyzer
```

---

## Core Modules

### 1. Sorting Visualizer
- **Algorithms**: Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, Quick Sort, Heap Sort.
- **Features**:
  - Live animated bar heights on Tkinter Canvas.
  - Active color highlights for comparisons (Amber), swaps (Crimson), pivots (Cyan), and sorted subarrays (Emerald Green).
  - Array size slider (8 to 50 elements) and custom comma-separated array input.
  - Ascending and Descending order toggle.
  - Real comparison counter and swap / write counter.

### 2. Searching Visualizer
- **Algorithms**: Linear Search, Binary Search, Jump Search, Interpolation Search.
- **Features**:
  - Target value input with instant search space division.
  - Step-by-step element probing with Low/High interval boundary indicators.
  - Automatic sorted array validation and notice banner for Binary, Jump, and Interpolation searches.
  - Exact comparison counters and target match highlights.

### 3. Graph Visualizer
- **Algorithms**: Breadth First Search (BFS), Depth First Search (DFS), Dijkstra's Algorithm, A* Search, Prim's Algorithm, Kruskal's Algorithm.
- **Features**:
  - Fully interactive Canvas: click empty space to create nodes, click two nodes to create weighted edges, drag nodes to adjust topology.
  - Preloaded network presets ("Classic Network", "Ring / Mesh").
  - Source and destination endpoint selector.
  - Highlights traversal paths, visited frontiers, shortest paths, and minimum spanning trees (MST) with total cost readouts.

### 4. Tree Visualizer
- **Structures & Traversals**:
  - Binary Search Tree (BST)
  - Self-Balancing AVL Tree
  - Traversals: Inorder, Preorder, Postorder, Level Order.
- **Features**:
  - Dynamic recursive tree layout calculation ensuring clean child node spacing.
  - Live AVL balance factor calculation ($bf = \text{height}(L) - \text{height}(R)$).
  - Demonstrates LL, RR, LR, and RL rotations in real time.
  - Node insertion, search, and two-child deletion with inorder successor relocation.

### 5. Data Structure Visualizer
- **Structures**:
  - **Stack (LIFO)**: Push, Pop, Peek, Overflow / Underflow indicators.
  - **Queue (FIFO)**: Enqueue, Dequeue, Front and Rear indicators.
  - **Circular Queue**: Ring buffer with modular index wrapping and pointer synchronization.
  - **Linked List**: Singly and Doubly linked modes with pointer navigation arrows and Null terminators.
  - **Hash Table**: Separate Chaining (linked buckets) and Linear Probing (open addressing collision resolution).

### 6. Performance Analyzer
- **Real Benchmarking**: Executes actual sorting algorithms on random arrays of custom sizes (50, 100, 250, 500, 1000).
- **Comparative Canvas Charts**:
  - Wall-clock runtime bar charts measured in milliseconds (`time.perf_counter()`).
  - Total comparisons and swaps comparison.
  - Toggle between runtime and operations count.

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `Space` | Play / Pause visualization playback |
| `Right Arrow` | Step forward 1 step in execution |
| `Left Arrow` | Step backward 1 step in execution history |

---

## Project Structure

```
AlgoScope/
│
├── design.md                      # Formalized design tokens from SKILL.md
├── main.py                        # Application entry point & screen orchestrator
├── requirements.txt               # Dependencies (standard library only)
├── test_algoscope.py              # Unit & integration test suite
├── README.md                      # Complete documentation
│
├── core/
│   ├── theme.py                   # Design tokens: palette, fonts, spacing, radius
│   ├── base_algorithm.py          # Step dataclass & algorithm contract
│   └── animation_engine.py        # Event loop scheduler & timeline scrubber
│
├── ui/
│   ├── components.py              # StyledButton, CardFrame, Badge, LabeledEntry
│   ├── sidebar.py                 # Persistent sidebar navigation & metrics
│   ├── dashboard.py               # Main Dashboard with module cards
│   └── landing_page.py            # Landing page with live hero sorting canvas
│
├── visualizers/
│   ├── base_visualizer.py         # Base layout: controls, pseudocode, complexities
│   ├── sorting_view.py            # Sorting Canvas
│   ├── searching_view.py          # Searching Canvas
│   ├── graph_view.py              # Interactive Graph Canvas
│   ├── tree_view.py               # Tree Canvas (BST & AVL)
│   ├── data_structure_view.py     # Data Structures Canvas
│   └── performance_view.py        # Real-time multi-algorithm benchmark charts
│
├── algorithms/
│   ├── sorting.py                 # Bubble, Selection, Insertion, Merge, Quick, Heap
│   ├── searching.py               # Linear, Binary, Jump, Interpolation
│   ├── graphs.py                  # BFS, DFS, Dijkstra, A*, Prim, Kruskal
│   ├── trees.py                   # BST & AVL insertion, deletion, rotations
│   ├── data_structures.py         # Stack, Queue, Circular Queue, Lists, Hash Table
│   └── benchmarks.py              # Non-simulated wall-clock benchmark profiler
│
└── data/
    └── algorithm_info.py          # Pseudocode lines, complexities & use cases
```

---

## Installation & Running

AlgoScope requires **Python 3.10+** with Tkinter (included with standard Python installations on Windows, macOS, and Linux).

1. Clone or download the repository to your local machine:
   ```bash
   cd "Algo Scope"
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Run the test suite:
   ```bash
   python test_algoscope.py
   ```

---

## License

MIT License. Designed and developed for computer science students and educators.

