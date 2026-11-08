"""
AlgoScope Educational Database
Contains accurate pseudocode, complexities, descriptions, and use cases for all algorithms.
"""

from typing import Dict
from core.base_algorithm import AlgorithmInfo

ALGORITHM_DATA: Dict[str, AlgorithmInfo] = {
    # ------------------ SORTING ------------------
    "Bubble Sort": AlgorithmInfo(
        name="Bubble Sort",
        category="Sorting",
        description="Repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order.",
        best_time="O(n)",
        avg_time="O(n²)",
        worst_time="O(n²)",
        space_complexity="O(1)",
        pseudocode=[
            "for i = 0 to n - 1:",
            "    swapped = false",
            "    for j = 0 to n - i - 2:",
            "        if arr[j] > arr[j + 1]:",
            "            swap(arr[j], arr[j + 1])",
            "            swapped = true",
            "    if not swapped: break"
        ],
        use_cases=[
            "Educational tool for introducing sorting concepts",
            "Detecting nearly-sorted lists with early termination",
            "Embedded systems where code footprint must be minimal"
        ]
    ),
    "Selection Sort": AlgorithmInfo(
        name="Selection Sort",
        category="Sorting",
        description="Divides the input list into a sorted and unsorted region, continuously finding the minimum element in the unsorted region and placing it at the beginning.",
        best_time="O(n²)",
        avg_time="O(n²)",
        worst_time="O(n²)",
        space_complexity="O(1)",
        pseudocode=[
            "for i = 0 to n - 1:",
            "    min_idx = i",
            "    for j = i + 1 to n - 1:",
            "        if arr[j] < arr[min_idx]:",
            "            min_idx = j",
            "    if min_idx != i:",
            "        swap(arr[i], arr[min_idx])"
        ],
        use_cases=[
            "Small arrays where simplicity is preferred",
            "Systems where memory write operations are extremely costly (minimizes swaps to O(n))",
            "Checking memory integrity without auxiliary buffers"
        ]
    ),
    "Insertion Sort": AlgorithmInfo(
        name="Insertion Sort",
        category="Sorting",
        description="Builds the final sorted array one item at a time by consuming one element from unsorted input and inserting it into its correct position among previously sorted elements.",
        best_time="O(n)",
        avg_time="O(n²)",
        worst_time="O(n²)",
        space_complexity="O(1)",
        pseudocode=[
            "for i = 1 to n - 1:",
            "    key = arr[i]",
            "    j = i - 1",
            "    while j >= 0 and arr[j] > key:",
            "        arr[j + 1] = arr[j]",
            "        j = j - 1",
            "    arr[j + 1] = key"
        ],
        use_cases=[
            "Small data sets (< 50 elements) due to low overhead",
            "Subroutine in hybrid algorithms (e.g. Timsort, Introsort)",
            "Online sorting where data is received incrementally"
        ]
    ),
    "Merge Sort": AlgorithmInfo(
        name="Merge Sort",
        category="Sorting",
        description="A divide-and-conquer algorithm that recursively splits an array in halves until subarrays have 1 element, then merges sorted subarrays in linear time.",
        best_time="O(n log n)",
        avg_time="O(n log n)",
        worst_time="O(n log n)",
        space_complexity="O(n)",
        pseudocode=[
            "function mergeSort(arr, l, r):",
            "    if l < r:",
            "        mid = (l + r) // 2",
            "        mergeSort(arr, l, mid)",
            "        mergeSort(arr, mid + 1, r)",
            "        merge(arr, l, mid, r)"
        ],
        use_cases=[
            "Guaranteed O(n log n) sorting where worst-case predictability matters",
            "Sorting linked lists without extra random access overhead",
            "External sorting for massive datasets that do not fit in RAM"
        ]
    ),
    "Quick Sort": AlgorithmInfo(
        name="Quick Sort",
        category="Sorting",
        description="Selects a 'pivot' element and partitions array so elements smaller than pivot are on left and larger on right, then recursively sorts partitions.",
        best_time="O(n log n)",
        avg_time="O(n log n)",
        worst_time="O(n²)",
        space_complexity="O(log n)",
        pseudocode=[
            "function quickSort(arr, low, high):",
            "    if low < high:",
            "        pi = partition(arr, low, high)",
            "        quickSort(arr, low, pi - 1)",
            "        quickSort(arr, pi + 1, high)",
            "function partition(arr, low, high):",
            "    pivot = arr[high]; i = low - 1",
            "    for j = low to high - 1:",
            "        if arr[j] < pivot: i++; swap(arr[i], arr[j])",
            "    swap(arr[i + 1], arr[high]); return i + 1"
        ],
        use_cases=[
            "General-purpose in-memory sorting (C qsort, standard libraries)",
            "High cache locality making it faster in practice than Merge Sort",
            "Graphics rendering and spatial partitioning"
        ]
    ),
    "Heap Sort": AlgorithmInfo(
        name="Heap Sort",
        category="Sorting",
        description="Converts the input array into a binary max-heap, then repeatedly extracts the maximum root element and places it at the end of the array, restoring the heap property.",
        best_time="O(n log n)",
        avg_time="O(n log n)",
        worst_time="O(n log n)",
        space_complexity="O(1)",
        pseudocode=[
            "for i = n // 2 - 1 down to 0: heapify(arr, n, i)",
            "for i = n - 1 down to 1:",
            "    swap(arr[0], arr[i])",
            "    heapify(arr, i, 0)",
            "function heapify(arr, n, i):",
            "    largest = i; left = 2*i + 1; right = 2*i + 2",
            "    if left < n and arr[left] > arr[largest]: largest = left",
            "    if right < n and arr[right] > arr[largest]: largest = right",
            "    if largest != i: swap(arr[i], arr[largest]); heapify(arr, n, largest)"
        ],
        use_cases=[
            "Embedded systems needing guaranteed O(n log n) without recursion or extra RAM",
            "Security-critical systems where O(n²) worst-case denial of service must be avoided",
            "Priority queue extraction and top-K item retrieval"
        ]
    ),

    # ------------------ SEARCHING ------------------
    "Linear Search": AlgorithmInfo(
        name="Linear Search",
        category="Searching",
        description="Sequentially checks each element of the list from start to finish until a match is found or the end of the array is reached.",
        best_time="O(1)",
        avg_time="O(n)",
        worst_time="O(n)",
        space_complexity="O(1)",
        pseudocode=[
            "for i = 0 to n - 1:",
            "    if arr[i] == target:",
            "        return i",
            "return -1"
        ],
        use_cases=[
            "Searching in unsorted or small datasets",
            "Searching singly linked lists or unindexed streams",
            "Hardware lookup tables with simple single-pass iterations"
        ]
    ),
    "Binary Search": AlgorithmInfo(
        name="Binary Search",
        category="Searching",
        description="Efficient algorithm that works on sorted arrays by repeatedly dividing the search interval in half. Compares target to the middle element.",
        best_time="O(1)",
        avg_time="O(log n)",
        worst_time="O(log n)",
        space_complexity="O(1)",
        pseudocode=[
            "low = 0; high = n - 1",
            "while low <= high:",
            "    mid = (low + high) // 2",
            "    if arr[mid] == target: return mid",
            "    else if arr[mid] < target: low = mid + 1",
            "    else: high = mid - 1",
            "return -1"
        ],
        use_cases=[
            "Database index queries (B-trees rely on binary search within nodes)",
            "Finding roots of mathematical functions (bisection method)",
            "Standard library searches (e.g. bisect in Python, std::binary_search)"
        ]
    ),
    "Jump Search": AlgorithmInfo(
        name="Jump Search",
        category="Searching",
        description="Searches a sorted array by jumping ahead by fixed steps of size √n, then performing a backward linear search once an element greater than target is found.",
        best_time="O(1)",
        avg_time="O(√n)",
        worst_time="O(√n)",
        space_complexity="O(1)",
        pseudocode=[
            "step = int(sqrt(n)); prev = 0",
            "while arr[min(step, n) - 1] < target:",
            "    prev = step; step += int(sqrt(n))",
            "    if prev >= n: return -1",
            "while arr[prev] < target:",
            "    prev += 1; if prev == min(step, n): return -1",
            "if arr[prev] == target: return prev",
            "return -1"
        ],
        use_cases=[
            "Systems where jumping backward is expensive compared to jumping forward",
            "Searching on magnetic tape or sequential optical drives",
            "Medium-sized sorted arrays where binary search branch misses are costly"
        ]
    ),
    "Interpolation Search": AlgorithmInfo(
        name="Interpolation Search",
        category="Searching",
        description="An improvement over binary search for uniformly distributed sorted values. Estimates position using formula: pos = low + [(target - arr[low]) * (high - low)] // (arr[high] - arr[low]).",
        best_time="O(1)",
        avg_time="O(log(log n))",
        worst_time="O(n)",
        space_complexity="O(1)",
        pseudocode=[
            "low = 0; high = n - 1",
            "while low <= high and target >= arr[low] and target <= arr[high]:",
            "    pos = low + ((target - arr[low]) * (high - low)) // (arr[high] - arr[low])",
            "    if arr[pos] == target: return pos",
            "    if arr[pos] < target: low = pos + 1",
            "    else: high = pos - 1",
            "return -1"
        ],
        use_cases=[
            "Searching telephone directories or uniformly distributed dictionaries",
            "Timestamp searches in continuous uniform time series",
            "In-memory tabular lookups with roughly uniform keys"
        ]
    ),

    # ------------------ GRAPHS ------------------
    "Breadth First Search (BFS)": AlgorithmInfo(
        name="Breadth First Search (BFS)",
        category="Graphs",
        description="Explores a graph level by level using a queue, visiting all neighbor vertices at current depth before moving to vertices at the next depth level.",
        best_time="O(V + E)",
        avg_time="O(V + E)",
        worst_time="O(V + E)",
        space_complexity="O(V)",
        pseudocode=[
            "create queue Q; mark start as visited; Q.enqueue(start)",
            "while Q is not empty:",
            "    u = Q.dequeue()",
            "    for each neighbor v of u:",
            "        if v is not visited:",
            "            mark v as visited",
            "            parent[v] = u",
            "            Q.enqueue(v)"
        ],
        use_cases=[
            "Finding shortest path in unweighted graphs",
            "Social networking friend suggestions (degrees of separation)",
            "Web crawlers indexing reachable links"
        ]
    ),
    "Depth First Search (DFS)": AlgorithmInfo(
        name="Depth First Search (DFS)",
        category="Graphs",
        description="Explores a graph along each branch as deeply as possible before backtracking, using recursion or an explicit stack.",
        best_time="O(V + E)",
        avg_time="O(V + E)",
        worst_time="O(V + E)",
        space_complexity="O(V)",
        pseudocode=[
            "function DFS(u):",
            "    mark u as visited",
            "    for each neighbor v of u:",
            "        if v is not visited:",
            "            parent[v] = u",
            "            DFS(v)"
        ],
        use_cases=[
            "Topological sorting in build dependency graphs",
            "Detecting cycles in graphs (e.g. deadlock detection)",
            "Solving mazes and puzzle state-space explorations"
        ]
    ),
    "Dijkstra's Algorithm": AlgorithmInfo(
        name="Dijkstra's Algorithm",
        category="Graphs",
        description="Finds the shortest paths between nodes in a graph with non-negative edge weights using a priority queue (min-heap).",
        best_time="O((V + E) log V)",
        avg_time="O((V + E) log V)",
        worst_time="O((V + E) log V)",
        space_complexity="O(V)",
        pseudocode=[
            "dist[source] = 0; for each v != source: dist[v] = inf",
            "pq.push((0, source))",
            "while pq is not empty:",
            "    d, u = pq.pop()",
            "    if d > dist[u]: continue",
            "    for each neighbor (v, weight) of u:",
            "        if dist[u] + weight < dist[v]:",
            "            dist[v] = dist[u] + weight",
            "            parent[v] = u; pq.push((dist[v], v))"
        ],
        use_cases=[
            "GPS Navigation and road map route planning (Google Maps)",
            "Network routing protocols (OSPF - Open Shortest Path First)",
            "Telecommunications bandwidth and latency optimization"
        ]
    ),
    "A* Search": AlgorithmInfo(
        name="A* Search",
        category="Graphs",
        description="Informed search algorithm that finds the shortest path by evaluating nodes using f(n) = g(n) + h(n), where g(n) is actual cost and h(n) is heuristic estimate to goal.",
        best_time="O(E)",
        avg_time="O(b^d)",
        worst_time="O(V + E log V)",
        space_complexity="O(V)",
        pseudocode=[
            "openSet = {start}; gScore[start] = 0",
            "fScore[start] = heuristic(start, goal)",
            "while openSet is not empty:",
            "    current = node in openSet with lowest fScore",
            "    if current == goal: return reconstruct_path(current)",
            "    openSet.remove(current)",
            "    for each neighbor v of current:",
            "        tentative_g = gScore[current] + weight(current, v)",
            "        if tentative_g < gScore[v]:",
            "            gScore[v] = tentative_g; fScore[v] = g + h(v, goal)",
            "            openSet.add(v)"
        ],
        use_cases=[
            "Video game NPC pathfinding around obstacles (Unity / Unreal)",
            "Robotics navigation in mapped environments",
            "Parsing natural languages and sequence alignments"
        ]
    ),
    "Prim's Algorithm": AlgorithmInfo(
        name="Prim's Algorithm",
        category="Graphs",
        description="Greedy algorithm that finds a Minimum Spanning Tree (MST) by growing a single tree from an arbitrary root node, repeatedly adding the minimum weight edge crossing the cut.",
        best_time="O(E log V)",
        avg_time="O(E log V)",
        worst_time="O(E log V)",
        space_complexity="O(V)",
        pseudocode=[
            "mstSet = {}; key[root] = 0; pq.push((0, root))",
            "while pq is not empty:",
            "    weight, u = pq.pop()",
            "    if u in mstSet: continue",
            "    mstSet.add(u)",
            "    for each neighbor (v, w) of u:",
            "        if v not in mstSet and w < key[v]:",
            "            key[v] = w; parent[v] = u",
            "            pq.push((w, v))"
        ],
        use_cases=[
            "Designing telecommunication and optical fiber networks",
            "Laying electrical power grids with minimum cable cost",
            "Approximation algorithm for Travelling Salesperson Problem (TSP)"
        ]
    ),
    "Kruskal's Algorithm": AlgorithmInfo(
        name="Kruskal's Algorithm",
        category="Graphs",
        description="Greedy algorithm that finds a Minimum Spanning Tree by sorting all edges by weight and adding them to the forest using a Disjoint Set Union (DSU) if they do not form a cycle.",
        best_time="O(E log E)",
        avg_time="O(E log E)",
        worst_time="O(E log E)",
        space_complexity="O(V + E)",
        pseudocode=[
            "sort edges by weight ascending",
            "initialize DSU with V sets",
            "for each edge (u, v, w) in sorted edges:",
            "    if find(u) != find(v):",
            "        union(u, v)",
            "        add edge (u, v) to MST"
        ],
        use_cases=[
            "Designing water supply networks or oil pipelines",
            "Hierarchical cluster analysis in data science",
            "Circuit board wiring layout optimization"
        ]
    ),

    # ------------------ TREES ------------------
    "Binary Search Tree (BST)": AlgorithmInfo(
        name="Binary Search Tree (BST)",
        category="Trees",
        description="A hierarchical node-based data structure where each node has at most two children. The left subtree contains keys smaller than the node, and the right subtree contains keys greater.",
        best_time="O(log n)",
        avg_time="O(log n)",
        worst_time="O(n)",
        space_complexity="O(n)",
        pseudocode=[
            "function insert(node, key):",
            "    if node is null: return new Node(key)",
            "    if key < node.key: node.left = insert(node.left, key)",
            "    else: node.right = insert(node.right, key)",
            "    return node",
            "function search(node, key):",
            "    if node is null or node.key == key: return node",
            "    if key < node.key: return search(node.left, key)",
            "    return search(node.right, key)"
        ],
        use_cases=[
            "Dynamic sets and associative lookup dictionaries",
            "Maintaining sorted streams of incoming items",
            "Syntax trees in compilers and expression evaluators"
        ]
    ),
    "AVL Tree": AlgorithmInfo(
        name="AVL Tree",
        category="Trees",
        description="A self-balancing binary search tree where the difference between heights of left and right subtrees (balance factor) cannot be more than 1 for all nodes. Balances via rotations (LL, RR, LR, RL).",
        best_time="O(log n)",
        avg_time="O(log n)",
        worst_time="O(log n)",
        space_complexity="O(n)",
        pseudocode=[
            "balanceFactor = height(left) - height(right)",
            "if balanceFactor > 1: # Left heavy",
            "    if key < left.key: return rightRotate(node) # LL",
            "    else: left = leftRotate(left); return rightRotate(node) # LR",
            "if balanceFactor < -1: # Right heavy",
            "    if key > right.key: return leftRotate(node) # RR",
            "    else: right = rightRotate(right); return leftRotate(node) # RL"
        ],
        use_cases=[
            "Read-intensive database indexing requiring strict O(log n) guarantees",
            "Memory management in real-time operating systems",
            "Lookup tables in financial trading systems with low latency bounds"
        ]
    ),

    # ------------------ DATA STRUCTURES ------------------
    "Stack": AlgorithmInfo(
        name="Stack",
        category="Data Structures",
        description="A linear data structure following the Last-In-First-Out (LIFO) principle. Elements can only be added or removed from the top.",
        best_time="O(1)",
        avg_time="O(1)",
        worst_time="O(1)",
        space_complexity="O(n)",
        pseudocode=[
            "function push(x):",
            "    top = top + 1; arr[top] = x",
            "function pop():",
            "    if isEmpty(): error 'Underflow'",
            "    val = arr[top]; top = top - 1; return val",
            "function peek():",
            "    return arr[top]"
        ],
        use_cases=[
            "Call stack for function execution in language runtimes",
            "Undo/redo mechanisms in text editors",
            "Expression parsing and syntax bracket matching"
        ]
    ),
    "Queue": AlgorithmInfo(
        name="Queue",
        category="Data Structures",
        description="A linear data structure following the First-In-First-Out (FIFO) principle. Elements are inserted at the rear and removed from the front.",
        best_time="O(1)",
        avg_time="O(1)",
        worst_time="O(1)",
        space_complexity="O(n)",
        pseudocode=[
            "function enqueue(x):",
            "    rear = rear + 1; arr[rear] = x",
            "function dequeue():",
            "    if isEmpty(): error 'Underflow'",
            "    val = arr[front]; front = front + 1; return val"
        ],
        use_cases=[
            "Job scheduling in operating systems (printer queues, task queues)",
            "Breadth-first search traversal in graphs",
            "Asynchronous message passing (e.g. RabbitMQ, Kafka buffers)"
        ]
    ),
    "Circular Queue": AlgorithmInfo(
        name="Circular Queue",
        category="Data Structures",
        description="A ring buffer implementation of a queue where the last position connects back to the first position, overcoming memory wastage of standard linear queues.",
        best_time="O(1)",
        avg_time="O(1)",
        worst_time="O(1)",
        space_complexity="O(n)",
        pseudocode=[
            "function enqueue(x):",
            "    if (rear + 1) % capacity == front: error 'Full'",
            "    rear = (rear + 1) % capacity; arr[rear] = x",
            "function dequeue():",
            "    if front == rear: error 'Empty'",
            "    front = (front + 1) % capacity; return arr[front]"
        ],
        use_cases=[
            "Audio/video streaming buffers",
            "CPU round-robin scheduling algorithms",
            "Memory-constrained embedded communication rings (UART buffers)"
        ]
    ),
    "Linked List": AlgorithmInfo(
        name="Linked List",
        category="Data Structures",
        description="A linear collection of data nodes whose order is not given by their physical placement in memory. Instead, each node points to the next (and optionally previous) node.",
        best_time="O(1) insert head",
        avg_time="O(n) search",
        worst_time="O(n) search",
        space_complexity="O(n)",
        pseudocode=[
            "function insertHead(val):",
            "    newNode = Node(val); newNode.next = head; head = newNode",
            "function delete(val):",
            "    curr = head; prev = null",
            "    while curr and curr.val != val: prev = curr; curr = curr.next",
            "    if curr: prev.next = curr.next"
        ],
        use_cases=[
            "Dynamic memory allocation (free list tracking)",
            "Building higher level data structures (Stacks, Queues, Graphs)",
            "Browser history navigation (forward and back with Doubly Linked List)"
        ]
    ),
    "Hash Table": AlgorithmInfo(
        name="Hash Table",
        category="Data Structures",
        description="Associative array that maps keys to values using a mathematical hash function. Collisions are handled using Separate Chaining or Open Addressing (Linear Probing).",
        best_time="O(1)",
        avg_time="O(1)",
        worst_time="O(n)",
        space_complexity="O(n)",
        pseudocode=[
            "index = hash(key) % capacity",
            "# Separate Chaining:",
            "bucket = table[index]; bucket.append((key, value))",
            "# Linear Probing:",
            "while table[index] is occupied: index = (index + 1) % capacity",
            "table[index] = (key, value)"
        ],
        use_cases=[
            "Database indexing and key-value stores (Redis, DynamoDB)",
            "Compiler symbol tables and variable scoping lookups",
            "Caching and memoization layers"
        ]
    )
}

