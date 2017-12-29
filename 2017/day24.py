from aoc_utilities import get_instructions
from utilities import timeit
import os


def make_parts(data):
    parts = {}
    for line in data.split('\n'):
        a, b = map(int, line.split('/'))
        if a not in parts:
            parts[a] = set()
        if b not in parts:
            parts[b] = set()
        parts[a].add(b)
        parts[b].add(a)
    return parts


def score_bridge(bridge):
    total = 0
    for part in bridge:
        total += sum(part)
    return total


def make_bridges(bridge, components):
    if bridge is None:
        bridge = set([(0, 0)]), 0
    current_end = bridge[-1]
    for option in components[current_end]:
        if current_end <= option:
            compare = (current_end, option)
        else:
            compare = (option, current_end)
        if compare not in bridge[0]:
            new = bridge[0] | {compare}, option
            yield new
            yield from make_bridges(new, components)


@timeit
def get_answer(data, part2=False):
    parts = make_parts(data)
    max_score = -1
    max_length = -1
    l_score = -1
    for bridge, _ in make_bridges(None, parts):
        score = score_bridge(bridge)
        length = len(bridge)
        if length > max_length or (length == max_length and score > l_score):
            max_length = length
            l_score = score
        if score > max_score:
            max_score = score
    if part2:
        return l_score
    return max_score


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
