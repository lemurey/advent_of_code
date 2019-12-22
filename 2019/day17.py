import sys
sys.path.append('/Users/lee.murray/projects/advent_of_code')

from aoc_utilities import get_instructions
import os
from intcode import Intcode
from collections import deque
import time


class colors:
    red = '\x1b[1;31;40m'
    blue = '\x1b[1;34;40m'
    yellow = '\x1b[1;33;40m'
    green = '\x1b[1;32;40m'
    white = '\x1b[1;37;40m'
    end = '\x1b[0m'

    @classmethod
    def color(cls, s, c='red'):
        if c == 'red':
            color = cls.red
        elif c == 'blue':
            color = cls.blue
        elif c == 'yellow':
            color = cls.yellow
        elif c == 'green':
            color = cls.green
        elif c == 'white':
            color = cls.white
        else:
            color = end
        return '{}{}{}'.format(color, s, cls.end)


class MapGrid:
    def __init__(self, grid):
        self.grid = grid
        self.orig = {k: v for k, v in grid.items()}
        self._get_grid_bounds()
        self.intersections = self.get_intersections(False)
        self.dirs = {'v': -1j,
                     '^':  1j,
                     '<':  -1,
                     '>':   1}
        self.facings = {v: k for k, v in self.dirs.items()}
        self.turn_to_d = {('L', -1j):   1,
                           ('L', 1j):  -1,
                           ('L', -1): -1j,
                            ('L', 1):  1j,
                          ('R', -1j):  -1,
                           ('R', 1j):   1,
                           ('R', -1):  1j,
                            ('R', 1): -1j,}
        self.d_to_turn = { (-1j, 1): 'L',
                           (1j, -1): 'L',
                          (-1, -1j): 'L',
                            (1, 1j): 'L',
                          (-1j, -1): 'R',
                            (1j, 1): 'R',
                           (-1, 1j): 'R',
                           (1, -1j): 'R',}

        self.start = [k for k in grid if grid[k] in ('^', '<', 'v', '>')][0]
        self.start_d = self.dirs[self.orig[self.start]]
        self.to_visit = {k: 0 for k in self.orig if self.orig[k] == '#'}
        self.to_visit[self.start] = 1
        self.top_score = len(self.to_visit)

    def _get_grid_bounds(self):
        self.min_y = int(min(self.grid, key=lambda x: x.imag).imag)
        self.max_y = int(max(self.grid, key=lambda x: x.imag).imag)
        self.min_x = int(min(self.grid, key=lambda x: x.real).real)
        self.max_x = int(max(self.grid, key=lambda x: x.real).real)

    def get_intersections(self, show=True):
        if getattr(self, 'intersections', None) is None:
            self._reset()
            intersections = set()
            for position in self:
                if self.grid[position] == '.':
                    continue
                for d in (-1j, 1j, -1, 1):
                    c = position + d
                    if (c not in self.grid) or (self.grid[c] != '#'):
                        break
                else:
                    intersections.add(position)
        else:
            intersections = self.intersections
        if show:
            for p in intersections:
                self.grid[p] = 'O'
            print(self)
            self._reset()
            return score_intersections(intersections)
        return intersections

    def _reset(self):
        self.grid = {k: v for k, v in self.orig.items()}

    def __iter__(self):
        for y in reversed(range(self.min_y, self.max_y + 1)):
            for x in range(self.min_x, self.max_x + 1):
                position = x + y * 1j
                if position in self.grid:
                    yield position

    def __str__(self):
        return ''.join(self.grid[x] for x in self)

    def follow_path(self, path, position, d, visits):
        for n in path.split(','):
            if n == '':
                continue
            if n in ('L', 'R'):
                d = self.turn_to_d[n, d]
                continue
            else:
                step = int(n)
            for _ in range(step):
                position += d
                if position in visits:
                    visits[position] = 1
                else:
                    print('trying to visit non # space')
        return position, d, visits

    def check_path(self, path, score=False):
        to_visit = {k: v for k, v in self.to_visit.items()}
        _, _, to_visit = self.follow_path(path, self.start, self.start_d, to_visit)
        if all(x == 1 for x in to_visit.values()):
            return True
        if score:
            return sum(to_visit.values())
        return False

    def display_path(self, path):
        new = {k: v for k,v in self.orig.items()}
        position = self.start
        d = self.start_d
        for n in path.split(','):
            if n == '':
                continue
            if n in ('L', 'R'):
                d = self.turn_to_d[n, d]
                continue
            step = int(n)
            for _ in range(step):
                position += d
                new[position] = colors.color(new[position], 'red')
        new[position] = colors.color(self.facings[d], 'white')
        self.grid = new
        print(self)
        self._reset()


    def search(self):
        position = self.start
        d = self.start_d

        Q = deque([('', position, d, set([position]))])
        iters = 0
        seen = set()
        while Q:
            iters += 1
            path, position, d, visited = Q.popleft()
            visited = set([x for x in visited])
            if path in seen:
                continue
            seen.add(path)
            # if iters % 10000 == 0:
            #     score = self.check_path(path, True)
            #     self.display_path(path)
            #     print('{}: {} - {}'.format(iters, len(Q), score))
            if self.check_path(path):
                return path.rstrip(',')

            ns = self._next_step(path, position, d)
            if ns == 'turn':
                valids = self._pick_turn(position, d)
                for next_d in valids:
                    turn = self.d_to_turn[(d, next_d)]
                    npath = path + '{},'.format(turn)
                    nd = self.turn_to_d[(turn, d)]

                    next_pos = position + nd
                    if next_pos in visited and len(valids) > 1:
                        continue
                    Q.append((npath, position, nd, visited))
            elif ns == 'step':
                valids = self._find_distance(position, d)
                for num_steps, np in valids:
                    if np in visited:
                        continue
                    visited.add(np)
                    npath = path + '{},'.format(num_steps)
                    Q.append((npath, np, d, visited))

    def _next_step(self, path, position, d):
        check = path[:-1]
        if len(path) == 0:
            return 'turn'
        elif check[-1] in ('L', 'R'):
            return 'step'
        else:
            return 'turn'

    def _pick_turn(self, position, prev_d):
        valids = []
        for d in (-1j, 1j, -1, 1):
            c = position + d
            if (
                (c not in self.grid) or
                (self.grid[c] in ('.', '\n')) or
                (c == (position - prev_d)) or
                ((prev_d, d) not in self.d_to_turn)
               ):
                continue
            valids.append(d)
        return valids

    def _find_distance(self, position, d):
        valids = []
        distance = 0
        while True:
            if position + d in self.grid:
                next_spot = self.grid[position + d]
            else:
                valids.append((distance, position))
                return valids
            if next_spot in ('.', '\n'):
                valids.append((distance, position))
                return valids
            if position in self.intersections and distance > 0:
                valids.append((distance, position))
            position += d
            distance += 1



