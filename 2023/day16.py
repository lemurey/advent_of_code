from aoc_utilities import get_instructions
from pathlib import Path
from collections import deque


INTERACTIONS = {
    (1, '/'): (1j, ), (-1, '/'): (-1j, ), (-1j, '/'): (-1, ), (1j, '/'): (1, ),
    (1, '\\'): (-1j, ), (-1, '\\'): (1j, ), (-1j, '\\'): (1, ), (1j, '\\'): (-1, ),
    (1, '|'): (1j, -1j), (-1, '|'): (1j, -1j), (-1j, '|'): (-1j, ), (1j, '|'): (1j, ),
    (1, '-'): (1, ), (-1, '-'): (-1, ), (-1j, '-'): (1, -1), (1j, '-'): (1, -1),
}


def run_beam(grid, start=0, start_d=1):
    Q = deque()
    Q.append((start, start_d))
    # fills = {k: [] for k in grid}
    fills = {k: 0 for k in grid}
    seen = set()

    while Q:
        loc, d = Q.popleft()

        # we might have stepped out of the grid: then do nothing
        if (loc not in grid):
            continue

        # if we have already been here pointing the same way: do nothing
        if (loc, d) in seen:
            continue
        seen.add((loc, d))

        # we have iluminated the spot we are in
        # fills[loc].append(d)
        fills[loc] = 1
        # if we are at a dot then we step forward without changing direction
        if grid[loc] == '.':
            Q.append((loc + d, d))
            continue
        # otherwise we interact with the object we are at
        new_d = INTERACTIONS[(d, grid[loc])]
        # add the outcomes of the interaction
        for nd in new_d:
            Q.append((loc+nd, nd))

    return fills


def get_grid(data):
    grid = {}
    for j, row in enumerate(data):
        for i, val in enumerate(row):
            c = i - 1j*j
            grid[c] = val
    return grid


def draw_grid(grid, is_fill=False, only_fill=False):
    mx = max(int(x.real) for x in grid)
    my = max(abs(int(x.imag)) for x in grid)
    out = ''
    d = {1: '>', -1: '<', 1j: '^', -1j: 'v'}
    for j in range(my+1):
        for i in range(mx+1):
            c = i - 1j*j
            if is_fill:
                v = len(grid[c])
                if v == 0:
                    out += '.'
                elif only_fill:
                    out += '#'
                elif v == 1:
                    out += d[grid[c][0]]
                elif v < 10:
                    out += f'{v}'
                else:
                    out += '*'
            else:
                out += grid[c]
        out += '\n'
    return out


def get_answer(data, part2=False):
    grid = get_grid(data)
    fills = run_beam(grid)
    # max_fill = sum(len(x) > 0 for x in fills.values())
    max_fill = sum(fills.values())
    print(max_fill)

    mx = max(int(x.real) for x in grid)
    my = max(abs(int(x.imag)) for x in grid)
    # run along the top/bottom
    for x in range(mx+1):
        f = run_beam(grid, x, -1j)
        cv = sum(f.values())
        if cv > max_fill:
            max_fill = cv
        f = run_beam(grid, x - 1j*my, 1j)
        cv = sum(f.values())
        if cv > max_fill:
            max_fill = cv

    # run along left/right side
    for y in range(my+1):
        f = run_beam(grid, -1j*y, 1)
        cv = sum(f.values())
        if cv > max_fill:
            max_fill = cv
        f = run_beam(grid, mx-1j*y, -1)
        cv = sum(f.values())
        if cv > max_fill:
            max_fill = cv

    return max_fill


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    # with open('alt_16_in.txt', 'r') as f:
    #     inputs = f.read().splitlines()
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
