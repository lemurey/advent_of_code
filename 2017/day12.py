from aoc_utilities import get_instructions
from collections import deque
import os


def traverse_pipes(start, pipes, history=None):
    if history is None:
        history = set()
    current = len(history)
    for node in pipes[start]:
        if node in history:
            continue
        history.add(node)
        traverse_pipes(node, pipes, history)
    return len(history), history


def get_answer(data, part2=False):
    pipes = {}
    for line in data.split('\n'):
        base, other = line.split('<->')
        base = int(base)
        if base not in pipes:
            pipes[base] = []

        for other in map(int, other.split(',')):
            pipes[base].append(other)

    seen = set()
    groups = []
    if not part2:
        return traverse_pipes(0, pipes)[0]

    for node in pipes:
        if node in seen:
            continue
        _, g = traverse_pipes(node, pipes)
        groups.append(g)
        seen = seen.union(g)

    return len(groups)


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
