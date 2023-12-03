from aoc_utilities import get_instructions
from pathlib import Path


OFFSETS = (-1+1j, 1j, 1+1j, -1, 1, -1-1j, -1j, 1-1j)

def get_neighbors(grid, key, seen=None, yield_coord=False):
    if seen is None:
        seen = set()
    seen.add(key)
    for of in OFFSETS:
        nk = (key + of)
        if nk in seen:
            continue
        seen.add(nk)
        if nk in grid:
            v = grid[nk]
            if yield_coord:
                yield v, nk
            else:
                yield v
            if v.isdigit():
                yield from get_neighbors(grid, nk, seen, yield_coord=yield_coord)


def parse_grid(data):
    grid = {}
    stars = set()
    for y, row in enumerate(data):
        for x, val in enumerate(row):
            key = complex(x, -y)
            grid[key] = val
            if val == '*':
                stars.add(key)

    nums = {}
    for y, row in enumerate(data):
        skip = 0
        for x, v in enumerate(row):
            store = v
            k = complex(x, -y)
            if skip > 0:
                skip -= 1
                continue
            if v.isdigit():
                for n in get_neighbors(grid, k):
                    if n.isdigit():
                        store += n
                nl = len(store)
                skip += nl
                nums[k] = int(store)

    return grid, nums, stars


def check(s, n, grid):
    for _, loc in get_neighbors(grid, n, yield_coord=True):
        if loc == s:
            return True
    return False


def get_answer(data, part2=False):
    grid, nums, stars = parse_grid(data)
    total = 0
    ratio = 0
    for k, v in nums.items():
        for n in get_neighbors(grid, k):
            if (n != '.') and (not n.isdigit()):
                break
        else:
            continue
        total += v

    for s in stars:
        nn = []
        for k, v in nums.items():
            if check(s, k, grid):
                nn.append(v)
        if len(nn) == 2:
            ratio += nn[0] * nn[1]
    return total, ratio


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
