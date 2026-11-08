"""
AlgoScope Data Structures
Interactive step-by-step logic for Stack, Queue, Circular Queue, Linked Lists, and Hash Table.
"""

from typing import Any, Dict, Generator, List, Optional
from core.base_algorithm import Step

class VisualStack:
    """Stack (LIFO) model yielding visualization steps."""
    def __init__(self, capacity: int = 8):
        self.capacity = capacity
        self.items: List[Any] = []

    def push(self, val: Any) -> Generator[Step, None, None]:
        if len(self.items) >= self.capacity:
            yield Step(
                action="overflow",
                state=list(self.items),
                message=f"Stack Overflow! Maximum capacity {self.capacity} reached."
            )
            return

        self.items.append(val)
        yield Step(
            action="push",
            state=list(self.items),
            indices=[len(self.items) - 1],
            message=f"Pushed {val} onto top of Stack (Top index: {len(self.items) - 1})."
        )

    def pop(self) -> Generator[Step, None, None]:
        if not self.items:
            yield Step(
                action="underflow",
                state=list(self.items),
                message="Stack Underflow! Stack is already empty."
            )
            return

        val = self.items.pop()
        yield Step(
            action="pop",
            state=list(self.items),
            indices=[len(self.items) - 1] if self.items else [],
            message=f"Popped {val} from top of Stack."
        )

    def peek(self) -> Generator[Step, None, None]:
        if not self.items:
            yield Step(
                action="empty",
                state=list(self.items),
                message="Stack is empty. Cannot peek."
            )
            return

        val = self.items[-1]
        yield Step(
            action="peek",
            state=list(self.items),
            indices=[len(self.items) - 1],
            message=f"Peeked top element: {val} at index {len(self.items) - 1}."
        )


class VisualQueue:
    """Linear Queue (FIFO) model yielding visualization steps."""
    def __init__(self, capacity: int = 8):
        self.capacity = capacity
        self.items: List[Any] = []

    def enqueue(self, val: Any) -> Generator[Step, None, None]:
        if len(self.items) >= self.capacity:
            yield Step(
                action="overflow",
                state=list(self.items),
                message=f"Queue Overflow! Maximum capacity {self.capacity} reached."
            )
            return

        self.items.append(val)
        yield Step(
            action="enqueue",
            state=list(self.items),
            indices=[len(self.items) - 1],
            secondary_indices=[0],
            message=f"Enqueued {val} at rear (Rear: {len(self.items) - 1}, Front: 0)."
        )

    def dequeue(self) -> Generator[Step, None, None]:
        if not self.items:
            yield Step(
                action="underflow",
                state=list(self.items),
                message="Queue Underflow! Queue is already empty."
            )
            return

        val = self.items.pop(0)
        yield Step(
            action="dequeue",
            state=list(self.items),
            indices=[0] if self.items else [],
            message=f"Dequeued {val} from front of Queue."
        )


class VisualCircularQueue:
    """Fixed-capacity Circular Queue (Ring Buffer) with front and rear pointers."""
    def __init__(self, capacity: int = 8):
        self.capacity = capacity
        self.buffer: List[Optional[Any]] = [None] * capacity
        self.front: int = -1
        self.rear: int = -1
        self.size: int = 0

    def snapshot(self) -> Dict[str, Any]:
        return {
            "buffer": list(self.buffer),
            "front": self.front,
            "rear": self.rear,
            "size": self.size,
            "capacity": self.capacity
        }

    def enqueue(self, val: Any) -> Generator[Step, None, None]:
        if self.size == self.capacity:
            yield Step(
                action="overflow",
                state=self.snapshot(),
                message="Circular Queue Overflow! Ring buffer is completely full."
            )
            return

        if self.front == -1:
            self.front = 0
            self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.capacity

        self.buffer[self.rear] = val
        self.size += 1

        yield Step(
            action="enqueue",
            state=self.snapshot(),
            indices=[self.rear],
            secondary_indices=[self.front],
            message=f"Enqueued {val} at index {self.rear} (Front: {self.front}, Rear: {self.rear}, Size: {self.size}/{self.capacity})."
        )

    def dequeue(self) -> Generator[Step, None, None]:
        if self.size == 0:
            yield Step(
                action="underflow",
                state=self.snapshot(),
                message="Circular Queue Underflow! Ring buffer is empty."
            )
            return

        val = self.buffer[self.front]
        self.buffer[self.front] = None
        old_front = self.front
        self.size -= 1

        if self.size == 0:
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity

        yield Step(
            action="dequeue",
            state=self.snapshot(),
            indices=[old_front],
            secondary_indices=[self.front] if self.front != -1 else [],
            message=f"Dequeued {val} from index {old_front} (New Front: {self.front}, Rear: {self.rear})."
        )


