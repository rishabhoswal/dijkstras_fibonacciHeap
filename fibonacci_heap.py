class FibonacciHeapNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.parent = None
        self.child = None
        self.left = self.right = self
        self.degree = 0
        self.marked = False

    def add_child(self, node):
        node.parent = self
        if not self.child:
            self.child = node
        else:
            node.left = self.child.left
            node.right = self.child
            self.child.left.right = node
            self.child.left = node
        self.degree += 1

    def remove_child(self, node):
        if self.child == node:
            if node.right == node:
                self.child = None
            else:
                self.child = node.right
                node.right.left = node.left
                node.left.right = node.right

        node.parent = None
        node.left = node.right = node
        self.degree -= 1


class FibonacciHeap:
    def __init__(self):
        self.min_node = None
        self.num_of_nodes = 0

    def is_empty(self):
        return self.num_of_nodes == 0

    def add_node(self, key, value):
        new_node = FibonacciHeapNode(key, value)
        if not self.min_node:
            self.min_node = new_node
        else:
            self.min_node.left.right = new_node
            new_node.left = self.min_node.left
            new_node.right = self.min_node
            self.min_node.left = new_node
            if new_node.key < self.min_node.key:
                self.min_node = new_node

        self.num_of_nodes += 1
        return new_node

    def remove_min_node(self):
        min_node = self.min_node
        if min_node:
            child = min_node.child
            while child:
                next_child = child.right
                self.min_node.lef.right = child
                child.left = self.min_node.left
                child.right = self.min_node
                self.min_node.left = child
                child.parent = None
                child = next_child

            min_node.left.right = min_node.right
            min_node.right.left = min_node.left

            if min_node == min_node.right:
                self.min_node = None
            else:
                self.min_node = min_node.right
                self._consolidate()

            self.num_of_nodes -= 1

        return min_node.key, min_node

    def decrease_key(self, node, new_key):
        if new_key > node.key:
            raise ValueError('New key is greater than current key')

        node.key = new_key
        parent = node.parent
        if parent and node.key < parent.key:
            self._cut(node, parent)
            self._cascading_cut(parent)

        if node.key < self.min_node.key:
            self.min_node = node

    def _cut(self, node, parent):
        parent.remove_child(node)
        self.min_node.left.right = node
        node.left = self.min_node.left
        node.right = self.min_node
        self.min_node.left = node
        node.parent = None
        node.marked = False

    def _cascading_cut(self, node):
        parent = node.parent
        if parent:
            if not node.marked:
                node.marked = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)

    def _consolidate(self):
        degree_table = [None] * self.num_of_nodes
        node = self.min_node
        root_nodes = []

        while node:
            if node in root_nodes:
                break
            root_nodes.append(node)
            next_node = node.right
            degree = node.degree

            while degree_table[degree] is not None:
                other = degree_table[degree]
                if other == node:
                    break
                if node.key > other.key:
                    node, other = other, node
                self._link(other, node)
                degree_table[degree] = None
                degree += 1

            degree_table[degree] = node
            node = next_node

        self.min_node = None
        for node in root_nodes:
            if self.min_node is None or node.key < self.min_node.key:
                self.min_node = node
        return

    def _link(self, child, parent):
        child.left.right = child.right
        child.right.left = child.left
        child.parent = parent

        if parent.child is None:
            parent.child = child
            child.left = child.right = child
        else:
            child.left = parent.child
            child.right = parent.child.right
            parent.child.right.left = child
            parent.child.right = child
        parent.degree += 1
        child.marked = False

    def find_node(self, key):
        return self._find_node_helper(key, self.min_node)

    def _find_node_helper(self, key, node):
        if not node:
            return None

        if node.key == key:
            return node

        child = node.child
        while child:
            result = self._find_node_helper(key, child)
            if result:
                return result
            child = child.right
        return None

    def delete_node(self, node):
        self.decrease_key(node, float('-inf'))
        self.remove_min_node()

    def merge(self, other_heap):
        self.min_node.left.right = other_heap.min_node.right
        other_heap.min_node.right.left = self.min_node.left
        self.min_node.left = other_heap.min_node
        other_heap.min_node.right = self.min_node

        if other_heap.min_node.key < self.min_node.key:
            self.min_node = other_heap.min_node

        self.num_of_nodes += other_heap.num_of_nodes
