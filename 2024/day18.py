from aoc_utilities import get_instructions
from pathlib import Path
from heapq import heappush, heappop

RED = '\033[91m'
END = '\033[0m'


def get_corrupted(data):
    corrupted = []
    for i, row in enumerate(data):
        x, y = map(int, row.split(','))
        corrupted.append((x, y))
    return corrupted


def get_neighbors(loc, grid, corrupted):
    for dx,dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        nx, ny = loc[0] + dx, loc[1] + dy
        if (nx, ny) in grid and (nx, ny) not in corrupted:
            yield 1, (nx, ny)


def get_path(grid, corrupted, start=(0, 0), end=(70, 70)):
    costs = {}
    Q = []
    heappush(Q, (0, start))

    while Q:
        cost, loc = heappop(Q)
        if loc == end:
            return cost

        for score, next_loc in get_neighbors(loc, grid, corrupted):
            # if we have seen this loc before get it's cost
            # otherwise cost is infinity
            prev_cost = costs.get(next_loc, float('inf'))
            next_cost = cost + score
            # have we found a cheaper way to get to here
            if next_cost < prev_cost:
                costs[next_loc] = next_cost
                heappush(Q, (next_cost, next_loc))
    return None


def print_grid(grid, path=None):
    if path is None:
        path = []
    out = ''
    for y in range(71):
        for x in range(71):
            p = (x, y)
            if p in path:
                out += f'{RED}#{END}'
            else:
                out += str(grid[p])
        out += '\n'
    print(out)


def get_blocker(grid, corrupted):
    low = 0
    original_high = len(corrupted)
    high = original_high

    count = 0
    while low != high:
        print(low, high)
        count += 1
        mid = (low + high) // 2
        if count > 2426:
            return 'this went too long'
        c_h = get_path(grid, set(corrupted[:mid]))
        if c_h is None:
            high = mid
        else:
            low = mid + 1

    return high


def get_answer(data, part2=False):
    grid = {(x, y): '.' for x in range(71) for y in range(71)}
    corrupted = get_corrupted(data)

    print_grid(grid, set(corrupted[:2990]))
    if part2:
        check = get_blocker(grid, corrupted)
        if get_path(grid, set(corrupted[:check])) is not None:
            return check+1, corrupted[check + 1], corrupted[check], corrupted[check-1]
        return check, corrupted[check], corrupted[check+1], corrupted[check-1]
    return get_path(grid, set(corrupted[:1024]))


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''5,4
# 4,2
# 4,5
# 3,0
# 2,1
# 6,3
# 2,4
# 1,5
# 0,6
# 3,3
# 2,6
# 5,1
# 1,2
# 5,5
# 2,5
# 6,5
# 1,4
# 0,4
# 6,4
# 1,1
# 6,1
# 1,0
# 0,5
# 1,6
# 2,0'''.split('\n')

    # print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
