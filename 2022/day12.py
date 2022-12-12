from aoc_utilities import get_instructions
from pathlib import Path
from collections import deque

VALS = dict(zip('abcdefghijklmnopqrstuvwxyz', range(27)))

def make_grid(data):
    grid = {}
    starts = []
    p1_start = None
    end = None
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            if val == 'a':
                starts.append((i, j))
            if val == 'S':
                val = 'a'
                p1_start = (i, j)
            elif val == 'E':
                end = (i, j)
                val = 'z'
            grid[(i, j)] = VALS[val]
    starts = [p1_start] + starts
    return grid, starts, end


def get_neighbors(grid, loc):
    cur = grid[loc]
    for d in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        nl = (loc[0] + d[0], loc[1] + d[1])
        if nl not in grid:
            continue
        if grid[nl] <= (grid[loc] + 1):
            yield nl


def search(grid, start, end):
    Q = deque()
    seen = set()
    Q.append((start, 0))
    while Q:
        loc, path = Q.popleft()
        if loc == end:
            return path
        if loc in seen:
            continue
        seen.add(loc)
        for next_loc in get_neighbors(grid, loc):
            Q.append((next_loc, path + 1))

    return float('inf')


def get_answer(data, part2=False):
    grid, starts, end = make_grid(data)
    paths = []
    for i, start in enumerate(starts):
        path = search(grid, start, end)
        if i == 0:
            print(path)
        paths.append(path)

    return min(paths)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''Sabqponm
# abcryxxl
# accszExk
# acctuvwj
# abdefghi'''.split('\n')
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
