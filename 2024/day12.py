from aoc_utilities import get_instructions
from pathlib import Path
from collections import deque


def parse_map(data):
    grid = {}
    for y, row in enumerate(data):
        for x, val in enumerate(row):
            coord = (x, y)
            grid[coord] = val
    return grid


def get_neighbors(loc, grid):
    crop = grid[loc]

    for step in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        n = (loc[0] + step[0], loc[1] + step[1])
        if n not in grid:
            yield None, 1
        elif grid[n] == grid[loc]:
            yield n, 0
        else:
            yield None, 1


def build_region(grid, cur):
    cur_region = {grid[cur]: {'locs': [cur], 'values': 0}}
    seen = set([cur])
    to_check = deque([cur])
    while to_check:
        checking = to_check.pop()
        for neighbor, val in get_neighbors(checking, grid):
            if neighbor in seen:
                continue
            if neighbor is not None:
                cur_region[grid[checking]]['locs'].append(neighbor)
                seen.add(neighbor)
                to_check.append(neighbor)
            cur_region[grid[checking]]['values'] += val

    return cur_region


def get_regions(grid):
    Q = deque(list(grid.keys()))

    regions = []
    while Q:
        cur = Q.pop()

        cur_region = build_region(grid, cur)
        for crop in cur_region[grid[cur]]['locs']:
            if crop == cur:
                continue
            Q.remove(crop)
        regions.append(cur_region)

    return regions



def get_answer(data, part2=False):
    grid = parse_map(data)
    regions = get_regions(grid)

    total = 0
    total2 = 0

    for entry in regions:
        for k in entry:
            # part 1 get perimeter and area
            v1 = len(entry[k]["locs"]) #area
            v2 = entry[k]["values"] #perimeter
            total += v1 * v2


            # part 2 each corner contributes a side
            r = set(entry[k]["locs"])
            sides = 0
            for (x, y) in r:

                # bottom right corner
                sides += (x + 1, y) not in r and (x, y + 1) not in r
                # bottom left corner
                sides += (x - 1, y) not in r and (x, y + 1) not in r
                # top right corner
                sides += (x + 1, y) not in r and (x, y - 1) not in r
                # top left corner
                sides += (x - 1, y) not in r and (x, y - 1) not in r

                # corner to top left
                sides += (x + 1, y) in r and (x, y + 1) in r and (x + 1, y + 1) not in r
                # corner to top right
                sides += (x - 1, y) in r and (x, y + 1) in r and (x - 1, y + 1) not in r
                # corner to bottom left
                sides += (x + 1, y) in r and (x, y - 1) in r and (x + 1, y - 1) not in r
                # corner to bottom right
                sides += (x - 1, y) in r and (x, y - 1) in r and (x - 1, y - 1) not in r
            total2 += v1 * sides
    return total, total2


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''RRRRIICCFF
# RRRRIICCCF
# VVRRRCCFFF
# VVRCCCJFFF
# VVVVCJJCFE
# VVIVCCJJEE
# VVIIICJJEE
# MIIIIIJJEE
# MIIISIJEEE
# MMMISSJEEE'''.split('\n')

#     inputs = '''AAAA
# BBCD
# BBCC
# EEEC'''.split('\n')

    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
