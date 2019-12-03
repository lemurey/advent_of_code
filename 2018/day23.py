from __future__ import division

from aoc_utilities import get_instructions
import os
import re
from heapq import heappop, heappush


def md(x1, y1, z1, x2=0, y2=0, z2=0):
    return abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1)


class Bot(object):
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def __add__(self, other):
        return md(self.x, self.y, self.z,
                  other.x, other.y, other.z)

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        elif key == 3:
            return self.r
        else:
            raise IndexError('index out of range')


class Box(object):
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def __contains__(self, bot):
        d = 0
        for i in (0, 1, 2):
            if bot[i] <= self.low[i]:
                d += (self.low[i] - bot[i])
            if bot[i] >= self.high[i]:
                d += (bot[i] - self.high[i])
        return d <= bot.r

    def split(self, off):
        for octant in ((0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
                       (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)):
            newlow = (self.low[i] + off * octant[i] for i in (0, 1, 2))
            newhigh = (self.high[i] + off for i in (0, 1, 2))
            yield Box(tuple(newlow), tuple(newhigh))


ORIGIN = Bot(0, 0, 0, 0)


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


def num_in_box(box, bots):
    return sum([b in box for b in bots])


def get_start_size(bots):
    return max(max(abs(b[i]) for b in bots) for i in (0, 1, 2))


def search(size, bots):
    fs = 'box at {}. distance of {}. {} bots in range'
    firstbox = Box((-size, -size, -size), (size, size, size))
    heap = [(-len(bots), -2*size, 3*size, firstbox)]
    count = 0

    while heap:
        negreach, neg_size, d, box = heappop(heap)
        count += 1
        # if count > 50:
            # break
        # print(fs.format(box.low, d, -negreach))
        if count % 100 == 0:
            print('{}: {}, {}'.format(count,len(heap), neg_size))

        if neg_size == -1:
            print fs.format(box.low, d, -negreach)
            return -1 * negreach
        new_size = neg_size // -2
        for newbox in box.split(new_size):
            reach = num_in_box(newbox, bots)
            new_d = md(*box.low)
            vals = (-reach, -new_size, new_d, newbox)
            heappush(heap, vals)


def get_answer(data, part2=False):
    b, mr, mb = parse_input(data)
    if part2:
        size = 1
        max_size = get_start_size(b)
        # print(max_size)
        while size <= max_size:
            size *= 2
        size = 4
        return search(size, b)

    count = 0
    for bot in b:
        d = bot + mb
        # d = md(x, y, z, x2, y2, z2)
        if d <= mr:
            count += 1
    return count


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    sample = '''pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1'''.split('\n')
    sample = '''pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5'''.split('\n')

    print(get_answer(sample, part2=True))
    # inputs = get_instructions(year, day)
    # print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
