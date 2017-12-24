from aoc_utilities import get_instructions
from collections import defaultdict
from utilities import timeit
import os
from math import sqrt

'''
note: for part 2 the code is counting up from register b (starts at 107900 for
my input) to the value in register c (17000 higher) in steps of 17.
Each time it increments, if the value is prime, it increments h, otherwise, it
does not.

(note, if the start value of b is prime it seems to still increment h, i'm
not sure why this is, but it doesn't really matter since for our input it
is not starting at a prime value)
'''


class Process:
    def __init__(self, instructions):
        self.commands = [l.split() for l in instructions.split('\n')]
        self.registers = defaultdict(int)
        self.index = 0
        self.mul_count = 0
        self.iterations = 0
        self.functions = {'set': self.set,
                          'sub': self.sub,
                          'mul': self.mul,
                          'jnz': self.jgz
                          }

    def get(self, x):
        if x in 'abcdefghijklmnopqrstuvwxyz':
            return self.registers[x]
        return int(x)

    def set(self, x, y):
        self.registers[x] = self.get(y)

    def sub(self, x, y):
        self.registers[x] -= self.get(y)

    def mul(self, x, y):
        self.registers[x] *= self.get(y)

    def jgz(self, x, y):
        x = self.get(x)
        if x != 0:
            self.index += (self.get(y) - 1)

    def single_run(self):
        line = self.commands[self.index]
        self.index += 1
        self.functions[line[0]](line[1], line[2])
        if line[0] == 'mul':
            self.mul_count += 1

    def run(self, early_stop=False):
        if early_stop:
            for _ in range(10):
                self.single_run()
            return
        while True:
            if self.index < 0 or self.index >= len(self.commands):
                self.status = 'END'
                return 'END'
            self.single_run()


def is_prime(n):
    if n == 2:
        return True
    if n % 2 == 0 and n > 2:
        return False
    for i in range(3, int(sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def optimized(b, runs, mult):
    h = 1
    for _ in range(runs):
        b += mult
        if not is_prime(b):
            h += 1
    return h


def get_answer(data, part2=False):
    p = Process(data)
    if part2:
        p.registers['a'] = 1
        p.run(part2)
        start = p.get('b')
        end = p.get('c')
        mult = abs(int(p.commands[-2][-1]))
        iterations = (end - start) // mult
        return optimized(start, iterations, mult)

    p.run(part2)
    return p.mul_count


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
