from aoc_utilities import get_instructions
from pathlib import Path
from collections import deque


def make_grid(data):
    grid = {}
    starts = []
    for y, row in enumerate(data):
        for x, val in enumerate(row):
            if val == '.':
                val = '-1'
            grid[(x, y)] = int(val)
            if int(val) == 0:
                starts.append((x, y))
            max_x = x
        max_y = y
    return grid, starts, max_x, max_y


def get_neighbors(loc, grid):
    for step in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        n = (loc[0] + step[0], loc[1] + step[1])
        if n not in grid:
            continue
        if grid[n] == grid[loc] + 1:
            yield n


def get_paths(grid, starts):
    seen = set()
    id_gen = count()
    Q = deque([(x, [x]) for x in starts])
    paths = set()

    log = open('logs10.txt', 'w')

    while Q:
        # get next step
        pos, path = Q.pop()

        # for each neighbor 
        for neighbor in get_neighbors(pos, grid):
            # if we have visited this before, continue
            if neighbor in path:
                continue
            # if we are at a 9 end the path
            if grid[neighbor] == 9:
                paths.add(tuple(path + [neighbor]))
            else:
                Q.append((neighbor, path + [neighbor]))
    log.close()
    return paths


def get_answer(data, part2=False):
    grid, starts, max_x, max_y = make_grid(data)

    paths = get_paths(grid, starts)

    if part2:
        return len(paths)

    trail_heads = {}

    for path in paths:
        if path[0] not in trail_heads:
            trail_heads[path[0]] = set()
        trail_heads[path[0]].add(path[-1])

    return sum([len(x) for x in trail_heads.values()])


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