class VisualLinkedList:
    """Linked list supporting both Singly and Doubly linked modes."""
    def __init__(self, is_doubly: bool = False):
        self.is_doubly = is_doubly
        self.nodes: List[Any] = []  # Array of node values

    def snapshot(self) -> Dict[str, Any]:
        return {"nodes": list(self.nodes), "is_doubly": self.is_doubly}

    def insert_head(self, val: Any) -> Generator[Step, None, None]:
        self.nodes.insert(0, val)
        yield Step(
            action="insert_head",
            state=self.snapshot(),
            indices=[0],
            message=f"Inserted new head node with value '{val}'."
        )

    def insert_tail(self, val: Any) -> Generator[Step, None, None]:
        self.nodes.append(val)
        yield Step(
            action="insert_tail",
            state=self.snapshot(),
            indices=[len(self.nodes) - 1],
            message=f"Appended node '{val}' at tail position {len(self.nodes) - 1}."
        )

    def delete(self, val: Any) -> Generator[Step, None, None]:
        if not self.nodes:
            yield Step(action="empty", state=self.snapshot(), message="Linked list is empty.")
            return

        # Animate searching for node first
        for i, item in enumerate(self.nodes):
            yield Step(
                action="traverse",
                state=self.snapshot(),
                indices=[i],
                message=f"Checking node at position {i}: val='{item}' vs target='{val}'"
            )
            if item == val:
                del self.nodes[i]
                yield Step(
                    action="deleted",
                    state=self.snapshot(),
                    indices=[i] if i < len(self.nodes) else [],
                    message=f"Deleted node with value '{val}' at position {i}."
                )
                return

        yield Step(
            action="not_found",
            state=self.snapshot(),
            message=f"Node '{val}' not found in linked list."
        )

    def search(self, val: Any) -> Generator[Step, None, None]:
        for i, item in enumerate(self.nodes):
            yield Step(
                action="traverse",
                state=self.snapshot(),
                indices=[i],
                message=f"Traversing pointer to index {i}: value = '{item}'"
            )
            if item == val:
                yield Step(
                    action="found",
                    state=self.snapshot(),
                    indices=[i],
                    message=f"Found node '{val}' at position {i}!"
                )
                return

        yield Step(
            action="not_found",
            state=self.snapshot(),
            message=f"Value '{val}' does not exist in linked list."
        )


