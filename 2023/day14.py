from aoc_utilities import get_instructions
from pathlib import Path


def step(grid, i, mx, which):
    updates = {}
    cd = {'N': 1j, 'S': -1j, 'E': 1, 'W': -1}

    for x in range(mx+1):
        c = x - 1j*i
        if c not in grid:
            continue
        if grid[c] in '.#':
            continue
        above = c + cd[which]
        if above not in grid:
            continue
        if grid[above] == '.':
            updates[above] = 'O'
            updates[c] = '.'

    if len(updates) > 0:
        grid.update(updates)
        return 1
    return 0


def tilt_grid(grid, mx, my, which='N'):
    c_val = 1
    attempts = 0
    while c_val > 0:
        c_val = 0
        if which == 'N':
            it = range(my+1)
            val = mx
        elif which == 'S':
            it = range(my, -1, -1)
            val = mx
        elif which == 'E':
            it = range(mx, -1, -1)
            val = my
        elif which == 'W':
            it = range(mx+1)
            val = my
        for j in it:
            c_val += step(grid, j, val, which)
        attempts += 1
        if attempts > 1000:
            print('something is up')
            return


def draw_grid(grid, mx, my, r=False):
    out = ''
    for j in range(my+1):
        for i in range(mx+1):
            out += grid[i - 1j*j]
        out += '\n'
    if r:
        return out.strip()
    print(out)
    print('\n')


def get_grid(data):
    grid = {}
    mx, my = 0, 0
    for j, row in enumerate(data):
        for i, val in enumerate(row):
            c = i - 1j*j
            grid[c] = val
        mx = i
    my = j
    return grid, mx, my


def check_period(grid, mx, my):
    history = {}
    count = 0
    periods = {}
    for i in range(10000):
        for w in 'NWSE':
            tilt_grid(grid, mx, my, w)
        cur = draw_grid(grid, mx, my, True)
        if cur not in history:
            history[cur] = 0
        else:
            if cur not in periods:
                periods[cur] = []
            periods[cur].append(i + 1)
            count += 1

        if i % 100 == 0:
            print(f'at iteration {i}: max(len(periods.values()))')

        if any(len(x) > 1 for x in periods.values()):
            return periods
        if count > 100:
            return periods


def sum_grid(string):
    total = 0
    for i, row in enumerate(string.split('\n')[::-1], start=1):
        for v in row:
            if v == 'O':
                total += i
    return total


def get_answer(data, part2=False):
    grid, mx, my = get_grid(data)

    if part2:
        p = check_period(grid, mx, my)
        period = len(p)
        values = []
        min_point = float('inf')
        for k, v in p.items():
            values.append(sum_grid(k))
            mp = min(v)
            if mp < min_point:
                min_point = mp
        return values[(1000000000 - min_point) % period]

    tilt_grid(grid, mx, my)
    return sum_grid(draw_grid(grid, mx, my, True))


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''O....#....
# O.OO#....#
# .....##...
# OO.#O....O
# .O.....O#.
# O.#..O.#.#
# ..O..#O..O
# .......O..
# #....###..
# #OO..#....'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
