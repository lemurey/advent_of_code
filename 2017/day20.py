from aoc_utilities import get_instructions
from numpy import sqrt, arccos, arcsin, sin
from utilities import timeit
import os

class Anything:
    def __eq__(self, other):
        return True


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

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            for i, val in enumerate(self):
                self[i] = val + other
        else:
            for i, val in enumerate(self):
                self[i] = val + other[i]
        return self

    def __rmul__(self, other):
        return self * other

    def __mul__(self, other):
        out = Particle([0, 0, 0])
        if isinstance(other, float) or isinstance(other, int):
            for i, val in enumerate(self):
                out[i] = val * other
        else:
            for i, val in enumerate(self):
                out[i] = val * other[i]
        return out

    def __imul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            for i, val in enumerate(self):
                self[i] = val * other
        else:
            for i, val in enumerate(self):
                self[i] = val * other[i]
        return self

    def __sub__(self, other):
        out = Particle([0, 0, 0])
        for i, val in enumerate(self):
            out[i] = val * other[i]
        return out

    def __truediv__(self, other):
        out = Particle([0, 0, 0])
        if isinstance(other, float) or isinstance(other, int):
            for i, val in enumerate(self):
                out[i] = val / other
        else:
            for i, val in enumerate(self):
                out[i] = val / other[i]
        return out

    def __eq__(self, other):
        if not isinstance(other, Particle):
            return False
        for i, val in enumerate(self):
            if round(val - other[i], 5) != 0:
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
    return Particle(out)


def d(p):
    return sum(map(abs, p))


def collide(p1, v1, a1, p2, v2, a2):

    c = (p2 - p1)
    b = (v2 + a2 / 2) - (v1 + a1 / 2)
    a = (a2  - a1 ) / 2

    t1 = b ** 2 - 4 * a * c
    if t1 < 0:
        return False

    if a == 0:
        if v1== v2:
            if p1 == p2:
                return (0, Anything())
            else:
                return False
        return (abs(c) / abs(b), )
    t1 = sqrt(t1)
    o1 = (-1 * b + t1) / (2 * a)
    o2 = (-1 * b - t1)  / (2 * a)
    if o1 >= 0 and o2 < 0:
        return (o1, )
    if o2 >= 0 and o1 < 0:
        return (o2, )
    if o1 < 0 and o2 < 0:
        return False
    return (o1, o2)


def closest_particle(a, p, v):
    min_r = float('inf')
    closest_p = 0
    for i, acc in enumerate(a):
        update = False
        if acc.r < min_r:
            update = True
        elif acc.r == min_r:
            if v[closest_p].r > v[i].r:
                update = True
            elif v[closest_p].r == v[i].r:
                if p[closest_p].r > p[i].r:
                    update = True
        if update:
            min_r = acc.r
            closest_p = i

    return closest_p


def p_at_t(t, p, v, a):
    return p + v * t + a * (t * (t + 1) / 2)


def test_collisions(p1, v1, a1, p2, v2, a2):

    x, y, z = 0, 1, 2
    test_x = collide(p1[x], v1[x], a1[x], p2[x], v2[x], a2[x])
    test_y = collide(p1[y], v1[y], a1[y], p2[y], v2[y], a2[y])
    test_z = collide(p1[z], v1[z], a1[z], p2[z], v2[z], a2[z])
    if not test_x:
        return
    if not test_y:
        return
    if not test_z:
        return

    for x_time in test_x:
        for y_time in test_y:
            for z_time in test_z:
                if x_time == y_time and z_time == x_time:
                    if isinstance(x_time, Anything):
                        if isinstance(y_time, Anything):
                            if isinstance(z_time, Anything):
                                yield 0
                            else:
                                yield z_time
                        else:
                            yield y_time
                    else:
                        yield x_time


@timeit
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
        return closest_particle(accelerations, positions, velocities)

    iterations = 0

    t_val = 1000

    positions = positions[:t_val]
    velocities = velocities[:t_val]
    accelerations = accelerations[:t_val]

    particles = set(range(len(positions)))

    multi_way = 0

    for i in list(particles):
        for j in list(particles):
            if i == j:
                continue
            if (i not in particles) or (j not in particles):
                continue
            if iterations % 100 == 0:
                print('at iteration {} {} particles left'.format(iterations, len(particles)))
            p1, v1, a1 = positions[i], velocities[i], accelerations[i]
            p2, v2, a2 = positions[j], velocities[j], accelerations[j]
            remove_i = False
            remove_j = False
            for time in test_collisions(p1, v1, a1, p2, v2, a2):
                check1 = p_at_t(time, p1, v1, a1)
                check2 = p_at_t(time, p2, v2, a2)
                if check1 == check2:
                    remove_i = True
                    remove_j = True
                for k in list(particles):
                    if k not in particles:
                        continue
                    iterations += 1
                    if k == i or k == j:
                        continue
                    p3, v3, a3 = positions[k], velocities[k], accelerations[k]
                    check3 = p_at_t(time, p3, v3, a3)
                    if check1 == check3:
                        multi_way += 1
                        particles.remove(k)
                        remove_i = True
                    if check2 == check3:
                        if k in particles:
                            particles.remove(k)
                            multi_way += 1
                        remove_j = True

            if remove_i:
                if i in particles:
                    particles.remove(i)
            if remove_j:
                if j in particles:
                    particles.remove(j)

    print(iterations)
    return len(particles)


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
