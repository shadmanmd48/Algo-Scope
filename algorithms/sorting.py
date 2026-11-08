"""
AlgoScope Sorting Algorithms
Real algorithm executions yielding step-by-step state snapshots for visualization.
"""

from typing import Generator, List
from core.base_algorithm import Step

def bubble_sort(arr: List[int], ascending: bool = True) -> Generator[Step, None, None]:
    """Bubble sort generator with real comparisons and swaps."""
    a = list(arr)
    n = len(a)
    comparisons = 0
    swaps = 0

    yield Step(
        action="start",
        state=list(a),
        indices=[],
        pseudocode_line=0,
        message="Starting Bubble Sort. We compare adjacent elements.",
        metrics={"comparisons": comparisons, "swaps": swaps}
    )

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            yield Step(
                action="compare",
                state=list(a),
                indices=[j, j + 1],
                pseudocode_line=3,
                message=f"Comparing arr[{j}]={a[j]} and arr[{j+1}]={a[j+1]}",
                metrics={"comparisons": comparisons, "swaps": swaps}
            )

            condition = (a[j] > a[j + 1]) if ascending else (a[j] < a[j + 1])
            if condition:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
                yield Step(
                    action="swap",
                    state=list(a),
                    indices=[j, j + 1],
                    pseudocode_line=4,
                    message=f"Swapped arr[{j}] and arr[{j+1}] -> {a[j]} and {a[j+1]}",
                    metrics={"comparisons": comparisons, "swaps": swaps}
                )

        yield Step(
            action="sorted_sub",
            state=list(a),
            indices=[n - i - 1],
            pseudocode_line=6,
            message=f"Element at index {n - i - 1} is now in its sorted position.",
            metrics={"comparisons": comparisons, "swaps": swaps}
        )
        if not swapped:
            break

    yield Step(
        action="done",
        state=list(a),
        indices=list(range(n)),
        pseudocode_line=6,
        message=f"Bubble Sort completed in {comparisons} comparisons and {swaps} swaps.",
        metrics={"comparisons": comparisons, "swaps": swaps}
    )


def selection_sort(arr: List[int], ascending: bool = True) -> Generator[Step, None, None]:
    """Selection sort generator finding the minimum/maximum in unsorted portion."""
    a = list(arr)
    n = len(a)
    comparisons = 0
    swaps = 0

    yield Step(
        action="start",
        state=list(a),
        indices=[],
        pseudocode_line=0,
        message="Starting Selection Sort. Finding the minimum in unsorted segment.",
        metrics={"comparisons": comparisons, "swaps": swaps}
    )

    for i in range(n):
        target_idx = i
        yield Step(
            action="highlight",
            state=list(a),
            indices=[i],
            pseudocode_line=1,
            message=f"Initial minimum for pass {i} assumed at index {i} (val={a[i]})",
            metrics={"comparisons": comparisons, "swaps": swaps}
        )

        for j in range(i + 1, n):
            comparisons += 1
            yield Step(
                action="compare",
                state=list(a),
                indices=[target_idx, j],
                pseudocode_line=3,
                message=f"Comparing current min arr[{target_idx}]={a[target_idx]} with arr[{j}]={a[j]}",
                metrics={"comparisons": comparisons, "swaps": swaps}
            )

            condition = (a[j] < a[target_idx]) if ascending else (a[j] > a[target_idx])
            if condition:
                target_idx = j
                yield Step(
                    action="new_min",
                    state=list(a),
                    indices=[target_idx],
                    secondary_indices=[i],
                    pseudocode_line=4,
                    message=f"Found new extreme value at index {target_idx} (val={a[target_idx]})",
                    metrics={"comparisons": comparisons, "swaps": swaps}
                )

        if target_idx != i:
            a[i], a[target_idx] = a[target_idx], a[i]
            swaps += 1
            yield Step(
                action="swap",
                state=list(a),
                indices=[i, target_idx],
                pseudocode_line=6,
                message=f"Swapped minimum {a[i]} into position {i}",
                metrics={"comparisons": comparisons, "swaps": swaps}
            )

        yield Step(
            action="sorted_sub",
            state=list(a),
            indices=[i],
            pseudocode_line=6,
            message=f"Index {i} (val={a[i]}) is now sorted.",
            metrics={"comparisons": comparisons, "swaps": swaps}
        )

    yield Step(
        action="done",
        state=list(a),
        indices=list(range(n)),
        pseudocode_line=6,
        message=f"Selection Sort completed in {comparisons} comparisons and {swaps} swaps.",
        metrics={"comparisons": comparisons, "swaps": swaps}
    )


