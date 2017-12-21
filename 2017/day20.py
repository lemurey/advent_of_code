from aoc_utilities import get_instructions
from math import sqrt
from utilities import timeit
from itertools import chain
import os


class Particle(list):

    def __add__(self, other):
        out = Particle([0, 0, 0])
        if isinstance(other, float) or isinstance(other, int):
            for i, val in enumerate(self):
                out[i] = val + other
        else:
            for i, val in enumerate(self):
                out[i] = val + other[i]
        return out

    def __mul__(self, other):
        out = Particle([0, 0, 0])
        if isinstance(other, float) or isinstance(other, int):
            for i, val in enumerate(self):
                out[i] = val * other
        else:
            for i, val in enumerate(self):
                out[i] = val * other[i]
        return out

    def spherical(self):
        self.r = sqrt(self[0] ** 2 + self[1] ** 2 + self[2] ** 2)


def clean_up(string):
    out = []
    for i, entry in enumerate(string.split(',')):
        if i > 2:
            continue
        out.append(int(entry.strip('<').strip('>')))
    return Particle(out)


def collide(p1, v1, a1, p2, v2, a2):

    times = []
    for i in range(3):
        c = (p2[i] - p1[i])
        b = (v2[i] + a2[i] / 2) - (v1[i] + a1[i] / 2)
        a = (a2[i] - a1[i]) / 2
        square_root_term = b ** 2 - 4 * a * c

        if a == 0 and b == 0 and c == 0:
            times.append((True, ))
        elif a == 0 and b != 0:
            times.append((abs(c) / abs(b), ))
        elif square_root_term > 0:
            square_root_term = sqrt(square_root_term)
            o1 = (-1 * b + square_root_term) / (2 * a)
            o2 = (-1 * b - square_root_term) / (2 * a)
            times.append((o1, o2))
        else:
            return []

    if (True,) in times:
        ind = times.index((True, ))
        times[ind] = times[ind - 1] + times[(ind + 1) % 3]
    x, y, z = times
    return set(x).intersection(set(y)).intersection(set(z))


def p_at_t(t, p, v, a):
    return p + v * t + a * (t * (t + 1) / 2)


def check_collisions(p, v, a, i, j, time, particles):
    c1 = p_at_t(time, p[i], v[i], a[i])
    c2 = p_at_t(time, p[j], v[j], a[j])
    if c1 == c2:
        to_remove = set([i, j])
    else:
        to_remove = set()
    for k in particles:
        if k == i or k == j:
            continue
        c3 = p_at_t(time, p[k], v[k], a[k])
        if c3 == c1:
            to_remove = to_remove.union([i, k])
        if c3 == c2:
            to_remove = to_remove.union([j, k])
    return to_remove


@timeit
def collisions(p, v, a):
    n = len(p)
    particles = set(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if (i not in particles) or (j not in particles):
                continue
            for time in collide(p[i], v[i], a[i], p[j], v[j], a[j]):
                for index in check_collisions(p, v, a, i, j, time, particles):
                    particles.remove(index)
    return particles


def get_answer(data, part2=False):

    positions = []
    velocities = []
    accelerations = []

    for i, line in enumerate(data.split('\n')):
        p, v, a = map(clean_up, line.split('<')[1:])
        p.spherical()
        v.spherical()
        a.spherical()
        positions.append(p)
        velocities.append(v)
        accelerations.append(a)

    if not part2:
        to_search = zip(accelerations, velocities, positions)
        smallest = min(to_search, key=lambda x: (x[0].r, x[1].r, x[2].r))
        return positions.index(smallest[2])

    test_size = 1000

    p = positions[:test_size]
    v = velocities[:test_size]
    a = accelerations[:test_size]

    particles_left = collisions(p, v, a)

    return len(particles_left)


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
