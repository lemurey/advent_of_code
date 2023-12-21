from aoc_utilities import get_instructions
from pathlib import Path
from itertools import count
from heapq import heappush, heappop

N = 131 ## grid size
'''
with a square grid of size 131, the number of steps mod 131 will follow
a quadratic pattern (because you basically get the diagonal of the square moving
out). the number we are checking for (26501365) is 131 * 202300 + 65. we assume
the number of locations after n steps is quadratic:
x2 * n**2 + x1 * n + x0 = locs
using the code below I can solve for n = 0, 1, 2 (65, 196, 327 steps) call those
answers c, b, a then we have
x0 = c
x2 + x1 + x0 = b
4x2 + 2x1 + x0 = c

these equations can be solved for x0, x1, and x2 then we can get the number
of locations for any number of steps (so long as that number is 0 mod N (after
subtracting 65))
'''

def get_grid(data):
    grid = {}
    for j, row in enumerate(data):
        for i, val in enumerate(row):
            c = i + 1j*j
            grid[c] = val
            if val == 'S':
                start = c
    return grid, start


def neighbors(grid, loc):

    for d in (-1, 1, 1j, -1j):
        n = loc + d
        n = (n.real % N) + (n.imag % N)*1j
        if grid.get(n, '') in '.S':
            yield loc + d


def walk(grid, start, max_steps=64):
    tiebreaker = count()
    seen = set()
    Q = [(0, next(tiebreaker), start)]
    while Q:
        num_steps, _, loc = heappop(Q)
        if num_steps > max_steps:
            return seen
        if (loc, num_steps) in seen:
            continue
        seen.add((loc, num_steps))

        for neighbor in neighbors(grid, loc):
            heappush(Q, (num_steps + 1, next(tiebreaker), neighbor))


def write_grid(grid, locs, size=None):
    if size is None:
        size = N
    out = ''
    for j in range(size + 1):
        for i in range(size + 1):
            c = i + 1j*j
            c = (c.real % N) + (c.imag % N)*1j
            if c in locs:
                out += 'O'
            else:
                out += grid[c]
        out += '\n'
    return out


def get_answer(data, part2=False):
    grid, start = get_grid(data)
    offset = 65

    step_check = offset + N * 2
    locs = walk(grid, start, step_check)
    can_visit_p1 = set()
    can_visit_n0 = set()
    can_visit_n1 = set()
    can_visit_n2 = set()

    for (l, n) in locs:
        if n == 64:
            can_visit_p1.add(l)
        elif n == offset:
            can_visit_n0.add(l)
        elif n == offset + N:
            can_visit_n1.add(l)
        elif n == offset + 2 * N:
            can_visit_n2.add(l)
    # part1 answer:
    print(len(can_visit_p1))

    a = len(can_visit_n2)
    b = len(can_visit_n1)
    c = len(can_visit_n0)
    x0 = c
    x1 = (4*b - 3*c - a) / 2
    x2 = (a - 2*b + c) / 2
    n = 202300
    return (x2 * n * n + x1 * n + x0)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''...........
# .....###.#.
# .###.##..#.
# ..#.#...#..
# ....#.#....
# .##..S####.
# .##..#...#.
# .......##..
# .##.#.####.
# .##..##.##.
# ...........'''.split('\n')
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
