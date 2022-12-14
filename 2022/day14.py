from aoc_utilities import get_instructions
from pathlib import Path
import sys
sys.setrecursionlimit(10000)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f'{self.x}, {self.y}'

OFFSETS = (Point(0, 1), Point(-1, 1), Point(1, 1))

def _get_fills(base, l, h, which):
    l, h = sorted([l ,h])
    if which == 'x':
        return ((base, other) for other in range(l, h + 1))
    else:
        return ((other, base) for other in range(l, h + 1))


def make_grid(data):
    grid = {}
    min_x = float('inf')
    max_x = 500
    min_y = 0
    max_y = -float('inf')
    grid[Point(500, 0)] = '+'
    for row in data:
        prev = None
        for x, y in (c.split(',') for c in row.split(' -> ')):
            x, y = map(int, (x, y))
            min_x, max_x = min(min_x, x), max(max_x, x)
            min_y, max_y = min(min_y, y), max(max_y, y)
            if prev is None:
                prev = Point(x, y)
                continue
            cur = Point(x, y)
            if prev.x == cur.x:
                fills = _get_fills(cur.x, prev.y, cur.y, 'x')
            else:
                fills = _get_fills(cur.y, prev.x, cur.x, 'y')

            for i, j in fills:
                grid[Point(i, j)] = '#'
            prev = cur
    return grid, min_x, max_x, min_y, max_y


def drop_sand(grid, max_y, orig=Point(500, 0), prev=None, part2=False):
    if prev is None:
        prev = orig
    # drop until you find something
    while prev + OFFSETS[0] not in grid:
        prev = prev + OFFSETS[0]
        # if you keep dropping past the bottom of grid you are done
        # prior to part2 this just checked agains max_y added offset so it
        # doesn't prematurely stop part2
        if (prev + OFFSETS[0]).y > max_y + 3:
            return grid, True
    # if you have plugged the hole in part2 then stop
    if part2 and grid[orig] == 'o':
        return grid, True
    # check to left
    val = prev + OFFSETS[1]
    if val not in grid:
        return drop_sand(grid, max_y, orig, val)
    # check to right
    val = prev + OFFSETS[2]
    if val not in grid:
        return drop_sand(grid, max_y, orig, val)

    grid[prev] = 'o'
    return grid, False


def show_grid(grid, min_x, max_x, min_y, max_y, part2=False):
    for y in range(min_y, max_y + 1):
        row = ''
        for x in range(min_x, max_x + 1):
            if Point(x, y) in grid:
                row += grid[Point(x, y)]
            else:
                row += '.'
        print(row)


def get_answer(data, part2=False):
    grid, min_x, max_x, min_y, max_y = make_grid(data)
    # show_grid(grid, min_x, max_x, min_y, max_y)
    if part2:
        for x_val in range(100, 901):
            grid[Point(x_val, max_y + 2)] = '#'
    c = 0
    while True:
        c += 1
        grid, stop = drop_sand(grid, max_y, part2=part2)
        if stop:
            break
        if c > 500000:
            break
        # print('-'*20)
    # show_grid(grid, min_x-20, max_x+20, min_y, max_y + 2)
    return sum(1 for x in grid.values() if x == 'o')


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''498,4 -> 498,6 -> 496,6
# 503,4 -> 502,4 -> 502,9 -> 494,9'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
