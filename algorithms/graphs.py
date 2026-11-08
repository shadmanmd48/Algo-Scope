"""
AlgoScope Graph Algorithms
Real implementations of BFS, DFS, Dijkstra, A*, Prim, and Kruskal yielding step snapshots.
"""

import heapq
import math
from typing import Dict, Generator, List, Set, Tuple
from core.base_algorithm import Step

def bfs(graph: Dict[str, List[Tuple[str, float]]], start: str, target: str = "") -> Generator[Step, None, None]:
    """Breadth First Search yielding traversal steps and shortest path in unweighted graph."""
    visited: Set[str] = set()
    queue: List[str] = [start]
    visited.add(start)
    parent: Dict[str, str] = {}
    traversal_order: List[str] = [start]

    yield Step(
        action="start",
        state={"visited": list(visited), "queue": list(queue), "order": list(traversal_order)},
        indices=[start],
        pseudocode_line=0,
        message=f"Starting BFS from node '{start}'. Added to queue."
    )

    found = False
    while queue:
        u = queue.pop(0)

        yield Step(
            action="visit",
            state={"visited": list(visited), "queue": list(queue), "order": list(traversal_order), "current": u},
            indices=[u],
            pseudocode_line=2,
            message=f"Dequeued node '{u}'. Exploring its neighbors."
        )

        if target and u == target:
            found = True
            break

        for v, _ in graph.get(u, []):
            if v not in visited:
                visited.add(v)
                parent[v] = u
                queue.append(v)
                traversal_order.append(v)

                yield Step(
                    action="enqueue",
                    state={"visited": list(visited), "queue": list(queue), "order": list(traversal_order), "edge": (u, v)},
                    indices=[v],
                    secondary_indices=[u],
                    pseudocode_line=5,
                    message=f"Discovered unvisited neighbor '{v}' via edge ({u} -> {v}). Added to queue."
                )

                if target and v == target:
                    found = True
                    break
        if found:
            break

    # Path reconstruction if target was specified
    path = []
    if target and (target in visited or found):
        curr = target
        while curr in parent:
            path.append(curr)
            curr = parent[curr]
        path.append(start)
        path.reverse()

    yield Step(
        action="done",
        state={
            "visited": list(visited),
            "order": list(traversal_order),
            "path": path,
            "target": target
        },
        indices=path if path else list(visited),
        pseudocode_line=5,
        message=f"BFS traversal completed. Explored {len(visited)} nodes. {'Shortest path: ' + ' -> '.join(path) if path else ''}"
    )


def dfs(graph: Dict[str, List[Tuple[str, float]]], start: str, target: str = "") -> Generator[Step, None, None]:
    """Depth First Search yielding steps with recursive / explicit stack traversal."""
    visited: Set[str] = set()
    stack: List[str] = [start]
    parent: Dict[str, str] = {}
    traversal_order: List[str] = []

    yield Step(
        action="start",
        state={"visited": list(visited), "stack": list(stack), "order": list(traversal_order)},
        indices=[start],
        pseudocode_line=0,
        message=f"Starting DFS from root node '{start}'."
    )

    found = False
    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        traversal_order.append(u)

        yield Step(
            action="visit",
            state={"visited": list(visited), "stack": list(stack), "order": list(traversal_order), "current": u},
            indices=[u],
            pseudocode_line=1,
            message=f"Popped node '{u}' from stack. Marking as visited."
        )

        if target and u == target:
            found = True
            break

        # Push neighbors (reverse order for intuitive left-to-right processing)
        neighbors = graph.get(u, [])
        for v, _ in reversed(neighbors):
            if v not in visited:
                parent[v] = u
                stack.append(v)
                yield Step(
                    action="push",
                    state={"visited": list(visited), "stack": list(stack), "order": list(traversal_order), "edge": (u, v)},
                    indices=[v],
                    secondary_indices=[u],
                    pseudocode_line=4,
                    message=f"Discovered edge ({u} -> {v}). Pushed '{v}' to stack."
                )

    path = []
    if target and target in visited:
        curr = target
        while curr in parent:
            path.append(curr)
            curr = parent[curr]
        path.append(start)
        path.reverse()

    yield Step(
        action="done",
        state={"visited": list(visited), "order": list(traversal_order), "path": path},
        indices=path if path else list(visited),
        pseudocode_line=4,
        message=f"DFS completed. Explored {len(visited)} nodes. {'Path found: ' + ' -> '.join(path) if path else ''}"
    )


