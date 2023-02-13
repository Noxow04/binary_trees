from dataclasses import dataclass
from typing import Self, Union


class Tree:
    @dataclass
    class Node:
        value: Union[int, None] = None
        left: Union[Self, None] = None
        right: Union[Self, None] = None

    def __init__(self, root_value: Union[int, None] = None, allow_duplicates: bool = False):
        self._root: Self.Node = Tree.Node(root_value) if root_value else None
        self._allow_duplicates: bool = allow_duplicates
        self._depth: Union[int, None] = None
        self._values: list = []

    def __iter__(self):
        return self._browse()

    def __eq__(self, other):
        if isinstance(other, Tree):
            for self_node, other_node in zip(self, other):
                if self_node != other_node:
                    return False
            return True
        else:
            return False

    @property
    def delta_variant(self):
        return self.delta_tree()

    @property
    def allow_duplicates(self):
        return self._allow_duplicates

    @property
    def root(self):
        return self._root

    @property
    def depth(self):
        return self.calculate_depth()

    @property
    def values(self):
        return self._values

    @root.setter
    def root(self, value: int):
        if not self._root:
            self._root = Tree.Node(value)
            self._values.append(value)
        else:
            raise SyntaxError("Root has already been set for this tree !")

    def _browse(self, node: Union[Node, None] = None):
        if not node:
            if self.root:
                node = self.root
            else:
                return None
        yield node
        if node.left:
            for elt in self._browse(node.left):
                yield elt
        if node.right:
            for elt in self._browse(node.right):
                yield elt

    def replace_root(self, new_root: Union[Node, int]):
        if isinstance(new_root, Tree.Node):
            self._root = new_root
        else:
            self._root = Tree.Node(new_root)
        self._values.append(new_root.value)

    def find(self, value: int, node: Union[Node, None] = None) -> bool:
        if not node:
            node = self.root
        if node.value == value:
            return True
        elif value < node.value:
            if node.left:
                return self.find(value, node.left)
            else:
                return False
        else:
            if node.right:
                return self.find(value, node.right)
            else:
                return False

    def iterations(self, value: int, node: Union[Node, None] = None) -> int:
        if self.allow_duplicates:
            if not node:
                node = self.root
            if node.value == value:
                if node.left:
                    return self.iterations(value, node.left) + 1
                else:
                    return 1
            elif value < node.value:
                if node.left:
                    return self.iterations(value, node.left)
                else:
                    return 0
            else:
                if node.right:
                    return self.iterations(value, node.right)
                else:
                    return 0
        else:
            return int(self.find(value))

    def add_node(self, value: int, node: Union[Node, None] = None):
        if not node:
            if not self.root:
                self.root = value
                return
            node = self.root
        if value == node.value and not self.allow_duplicates:
            return
        elif value <= node.value:
            if node.left:
                self.add_node(value, node.left)
            else:
                node.left = Tree.Node(value)
                self._values.append(value)
        else:
            if node.right:
                self.add_node(value, node.right)
            else:
                node.right = Tree.Node(value)
                self._values.append(value)

    def insert_values(self, *values: int):
        if not self.root:
            self.root = values[0]
            values = values[1:]
        for elt in values:
            self.add_node(elt)

    def delta_tree(self):
        delta_tree = self.copy()
        root_value = delta_tree.root.value
        for elt in delta_tree:
            if elt != delta_tree.root:
                elt.value -= root_value
        return delta_tree

    def copy(self):
        tree_duplicate = Tree(allow_duplicates=self.allow_duplicates)
        for elt in self:
            tree_duplicate.add_node(elt.value)
        return tree_duplicate

    def as_list(self, node: Union[Node, None] = None):
        if not node:
            node = self.root
        return [node.value,
                self.as_list(node.left) if node.left else None,
                self.as_list(node.right) if node.right else None]

    def calculate_depth(self, node: Union[Node, None] = None, include_root_in_depth: bool = True) -> int:
        if not node:
            if self.root:
                node = self.root
            else:
                raise SyntaxError("Tree is empty")
        if not node.left:
            if not node.right:
                return 1 if include_root_in_depth else 0
            else:
                return self.calculate_depth(node.right, include_root_in_depth) + 1
        else:
            if not node.right:
                return self.calculate_depth(node.left, include_root_in_depth) + 1
            else:
                return max(self.calculate_depth(node.left, include_root_in_depth),
                           self.calculate_depth(node.right, include_root_in_depth)) + 1

    def optimize(self, keep_root: bool = False):
        if keep_root:
            optimized_tree = Tree(root_value=self.root.value)
            values = self.values[1:]
            values.sort()
        else:
            values = self.values
            values.sort()
            root = values.pop(len(values) // 2)
            optimized_tree = Tree(root_value=root)
        Tree._sorted_insert(values, optimized_tree.root)
        self.replace_root(optimized_tree.root)

    @classmethod
    def build_from_values(cls, root_value: int, *values: int, allow_duplicates: bool = False) -> Self:
        tree = Tree(root_value, allow_duplicates)
        for elt in values:
            tree.add_node(elt)
        return tree

    @staticmethod
    def _sorted_insert(values: list, node: Node):
        half_index = len(values) // 2
        left_half, right_half = values[:half_index], values[half_index:]
        if left_half:
            left_half_pop = left_half.pop(len(left_half) // 2)
            node.left = Tree.Node(left_half_pop)
            Tree._sorted_insert(left_half, node.left)
        if right_half:
            right_half_pop = right_half.pop(len(right_half) // 2)
            node.right = Tree.Node(right_half_pop)
            Tree._sorted_insert(right_half, node.right)


def main():
    t = Tree.build_from_values(5, 2, 9, 8, allow_duplicates=True)
    t.insert_values(4, 3, 5)
    print(t.root)
    print(t.find(2))
    print(t.iterations(5))
    print(t.depth)
    print(t.as_list())
    print(t.values)
    t_d = t.delta_variant
    print(t_d.as_list())
    t_c = t.copy()
    t_c.optimize()
    print(t_c.as_list())
    print(f"{t.depth} >= {t_c.depth}")
    print(Tree(2) == Tree(2))
    for i in t:
        print(i)


if __name__ == "__main__":
    main()
