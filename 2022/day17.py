from aoc_utilities import get_instructions
from pathlib import Path
import itertools
from collections import defaultdict
import functools

'''
bar: ####

rod: #
     #
     #
     #

cross:  #
       ###
        #

hinge:  #
        #
      ###

square: ##
        ##
'''

with open('log_day17.txt', 'w') as f:
    f.write('')

class Segment:
    fills = defaultdict(lambda: 'I')
    fills[1] = '#'
    fills[0] = '.'
    def __init__(self, values, offset=0):
        temp = ([0] * offset) + list(values)
        if len(temp) < 7:
            temp += [0] * (7 - len(temp))
        if len(temp) > 7:
            raise ValueError('Segment must be less than 7 wide')
        self.values = tuple(temp)

    def is_valid(self):
        return not any([(x > 1) for x in self.values])

    def __add__(self, other):
        temp = [x + y for x, y in zip(self.values, other.values)]
        return Segment(temp)

    def __hash__(self):
        return hash(self.values)

    def __str__(self):
        row = ''.join(self.fills[x] for x in self.values)
        return  f'|{row}|'


class Rock:
    bottoms = {'C': (0, 1, 0), 'H': (1, 1, 1)}
    middles = {'C': (1, 1, 1), 'H': (0, 0, 1)}
    tops = {'C': (0, 1, 0), 'H': (0, 0, 1)}
    collected = (bottoms, middles, tops)
    widths = {'B': 4, 'R': 1, 'C': 3, 'H': 3, 'S': 2}
    heights = {'B': 1, 'R': 4, 'C': 3, 'H': 3, 'S': 2}
    def __init__(self, shape, height, left=3):
        self.left = left
        self.shape = shape
        self.height = height

    def push(self, d, grid):
        start = self.left
        if d == '>':
            self.left += 1
        else:
            self.left -= 1
        if (self.left < 1) or ((self.left + self.widths[self.shape] - 1) > 7):
            self.left = start
        if self.check(grid) != -1:
            self.left = start

    def __iter__(self):
        if self.shape in 'BRS':
            for _ in range(self.heights[self.shape]):
                s = Segment([1] * self.widths[self.shape], self.left - 1)
                yield s
        else:
            for r in self.collected:
                s = Segment(r[self.shape], self.left - 1)
                yield s

    def land(self, grid, loc):
        for o, s in enumerate(self):
            h = loc + o
            if h >= len(grid):
                grid.append(s)
            else:
                new = grid[h] + s
                if not new.is_valid():
                    print_grid(grid, LOG)
                    print(h, o, self.shape)
                    print(new)
                    raise ValueError('invalid grid created')
                grid[h] = new

    def check(self, grid):
        for o, s in enumerate(self):
            h = (self.height + o)
            if (h >= len(grid)) or (h < 0):
                continue
            if not (s + grid[h]).is_valid():
                return self.height + 1
        return -1

    def __str__(self):
        base = [str(x) for x in self]
        return '\n'.join(base[::-1]).replace('#', '@')


def print_grid(grid, f=None):
    for row in grid[::-1]:
        if f is None:
            print(row)
        else:
            f.write(str(row) + '\n')
    if f is None:
        print('+-------+')
        print()
        print()
    else:
        f.write('+-------+' + '\n')


def run_drops(jets, num_rounds):
    rocks = itertools.cycle('BCHRS')
    grid = []
    jet_index = 0

    cycles = {}

    for num_rocks in range(num_rounds):
        which = next(rocks)
        r = Rock(which, height=len(grid) + 3)
        # with open('log_day17.txt', 'a') as f:
        #     print_grid(grid, f)
        #     f.write(f'{which}, {jet_index}\n\n')
        while True:
            cycle_key = (which, jet_index)
            if cycle_key in cycles:
                prev_num_rocks, prev_height = cycles[cycle_key]
                period = num_rocks - prev_num_rocks
                if (num_rocks % period) == (num_rounds % period):
                    height_in_cycle = len(grid) - prev_height
                    cycles_left = ((num_rounds - num_rocks) // period) + 1
                    return prev_height + (height_in_cycle * cycles_left)
            else:
                cycles[cycle_key] = (num_rocks, len(grid))

            d = jets[jet_index]
            jet_index = (jet_index + 1) % len(jets)
            r.push(d, grid)
            r.height -= 1
            c = r.check(grid)
            if (c > -1):
                r.land(grid, c)
                break
            elif r.height == -1:
                r.land(grid, 0)
                break

    return len(grid)


def get_answer(data, part2=False):
    # jets = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'

    jets = data[0]

    cycles = 2022
    if part2:
        cycles = 1000000000000

    grid_height = run_drops(jets, num_rounds=cycles)

    return grid_height

if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
