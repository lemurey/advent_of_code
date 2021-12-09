from aoc_utilities import get_instructions
from pathlib import Path


def parse_grid(data):
    grid = {}
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            grid[(i, j)] = int(val)
    return grid


def get_neighbors(grid, i, j):
    for offset in (-1, 1):
        p = (i + offset, j)
        if p in grid:
            yield p
        p = (i, j + offset)
        if p in grid:
            yield p


def get_lows(grid):
    lows = []
    for loc in grid:
        c = grid[loc]
        for n in get_neighbors(grid, *loc):
            if grid[n] <= c:
                break
        else:
            lows.append(loc)
    return lows


def get_basin(grid, i, j):
    basin = set([(i, j)])
    for neighbor in get_neighbors(grid, i, j):
        if grid[neighbor] > grid[(i, j)] and grid[neighbor] < 9:
            basin = basin | get_basin(grid, *neighbor)
    return basin


def get_answer(data, part2=False):
    grid = parse_grid(data)
    lows = get_lows(grid)

    if part2:
        basins = sorted([get_basin(grid, *x) for x in lows], key=len, reverse=True)
        return len(basins[0]) * len(basins[1]) * len(basins[2])

    return sum(grid[x] + 1 for x in lows)

if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
