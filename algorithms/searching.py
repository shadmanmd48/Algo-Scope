"""
AlgoScope Searching Algorithms
Real implementations of Linear, Binary, Jump, and Interpolation search yielding step snapshots.
"""

import math
from typing import Generator, List
from core.base_algorithm import Step

def linear_search(arr: List[int], target: int) -> Generator[Step, None, None]:
    """Linear search sequentially scanning elements."""
    n = len(arr)
    comparisons = 0

    yield Step(
        action="start",
        state=list(arr),
        indices=[],
        pseudocode_line=0,
        message=f"Starting Linear Search for target {target}.",
        metrics={"comparisons": comparisons}
    )

    for i in range(n):
        comparisons += 1
        yield Step(
            action="compare",
            state=list(arr),
            indices=[i],
            pseudocode_line=1,
            message=f"Checking index {i}: arr[{i}] = {arr[i]} vs target = {target}",
            metrics={"comparisons": comparisons}
        )

        if arr[i] == target:
            yield Step(
                action="found",
                state=list(arr),
                indices=[i],
                pseudocode_line=2,
                message=f"Target {target} found at index {i} in {comparisons} comparisons!",
                metrics={"comparisons": comparisons, "found_index": i}
            )
            return

    yield Step(
        action="not_found",
        state=list(arr),
        indices=[],
        pseudocode_line=3,
        message=f"Target {target} was not found in the array after {comparisons} comparisons.",
        metrics={"comparisons": comparisons, "found_index": -1}
    )


def binary_search(arr: List[int], target: int) -> Generator[Step, None, None]:
    """Binary search dividing interval in half. Array must be sorted."""
    a = list(arr)
    n = len(a)
    comparisons = 0
    low = 0
    high = n - 1

    yield Step(
        action="start",
        state=list(a),
        indices=[],
        secondary_indices=[low, high],
        pseudocode_line=0,
        message=f"Starting Binary Search for target {target} in sorted range [0..{high}].",
        metrics={"comparisons": comparisons}
    )

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1

        yield Step(
            action="probe",
            state=list(a),
            indices=[mid],
            secondary_indices=[low, high],
            pseudocode_line=2,
            message=f"Inspecting middle index {mid}: arr[{mid}] = {a[mid]} (low={low}, high={high})",
            metrics={"comparisons": comparisons}
        )

        if a[mid] == target:
            yield Step(
                action="found",
                state=list(a),
                indices=[mid],
                secondary_indices=[low, high],
                pseudocode_line=3,
                message=f"Target {target} found at index {mid} after {comparisons} comparisons!",
                metrics={"comparisons": comparisons, "found_index": mid}
            )
            return
        elif a[mid] < target:
            yield Step(
                action="compare",
                state=list(a),
                indices=[mid],
                secondary_indices=[mid + 1, high],
                pseudocode_line=4,
                message=f"arr[{mid}]={a[mid]} < target {target}. Target must be in right half.",
                metrics={"comparisons": comparisons}
            )
            low = mid + 1
        else:
            yield Step(
                action="compare",
                state=list(a),
                indices=[mid],
                secondary_indices=[low, mid - 1],
                pseudocode_line=5,
                message=f"arr[{mid}]={a[mid]} > target {target}. Target must be in left half.",
                metrics={"comparisons": comparisons}
            )
            high = mid - 1

    yield Step(
        action="not_found",
        state=list(a),
        indices=[],
        secondary_indices=[],
        pseudocode_line=6,
        message=f"Target {target} was not found in the array after {comparisons} comparisons.",
        metrics={"comparisons": comparisons, "found_index": -1}
    )


