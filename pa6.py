class Tree:
    """Represents a hierarchical tree structure"""
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.children = []

    def add_child(self, child):
        """Adds a child node"""
        self.children.append(child)

    def prune(self):
        """Removes all childless nodes"""
        for child in self.children[:]:
            child.prune()
        self.children = [c for c in self.children if c.children]

    def all_nodes(self):
        """Returns all nodes in depth-first order"""
        nodes = [self]
        for child in self.children:
            nodes.extend(child.all_nodes())
        return nodes


def dict_filter(func, d):
    """Filters dictionary using key-value predicate"""
    return {k: v for k, v in d.items() if func(k, v)}


class KVTree:
    """Key-Value tree structure"""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.children = []

    def add_child(self, child):
        """Adds child node"""
        self.children.append(child)

def treemap(func, tree):
    """Applies function to all nodes"""
    tree.key, tree.value = func(tree.key, tree.value)
    for child in tree.children:
        treemap(func, child)


class DTree:
    """Decision tree for outcome determination"""
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
            raise ValueError("Invalid parameter combination")

        self.variable = variable
        self.threshold = threshold
        self.lessequal = lessequal
        self.greater = greater
        self.outcome = outcome

    def tuple_atleast(self):
        """Minimum required tuple size"""
        variables = set()
        
        def _traverse(node):
            if node.outcome is None:
                variables.add(node.variable)
                _traverse(node.lessequal)
                _traverse(node.greater)
        
        _traverse(self)
        return max(variables) + 1 if variables else 0

    def find_outcome(self, observations):
        """Determine outcome from observations"""
        current = self
        while current.outcome is None:
            obs = observations[current.variable]
            current = (current.lessequal if obs <= current.threshold
                       else current.greater)
        return current.outcome

    def no_repeats(self):
        """Check for repeated variable checks"""
        def _check(node, seen):
            if node.outcome is not None:
                return True
            if node.variable in seen:
                return False
            return (_check(node.lessequal, seen | {node.variable}) and
                    _check(node.greater, seen | {node.variable}))
        
        return _check(self, set())