def insertion_sort(arr: List[int], ascending: bool = True) -> Generator[Step, None, None]:
    """Insertion sort inserting each element into its sorted left partition."""
    a = list(arr)
    n = len(a)
    comparisons = 0
    swaps = 0

    yield Step(
        action="start",
        state=list(a),
        indices=[0],
        pseudocode_line=0,
        message="Starting Insertion Sort. Left partition is sorted one item at a time.",
        metrics={"comparisons": comparisons, "swaps": swaps}
    )

    for i in range(1, n):
        key = a[i]
        j = i - 1

        yield Step(
            action="pickup",
            state=list(a),
            indices=[i],
            pseudocode_line=1,
            message=f"Picked up key arr[{i}] = {key} to insert into sorted left portion.",
            metrics={"comparisons": comparisons, "swaps": swaps}
        )

        while j >= 0:
            comparisons += 1
            yield Step(
                action="compare",
                state=list(a),
                indices=[j, j + 1],
                pseudocode_line=3,
                message=f"Comparing arr[{j}]={a[j]} with key={key}",
                metrics={"comparisons": comparisons, "swaps": swaps}
            )

            condition = (a[j] > key) if ascending else (a[j] < key)
            if condition:
                a[j + 1] = a[j]
                swaps += 1
                yield Step(
                    action="shift",
                    state=list(a),
                    indices=[j, j + 1],
                    pseudocode_line=4,
                    message=f"Shifted {a[j]} right to position {j + 1}",
                    metrics={"comparisons": comparisons, "swaps": swaps}
                )
                j -= 1
            else:
                break

        a[j + 1] = key
        yield Step(
            action="insert",
            state=list(a),
            indices=[j + 1],
            pseudocode_line=6,
            message=f"Inserted key {key} at position {j + 1}",
            metrics={"comparisons": comparisons, "swaps": swaps}
        )

    yield Step(
        action="done",
        state=list(a),
        indices=list(range(n)),
        pseudocode_line=6,
        message=f"Insertion Sort completed in {comparisons} comparisons and {swaps} shifts.",
        metrics={"comparisons": comparisons, "swaps": swaps}
    )


def merge_sort(arr: List[int], ascending: bool = True) -> Generator[Step, None, None]:
    """Iterative or auxiliary Merge Sort yielding steps."""
    a = list(arr)
    n = len(a)
    metrics = {"comparisons": 0, "swaps": 0}

    yield Step(
        action="start",
        state=list(a),
        indices=[],
        pseudocode_line=0,
        message="Starting Merge Sort. Recursively splitting and merging subarrays.",
        metrics=dict(metrics)
    )

    def _merge(l: int, m: int, r: int) -> Generator[Step, None, None]:
        left_part = a[l:m + 1]
        right_part = a[m + 1:r + 1]
        i = j = 0
        k = l

        yield Step(
            action="highlight",
            state=list(a),
            indices=list(range(l, r + 1)),
            pseudocode_line=5,
            message=f"Merging subarray range [{l}..{m}] and [{m+1}..{r}]",
            metrics=dict(metrics)
        )

        while i < len(left_part) and j < len(right_part):
            metrics["comparisons"] += 1
            cond = (left_part[i] <= right_part[j]) if ascending else (left_part[i] >= right_part[j])

            yield Step(
                action="compare",
                state=list(a),
                indices=[l + i, m + 1 + j],
                secondary_indices=[k],
                pseudocode_line=5,
                message=f"Comparing left element {left_part[i]} with right element {right_part[j]}",
                metrics=dict(metrics)
            )

            if cond:
                a[k] = left_part[i]
                i += 1
            else:
                a[k] = right_part[j]
                j += 1
            metrics["swaps"] += 1

            yield Step(
                action="overwrite",
                state=list(a),
                indices=[k],
                pseudocode_line=5,
                message=f"Placed {a[k]} at index {k}",
                metrics=dict(metrics)
            )
            k += 1

        while i < len(left_part):
            a[k] = left_part[i]
            metrics["swaps"] += 1
            yield Step(
                action="overwrite",
                state=list(a),
                indices=[k],
                pseudocode_line=5,
                message=f"Placed remaining left element {a[k]} at index {k}",
                metrics=dict(metrics)
            )
            i += 1
            k += 1

        while j < len(right_part):
            a[k] = right_part[j]
            metrics["swaps"] += 1
            yield Step(
                action="overwrite",
                state=list(a),
                indices=[k],
                pseudocode_line=5,
                message=f"Placed remaining right element {a[k]} at index {k}",
                metrics=dict(metrics)
            )
            j += 1
            k += 1

    def _sort(l: int, r: int) -> Generator[Step, None, None]:
        if l < r:
            m = (l + r) // 2
            yield from _sort(l, m)
            yield from _sort(m + 1, r)
            yield from _merge(l, m, r)

    yield from _sort(0, n - 1)

    yield Step(
        action="done",
        state=list(a),
        indices=list(range(n)),
        pseudocode_line=5,
        message=f"Merge Sort completed in {metrics['comparisons']} comparisons and {metrics['swaps']} writes.",
        metrics=dict(metrics)
    )


