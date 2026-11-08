"""
AlgoScope Tree Algorithms
Real implementations of BST and AVL trees with rotations, balance factors, and traversals.
"""

from typing import Any, Dict, Generator, List, Optional
from core.base_algorithm import Step

class TreeNode:
    """Represents a node in BST or AVL Tree."""
    def __init__(self, key: int):
        self.key = key
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None
        self.height: int = 1

    def to_dict(self) -> Dict[str, Any]:
        """Serialize tree to dict for step snapshots."""
        left_h = self.left.height if self.left else 0
        right_h = self.right.height if self.right else 0
        balance = left_h - right_h
        return {
            "key": self.key,
            "height": self.height,
            "balance": balance,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }


def get_height(node: Optional[TreeNode]) -> int:
    return node.height if node else 0

def get_balance(node: Optional[TreeNode]) -> int:
    return get_height(node.left) - get_height(node.right) if node else 0

def update_height(node: TreeNode):
    node.height = 1 + max(get_height(node.left), get_height(node.right))


class TreeManager:
    """Manages mutable tree state and generates visualization steps for operations."""
    def __init__(self, is_avl: bool = False):
        self.root: Optional[TreeNode] = None
        self.is_avl = is_avl

    def snapshot(self) -> Optional[Dict[str, Any]]:
        return self.root.to_dict() if self.root else None

    def insert(self, key: int) -> Generator[Step, None, None]:
        """Insert a key into BST or AVL tree."""
        yield Step(
            action="start",
            state=self.snapshot(),
            indices=[key],
            pseudocode_line=0,
            message=f"Starting insertion of key {key} into {'AVL' if self.is_avl else 'BST'}."
        )

        def _insert(node: Optional[TreeNode], val: int) -> Generator[Step, None, TreeNode]:
            if not node:
                new_node = TreeNode(val)
                yield Step(
                    action="create_node",
                    state=self.snapshot(),
                    indices=[val],
                    pseudocode_line=1,
                    message=f"Created new leaf node with key {val}."
                )
                return new_node

            yield Step(
                action="compare",
                state=self.snapshot(),
                indices=[node.key],
                secondary_indices=[val],
                pseudocode_line=2,
                message=f"Comparing incoming key {val} with node {node.key}"
            )

            if val < node.key:
                gen = _insert(node.left, val)
                res = None
                try:
                    while True:
                        yield next(gen)
                except StopIteration as e:
                    res = e.value
                node.left = res
            elif val > node.key:
                gen = _insert(node.right, val)
                res = None
                try:
                    while True:
                        yield next(gen)
                except StopIteration as e:
                    res = e.value
                node.right = res
            else:
                yield Step(
                    action="duplicate",
                    state=self.snapshot(),
                    indices=[val],
                    pseudocode_line=1,
                    message=f"Key {val} already exists in tree. Skipping."
                )
                return node

            update_height(node)

            if self.is_avl:
                balance = get_balance(node)
                yield Step(
                    action="check_balance",
                    state=self.snapshot(),
                    indices=[node.key],
                    pseudocode_line=0,
                    message=f"Node {node.key} balance factor = {balance} (Height = {node.height})"
                )

                # Left Left (LL)
                if balance > 1 and val < node.left.key:
                    yield Step(
                        action="rotate_ll",
                        state=self.snapshot(),
                        indices=[node.key, node.left.key],
                        pseudocode_line=2,
                        message=f"LL Imbalance at {node.key}! Performing Right Rotation."
                    )
                    return right_rotate(node)

                # Right Right (RR)
                if balance < -1 and val > node.right.key:
                    yield Step(
                        action="rotate_rr",
                        state=self.snapshot(),
                        indices=[node.key, node.right.key],
                        pseudocode_line=4,
                        message=f"RR Imbalance at {node.key}! Performing Left Rotation."
                    )
                    return left_rotate(node)

                # Left Right (LR)
                if balance > 1 and val > node.left.key:
                    yield Step(
                        action="rotate_lr",
                        state=self.snapshot(),
                        indices=[node.key, node.left.key],
                        pseudocode_line=3,
                        message=f"LR Imbalance at {node.key}! Left rotate child {node.left.key}, then right rotate {node.key}."
                    )
                    node.left = left_rotate(node.left)
                    return right_rotate(node)

                # Right Left (RL)
                if balance < -1 and val < node.right.key:
                    yield Step(
                        action="rotate_rl",
                        state=self.snapshot(),
                        indices=[node.key, node.right.key],
                        pseudocode_line=5,
                        message=f"RL Imbalance at {node.key}! Right rotate child {node.right.key}, then left rotate {node.key}."
                    )
                    node.right = right_rotate(node.right)
                    return left_rotate(node)

            return node

        def right_rotate(z: TreeNode) -> TreeNode:
            y = z.left
            T3 = y.right
            y.right = z
            z.left = T3
            update_height(z)
            update_height(y)
            return y

        def left_rotate(z: TreeNode) -> TreeNode:
            y = z.right
            T2 = y.left
            y.left = z
            z.right = T2
            update_height(z)
            update_height(y)
            return y

        gen = _insert(self.root, key)
        try:
            while True:
                yield next(gen)
        except StopIteration as e:
            self.root = e.value

        yield Step(
            action="done",
            state=self.snapshot(),
            indices=[key],
            pseudocode_line=4,
            message=f"Key {key} successfully integrated. Tree height is {get_height(self.root)}."
        )

    def search(self, key: int) -> Generator[Step, None, None]:
        """Search for a key in BST or AVL Tree."""
        yield Step(
            action="start",
            state=self.snapshot(),
            indices=[key],
            pseudocode_line=4,
            message=f"Starting search for key {key}."
        )

        curr = self.root
        while curr:
            yield Step(
                action="compare",
                state=self.snapshot(),
                indices=[curr.key],
                secondary_indices=[key],
                pseudocode_line=5,
                message=f"Inspecting node {curr.key} against target {key}."
            )

            if curr.key == key:
                yield Step(
                    action="found",
                    state=self.snapshot(),
                    indices=[curr.key],
                    pseudocode_line=5,
                    message=f"Found key {key} in tree!"
                )
                return
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right

        yield Step(
            action="not_found",
            state=self.snapshot(),
            indices=[],
            pseudocode_line=7,
            message=f"Key {key} not found in tree."
        )

    def delete(self, key: int) -> Generator[Step, None, None]:
        """Delete a key from the tree."""
        yield Step(
            action="start",
            state=self.snapshot(),
            indices=[key],
            pseudocode_line=0,
            message=f"Searching for node {key} to delete."
        )

        def min_value_node(node: TreeNode) -> TreeNode:
            current = node
            while current.left is not None:
                current = current.left
            return current

        def _delete(node: Optional[TreeNode], val: int) -> Generator[Step, None, Optional[TreeNode]]:
            if not node:
                yield Step(
                    action="not_found",
                    state=self.snapshot(),
                    indices=[val],
                    pseudocode_line=0,
                    message=f"Key {val} not found for deletion."
                )
                return None

            if val < node.key:
                gen = _delete(node.left, val)
                res = None
                try:
                    while True:
                        yield next(gen)
                except StopIteration as e:
                    res = e.value
                node.left = res
            elif val > node.key:
                gen = _delete(node.right, val)
                res = None
                try:
                    while True:
                        yield next(gen)
                except StopIteration as e:
                    res = e.value
                node.right = res
            else:
                yield Step(
                    action="found_delete",
                    state=self.snapshot(),
                    indices=[node.key],
                    pseudocode_line=1,
                    message=f"Found node {node.key} to delete."
                )

                # Node with only one child or no child
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left

                # Node with two children: Get the inorder successor
                temp = min_value_node(node.right)
                yield Step(
                    action="successor",
                    state=self.snapshot(),
                    indices=[temp.key],
                    secondary_indices=[node.key],
                    pseudocode_line=2,
                    message=f"Inorder successor for {node.key} is {temp.key}."
                )
                node.key = temp.key

                gen = _delete(node.right, temp.key)
                res = None
                try:
                    while True:
                        yield next(gen)
                except StopIteration as e:
                    res = e.value
                node.right = res

            if node is None:
                return None

            update_height(node)
            return node

        gen = _delete(self.root, key)
        try:
            while True:
                yield next(gen)
        except StopIteration as e:
            self.root = e.value

        yield Step(
            action="done",
            state=self.snapshot(),
            indices=[],
            pseudocode_line=0,
            message=f"Deletion completed. Current tree height: {get_height(self.root)}."
        )

    def traverse(self, mode: str) -> Generator[Step, None, None]:
        """
        Traverse the tree: 'inorder', 'preorder', 'postorder', or 'levelorder'.
        """
        order: List[int] = []

        if mode == "inorder":
            def _in(node: Optional[TreeNode]):
                if node:
                    yield from _in(node.left)
                    order.append(node.key)
                    yield Step(
                        action="traverse_visit",
                        state=self.snapshot(),
                        indices=[node.key],
                        secondary_indices=list(order),
                        message=f"Inorder visit: {node.key} (Sequence: {order})"
                    )
                    yield from _in(node.right)
            yield from _in(self.root)

        elif mode == "preorder":
            def _pre(node: Optional[TreeNode]):
                if node:
                    order.append(node.key)
                    yield Step(
                        action="traverse_visit",
                        state=self.snapshot(),
                        indices=[node.key],
                        secondary_indices=list(order),
                        message=f"Preorder visit: {node.key} (Sequence: {order})"
                    )
                    yield from _pre(node.left)
                    yield from _pre(node.right)
            yield from _pre(self.root)

        elif mode == "postorder":
            def _post(node: Optional[TreeNode]):
                if node:
                    yield from _post(node.left)
                    yield from _post(node.right)
                    order.append(node.key)
                    yield Step(
                        action="traverse_visit",
                        state=self.snapshot(),
                        indices=[node.key],
                        secondary_indices=list(order),
                        message=f"Postorder visit: {node.key} (Sequence: {order})"
                    )
            yield from _post(self.root)

        elif mode == "levelorder":
            if self.root:
                q = [self.root]
                while q:
                    curr = q.pop(0)
                    order.append(curr.key)
                    yield Step(
                        action="traverse_visit",
                        state=self.snapshot(),
                        indices=[curr.key],
                        secondary_indices=list(order),
                        message=f"Level-order visit: {curr.key} (Sequence: {order})"
                    )
                    if curr.left:
                        q.append(curr.left)
                    if curr.right:
                        q.append(curr.right)

        yield Step(
            action="done",
            state=self.snapshot(),
            indices=list(order),
            message=f"{mode.capitalize()} traversal finished: {order}"
        )

