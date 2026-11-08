"""
AlgoScope Real Performance Profiler & Benchmark Runner
Executes actual sorting algorithms to collect real runtime, comparisons, and swaps.
"""

import random
import time
from typing import Callable, Dict, List, Tuple

def benchmark_bubble_sort(arr: List[int]) -> Tuple[float, int, int]:
    """Run real Bubble Sort and record elapsed ms, comparisons, and swaps."""
    a = list(arr)
    n = len(a)
    comps = 0
    swaps = 0

    t0 = time.perf_counter()
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comps += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return elapsed_ms, comps, swaps


def benchmark_selection_sort(arr: List[int]) -> Tuple[float, int, int]:
    """Run real Selection Sort."""
    a = list(arr)
    n = len(a)
    comps = 0
    swaps = 0

    t0 = time.perf_counter()
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comps += 1
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return elapsed_ms, comps, swaps


def benchmark_insertion_sort(arr: List[int]) -> Tuple[float, int, int]:
    """Run real Insertion Sort."""
    a = list(arr)
    n = len(a)
    comps = 0
    swaps = 0

    t0 = time.perf_counter()
    for i in range(1, n):
        key = a[i]
        j = i - 1
        while j >= 0:
            comps += 1
            if a[j] > key:
                a[j + 1] = a[j]
                swaps += 1
                j -= 1
            else:
                break
        a[j + 1] = key
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return elapsed_ms, comps, swaps


def benchmark_merge_sort(arr: List[int]) -> Tuple[float, int, int]:
    """Run real Merge Sort."""
    a = list(arr)
    comps = 0
    swaps = 0

    t0 = time.perf_counter()

    def _ms(lst):
        nonlocal comps, swaps
        if len(lst) <= 1:
            return lst
        mid = len(lst) // 2
        left = _ms(lst[:mid])
        right = _ms(lst[mid:])

        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            comps += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
            swaps += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    _ms(a)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return elapsed_ms, comps, swaps


def benchmark_quick_sort(arr: List[int]) -> Tuple[float, int, int]:
    """Run real Quick Sort."""
    a = list(arr)
    comps = 0
    swaps = 0

    t0 = time.perf_counter()

    def _qs(low, high):
        nonlocal comps, swaps
        if low < high:
            pivot = a[high]
            i = low - 1
            for j in range(low, high):
                comps += 1
                if a[j] < pivot:
                    i += 1
                    a[i], a[j] = a[j], a[i]
                    swaps += 1
            a[i + 1], a[high] = a[high], a[i + 1]
            swaps += 1
            pi = i + 1

            _qs(low, pi - 1)
            _qs(pi + 1, high)

    _qs(0, len(a) - 1)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return elapsed_ms, comps, swaps


def benchmark_heap_sort(arr: List[int]) -> Tuple[float, int, int]:
    """Run real Heap Sort."""
    a = list(arr)
    n = len(a)
    comps = 0
    swaps = 0

    t0 = time.perf_counter()

    def _heapify(size, i):
        nonlocal comps, swaps
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < size:
            comps += 1
            if a[l] > a[largest]:
                largest = l
        if r < size:
            comps += 1
            if a[r] > a[largest]:
                largest = r
        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            swaps += 1
            _heapify(size, largest)

    for i in range(n // 2 - 1, -1, -1):
        _heapify(n, i)
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        swaps += 1
        _heapify(i, 0)

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return elapsed_ms, comps, swaps


BENCHMARK_FUNCTIONS: Dict[str, Callable[[List[int]], Tuple[float, int, int]]] = {
    "Bubble Sort": benchmark_bubble_sort,
    "Selection Sort": benchmark_selection_sort,
    "Insertion Sort": benchmark_insertion_sort,
    "Merge Sort": benchmark_merge_sort,
    "Quick Sort": benchmark_quick_sort,
    "Heap Sort": benchmark_heap_sort
}

def run_benchmark(algorithm_names: List[str], size: int) -> Dict[str, Dict[str, float]]:
    """Generate random array of given size and benchmark requested algorithms."""
    data = [random.randint(1, 1000) for _ in range(size)]
    results = {}
    for name in algorithm_names:
        if name in BENCHMARK_FUNCTIONS:
            fn = BENCHMARK_FUNCTIONS[name]
            elapsed_ms, comps, swaps = fn(data)
            results[name] = {
                "time_ms": round(elapsed_ms, 2),
                "comparisons": comps,
                "swaps": swaps,
                "size": size
            }
    return results

