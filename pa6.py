class Tree:
    """Represents a hierarchical tree structure."""
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.children = []

    def add_child(self, child):
        """Adds a child node."""
        self.children.append(child)

    def prune(self):
        """Removes all leaf nodes (nodes with no children)."""
        for child in self.children[:]:  
            child.prune()
        self.children = [c for c in self.children if c.children]

    def all_nodes(self):
        """Returns all nodes in depth-first order."""
        nodes = [self]
        for child in self.children:
            nodes.extend(child.all_nodes())
        return nodes


def dict_filter(func, d):
    """Filters a dictionary using a key-value predicate."""
    return {k: v for k, v in d.items() if func(k, v)}


class KVTree:
    """Represents a key-value tree structure."""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.children = []

    def add_child(self, child):
        """Adds a child node."""
        self.children.append(child)


def treemap(func, tree):
    """Applies a function to transform all tree nodes."""
    tree.key, tree.value = func(tree.key, tree.value)
    for child in tree.children:
        treemap(func, child)


class DTree:
    """Represents a decision tree for outcome determination."""
    def __init__(self, variable, threshold, lessequal, greater, outcome):
        valid_combination = (
            (outcome is None and
             variable is not None and
             threshold is not None and
             lessequal is not None and
             greater is not None) or
            (outcome is not None and
             variable is None and
             threshold is None and
             lessequal is None and
             greater is None)
        )
        if not valid_combination:
            self.new_method()
        self.variable = variable
        self.threshold = threshold
        self.lessequal = lessequal
        self.greater = greater
        self.outcome = outcome

    def new_method(self):
        raise ValueError("Invalid parameter combination")

    def tuple_atleast(self):
        """Determines the minimum required tuple size."""
        variables = set()
        def helper(node):
            if node.outcome is None:
                variables.add(node.variable)
                helper(node.lessequal)
                helper(node.greater)
        helper(self)
        return max(variables) + 1 if variables else 0

    def find_outcome(self, observations):
        """Determines the outcome based on observations."""
        current = self
        while current.outcome is None:
            value = observations[current.variable]
            current = current.lessequal if value <= current.threshold else current.greater
        return current.outcome

    def no_repeats(self):
        """Checks for repeated variable checks in any path."""
        def helper(node, seen_vars):
            if node.outcome is not None:
                return True
            if node.variable in seen_vars:
                return False
            return (
                helper(node.lessequal, seen_vars | {node.variable}) and
                helper(node.greater, seen_vars | {node.variable})
            )
        return helper(self, set())