def dijkstra(graph: Dict[str, List[Tuple[str, float]]], start: str, target: str = "") -> Generator[Step, None, None]:
    """Dijkstra's shortest path algorithm using a min-heap priority queue."""
    dist: Dict[str, float] = {node: float("inf") for node in graph}
    dist[start] = 0.0
    parent: Dict[str, str] = {}
    visited: Set[str] = set()
    pq: List[Tuple[float, str]] = [(0.0, start)]

    yield Step(
        action="start",
        state={"dist": dict(dist), "visited": list(visited)},
        indices=[start],
        pseudocode_line=0,
        message=f"Initialized Dijkstra. Distance to source '{start}' is 0, all others ∞."
    )

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)

        yield Step(
            action="visit",
            state={"dist": dict(dist), "visited": list(visited), "current": u},
            indices=[u],
            pseudocode_line=3,
            message=f"Selected node '{u}' with minimum tentative distance {d:.1f}.",
            metrics={"current_dist": d}
        )

        if target and u == target:
            break

        for v, weight in graph.get(u, []):
            if v not in visited:
                new_dist = dist[u] + weight
                yield Step(
                    action="relax_check",
                    state={"dist": dict(dist), "visited": list(visited), "edge": (u, v)},
                    indices=[v],
                    secondary_indices=[u],
                    pseudocode_line=5,
                    message=f"Checking edge ({u} -> {v}, w={weight:.1f}). New dist: {dist[u]:.1f} + {weight:.1f} = {new_dist:.1f}"
                )

                if new_dist < dist[v]:
                    dist[v] = new_dist
                    parent[v] = u
                    heapq.heappush(pq, (new_dist, v))

                    yield Step(
                        action="relax_update",
                        state={"dist": dict(dist), "visited": list(visited), "edge": (u, v)},
                        indices=[v],
                        secondary_indices=[u],
                        pseudocode_line=6,
                        message=f"Relaxed distance to '{v}' down to {new_dist:.1f} via '{u}'."
                    )

    path = []
    if target and target in dist and dist[target] < float("inf"):
        curr = target
        while curr in parent:
            path.append(curr)
            curr = parent[curr]
        path.append(start)
        path.reverse()

    cost_str = f"Total path cost: {dist[target]:.1f}" if (target and target in dist and dist[target] < float("inf")) else ""
    yield Step(
        action="done",
        state={"dist": dict(dist), "visited": list(visited), "path": path},
        indices=path if path else list(visited),
        pseudocode_line=6,
        message=f"Dijkstra finished. {cost_str} ({' -> '.join(path) if path else 'All reachable nodes calculated'})"
    )


def a_star(
    graph: Dict[str, List[Tuple[str, float]]],
    positions: Dict[str, Tuple[float, float]],
    start: str,
    target: str
) -> Generator[Step, None, None]:
    """A* Search using Euclidean heuristic to target coordinates."""
    def heuristic(a: str, b: str) -> float:
        if a not in positions or b not in positions:
            return 0.0
        x1, y1 = positions[a]
        x2, y2 = positions[b]
        return math.hypot(x2 - x1, y2 - y1) / 10.0  # Normalized scale

    g_score: Dict[str, float] = {node: float("inf") for node in graph}
    g_score[start] = 0.0
    f_score: Dict[str, float] = {node: float("inf") for node in graph}
    f_score[start] = heuristic(start, target)

    open_set: List[Tuple[float, str]] = [(f_score[start], start)]
    parent: Dict[str, str] = {}
    closed_set: Set[str] = set()

    yield Step(
        action="start",
        state={"g_score": dict(g_score), "f_score": dict(f_score), "closed": list(closed_set)},
        indices=[start],
        pseudocode_line=0,
        message=f"Starting A* Search from '{start}' to '{target}'. Heuristic h({start})={f_score[start]:.1f}"
    )

    found = False
    while open_set:
        f, u = heapq.heappop(open_set)
        if u in closed_set:
            continue
        closed_set.add(u)

        yield Step(
            action="visit",
            state={"g_score": dict(g_score), "f_score": dict(f_score), "closed": list(closed_set), "current": u},
            indices=[u],
            pseudocode_line=3,
            message=f"Expanding node '{u}' with minimum f(n) = g({g_score[u]:.1f}) + h({f - g_score[u]:.1f}) = {f:.1f}"
        )

        if u == target:
            found = True
            break

        for v, weight in graph.get(u, []):
            if v in closed_set:
                continue

            tentative_g = g_score[u] + weight
            if tentative_g < g_score[v]:
                parent[v] = u
                g_score[v] = tentative_g
                h = heuristic(v, target)
                f_score[v] = tentative_g + h
                heapq.heappush(open_set, (f_score[v], v))

                yield Step(
                    action="relax_update",
                    state={"g_score": dict(g_score), "f_score": dict(f_score), "closed": list(closed_set), "edge": (u, v)},
                    indices=[v],
                    secondary_indices=[u],
                    pseudocode_line=7,
                    message=f"Discovered better path to '{v}': g={tentative_g:.1f}, h={h:.1f}, f={f_score[v]:.1f}"
                )

    path = []
    if found:
        curr = target
        while curr in parent:
            path.append(curr)
            curr = parent[curr]
        path.append(start)
        path.reverse()

    yield Step(
        action="done",
        state={"path": path, "closed": list(closed_set)},
        indices=path,
        pseudocode_line=7,
        message=f"A* Search completed. Path: {' -> '.join(path)} (Total cost: {g_score[target]:.1f})"
    )