def jump_search(arr: List[int], target: int) -> Generator[Step, None, None]:
    """Jump search stepping ahead by sqrt(n) then linear scan back."""
    a = list(arr)
    n = len(a)
    comparisons = 0
    step = int(math.sqrt(n))
    prev = 0

    yield Step(
        action="start",
        state=list(a),
        indices=[],
        secondary_indices=[0, min(step, n) - 1],
        pseudocode_line=0,
        message=f"Starting Jump Search for target {target} with block size √{n} ≈ {step}.",
        metrics={"comparisons": comparisons}
    )

    # Jumping phase
    while a[min(step, n) - 1] < target:
        comparisons += 1
        curr_block_end = min(step, n) - 1
        yield Step(
            action="jump",
            state=list(a),
            indices=[curr_block_end],
            secondary_indices=[prev, curr_block_end],
            pseudocode_line=1,
            message=f"Block end arr[{curr_block_end}]={a[curr_block_end]} < target {target}. Jumping ahead.",
            metrics={"comparisons": comparisons}
        )
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            yield Step(
                action="not_found",
                state=list(a),
                indices=[],
                pseudocode_line=3,
                message=f"Jumping past array boundary. Target {target} not present.",
                metrics={"comparisons": comparisons, "found_index": -1}
            )
            return

    # Linear scan phase within the block
    yield Step(
        action="highlight",
        state=list(a),
        indices=list(range(prev, min(step, n))),
        secondary_indices=[prev, min(step, n) - 1],
        pseudocode_line=4,
        message=f"Target {target} potentially in block [{prev}..{min(step, n) - 1}]. Linear scanning...",
        metrics={"comparisons": comparisons}
    )

    while a[prev] < target:
        comparisons += 1
        yield Step(
            action="compare",
            state=list(a),
            indices=[prev],
            secondary_indices=[prev, min(step, n) - 1],
            pseudocode_line=4,
            message=f"Checking block item arr[{prev}] = {a[prev]} vs target = {target}",
            metrics={"comparisons": comparisons}
        )
        prev += 1
        if prev == min(step, n):
            yield Step(
                action="not_found",
                state=list(a),
                indices=[],
                pseudocode_line=5,
                message=f"Reached end of block without finding target {target}.",
                metrics={"comparisons": comparisons, "found_index": -1}
            )
            return

    comparisons += 1
    if a[prev] == target:
        yield Step(
            action="found",
            state=list(a),
            indices=[prev],
            pseudocode_line=6,
            message=f"Target {target} found at index {prev} in {comparisons} comparisons!",
            metrics={"comparisons": comparisons, "found_index": prev}
        )
    else:
        yield Step(
            action="not_found",
            state=list(a),
            indices=[],
            pseudocode_line=7,
            message=f"Target {target} not found after {comparisons} comparisons.",
            metrics={"comparisons": comparisons, "found_index": -1}
        )


def interpolation_search(arr: List[int], target: int) -> Generator[Step, None, None]:
    """Interpolation search using linear interpolation formula."""
    a = list(arr)
    n = len(a)
    comparisons = 0
    low = 0
    high = n - 1

    yield Step(
        action="start",
        state=list(a),
        indices=[],
        secondary_indices=[low, high],
        pseudocode_line=0,
        message=f"Starting Interpolation Search for target {target} across range [0..{high}].",
        metrics={"comparisons": comparisons}
    )

    while low <= high and target >= a[low] and target <= a[high]:
        comparisons += 1
        if low == high:
            if a[low] == target:
                yield Step(
                    action="found",
                    state=list(a),
                    indices=[low],
                    pseudocode_line=2,
                    message=f"Single remaining element arr[{low}] matches target {target}!",
                    metrics={"comparisons": comparisons, "found_index": low}
                )
                return
            break

        # Interpolation formula
        denominator = a[high] - a[low]
        if denominator == 0:
            pos = low
        else:
            pos = low + int(((float(high - low) / denominator) * (target - a[low])))

        pos = max(low, min(pos, high))

        yield Step(
            action="probe",
            state=list(a),
            indices=[pos],
            secondary_indices=[low, high],
            pseudocode_line=1,
            message=f"Probing interpolated position {pos}: arr[{pos}] = {a[pos]} (range [{low}..{high}])",
            metrics={"comparisons": comparisons}
        )

        if a[pos] == target:
            yield Step(
                action="found",
                state=list(a),
                indices=[pos],
                secondary_indices=[low, high],
                pseudocode_line=2,
                message=f"Target {target} found at interpolated index {pos} in {comparisons} comparisons!",
                metrics={"comparisons": comparisons, "found_index": pos}
            )
            return
        elif a[pos] < target:
            yield Step(
                action="compare",
                state=list(a),
                indices=[pos],
                secondary_indices=[pos + 1, high],
                pseudocode_line=3,
                message=f"arr[{pos}]={a[pos]} < target {target}. Adjusting search lower bound.",
                metrics={"comparisons": comparisons}
            )
            low = pos + 1
        else:
            yield Step(
                action="compare",
                state=list(a),
                indices=[pos],
                secondary_indices=[low, pos - 1],
                pseudocode_line=4,
                message=f"arr[{pos}]={a[pos]} > target {target}. Adjusting search upper bound.",
                metrics={"comparisons": comparisons}
            )
            high = pos - 1

    yield Step(
        action="not_found",
        state=list(a),
        indices=[],
        pseudocode_line=5,
        message=f"Target {target} not found after {comparisons} comparisons.",
        metrics={"comparisons": comparisons, "found_index": -1}
    )

