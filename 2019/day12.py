from aoc_utilities import get_instructions
import os
from math import gcd


class Moon:
    def __init__(self, name, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.name = name
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def step(self):
        for axis, v in zip('xyz', (self.vx, self.vy, self.vz)):
            setattr(self, axis, getattr(self, axis) + v)

    def energy(self):
        return self._kinetic() * self._potential()

    def _potential(self):
        return sum(map(abs, (self.x, self.y, self.z)))

    def _kinetic(self):
        return sum(map(abs, (self.vx, self.vy, self.vz)))

    def __hash__(self):
        return hash((self.name, self.x, self.y, self.z, self.vx, self.vy,
                     self.vz))

    def __eq__(self, other):
        return (self.name == other.name and
                self.x == other.x and
                self.y == other.y and
                self.z == other.z and
                self.vx == other.vx and
                self.vy == other.vy and
                self.vz == other.vz)

    def __str__(self):
        e = self.energy()
        return (f'pos=<x={self.x:3}, y={self.y:3} z={self.z:3}>, '
                f'vel=<x={self.vx:3}, y={self.vy:3} z={self.vz:3}>'
                f'\nEnergy: {e}'
                )

    def __repr__(self):
        return (f'({self.x}, {self.y}, {self.z}, {self.vz}'
                f', {self.vy}, {self.vz})')


def gravity(moons):
    for i, moon1 in enumerate(moons):
        for moon2 in moons[i:]:
            if moon1.name == moon2.name:
                continue
            for axis in 'xyz':
                p1 = getattr(moon1, axis)
                p2 = getattr(moon2, axis)

                v1 = getattr(moon1, 'v{}'.format(axis))
                v2 = getattr(moon2, 'v{}'.format(axis))
                if p1 < p2:
                    setattr(moon1, 'v{}'.format(axis), v1 + 1)
                    setattr(moon2, 'v{}'.format(axis), v2 - 1)
                elif p1 > p2:
                    setattr(moon1, 'v{}'.format(axis), v1 - 1)
                    setattr(moon2, 'v{}'.format(axis), v2 + 1)


def step(moons):
    gravity(moons)
    for moon in moons:
        moon.step()


def energy(moons):
    total = 0
    for moon in moons:
        total += moon.energy()
    return total


def parse(data):
    moons = []
    for name, line in zip(('Io', 'Europa', 'Ganymede', 'Callisto'), data):
        line = line.strip('<>')
        x, y, z = [int(x.split('=')[1]) for x in line.split(', ')]
        moons.append(Moon(name, x, y, z))

    return moons


def log(moons, history, cycles_found, t):
    for axis in 'xyz':
        val = []
        for moon in moons:
            p = getattr(moon, axis)
            v = getattr(moon, 'v{}'.format(axis))
            val.extend([p, v])
        val = tuple(val)
        if val in history[axis]:
            if not cycles_found[axis]:
                cycles_found[axis] = t
        history[axis].add(val)


def check_found(cycles_found):
    for axis in cycles_found:
        if not cycles_found[axis]:
            break
    else:
        return False
    return True


def lcm(*args):
    def _lcm(x, y): return (x * y) // gcd(x, y)
    val = args[0]
    for v in args[1:]:
        val = int(_lcm(val, v))
    return val


def get_answer(data, part2=False):
    moons = parse(data)
    if part2:
        history = {'x': set(),
                   'y': set(),
                   'z': set()}
        t = 0
        cycles_found = {'x': False,
                        'y': False,
                        'z': False}

        while check_found(cycles_found):
            log(moons, history, cycles_found, t)
            step(moons)
            t += 1
            if t % 10000 == 0:
                print(cycles_found, t)
        return lcm(*cycles_found.values())

    for _ in range(1000):
        step(moons)
    return energy(moons)


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
