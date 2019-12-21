from aoc_utilities import get_instructions
import os
from day17 import colors as c
from collections import deque
from heapq import heappop, heappush
import time


def memoize(f):
    memo = {}
    def helper(*args):
        key = tuple(args)
        if key not in memo:
            memo[key] = f(*args)
        return memo[key]
    return helper


class Tunnels:
    def __init__(self, data):
        self._initialize_grid(data)
        self.st = time.time()

    def _initialize_grid(self, data):
        grid = {}
        keys = {}
        doors = {}
        for j, row in enumerate(data):
            # y = -1 * i
            for i, val in enumerate(row):
                position = (i, j)
                grid[position] = val
                if val == '@':
                    self.start = position
                if val not in ('#', '.', '@'):
                    if val.isupper():
                        doors[position] = val
                    else:
                        keys[position] = val
            grid[position[0] + 1, position[1]] = '\n'
        self.grid = grid
        self.keys = keys
        self.all_keys = set(self.keys.values())
        self.doors = doors
        self.min_y = int(min(grid, key=lambda x: x[1])[1])
        self.max_y = int(max(grid, key=lambda x: x[1])[1])
        self.min_x = int(min(grid, key=lambda x: x[1])[1])
        self.max_x = int(max(grid, key=lambda x: x[0])[0])

    def __iter__(self):
        for y in reversed(range(self.min_y, self.max_y + 1)):
            for x in range(self.min_x, self.max_x + 1):
                position = (x, y)
                if position in self.grid:
                    yield position

    def __str__(self):
        o = ''
        for p in self:
            if p in self.keys:
                val = c.color(self.grid[p])
            elif p in self.doors:
                val = c.color(self.grid[p], 'green')
            elif self.grid[p] == '@':
                val = c.color('@', 'white')
            else:
                val = self.grid[p]
            o += val
        return o

    @memoize
    def reachable_keys(self, p, keys):
        q = deque([(p, 0)])
        seen = set()
        while q:
            cp, steps = q.popleft()
            # grab key
            if cp in self.keys and self.keys[cp] not in keys:
                yield steps, cp, self.keys[cp]
                continue
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                np = cp[0] + d[0], cp[1] + d[1]
                if np in seen:
                    continue
                seen.add(np)

                # stop at walls
                if self.grid[np] == '#':
                    continue
                # stop at doors you don't have key for
                if np in self.doors and self.grid[np].lower() not in keys:
                    continue
                q.append((np, steps + 1))

    def __hash__(self):
        return hash(self.st)


def update(tup, index, val):
    return tup[:index] + (val, ) + tup[index + 1:]


def run_search(tunnel, start_pos, start_keys, all_keys):
    trips = [(0, tuple(start_pos), start_keys)]
    while True:
        steps, robots, keys = heappop(trips)

        # end condtion, found all the keys
        if keys == all_keys:
            return steps

        # iterate over robots
        for i, pos in enumerate(robots):
            # iterate over found keys
            for num_steps, key_loc, new_key in tunnel.reachable_keys(pos, keys):
                new_key = frozenset([new_key])
                new_robots = update(robots, i, key_loc)
                heappush(trips, (steps + num_steps, new_robots, keys | new_key))


def get_answer(data, part2=False):
    tunnel = Tunnels(data)
    start_keys = frozenset()
    start_pos = [tunnel.start]
    all_keys = tunnel.all_keys

    if part2:
        robots = []
        for d in ((0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)):
            p = (tunnel.start[0] + d[0], tunnel.start[1] + d[1])
            tunnel.grid[p] = '#'

        for d in ((1, 1), (-1, -1), (1, -1), (-1, 1)):
            p = (tunnel.start[0] + d[0], tunnel.start[1] + d[1])
            tunnel.grid[p] = '@'
            robots.append(p)

        return run_search(tunnel, robots, start_keys, all_keys)

    return run_search(tunnel, start_pos, start_keys, all_keys)


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
