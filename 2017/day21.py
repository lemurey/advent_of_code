from aoc_utilities import get_instructions
from utilities import timeit
from itertools import combinations
import os


class Grid:
    def __init__(self, start=None):
        if start is None:
            self.grid = [['.' for _ in range(3)] for _ in range(3)]
            self.grid[0][1] = '#'
            self.grid[1][2] = '#'
            self.grid[2] = ['#' for _ in range(3)]
        else:
            self.grid = []
            for row in start.strip('/').split('/'):
                self.grid.append(list(row))
        self.size = len(self.grid)

    def rotate(self):
        self.grid = list(zip(*self.grid))
        self.flip(False)

    def flip(self, up=True):
        if up:
            for i, row in enumerate(self.grid[::-1]):
                self.grid[i] = row
        else:
            for i, row in enumerate(self.grid[:]):
                self.grid[i] = row[::-1]

    def all(self):
        for i in range(4):
            self.rotate()
            yield Grid(self.__repr__())
            self.flip(True)
            yield Grid(self.__repr__())
            self.flip(False)
            yield Grid(self.__repr__())

    def split(self, joins, size):
        for i in range(joins):
            for j in range(joins):
                t = '/'.join(''.join(row[j * size: (j + 1) * size])
                             for row in self.grid[i * size: (i + 1) * size])
                yield Grid(t)

    def on(self):
        count = 0
        for row in self.grid:
            count += row.count('#')
        return count

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid).strip()

    def __repr__(self):
        return self.__str__().replace("\n", '/')

    def __eq__(self, other):
        if not isinstance(other, Grid):
            return False
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return hash(self.__repr__())

    def __add__(self, other):
        out = ''
        for i, row in enumerate(self.grid):
            out += ''.join(row) + ''.join(other.grid[i]) + '/'
        return Grid(out)


def single_cycle(g, transforms):
    if g.size % 2 == 0:
        joins = g.size // 2
        size = 2
    else:
        joins = g.size // 3
        size = 3
    subs = g.split(joins, size)
    constructor = ''
    for _ in range(joins):
        g_p = None
        for _ in range(joins):
            n = transforms[next(subs)]
            if g_p is None:
                g_p = n
            else:
                g_p += n
        constructor += '/' + repr(g_p)
    return Grid(constructor.strip('/'))


def three_cycles(g, transforms):
    counts = {}
    for _ in range(3):
        g = single_cycle(g, transforms)
    for grid in g.split(3, 3):
        if grid not in counts:
            counts[grid] = 0
        counts[grid] += 1
    return counts


@timeit
def run_cycles(n, transforms):
    counts = {Grid(): 1}
    grids = {}
    num_3 = n // 3
    runs = 0
    count = 0
    for _ in range(num_3):
        runs += 3
        run_count = {}
        for g, count in counts.items():
            if g not in grids:
                grids[g] = three_cycles(g, transforms)
            for sub_grid, number_made in grids[g].items():
                if sub_grid not in run_count:
                    run_count[sub_grid] = 0
                run_count[sub_grid] += count * number_made
        counts = run_count

    if n % 3 == 0:
        total_on = sum(g.on() * c for g, c in counts.items())
    else:
        total_on = 0
        for g, mult in counts.items():
            for _ in range(n % 3):
                g = single_cycle(g, transforms)
            total_on += g.on() * mult
    return '{} on after {} runs'.format(total_on, n)


@timeit
def get_answer(data, part2=False):

    # test = Grid('/..#/.#./###')
    # print(test)

    transforms = {}
    for row in data.split('\n'):
        before, after = row.split(' => ')
        rule = Grid(after)
        for mod in Grid(before).all():
            transforms[mod] = rule
    if part2:
        iters = 18
    else:
        iters = 5

    # g = Grid()
    # for _ in range(iters):
    #     g = single_cycle(g, transforms)
    # return g.on()

    # I originally ran it manually 18 times, fancy multiples of 3 idea
    # came from reddit
    return run_cycles(iters, transforms)


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
