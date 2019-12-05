from __future__ import division

from aoc_utilities import get_instructions
import os
import re
from heapq import heappop, heappush
from itertools import product


def to_4d(x, y, z):
    return (x + y + z, x - y + z, x + y - z, x - y - z)


def to_3d(t, u, v, w):
    '''
    x + y + z = t
    x - y + z = u
    x + y - z = v
    x - y - z = w
    x = (t + w) / 2
    y = (v - w) / 2
    z = (t - v) / 2
    t + u = v + w
    '''
    xp = (t + w)
    if xp % 2 != 0:
        return
    yp = (v - w)
    if yp % 2 != 0:
        return
    zp = (t - v)
    if zp % 2 != 0:
        return
    x = xp / 2
    y = yp / 2
    z = zp / 2
    if x - y + z != u:
        return
    return (x, y, z)


class Bot():
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.coords = to_4d(x, y, z)
        self.min = [c - r for c in self.coords]
        self.max = [c + r for c in self.coords]

    def __getitem__(self, idx):
        if idx <= 3:
            return self.coords[idx]
        elif idx == 4:
            return self.r
        else:
            raise IndexError('index out of range')

    def distance(self, other):
        return md(self.x, self.y, self.z, other.x, other.y, other.z)

    def __contains__(self, other):
        return self.distance(other) <= self.r


class Box():

    def __init__(self, min_vals, max_vals, min_idx,
                 max_idx):
        self.min = min_vals
        self.max = max_vals
        self.min_idx = min_idx
        self.max_idx = max_idx
        self.sizes = [y - x + 1 for x, y in zip(min_idx, max_idx)]
        self.size = 1
        for val in self.sizes:
            self.size *= val
        self.point = self._get_point()
        self.d_to_o = None

    def _get_point(self):

        c = all([x == y for x, y in zip(self.min, self.max)])
        if c:
            return to_3d(*self.min)
        return

    def distance_to_origin(self):
        if self.d_to_o is not None:
            return self.d_to_o

        if self.point is not None:
            self.d_to_o = sum([abs(x) for x in self.point])
        else:
            distances = []
            for low, high in zip(self.min, self.max):
                if low * high <= 0:
                    distances.append(0)
                elif low >= 0:
                    distances.append(low)
                else:
                    distances.append(high)
            self.d_to_o = max(distances)
        return self.d_to_o

    def _split_single(self):
        ranges = []
        for miv, mav in zip(self.min, self.max):
            if mav - miv < 20:
                r = list(range(miv, mav + 1))
            else:
                r = [miv, miv + 1, mav - 1, mav]
            ranges.append(r)
        valids = []
        for check in product(*ranges):
            if to_3d(*check) is not None:
                valids.append(check)
        return [Box(p, p, [], []) for p in valids]

    def split(self, splits):
        axis, size = max(enumerate(self.sizes), key=lambda x: x[1])

        if size == 1:
            # find points in 3d space for this box
            return self._split_single()

        to_split = splits[axis]

        miv, mav = self.min_idx[axis], self.max_idx[axis]
        mid = (miv + mav) // 2

        left_max = [x for x in self.max]
        left_max[axis] = to_split[mid]
        left_max_idx = [x for x in self.max_idx]
        left_max_idx[axis] = mid

        right_min = [x for x in self.min]
        right_min[axis] = to_split[mid] + 1
        right_min_idx = [x for x in self.min_idx]
        right_min_idx[axis] = mid + 1

        left = Box(self.min, left_max, self.min_idx, left_max_idx)
        right = Box(right_min, self.max, right_min_idx, self.max_idx)

        return (left, right)

    def __contains__(self, bot):
        for b_min, b_max, miv, mav in zip(bot.min, bot.max,
                                          self.min, self.max):
            if (b_min > mav) or (miv > b_max):
                return False
        return True

    def __str__(self):
        if self.point:
            return str(self.point)
        outputs = []
        for miv, mav in zip(self.min, self.max):
            if miv == mav:
                outputs.append(range(miv, mav))
        return str(outputs)

    def __lt__(self, other):
        return self.size < other.size


def get_splits(bots):
    ts = set()
    us = set()
    vs = set()
    ws = set()
    for b in bots:
        ts.add(b.min[0])
        us.add(b.min[1])
        vs.add(b.min[2])
        ws.add(b.min[3])

        ts.add(b.max[0])
        us.add(b.max[1])
        vs.add(b.max[2])
        ws.add(b.max[3])
    return sorted(ts), sorted(us), sorted(vs), sorted(ws)


def search_boxes(bots):
    splits = get_splits(bots)

    first_min = []
    first_max = []
    min_idxs = [0] * 4
    max_idxs = []
    for sub in splits:
        first_min.append(min(sub))
        first_max.append(max(sub))
        max_idxs.append(len(sub) - 1)

    start = Box(first_min, first_max, min_idxs, max_idxs)
    pops = 0
    heap = [(-len(bots), start.distance_to_origin(), start.size, start)]

    while heap:
        pops += 1

        bound, _, _, box = heappop(heap)

        bound = -1 * bound

        if pops % 1000 == 0:
            print('pops: {}, size: {}'.format(pops, len(heap)))

        if box.point:
            print('{} found with {} bots after {} checks'.format(
                    box, bound, pops))
            return box

        for new_box in box.split(splits):
            ub = sum(b in new_box for b in bots)
            heappush(heap, (-ub, new_box.distance_to_origin(),
                            new_box.size, new_box))


def md(x1, y1, z1, x2=0, y2=0, z2=0):
    return abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1)


def parse_input(data):
    max_radius = 0
    bots = []
    for line in data:
        (x, y, z, r) = map(int, re.findall('-?\d+', line))
        cur_bot = Bot(x, y, z, r)
        bots.append(cur_bot)
        if r > max_radius:
            max_radius = r
            max_bot = cur_bot
    return bots, max_radius, max_bot


def get_answer(data, part2=False):
    b, mr, mb = parse_input(data)
    t_b = Box([33, 11, 11, -11], [33, 11, 11, -11], [], [])

    if part2:
        best_box = search_boxes(b)
        best_point = best_box.point
        return sum(abs(x) for x in best_point)

    count = 0
    for bot in b:
        d = md(bot.x, bot.y, bot.z, mb.x, mb.y, mb.z)
        if d <= mr:
            count += 1
    return count


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])

    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