def quick_sort(arr: List[int], ascending: bool = True) -> Generator[Step, None, None]:
    """Quick sort generator with in-place partition and pivot highlighting."""
    a = list(arr)
    n = len(a)
    metrics = {"comparisons": 0, "swaps": 0}

    yield Step(
        action="start",
        state=list(a),
        indices=[],
        pseudocode_line=0,
        message="Starting Quick Sort. Partitioning around pivot elements.",
        metrics=dict(metrics)
    )

    def _partition(low: int, high: int) -> Generator[Step, None, int]:
        pivot = a[high]
        i = low - 1

        yield Step(
            action="pivot",
            state=list(a),
            indices=[high],
            pseudocode_line=6,
            message=f"Selected pivot arr[{high}] = {pivot} for subarray [{low}..{high}]",
            metrics=dict(metrics)
        )

        for j in range(low, high):
            metrics["comparisons"] += 1
            yield Step(
                action="compare",
                state=list(a),
                indices=[j, high],
                secondary_indices=[i if i >= 0 else low],
                pseudocode_line=8,
                message=f"Comparing arr[{j}]={a[j]} with pivot {pivot}",
                metrics=dict(metrics)
            )

            cond = (a[j] < pivot) if ascending else (a[j] > pivot)
            if cond:
                i += 1
                if i != j:
                    a[i], a[j] = a[j], a[i]
                    metrics["swaps"] += 1
                    yield Step(
                        action="swap",
                        state=list(a),
                        indices=[i, j],
                        secondary_indices=[high],
                        pseudocode_line=8,
                        message=f"Swapped arr[{i}] and arr[{j}] (both smaller than pivot)",
                        metrics=dict(metrics)
                    )

        a[i + 1], a[high] = a[high], a[i + 1]
        metrics["swaps"] += 1
        yield Step(
            action="swap",
            state=list(a),
            indices=[i + 1, high],
            pseudocode_line=9,
            message=f"Placed pivot {pivot} into its sorted position at index {i + 1}",
            metrics=dict(metrics)
        )
        return i + 1

    def _qsort(low: int, high: int) -> Generator[Step, None, None]:
        if low < high:
            pi_gen = _partition(low, high)
            pi = None
            try:
                while True:
                    step = next(pi_gen)
                    yield step
            except StopIteration as e:
                pi = e.value

            yield from _qsort(low, pi - 1)
            yield from _qsort(pi + 1, high)
        elif low == high:
            yield Step(
                action="sorted_sub",
                state=list(a),
                indices=[low],
                pseudocode_line=3,
                message=f"Single element at index {low} is already sorted.",
                metrics=dict(metrics)
            )

    yield from _qsort(0, n - 1)

    yield Step(
        action="done",
        state=list(a),
        indices=list(range(n)),
        pseudocode_line=9,
        message=f"Quick Sort completed in {metrics['comparisons']} comparisons and {metrics['swaps']} swaps.",
        metrics=dict(metrics)
    )


def heap_sort(arr: List[int], ascending: bool = True) -> Generator[Step, None, None]:
    """Heap sort generator building binary max-heap / min-heap and extracting roots."""
    a = list(arr)
    n = len(a)
    metrics = {"comparisons": 0, "swaps": 0}

    yield Step(
        action="start",
        state=list(a),
        indices=[],
        pseudocode_line=0,
        message="Starting Heap Sort. First phase: build heap.",
        metrics=dict(metrics)
    )

    def _heapify(size: int, i: int) -> Generator[Step, None, None]:
        extreme = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < size:
            metrics["comparisons"] += 1
            cond_l = (a[left] > a[extreme]) if ascending else (a[left] < a[extreme])
            if cond_l:
                extreme = left

        if right < size:
            metrics["comparisons"] += 1
            cond_r = (a[right] > a[extreme]) if ascending else (a[right] < a[extreme])
            if cond_r:
                extreme = right

        if extreme != i:
            a[i], a[extreme] = a[extreme], a[i]
            metrics["swaps"] += 1
            yield Step(
                action="swap",
                state=list(a),
                indices=[i, extreme],
                pseudocode_line=8,
                message=f"Heapify swap: arr[{i}] and arr[{extreme}] to restore heap property",
                metrics=dict(metrics)
            )
            yield from _heapify(size, extreme)

    # Build heap
    for i in range(n // 2 - 1, -1, -1):
        yield Step(
            action="highlight",
            state=list(a),
            indices=[i],
            pseudocode_line=0,
            message=f"Heapifying subtree rooted at index {i}",
            metrics=dict(metrics)
        )
        yield from _heapify(n, i)

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        metrics["swaps"] += 1
        yield Step(
            action="swap",
            state=list(a),
            indices=[0, i],
            pseudocode_line=2,
            message=f"Extracted root {a[i]} to index {i} and replaced with arr[0]={a[0]}",
            metrics=dict(metrics)
        )
        yield from _heapify(i, 0)

    yield Step(
        action="done",
        state=list(a),
        indices=list(range(n)),
        pseudocode_line=8,
        message=f"Heap Sort completed in {metrics['comparisons']} comparisons and {metrics['swaps']} swaps.",
        metrics=dict(metrics)
    )

