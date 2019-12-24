from aoc_utilities import get_instructions
import os
from collections import defaultdict


class Bugs:
    def __init__(self, data, verbose=False):
        self._initialitze_grid(data)
        self.seen = set()
        self.verbose = verbose
        if self.verbose:
            print(self)

    def _initialitze_grid(self, data):
        grid = {}
        for j, row in enumerate(data):
            for i, val in enumerate(row):
                position = i + j * 1j
                grid[position] = val
        self.grid = grid
        self.min_y = int(min(grid, key=lambda x: x.imag).imag)
        self.max_y = int(max(grid, key=lambda x: x.imag).imag)
        self.min_x = int(min(grid, key=lambda x: x.real).real)
        self.max_x = int(max(grid, key=lambda x: x.real).real)

    def step(self):
        new = {}
        ss = ''
        for p in self:
            s = 1 if self.grid[p] == '#' else 0
            b = s
            for n in self._get_neighbors(p):
                if n == '#':
                    s += 1
            if s == 2:
                val = '#'
                state = '1'
            elif s == 1 and b == 0:
                val = '#'
                state = '1'
            else:
                val = '.'
                state = '0'

            new[p] = val
            ss += state
        return new, ss

    def run(self, n=float('inf')):
        i = 0
        while i < n:
            i += 1
            new, state = self.step()
            self.grid = new
            if self.verbose:
                print(self)
            if state in self.seen:
                return self.score(state[::-1])
            self.seen.add(state)

    def score(self, state):
        return int(state, 2)

    def __iter__(self):
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                position = x + y * 1j
                if position in self.grid:
                    yield position

    def __str__(self):
        o = ''
        for i, p in enumerate(self, start=1):
            o += self.grid[p]
            if i % 5 == 0:
                o += '\n'
        return o

    def _get_neighbors(self, p):
        for d in (1, -1, -1j, 1j):
            if p + d not in self.grid:
                continue
            if self.grid[p + d] == '\n':
                continue
            yield self.grid[p + d]


class rBugs():
    def __init__(self, data):
        self._initialitze_grid(data)
        self.step_num = 0

    def _initialitze_grid(self, data):
        grid = defaultdict(lambda: '.')
        for j, row in enumerate(data):
            for i, val in enumerate(row):
                position = i + j * 1j
                if position == 2 + 2j:
                    continue
                grid[(0, position)] = val
        self.grid = grid

    def _step_level(self, level):
        '''
        if 1 + 2j, 2 + 1j, 2 + 3j, or 3 + 2j are populated you will step down
        a level, and if we label abose states as 1, 2, 3, 4 the lower level
        will start as:
        1+2  2   2   2  2+3
         1   .   .   .   3
         1   .   ?   .   3
         1   .   .   .   3
        1+4   4   4   4  3+4

        stepping up depends on sums of values in outer ring
        ....#
        #..#.
        #.?##
        #.#..
        .....

        the top row has 1 bug, so it will step up
        the right column has 2 bugs, so it will step up
        the bottom row has 0 bugs, so it will not step up
        the left column has 3 bugs, so it iwll not step up

        the outer level would be
        .....
        .###.
        ..?#.
        ...#.
        .....

        after doing this thinking, it occurs to me the net result is you
        will step levels every other iteration, so if we are running 200
        we need to consider levels from -100 to 100 and no others, and I won't
        worry about this calcualtion
        '''
        new = {}
        for y in range(5):
            for x in range(5):
                p = x + y * 1j
                if p == 2 + 2j:
                    continue
                s = 1 if self.grid[(level, p)] == '#' else 0
                b = s
                for n in self._get_neighbors(level, p):
                    if n == '#':
                        s += 1
                if s == 2:
                    val = '#'
                elif s == 1 and b == 0:
                    val = '#'
                else:
                    val = '.'
                new[(level, p)] = val
        return new

    def step(self):
        subs = []
        self.step_num += 1
        v = (self.step_num + 1) // 2
        for level in range(-v, v+1):
            sub = self._step_level(level)
            subs.append(sub)

        for sub in subs:
            for k, v in sub.items():
                self.grid[k] = v

    def run(self, n):
        for _ in range(n):
            self.step()

    def _get_neighbors(self, level, point):
        for d in (1, 1j, -1j, -1):
            c = point + d
            if c == 2 + 2j: # need 5 neighbors from next level up
                if point == 2 + 1j:
                    y = [0]
                    x = range(5)
                elif point == 1 + 2j:
                    x = [0]
                    y = range(5)
                elif point == 3 + 2j:
                    y = range(5)
                    x = [4]
                elif point == 2 + 3j:
                    x = range(5)
                    y = [4]
                for x_val in x:
                    for y_val in y:
                        sp = x_val + y_val * 1j
                        yield self.grid[(level + 1, sp)]
            elif c.imag < 0: # need 1 neighbor from next level down
                sp = 2 + 1j
                yield self.grid[(level - 1, sp)]
            elif c.imag > 4: # need 1 neighbor from next level down
                sp = 2 + 3j
                yield self.grid[(level - 1, sp)]
            elif c.real < 0: # need 1 neighbor from next level down
                sp = 1 + 2j
                yield self.grid[(level - 1, sp)]
            elif c.real > 4: # need 1 neighbor from next level down
                sp = 3 + 2j
                yield self.grid[(level - 1, sp)]
            else:
                yield self.grid[(level, c)]

    def plot_levels(self, min_l=-100, max_l=100):
        for level in range(min_l, max_l + 1):
            print('depth {}'.format(level))
            for y in range(5):
                row = ''
                for x in range(5):
                    p = x + 1j * y
                    if p == 2 + 2j:
                        row += '?'
                    else:
                        row += self.grid[(level, p)]
                print(row)
            print()


def get_answer(data, part2=False):
    if part2:
        game = rBugs(data)
        game.run(200)
        bug_count = 0
        for b in game.grid.values():
            if b == '#':
                bug_count += 1
        return bug_count

    game = Bugs(data)
    return game.run()


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
#     sample = '''....#
# #..#.
# #..##
# ..#..
# #....'''.split('\n')
#     print(get_answer(sample, part2=True))
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
