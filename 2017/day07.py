from aoc_utilities import get_instructions
import os

class Node:
    def __init__(self, name, weight, parent=None):
        self.name = name
        self.weight = weight
        self._parent = None
        self._children = []
        self.supported_weight = None
        self.set_parent(parent)

    def add_child(self, other):
        if not self.has_child(other):
            self._children.append(other)

        if not other._parent == self:
            other.set_parent(self)

    def remove_child(self, other):
        index = self._children.index(other)
        return self._children.pop(index)

    def set_parent(self, other):
        if self._parent is not None:
            if self._parent.has_child(self):
                self._parent.remove_child(self)

        self._parent = other

        if isinstance(other, Node):
            other.add_child(self)

    def has_child(self, child):
        if child in self._children:
            return True
        return False

    def _get_error_layer(self, output=None):
        if output is None:
            output = []
        if self.supported_weight is None:
            self.calculate_supported_weight()
        if len(self._children) == 0:
            return 0
        check = get_different_element(self._child_support())
        if check == -1:
            return 0
        output.append(check)
        while 0 not in output:
            temp = self._children[check]._get_error_layer(output)
            output.append(temp)
        return output[:output.index(0)]

    def check_node(self):
        order = self._get_error_layer()
        problem = self._children[order[0]]
        for index in order[1:-1]:
            problem = problem._children[index]
        index = order[-1]
        array = problem._child_support()
        diff = array[index - 1] - array[index]
        return diff + problem._children[index].weight

    def _child_support(self):
        return [x.weight + x.supported_weight for x in self._children]

    def calculate_supported_weight(self):
        if len(self._children) == 0:
            self.supported_weight = 0

        for child in self._children:
            child.calculate_supported_weight()

        total = 0
        for child in self._children:
            total += child.supported_weight
            total += child.weight
        self.supported_weight = total

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


def get_different_element(array):
    check = array[0]
    test = [x == check for x in array[1:]]
    if all(test):
        return -1
    if not any(test):
        return 0
    return test.index(False) + 1


def parse_data(data):
    storage = {}
    for line in data.split('\n'):
        second = None
        if '->' in line:
            first, second = line.split('->')
        else:
            first = line
        name, weight = first.split('(')
        name = name.strip()
        weight = int(weight.strip(') '))
        if second:
            support = [x.strip() for x in second.split(',')]
        else:
            support = []
        if name not in storage:
            storage[name] = (support, weight)
        else:
            print('bad stuff happened')
    return storage


def get_node(name, nodes):
    for node in nodes:
        if node.name == name:
            return node


def make_tree(data):
    storage = parse_data(data)
    node_set = set()
    nodes = []

    for name, (support, weight) in storage.items():
        if len(support) == 0:
            continue

        if name not in node_set:
            cur_node = Node(name, weight)
            nodes.append(cur_node)
            node_set.add(name)
        else:
            cur_node = get_node(name, nodes)

        for entry in support:
            if entry in node_set:
                child = get_node(entry, nodes)
                child.set_parent(cur_node)
            else:
                child = Node(entry, storage[entry][1], cur_node)
                nodes.append(child)
                node_set.add(entry)
    return nodes


def get_answer(tree, part2=False):

    for node in tree:
        if node._parent is None:
            root = node

    if not part2:
        return root

    root.calculate_supported_weight()

    return root.check_node()


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    tree = make_tree(inputs)

    print(get_answer(tree, part2=False))
    print(get_answer(tree, part2=True))