def score_intersections(intersections):
    score = 0
    for p in sorted(intersections, key=lambda x: (abs(x.imag), abs(x.real))):
        score += abs(p.real) * abs(p.imag)
    return score


class Robot:
    def __init__(self, program):
        self.core = Intcode(program, mode='ascii robot')
        self.grid = {}
        self.init_grid()
        self.seen = set()

    def init_grid(self):
        position = 0 + 0j
        for val in self._get_grid():
            self.grid[position] = val
            if val == '\n':
                position = position - position.real - 1j
            else:
                position += 1
        self.grid[position] = '\n'

    def _get_grid(self):
        while True:
            val = self.step()
            if val == -1:
                return 'END'
            yield chr(val)

    def step(self):
        self.core.waiting = False
        val = self.core.run()
        return val

    def _to_ascii(self, string, joiner=''):
        vals = []
        for char in string:
            vals.append(ord(char))
        return vals

    def check_output(self):
        while True:
            self.core.waiting = False
            val = self.core.run()
            self.seen.add(val)
            if val < 0 or val > 128:
                print(val)
                return
            else:
                print(chr(val), end='')
            if chr(val) in (':', '?'):
                self.core.waiting = False
                print(chr(self.core.run()))
                return

    def run(self, program, A, B, C, show=False):
        self.core.reset()
        self.core.program[0] = 2

        if show:
            final = 'y\n'
        else:
            final = 'n\n'

        # step 1 -- draw map, ask for main
        self.check_output()

        # calculate all the inputs it wants
        inputs = []
        for entry in (program, A, B, C, final):
            inputs.extend(self._to_ascii(entry))

        # pass set of inputs for it to grab as needed
        self.core.secondary = inputs

        # run for function input
        val = self.core.run()

        # ask for function A:
        self.check_output()
        val = self.core.run()

        # ask for function B:
        self.check_output()
        val = self.core.run()

        # ask for function C:
        self.check_output()
        val = self.core.run()

        # ask for video feed:
        self.check_output()

        if show:
            self._run_video()
        else:
            self.check_output()


def to_grid(text):
    grid = {}
    position = 0 + 0j
    for val in text:
        grid[position] = val
        if val == '\n':
            position = position - position.real - 1j
        else:
            position += 1
    grid[position] = '\n'
    return grid


import re
def single_run(string, A_len, C_len):
    try_A = string[:A_len]
    try_C = string[-C_len:]
    rem = re.sub(try_A, 'A', string)
    rem = re.sub(try_C, 'C', rem)

    checks = rem.split(',')
    prev_val = None
    try_B = []
    for val in checks:
        if val in ('A', 'C'):
            if len(try_B) > 0:
                break
            continue
        if prev_val not in ('A', 'C'):
            try_B.append(val)
    try_B = ','.join(try_B)
    rem = re.sub(try_B, 'B', rem)
    return rem, try_A, try_B, try_C


def subset(string):
    orig = string
    for A_len in range(20, 2, -1):
        for C_len in range(20, 2, -1):
            string = orig
            rem, try_A, try_B, try_C = single_run(string, A_len, C_len)
            if set(rem.split(',')) == set('ABC'):
                return rem, try_A, try_B, try_C


def get_answer(data, part2=False):
    program = list(map(int, data[0].split(',')))
    r = Robot([x for x in program])

    m = MapGrid(r.grid)

    tp = m.search()
    m.display_path(tp)

    pattern, a, b, c = subset(tp)

    r.run(pattern + '\n', a + '\n', b + '\n' , c + '\n')


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])

    sample = '''#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......'''
    # print(get_answer(sample))
    inputs = get_instructions(year, day)
    # print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
