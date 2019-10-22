from aoc_utilities import get_instructions
import os
import re
from heapq import heappop, heappush


def md(x1, y1, z1, x2=0, y2=0, z2=0):
    return abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1)


def parse_input(data):
    positions = {}
    max_radius = 0
    for line in data:
        (x, y, z, r) = map(int, re.findall('-?\d+', line))
        positions[(x, y, z)] = r
        if r > max_radius:
            max_radius = r
            max_pos = (x, y, z)
    return positions, max_radius, max_pos


def search():
    pass





def d_func(coord, r, d):
    for c in range(coord - r, coord + r + 1):
        if c not in d:
            d[c] = 0
        d[c] += 1


def search_coordinates(p):
    xd = {}
    yd = {}
    zd = {}
    for x, y, z in p:
        r = p[(x, y, z)]
        d_func(x, r, xd)
        d_func(y, r, yd)
        d_func(z, r, zd)
    return xd, yd, zd


def find_coordinates(d, n1, n2=None):
    ds = sorted(d.items(), key=lambda x: x[1])
    if n2 is None:
        vals = ds[-n1:]
    else:
        vals = ds[-n1:-n2]
    for coord, _ in vals:
        yield coord


def find_most(p, n1, n2=None):
    xd, yd, zd = search_coordinates(p)
    counts = {}

    for xc in find_coordinates(xd, n1, n2):
        print xc
        for yc in find_coordinates(yd, n1, n2):
            print yc
            for zc in find_coordinates(zd, n1, n2):
                counts[(xc, yc, zc)] = 0
                for x, y, z in p:
                    d = md(xc, yc, zc, x, y, z)
                    if d <= p[(x, y, z)]:
                        counts[(xc, yc, zc)] += 1

    return counts

def get_answer(data, part2=False):
    p, mr, mp = parse_input(data)
    if part2:
        counts = find_most(p, 5)
        return max(counts.items(), key=lambda x: x[1])

    count = 0
    x2, y2, z2 = mp
    for (x, y, z) in p:
        d = md(x, y, z, x2, y2, z2)
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

    # print(get_answer(sample, part2=True))
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))