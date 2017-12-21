from aoc_utilities import get_instructions
from math import sqrt
from utilities import timeit
from itertools import chain
import os


class Particle:

    def __init__(self, p, v, a):
        self.p = p
        self.v = v
        self.a = a
        self.dead = False

    def update(self):
        self.v = self.v + self.a
        self.p = self.p + self.v

    def kill(self):
        self.dead = True

    def alive(self):
        return not self.dead


class Coordinate(list):

    def __add__(self, other):
        out = Coordinate([0, 0, 0])
        if isinstance(other, float) or isinstance(other, int):
            for i, val in enumerate(self):
                out[i] = val + other
        else:
            for i, val in enumerate(self):
                out[i] = val + other[i]
        return out

    def __mul__(self, other):
        out = Coordinate([0, 0, 0])
        if isinstance(other, float) or isinstance(other, int):
            for i, val in enumerate(self):
                out[i] = val * other
        else:
            for i, val in enumerate(self):
                out[i] = val * other[i]
        return out

    def __eq__(self, other):
        if not isinstance(other, Coordinate):
            return False
        for i, val in enumerate(self):
            if other[i] != val:
                return False
        return True

    def __hash__(self):
        return hash(tuple(self))

    def spherical(self):
        self.r = sqrt(self[0] ** 2 + self[1] ** 2 + self[2] ** 2)


def clean_up(string):
    out = []
    for i, entry in enumerate(string.split(',')):
        if i > 2:
            continue
        out.append(int(entry.strip('<').strip('>')))
    return Coordinate(out)


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


@timeit
def sim_version(particles):
    cycle = 0
    last_killed = 0
    while cycle < last_killed + 100:
        positions = {}
        for particle in particles:
            if particle.alive():
                particle.update()
                positions[particle.p] = positions.get(particle.p, 0) + 1

        for particle in particles:
            if particle.alive():
                if positions[particle.p] > 1:
                    particle.kill()
                    last_killed = cycle
        cycle += 1

    return [p for p in particles if p.alive()]


def get_answer(data, part2=False):

    positions = []
    velocities = []
    accelerations = []
    particles = []

    for i, line in enumerate(data.split('\n')):
        p, v, a = map(clean_up, line.split('<')[1:])

        p.spherical()
        v.spherical()
        a.spherical()

        particles.append(Particle(p, v, a))

        positions.append(p)
        velocities.append(v)
        accelerations.append(a)

    if not part2:
        to_search = zip(accelerations, velocities, positions)
        smallest = min(to_search, key=lambda x: (x[0].r, x[1].r, x[2].r))
        return positions.index(smallest[2])

    p_left = sim_version(particles)

    particles_left = collisions(positions, velocities, accelerations)

    return len(particles_left), len(p_left)


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    # print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
