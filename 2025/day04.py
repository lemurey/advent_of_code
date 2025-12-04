from aoc_utilities import get_instructions
from pathlib import Path


DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0),
        (-1, 1), (-1, -1), (1, -1), (1, 1)]


def _combine_loc(loc, other):
    return (loc[0] + other[0], loc[1] + other[1])


def get_neighbors(grid, loc):
    for d in DIRS:
        new_l = _combine_loc(loc, d)
        if new_l in grid:
            yield grid[new_l]
        else:
            yield '.'


def can_access(grid, loc):
    count = 0
    for n in get_neighbors(grid, loc):
        if n == '@':
            count += 1
    if count >= 4:
        return False
    return True


def parse_input(lines):
    grid = {}
    for j, row in enumerate(lines):
        for i, val in enumerate(row):
            grid[(i, j)] = val
    return grid


def run_access(grid):
    count = 0
    locs = set()
    for loc, item in grid.items():
        if item == '@':
            if can_access(grid, loc):
                count += 1
                locs.add(loc)
    return count, locs


def run_part2(grid):
    ng = {k: v for k, v in grid.items()}
    removed = 0
    while True:
        count, to_remove = run_access(ng)
        if len(to_remove) == 0:
            return removed
        removed += len(to_remove)
        ng = {k: v for k, v in ng.items() if k not in to_remove}



def get_answer(data, part2=False):
    grid = parse_input(data)
    if part2:
        return run_part2(grid)
    count, _ = run_access(grid)
    return count


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)


#     inputs = '''..@@.@@@@.
# @@@.@.@.@@
# @@@@@.@.@@
# @.@@@@..@.
# @@.@@@@.@@
# .@@@@@@@.@
# .@.@.@.@@@
# @.@@@.@@@@
# .@@@@@@@@.
# @.@.@@@.@.'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
