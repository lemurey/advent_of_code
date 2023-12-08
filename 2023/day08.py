from aoc_utilities import get_instructions
from pathlib import Path
from itertools import cycle
from math import lcm


def get_nodes(data):
    nodes = {}
    for i, line in enumerate(data):
        if i == 0:
            instructions = line
            continue
        elif line == '':
            continue
        k, v = line.split('=')
        nodes[k.strip()] = tuple(v.strip()[1:-1].split(', '))
    instructions = cycle(instructions)
    return instructions, nodes


def run_instructions(data):
    dirs = {'R': 1, 'L': 0}
    instructions, nodes = get_nodes(data)
    cur_node = 'AAA'
    steps = 0
    while cur_node != 'ZZZ':
        d = dirs[next(instructions)]
        cur_node = nodes[cur_node][d]
        steps += 1
    return steps


def check_for_cycles(data):
    dirs = {'R': 1, 'L': 0}
    instructions, nodes = get_nodes(data)
    to_check = [x for x in nodes if x.endswith('A')]
    cycles = {n: 0 for n in to_check}
    for node in to_check:
        instructions = cycle(data[0])
        cur_node = node
        steps = 0
        while not cur_node.endswith('Z'):
            d = dirs[next(instructions)]
            cur_node = nodes[cur_node][d]
            steps += 1
        # log current steps
        prev = steps
        # take one more step
        d = dirs[next(instructions)]
        cur_node = nodes[cur_node][d]
        steps += 1
        # find next time it hits a Z
        while not cur_node.endswith('Z'):
            d = dirs[next(instructions)]
            cur_node = nodes[cur_node][d]
            steps += 1
        if steps % prev == 0:
            print(f'found cycle for node {node}: {steps, prev, steps / prev}')
            cycles[node] = prev

    return lcm(*cycles.values())


# def run_simulaneous_instructions(data):
#     dirs = {'R': 1, 'L': 0}
#     instructions, nodes = get_nodes(data)

#     cur = [x for x in nodes if x.endswith('A')]

#     steps = 0
#     while True:
#         steps += 1
#         checks = [False for _ in cur]
#         d = dirs[next(instructions)]
#         new = cur[:]
#         for i, c in enumerate(cur):
#             new[i] = nodes[c][d]
#             if new[i].endswith('Z'):
#                 checks[i] = True
#         cur = new[:]
#         if all(checks):
#             return steps

#         if (steps % 100000) == 0:
#             print(f'at step {steps}')


def get_answer(data, part2=False):
    if part2:
        return check_for_cycles(data)
    return run_instructions(data)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''LR

# 11A = (11B, XXX)
# 11B = (XXX, 11Z)
# 11Z = (11B, XXX)
# 22A = (22B, XXX)
# 22B = (22C, 22C)
# 22C = (22Z, 22Z)
# 22Z = (22B, 22B)
# XXX = (XXX, XXX)'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
