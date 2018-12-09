from aoc_utilities import get_instructions
import os
from itertools import count

NODE_NUMBER = count()


class Node(object):
    def __init__(self, num_children, num_meta, parent=None):
        self.id = next(NODE_NUMBER)
        self.parent = parent
        self.num_children = num_children
        self.to_take = num_meta
        self.meta_entries = []
        self.children = []
        self.value = None

    def is_root(self):
        return self.parent is None

    def process_children(self, rest):
        while len(self.children) < self.num_children:
            (num_children, num_meta), rest = rest[:2], rest[2:]
            child = Node(num_children, num_meta, self.id)
            self.children.append(child)
            rest = child.process_children(rest)
        self.meta_entries, rest = rest[:self.to_take], rest[self.to_take:]
        return rest

    def calc_score(self):
        start = sum(self.meta_entries)
        return start + sum([x.calc_score() for x in self.children])

    def _get_value(self):
        if len(self.children) == 0:
            return sum(self.meta_entries)
        total = 0
        for entry in self.meta_entries:
            index = entry - 1
            if index < len(self.children):
                current = self.children[index]
                total += current.calc_value()
        return total

    def calc_value(self):
        if self.value is None:
            self.value = self._get_value()
        return self.value

    def __repr__(self):
        return 'Node object id_num: {} -- value: {}'.format(self.id,
            self.calc_value())

def get_answer(data, part2=False):
    nums = map(int, data[0].split())
    (num_children, num_meta), rest = nums[:2], nums[2:]
    root = Node(num_children, num_meta)
    root.process_children(rest)
    if part2:
        return root.calc_value()
    return root.calc_score()


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    sample = ['2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2']
    print(get_answer(sample, part2=True))
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))