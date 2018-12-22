from aoc_utilities import get_instructions
import os

from heapq import heappop, heappush


'''
notes:
0, 0 -> gi=0
target -> gi=0
x, 0 -> gi=16807 * x
0, y -> gi=48271 * y
el = (gi + d) % 20183

x, y -> el[X-1, Y] * el[X, Y-1]

el % 3 == 0 -> rocky
el % 3 == 1 -> wet
el % 3 == 2 -> narrow

risk = {0: rocky, 1: wet, 2: narrow}
tools = {0: neither, 1: torch, 2: climbing gear}

if risk == 0 # use 1, 2
if risk == 1 # use 0, 2
if risk == 2 # use 0, 1

so are not allowed to use the tool corresponding to the risk of the region
'''


class Caves(object):
    def __init__(self, target, depth):
        self.x, self.y = target
        self.depth = depth
        self.el = {(self.x, self.y): 0, (0, 0): 0}
        self._calc_erosion()

    def _calc_erosion(self):
        for y in range(self.y + 1):
            for x in range(self.x + 1):
                self._get_el(x, y)

    def _get_el(self, x, y):
        if (x, y) in self.el:
             return self.el[(x, y)]
        if y == 0:
            gi = x * 16807
        elif x == 0:
            gi = y * 48271
        else:
            gi = self._get_el(x - 1, y) * self._get_el(x, y - 1)

        self.el[(x, y)] = (gi + self.depth) % 20183

        return self.el[(x, y)]

    def _get_risk(self, x, y):
        return self._get_el(x, y) % 3

    def get_sum(self):
        total = 0
        for y in range(self.y + 1):
            for x in range(self.x + 1):
                total += self._get_risk(x, y)
        return total

    def _check_tool(self, x, y, t):
        for tool in (0, 1, 2):
            if tool == self._get_risk(x, y): # cannot switch to disallowed tool
                continue
            if t == tool: # no cost to switching to same tool
                continue
            yield x, y, tool

    def _neighbors(self, x, y, tool):
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            cx = x + dx
            cy = y + dy
            if cx < 0 or cy < 0: # cannot go to negative areas
                continue
            if tool == self._get_risk(cx, cy): # cannot go to area with wrong tool
                continue
            yield cx, cy, tool

    def search_paths(self):
        q = [(0, 0, 0, 1)] # time, x, y, equiped tool
        best = {}

        target = (self.x, self.y, 1)

        while q:
            time, x, y, tool = heappop(q)
            key = (x, y, tool)
            # if there is a better time to this room, skip checks
            if key in best:
                if best[key] <= time:
                    continue
            # add current time as best time to this room
            best[key] = time
            # if at the end, return
            if key == target:
                return time
            # check tools
            for nx, ny, nt in self._check_tool(*key):
                heappush(q, (time + 7, nx, ny, nt))
            # check neighbors
            for nx, ny, nt in self._neighbors(x, y, tool):
                heappush(q, (time + 1, nx, ny, nt))
        return best


def get_answer(data, part2=False):
    for line in data:
        label, nums = line.split(': ')
        if label == 'depth':
            depth = int(nums.strip())
        else:
            target = tuple(map(int, nums.strip().split(',')))

    c = Caves(target, depth)

    if part2:
        return c.search_paths()
    return c.get_sum()


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
