from aoc_utilities import get_instructions
import os
from day18 import memoize
from day17 import colors as c
from heapq import heappop, heappush
from collections import deque, Counter
import time
from itertools import count

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def combine(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __repr__(self):
        return str(self)

class Grid:
    def __init__(self, data):
        self.do = [Point(i, j) for i, j in ((0, 1), (1, 0), (-1, 0), (0, -1))]
        self.directions = {Point(0, 1): 'down',
                           Point(1, 0): 'right',
                           Point(0, -1): 'up',
                           Point(-1, 0): 'left'}
        self._init_grid(data)
        self._setup_portals()
        st = time.time()

    def _init_grid(self, data):
        self.grid = {}
        self.portals = {}
        for j, line in enumerate(data):
            for i, val in enumerate(line):
                position = Point(i, j)
                self.grid[position] = val
            self.grid[Point(i + 1, j)] = '\n'

        self.min_y = int(min(self.grid, key=lambda x: x.y).y)
        self.max_y = int(max(self.grid, key=lambda x: x.y).y)
        self.min_x = int(min(self.grid, key=lambda x: x.x).x)
        self.max_x = int(max(self.grid, key=lambda x: x.x).x)

    def _near_edge(self, point):
        if point.y - self.min_y <= 2:
            return True
        if self.max_y - point.y <= 2:
            return True
        if self.max_x - point.x <= 2:
            return True
        if point.x - self.min_x <= 2:
            return True
        return False

    def _setup_portals(self):
        for p in self:
            val = self.grid[p]
            if val not in (' ', '#', '.', '\n'):
                ap, n = self._setup_portal(p)
                if n not in self.portals:
                    self.portals[n] = {'outer': None, 'inner': None}
                if self._near_edge(p):
                    self.portals[n]['outer'] = ap
                else:
                    self.portals[n]['inner'] = ap

        self.start = self.portals['AA']['outer']
        self.end = self.portals['ZZ']['outer']

        self.teleports = {}
        self.labels = {}
        for k, v in self.portals.items():
            a, b = v.values()
            if a is None or b is None:
                continue
            self.teleports[a] = b
            self.teleports[b] = a
            self.labels[a] = k
            self.labels[b] = k

    def _find_valid_neighbor(self, point):
        for d in self.do:
            np = point.combine(d)
            if np in self.grid and self.grid[np] == '.':
                yield np

    def _setup_portal(self, point):
        point_letter = self.grid[point]
        other_letter = ''
        tele_point = None

        for d in self.do:
            neighbor = point.combine(d)
            if neighbor not in self.grid: # ignore out of bounds
                continue
            elif self.grid[neighbor].isalpha(): # a letter
                other_letter = self.grid[neighbor]
                neighbor_point = neighbor
            elif self.grid[neighbor] == '.': # teleport point
                tele_point = neighbor
                tele_dir = d
                first = True

        if tele_point is None:
            for d in self.do:
                check = neighbor_point.combine(d)
                if self.grid[check] == '.': #teleport point
                    tele_point = check
                    tele_dir = d
                    first = False

        close = min((point, neighbor_point), key=lambda x: x.dist(tele_point))
        d = self.directions[tele_dir]

        if close.dist(point) < close.dist(neighbor_point):
            if d in ('up', 'left'):
                o1 = True
            else:
                o1 = False
        else:
            if d in ('up', 'left'):
                o1 = False
            else:
                o1 = True
        if o1:
            name = point_letter + other_letter
        else:
            name = other_letter + point_letter
        return tele_point, name

    def __iter__(self):
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                position = Point(x, y)
                if position in self.grid:
                    yield position

    def __str__(self):
        o = ''
        for p in self:
            val = self.grid[p]
            o += val
        return o

    def show_path(self, path):
        path = set(path)
        o = ''
        for p in self:
            val = self.grid[p]
            if p in path:
                val = c.color(val)
            o += val
        print(o)

    @memoize
    def search(self, start=None, mode='tele'):
        if start is None:
            start = self.start
        q = deque([(0, 0, start, frozenset([start]), Point(0, 0), [])])
        seen = set([(start, 0)])
        iters = 0
        while q:
            iters += 1
            num_steps, level, pos, path, prev, levels = q.popleft()

            if pos == self.end and level == 0:
                return num_steps, path, levels

            if pos in self.teleports:
                skip_tele = False
                if mode != 'tele':
                    portal = self.labels[pos]
                    if self.portals[portal]['inner'] == pos: # jump down a level
                        level += 1
                    elif self.portals[portal]['outer'] == pos:
                        if level == 0:
                            skip_tele = True
                        else:
                            level -= 1
                    else:
                        print('no good')
                if not skip_tele:
                    pos = self.teleports[pos]
                    path = path | set([pos])
                    num_steps += 1

            for neighbor in self._find_valid_neighbor(pos):
                if level >= len(self.portals):
                    continue
                if (neighbor, level) in seen:
                    continue
                seen.add((neighbor, level))
                nlevels = levels + [level]
                npath = path | frozenset([neighbor])
                q.append((num_steps + 1, level, neighbor, npath, pos, nlevels))


def get_answer(data, part2=False):
    grid = Grid(data)

    if part2:
        ns, p, l = grid.search(grid.start, 'recurse')

    else:
        ns, p, l = grid.search(grid.start)
    grid.show_path(p)
    print(Counter(l))
    return ns


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
