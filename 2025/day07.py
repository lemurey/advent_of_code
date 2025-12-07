from aoc_utilities import get_instructions
from pathlib import Path
from functools import cache

class Beam:
    def __init__(self, grid):
        self.grid = grid
        self.num_splits = 0
        self.orig_grid = {k: v for k,v in grid.items()}
        self.beams = {self._get_start(): 1}
        self.max_x = max(k[0] for k in self.grid)
        self.max_y = max(k[1] for k in self.grid)
        self.num_splits = 0
        self.seen = set()

    def _get_start(self):
        for k, v in self.grid.items():
            if v == 'S':
                return k

    def num_timelines(self):
        return sum(self.beams.values())

    def reset(self):
        self.grid = {k: v for k, v in self.orig_grid}
        self.beams = {self._get_start(): 1}
        self.num_splits = 0
        self.seen = set()

    def step(self, row_num):
        new_beams = {}
        for loc in self.beams:
            if loc[1] != row_num:
                continue
            new = self._drop(loc)
            if new not in self.grid:
                continue
            if self.grid[new] == '^':
                nl = self._left(new)
                if nl not in new_beams:
                    new_beams[nl] = 0
                new_beams[nl] += self.beams[loc]
                nr = self._right(new)
                if nr not in new_beams:
                    new_beams[nr] = 0
                new_beams[nr] += self.beams[loc]
                self.num_splits += 1
            else:
                if new not in new_beams:
                    new_beams[new] = 0
                new_beams[new] += self.beams[loc]
        self.seen.update(new_beams.keys())
        if len(new_beams) == 0:
            return False
        self.beams = new_beams
        return True

    def _drop(self, loc):
        x, y = loc
        return (x, y + 1)

    def _left(self, loc):
        x, y = loc
        return (x - 1, y)

    def _right(self, loc):
        x, y = loc
        return (x + 1, y)

    def __str__(self):
        out = ''
        for y in range(0, self.max_y + 1):
            for x in range(0, self.max_x + 1):
                loc = (x, y)
                if self.grid[loc] == 'S':
                    out += 'S'
                elif loc in self.seen:
                    out += '|'
                else:
                    out += self.grid[loc]
            out += '\n'
        return out



def parse_input(lines):
    grid = {}
    for j, row in enumerate(lines):
        for i, val in enumerate(row):
            grid[(i, j)] = val
    return grid


def get_answer(data, part2=False):
    grid = Beam(parse_input(data))
    c = -1
    print(grid)
    while True:
        c += 1
        check = grid.step(c)
        if not check:
            break
        # if c > 50:
        #     print('something fishy happening')
        #     break
    print(grid)
    if part2:
        return grid.num_timelines()
    return grid.num_splits


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''.......S.......
# ...............
# .......^.......
# ...............
# ......^.^......
# ...............
# .....^.^.^.....
# ...............
# ....^.^...^....
# ...............
# ...^.^...^.^...
# ...............
# ..^...^.....^..
# ...............
# .^.^.^.^.^...^.
# ...............
# '''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