def prim_mst(graph: Dict[str, List[Tuple[str, float]]], start: str) -> Generator[Step, None, None]:
    """Prim's Minimum Spanning Tree algorithm."""
    mst_edges: List[Tuple[str, str, float]] = []
    visited: Set[str] = {start}
    edges_pq: List[Tuple[float, str, str]] = []

    for neighbor, weight in graph.get(start, []):
        heapq.heappush(edges_pq, (weight, start, neighbor))

    yield Step(
        action="start",
        state={"mst_edges": list(mst_edges), "visited": list(visited)},
        indices=[start],
        pseudocode_line=0,
        message=f"Starting Prim's MST from node '{start}'. Added incident edges to priority queue."
    )

    total_weight = 0.0
    while edges_pq and len(visited) < len(graph):
        weight, u, v = heapq.heappop(edges_pq)
        if v in visited:
            continue

        visited.add(v)
        mst_edges.append((u, v, weight))
        total_weight += weight

        yield Step(
            action="add_edge",
            state={"mst_edges": list(mst_edges), "visited": list(visited), "last_edge": (u, v)},
            indices=[v],
            secondary_indices=[u],
            pseudocode_line=3,
            message=f"Added edge ({u} - {v}, w={weight:.1f}) to MST. Total cost: {total_weight:.1f}"
        )

        for next_node, next_w in graph.get(v, []):
            if next_node not in visited:
                heapq.heappush(edges_pq, (next_w, v, next_node))

    yield Step(
        action="done",
        state={"mst_edges": list(mst_edges), "visited": list(visited), "total_weight": total_weight},
        indices=list(visited),
        pseudocode_line=3,
        message=f"Prim's MST completed! Spanned {len(visited)} nodes with total weight {total_weight:.1f}"
    )


def kruskal_mst(graph: Dict[str, List[Tuple[str, float]]]) -> Generator[Step, None, None]:
    """Kruskal's Minimum Spanning Tree algorithm using Disjoint Set Union."""
    edges: List[Tuple[float, str, str]] = []
    seen = set()
    for u in graph:
        for v, w in graph[u]:
            edge_key = tuple(sorted([u, v]))
            if edge_key not in seen:
                seen.add(edge_key)
                edges.append((w, u, v))

    edges.sort(key=lambda x: x[0])  # Sort by weight

    # DSU data structures
    parent = {node: node for node in graph}
    rank = {node: 0 for node in graph}

    def find(i):
        if parent[i] == i:
            return i
        parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            if rank[root_i] < rank[root_j]:
                parent[root_i] = root_j
            elif rank[root_i] > rank[root_j]:
                parent[root_j] = root_i
            else:
                parent[root_j] = root_i
                rank[root_i] += 1
            return True
        return False

    mst_edges: List[Tuple[str, str, float]] = []
    total_weight = 0.0

    yield Step(
        action="start",
        state={"mst_edges": list(mst_edges)},
        indices=[],
        pseudocode_line=0,
        message=f"Starting Kruskal's MST. Sorted all {len(edges)} unique edges by weight."
    )

    for w, u, v in edges:
        root_u = find(u)
        root_v = find(v)

        yield Step(
            action="check_edge",
            state={"mst_edges": list(mst_edges), "check_edge": (u, v, w)},
            indices=[u, v],
            pseudocode_line=2,
            message=f"Considering minimum edge ({u} - {v}, w={w:.1f})."
        )

        if root_u != root_v:
            union(u, v)
            mst_edges.append((u, v, w))
            total_weight += w

            yield Step(
                action="add_edge",
                state={"mst_edges": list(mst_edges), "last_edge": (u, v)},
                indices=[u, v],
                pseudocode_line=4,
                message=f"Added edge ({u} - {v}, w={w:.1f}) to MST without creating a cycle."
            )
        else:
            yield Step(
                action="discard_edge",
                state={"mst_edges": list(mst_edges), "discard_edge": (u, v, w)},
                indices=[u, v],
                pseudocode_line=3,
                message=f"Discarded edge ({u} - {v}, w={w:.1f}) because it forms a cycle."
            )

    yield Step(
        action="done",
        state={"mst_edges": list(mst_edges), "total_weight": total_weight},
        indices=[],
        pseudocode_line=4,
        message=f"Kruskal's MST completed! Total tree weight: {total_weight:.1f}"
    )

