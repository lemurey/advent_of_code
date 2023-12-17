from aoc_utilities import get_instructions
from pathlib import Path
from heapq import heappush, heappop


DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def search(grid, end, min_step, max_step):
    Q = [(0, 0, 0, (0, 0), ())]

    seen = set()
    costs = {}
    while Q:
        cost, x, y, d, path = heappop(Q)
        if (x, y) == end:
            return cost, path
        if (x, y, d) in seen:
            continue
        seen.add((x, y, d))

        for nd in DIRS:
            # can't back up check
            if d == tuple(-1*x for x in nd):
                continue
            # can't go any more
            if d == nd:
                continue
            total_cost = 0
            np = []
            # take the possible number of steps
            for step in range(1, max_step+1):
                nx = x + nd[0] * step
                ny = y + nd[1] * step
                if (nx, ny) not in grid:
                    continue
                np.append((nx, ny, nd))
                total_cost += grid[(nx, ny)]
                if step < min_step:
                    continue
                nc = cost + total_cost
                if costs.get((nx, ny, nd), float('inf')) <= nc:
                    continue
                costs[(nx, ny, nd)] = nc
                heappush(Q, (nc, nx, ny, nd, (*np, *path)))


def get_grid(data):
    grid = {}
    for j, row in enumerate(data):
        for i, val in enumerate(row):
            c = (i, j)
            grid[c] = int(val)
    return grid, c


def show_path(grid, path):
    out = ''
    mx = max(x[0] for x in grid)
    my = max(x[1] for x in grid)
    ll = {(0, 1): 'v', (0, -1): '^', (1, 0): '>', (-1, 0): '<'}
    path = {(x[0], x[1]): x[2] for x in path}
    for j in range(my + 1):
        for i in range(mx + 1):
            c = (i, j)
            if c in path:
                out += ll[path[c]]
            else:
                out += f'{grid[c]}'
        out += '\n'
    print(out)


def convert_path(path):
    np = {}
    for prev, cur in zip(path[:-1], path[1:]):
        px, py, pd = prev
        cx, cy, cd = cur

        if px == cx:
            y_vals = range(1 + abs(py - cy))
            x_vals = [0 for _ in range(1 + abs(py - cy))]
        else:
            x_vals = range(1 + abs(px - cx))
            y_vals = [0 for _ in range(1 + abs(px - cx))]

        for (x, y) in zip(x_vals, y_vals):
            new = (px + x, py + y)
            np[new] = cd

    return np


def get_answer(data, part2=False):
    grid, end = get_grid(data)
    if part2:
        min_d, max_d = 4, 10
    else:
        min_d, max_d = 1, 3
    cost, path = search(grid, end, min_d, max_d)

    return cost


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs='''2413432311323
# 3215453535623
# 3255245654254
# 3446585845452
# 4546657867536
# 1438598798454
# 4457876987766
# 3637877979653
# 4654967986887
# 4564679986453
# 1224686865563
# 2546548887735
# 4322674655533'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