class VisualHashTable:
    """Hash Table supporting Separate Chaining or Linear Probing collision resolution."""
    def __init__(self, capacity: int = 7, mode: str = "chaining"):
        self.capacity = capacity
        self.mode = mode  # 'chaining' or 'linear_probing'
        if mode == "chaining":
            self.table: List[List[Tuple[str, Any]]] = [[] for _ in range(capacity)]
        else:
            self.table: List[Optional[Tuple[str, Any]]] = [None] * capacity

    def _hash(self, key: str) -> int:
        if key.isdigit():
            return int(key) % self.capacity
        # Polynomial rolling hash
        h = 0
        for ch in key:
            h = (h * 31 + ord(ch)) % self.capacity
        return h

    def snapshot(self) -> Dict[str, Any]:
        return {
            "capacity": self.capacity,
            "mode": self.mode,
            "table": [list(b) if isinstance(b, list) else b for b in self.table]
        }

    def insert(self, key: str, val: Any) -> Generator[Step, None, None]:
        h_idx = self._hash(key)
        yield Step(
            action="hash",
            state=self.snapshot(),
            indices=[h_idx],
            message=f"Computed hash index for key '{key}': hash('{key}') % {self.capacity} = {h_idx}"
        )

        if self.mode == "chaining":
            bucket = self.table[h_idx]
            # Check for update
            for i, (k, _) in enumerate(bucket):
                if k == key:
                    bucket[i] = (key, val)
                    yield Step(
                        action="update",
                        state=self.snapshot(),
                        indices=[h_idx],
                        message=f"Updated existing key '{key}' to value '{val}' in bucket {h_idx}."
                    )
                    return

            bucket.append((key, val))
            yield Step(
                action="chain_insert",
                state=self.snapshot(),
                indices=[h_idx],
                message=f"Inserted ({key}: {val}) into bucket {h_idx} (Chain length: {len(bucket)})."
            )
        else:
            # Linear probing
            curr = h_idx
            probes = 0
            while self.table[curr] is not None and self.table[curr][0] != key:
                yield Step(
                    action="collision",
                    state=self.snapshot(),
                    indices=[curr],
                    message=f"Collision at slot {curr}! Probing next slot..."
                )
                curr = (curr + 1) % self.capacity
                probes += 1
                if probes >= self.capacity:
                    yield Step(
                        action="overflow",
                        state=self.snapshot(),
                        message="Hash Table is completely full! Cannot insert."
                    )
                    return

            self.table[curr] = (key, val)
            yield Step(
                action="probe_insert",
                state=self.snapshot(),
                indices=[curr],
                message=f"Placed ({key}: {val}) at slot {curr} after {probes} probe(s)."
            )

    def search(self, key: str) -> Generator[Step, None, None]:
        h_idx = self._hash(key)
        yield Step(
            action="hash",
            state=self.snapshot(),
            indices=[h_idx],
            message=f"Looking up key '{key}' starting at hash index {h_idx}."
        )

        if self.mode == "chaining":
            bucket = self.table[h_idx]
            for k, v in bucket:
                if k == key:
                    yield Step(
                        action="found",
                        state=self.snapshot(),
                        indices=[h_idx],
                        message=f"Found key '{key}' with value '{v}' in bucket {h_idx}!"
                    )
                    return
            yield Step(
                action="not_found",
                state=self.snapshot(),
                indices=[h_idx],
                message=f"Key '{key}' not found in bucket {h_idx}."
            )
        else:
            curr = h_idx
            probes = 0
            while self.table[curr] is not None:
                yield Step(
                    action="probe_check",
                    state=self.snapshot(),
                    indices=[curr],
                    message=f"Checking slot {curr} for key '{key}'..."
                )
                if self.table[curr][0] == key:
                    yield Step(
                        action="found",
                        state=self.snapshot(),
                        indices=[curr],
                        message=f"Found key '{key}' with value '{self.table[curr][1]}' at slot {curr}!"
                    )
                    return
                curr = (curr + 1) % self.capacity
                probes += 1
                if probes >= self.capacity:
                    break

            yield Step(
                action="not_found",
                state=self.snapshot(),
                message=f"Key '{key}' not found in hash table."
            )

    def delete(self, key: str) -> Generator[Step, None, None]:
        h_idx = self._hash(key)
        if self.mode == "chaining":
            bucket = self.table[h_idx]
            for i, (k, _) in enumerate(bucket):
                if k == key:
                    del bucket[i]
                    yield Step(
                        action="deleted",
                        state=self.snapshot(),
                        indices=[h_idx],
                        message=f"Deleted key '{key}' from bucket {h_idx}."
                    )
                    return
            yield Step(action="not_found", state=self.snapshot(), message=f"Key '{key}' not found.")
        else:
            curr = h_idx
            probes = 0
            while self.table[curr] is not None:
                if self.table[curr][0] == key:
                    self.table[curr] = None
                    yield Step(
                        action="deleted",
                        state=self.snapshot(),
                        indices=[curr],
                        message=f"Deleted key '{key}' at slot {curr}."
                    )
                    return
                curr = (curr + 1) % self.capacity
                probes += 1
                if probes >= self.capacity:
                    break
            yield Step(action="not_found", state=self.snapshot(), message=f"Key '{key}' not found.")

