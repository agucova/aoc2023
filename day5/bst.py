from dataclasses import dataclass, field
from typing import Optional

@dataclass
class TreeNode:
    source_interval: range
    target_interval: range
    left: Optional["TreeNode"] = field(default=None)
    right: Optional["TreeNode"] = field(default=None)


@dataclass
class BinarySearchTree:
    root: Optional["TreeNode"] = field(default=None, repr=False)

    def insert(self, source: range, target: range) -> None:
        if self.root is None:
            self.root = TreeNode(source, target)
        else:
            self._insert(source, target, self.root)

    def _insert(self, source: range, target: range, node: TreeNode) -> None:
        if source.stop <= node.source_interval.start:
            if node.left is None:
                node.left = TreeNode(source, target)
            else:
                self._insert(source, target, node.left)
        elif node.source_interval.stop <= source.start:
            if node.right is None:
                node.right = TreeNode(source, target)
            else:
                self._insert(source, target, node.right)
        elif (
            source.start != node.source_interval.start
            or source.stop != node.source_interval.stop
        ):
            raise ValueError("Overlapping interval provided.")

    def map(self, value: int) -> int:
        search_result = self.find(value)
        if search_result is None:
            return value
        source_interval, target_interval = search_result
        return target_interval.start + (value - source_interval.start)

    def find_maps(self, interval: range) -> list[tuple[range, range]]:
        # Recursively all intervals which fit inside the given interval
        # And union all of their target intervals
        return self._interval_map(interval, self.root)

    def _interval_map(
        self, interval: range, node: TreeNode | None
    ) -> list[tuple[range, range]]:
        if node is None:
            return []
        elif interval.stop <= node.source_interval.start:
            return self._interval_map(interval, node.left)
        elif node.source_interval.stop <= interval.start:
            return self._interval_map(interval, node.right)
        else:
            return (
                [(node.source_interval, node.target_interval)]
                + self._interval_map(interval, node.left)
                + self._interval_map(interval, node.right)
            )

    def find(self, value: int) -> tuple[range, range] | None:
        return self._find(value, self.root)

    def _find(self, value: int, node: TreeNode | None) -> tuple[range, range] | None:
        if node is None:
            return None
        elif value < node.source_interval.start:
            return self._find(value, node.left)
        elif value > node.source_interval.stop:
            return self._find(value, node.right)
        else:
            return (node.source_interval, node.target_interval)