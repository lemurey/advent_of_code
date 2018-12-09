from aoc_utilities import get_instructions
from utilities import timeit
import os


class Grid(object):
    def __init__(self, data):
        self.points = set()
        (self.min_x, self.min_y,
         self.max_x, self.max_y) = self._process_data(data)
        self.top_screen = {}
        self.left_screen = {}
        self.right_screen = {}
        self.bottom_screen = {}
        self.distances = None

    def _process_data(self, data):
        min_x = None
        min_y = None
        max_x = None
        max_y = None
        for entry in data:
            x, y = map(int, entry.split(', '))
            self.points.add((x, y))
            if (max_x is None) or (x > max_x):
                max_x = x
            if (min_x is None) or (x < min_x):
                min_x = x
            if (max_y is None) or (y > max_y):
                max_y = y
            if (min_y is None) or (y < min_y):
                min_y = y
        return min_x, min_y, max_x, max_y

    def _md(self, p1, p2):
        x = p2[0] - p1[0]
        y = p2[1] - p1[1]
        d = abs(x) + abs(y)
        return x, y, d

    def _check_points(self, x, y, d, p1, p2):
        if (d / 2.) <= abs(x):
            if x > 0:
                self.left_screen[p2] = p1
                self.right_screen[p1] = p2
            elif x < 0:
                self.left_screen[p1] = p2
                self.right_screen[p2] = p1
        if (d / 2.) <= abs(y):
            if y > 0:
                self.top_screen[p2] = p1
                self.bottom_screen[p1] = p2
            elif y < 0:
                self.top_screen[p1] = p2
                self.bottom_screen[p2] = p1

    def _get_distances(self):
        ds = {}
        for p1 in self.points:
            for p2 in self.points:
                x, y, d = self._md(p1, p2)
                self._check_points(x, y, d, p1, p2)
                ds[(p1, p2)] = d
        self.distances = ds

    def _check_point(self, p):
        return ((p in self.top_screen) &
                (p in self.left_screen) &
                (p in self.right_screen) &
                (p in self.bottom_screen)
               )

    def solve(self, max_d=10000):
        if self.distances is None:
            self._get_distances()
        outputs = {}
        region = {}
        for xi in xrange(self.min_x, self.max_x + 1):
            for yi in xrange(self.min_y, self.max_y + 1):
                min_d = None
                d_sum = 0
                for point in self.points:
                    _, _, d = self._md((xi, yi), point)
                    d_sum += d
                    if (min_d is None) or (d < min_d):
                        min_d = d
                        cur_min = point
                    elif d == min_d:
                        cur_min = None
                if d_sum < max_d:
                    region[(xi, yi)] = 1
                if cur_min is None:
                    continue
                if cur_min not in outputs:
                    outputs[cur_min] = 0
                outputs[cur_min] += 1
        self.region = region
        self.outputs = {k: v for k, v in outputs.iteritems() if self._check_point(k)}


def get_answer(data, part2=False):
    g = Grid(data)
    g.solve()
    print max(g.outputs.values())
    return sum(g.region.values())


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
#     sample = '''1, 1
# 1, 6
# 8, 3
# 3, 4
# 5, 5
# 8, 9'''.split('\n')
#     print(get_answer(sample))
    print(get_answer(inputs, part2=False))