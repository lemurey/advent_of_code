from aoc_utilities import get_instructions
from pathlib import Path
from operator import add, mul, truediv, sub, lt, gt
from itertools import cycle

OPERATIONS = {'+': add, '*': mul, '/': truediv, '-': sub}

class MonkeyNode:
    def __init__(self, name, children=None, value=None, op=None):
        self.name = name
        assert (value is None) or (children is None)
        if children is not None:
            assert op is not None
        self.value = value
        self.children = children
        self.op = op

    def __call__(self, human=None):
        if self.children is None:
            if self.name == 'humn' and human is not None:
                return human
            return self.value
        else:
            if self.name == 'root' and human is not None:
                return self.children[0](human), self.children[1](human)
            return self.op(self.children[0](human), self.children[1](human))


def process_data(data):
    monkey_store = {}
    for row in data:
        name, rest = row.split(':')
        if rest.strip().isdigit():
            monkey_store[name] = int(rest.strip())
        else:
            c1, op, c2 = rest.split()
            monkey_store[name] = ((c1, c2), OPERATIONS[op])

    return monkey_store


def process_monkies(store):
    monkies = {}
    needs_children = []
    for name, v in store.items():
        if isinstance(v, int):
            monkies[name] = MonkeyNode(name, value=v)
        else:
            (c1, c2), op = v
            if (c1 in monkies) and (c2 in monkies):
                children = monkies[c1], monkies[c2]
                monkies[name] = MonkeyNode(name, children=children, op=op)
            else:
                needs_children.append(name)
    to_find = len(needs_children)
    found = 0
    needs_children = cycle(needs_children)
    while found < to_find:
        name = next(needs_children)
        if name not in monkies:
            (c1, c2), op = store[name]
            if (c1 in monkies) and (c2 in monkies):
                children = monkies[c1], monkies[c2]
                monkies[name] = MonkeyNode(name, children=children, op=op)
                found += 1

    return monkies['root']


def search_a(root, fixed, op, flip):
    c = 1
    s, f = root(c)
    if flip:
        f, s = s, f

    while True:
        c *= 2
        s, f = root(c)
        if flip:
            f, s = s, f
        if not op(s, f):
            break
        if c > 2 ** 52:
            print('you fucked up')
            return False

    high = c
    low = c // 2
    low, high = sorted((low, high))
    i = 0
    while low < high:
        i += 1
        mid = (high + low) / 2

        s, f = root(mid)
        if (s == low) or (s == high):
            print('you fucked up')
            return False
        if flip:
            f, s = s, f
        print(i, s, f, mid)
        if op(s, f):
            low = mid
        elif not op(s, f):
            high = mid
        else:
            return mid
        # damn floats
        if abs(s - f) < 1e-5:
            return mid


def monkey_search(root):
    seen_a = set()
    seen_b = set()
    for i in range(10):
        a, b = root(i)
        if i == 0:
            first_a = a
            first_b = b
        seen_a.add(a)
        seen_b.add(b)
    if len(seen_a) == 1:
        fixed = a
        if first_a < first_b:
            op = gt
        else:
            op = lt
        flip = True
    else:
        fixed = b
        if first_a < first_b:
            op = lt
        else:
            op = gt
        flip = False
    return search_a(root, fixed, op, flip)


def get_answer(data, part2=False):
    monkey_store = process_data(data)
    root = process_monkies(monkey_store)
    if part2:
        return monkey_search(root)
    return root()


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''root: pppw + sjmn
# dbpl: 5
# cczh: sllz + lgvd
# zczc: 2
# ptdq: humn - dvpt
# dvpt: 3
# lfqf: 4
# humn: 5
# ljgn: 2
# sjmn: drzm * dbpl
# sllz: 4
# pppw: cczh / lfqf
# lgvd: ljgn * ptdq
# drzm: hmdt - zczc
# hmdt: 32'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
