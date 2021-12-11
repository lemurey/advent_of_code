from aoc_utilities import get_instructions
from pathlib import Path


def get_neighbors(i, j):
    offsets = (-1, 0, 1)
    for x in offsets:
        for y in offsets:
            ni = i + x
            nj = j + y
            if (ni, nj) == (i, j):
                continue
            yield i + x, j + y


def run_grid(grid, n):
    total = 0
    for _ in range(n):
        grid, c = step_grid(grid)
        total += c
    return grid, total


def step_grid(grid):
    flashes = set()
    for key in grid:
        grid[key] += 1

    cont = True
    while cont:
        prev = len(flashes)
        for key in grid:
            if key in flashes:
                continue
            if grid[key] > 9:
                flashes.add(key)
                for nk in get_neighbors(*key):
                    if nk in flashes:
                        continue
                    if nk in grid:
                        grid[nk] += 1
        cont = len(flashes) > prev

    for key in flashes:
        grid[key] = 0

    return grid, len(flashes)


def get_grid(data):
    grid = {}
    for i, line in enumerate(data):
        for j, val in enumerate(line):
            grid[i, j] = int(val)
    return grid


def print_grid(grid):
    out = ''
    for i in range(10):
        for j in range(10):
            out += str(grid[i, j])
        out += '\n'
    return out


def get_answer(data, part2=False):
    grid = get_grid(data)
    if part2:
        count = 0
        while True:
            count += 1
            grid, num = step_grid(grid)
            if num == 100:
                break
        return count
    grid, total = run_grid(grid, 100)
    return total

if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''5483143223
# 2745854711
# 5264556173
# 6141336146
# 6357385478
# 4167524645
# 2176841721
# 6882881134
# 4846848554
# 5283751526'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
