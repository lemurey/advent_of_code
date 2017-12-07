from aoc_utilities import get_instructions
import os


class Node:
    def __init__(self, name, weight, parent=None):
        self.name = name
        self.weight = weight
        self._parent = None
        self._children = set()
        self.total_weight = self.weight
        self.child_support = None
        if parent is not None:
            self.set_parent(parent)

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return self.__str__()

    def add_child(self, other):
        if not isinstance(other, Node):
            raise NotImplementedError('Cannot have non Node be child or parent'
                                      ' of Node')
        if other not in self._children:
            self._children.add(other)

        if not other._parent == self:
            other.set_parent(self)

    def set_parent(self, other):
        if not isinstance(other, Node):
            raise NotImplementedError('Cannot have non Node be child or parent '
                                      'of Node')
        if self._parent is not None:
            if self in self._parent._children:
                self._parent._children.remove(self)

        self._parent = other
        other.add_child(self)

    def update_weights(self):
        for child in self._children:
            child.update_weights()
        self.child_support = self._child_support()
        self.total_weight = sum(self.child_support) + self.weight

    def _child_support(self):
        return [c.total_weight for c in self._children]

    def check_node(self):
        if self.total_weight == 0:
            self.update_weights()
        test_layer = self.child_support
        index = get_different_element(test_layer)
        if index == -1:
            return 0
        offender = self.get_offender(index)
        while True:
            prev_layer = test_layer
            test_layer = offender.child_support
            prev_index = index
            index = get_different_element(test_layer)
            if index != -1:
                offender = offender.get_offender(index)
            else:
                diff = prev_layer[prev_index - 1] - prev_layer[prev_index]
                return diff + offender.weight

    def get_offender(self, key):
        if self.child_support is None:
            self.update_weights()
        for child in self._children:
            if child.total_weight == self.child_support[key]:
                return child


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


def make_tree(data):
    storage = parse_data(data)
    nodes = {}
    for name, (support, weight) in storage.items():
        if name not in nodes:
            cur_node = Node(name, weight)
            nodes[cur_node.name] = cur_node
        else:
            cur_node = nodes[name]

        for child_name in support:
            if child_name in nodes:
                child_node = nodes[child_name]
                child_node.set_parent(cur_node)
            else:
                child_weight = storage[child_name][1]
                child_node = Node(child_name, child_weight, cur_node)
                nodes[child_name] = child_node
    return nodes


def get_answer(tree, part2=False):

    for node in tree.values():
        if node._parent is None:
            root = node

    if not part2:
        return root

    root.update_weights()

    return root.check_node()


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    tree = make_tree(inputs)

    print(get_answer(tree, part2=False))
    print(get_answer(tree, part2=True))
