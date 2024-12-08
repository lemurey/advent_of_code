from aoc_utilities import get_instructions
from pathlib import Path


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.opts = {'++': (1, 1), 
                     '+-': (1, -1),
                     '-+': (-1, 1),
                     '--': (-1, -1),
                    }

    def _check_other(self, other):
        if self.x >= other.x and self.y >= other.y:
            return self.opts['++']
        elif self.x >= other.x and self.y <= other.y:
            return self.opts['+-']
        elif self.x <= other.x and self.y >= other.y: 
            return self.opts['-+']
        else:
            return self.opts['--']

    def node(self, other, mult=1):
        mod_x, mod_y = self._check_other(other)
        new_x = self.x + (mod_x * mult * abs(self.x - other.x))
        new_y = self.y + (mod_y * mult * abs(self.y - other.y))
        return Point(new_x, new_y)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __hash__(self):
        return hash((self.x, self.y))



def process_data(data):
    grid = {}
    maps = {}
    for y, row in enumerate(data):
        for x, val in enumerate(row):
            grid[Point(x, y)] = val
            if val == '.':
                continue
            if val not in maps:
                maps[val] = []
            maps[val].append(Point(x, y))
    return grid, maps


def get_resonant_antinodes(p1, p2, grid):
    c = 0
    mult = 0
    antinodes = set()
    while True:
        prev_len = len(antinodes)

        for node in (p1.node(p2, mult), p2.node(p1, mult)):
            if node in grid:
                antinodes.add(node)
        mult += 1

        if len(antinodes) == prev_len:
            break
    return antinodes


def find_antinodes(grid, maps, part2):
    antinodes = set()
    for key in maps:
        for i, p1 in enumerate(maps[key]):
            for p2 in maps[key][i+1:]:
                if p1 == p2:
                    continue
                if part2:
                    new_nodes = get_resonant_antinodes(p1, p2, grid)
                    antinodes = antinodes.union(new_nodes)
                else:
                    n1 = p1.node(p2)
                    n2 = p2.node(p1)
                    if n1 in grid:
                        antinodes.add(n1)
                    if n2 in grid:
                        antinodes.add(n2)
    return antinodes


def plot_grid(grid, antinodes):
    max_x = max(p.x for p in grid)
    max_y = max(p.y for p in grid)
    
    out = ''
    for y in range(max_y + 1):
        for x in range(max_x +1):
            p = Point(x, y)
            if p in antinodes and grid[p] == '.':
                out += '#'
            else:
                out += grid[p]
        out += '\n'

    print(out)


def get_answer(data, part2=False):
    grid, maps = process_data(data)

    antinodes = find_antinodes(grid, maps, part2)

    # plot_grid(grid, antinodes)

    return len(antinodes)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''............
# ........0...
# .....0......
# .......0....
# ....0.......
# ......A.....
# ............
# ............
# ........A...
# .........A..
# ............
# ............'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
