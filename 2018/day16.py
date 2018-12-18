from aoc_utilities import get_instructions
import os


class OPR(object):
    def __init__(self):
        self.registers = [0, 0, 0, 0]
        self.op_list = (self.addr, self.addi, self.mulr, self.muli, self.banr,
                        self.bani, self.borr, self.bori, self.setr, self.seti,
                        self.gtir, self.gtri, self.gtrr, self.eqir, self.eqri,
                        self.eqrr)
        self.op_map = {f.__name__: f for f in self.op_list}

    def set_registers(self, reg):
        if len(reg) != 4:
            raise ValueError('register must have 4 entries')
        self.registers = reg[:]

    def run_check(self, br, inputs, ar, debug=False):
        c = {}
        for f in self.op_list:
            self.set_registers(br)
            f(*inputs[1:])
            if self.registers == ar:
                c[f.__name__] = inputs[0]
        if debug:
            return c
        return len(c.keys())

    def run_program(self, codes, mappings):
        for op, a, b, c in codes:
            f = self.op_map[mappings[op]]
            f(a, b, c)
        return self.registers[0]

    def check_ops(self, br, inputs, ar):
        op = False
        for f in self.op_list:
            self.set_registers(br)
            f(*inputs[1:])
            mod_reg = inputs[-1]
            comp = [x == y for x, y in zip(br, self.registers)]

            if sum(comp) < 3:
                print (f.__name__, br, inputs, ar, self.registers, 'total')
                op = True
            if any([not c for i, c in enumerate(comp) if i != mod_reg]):
                print (f.__name__, br, inputs, ar, self.registers, 'location')
                op = True
        if op:
            print '-' * 15

    def addr(self, a, b, c):
        self.registers[c] = self.registers[a] + self.registers[b]

    def addi(self, a, b, c):
        self.registers[c] = self.registers[a] + b

    def mulr(self, a, b, c):
        self.registers[c] = self.registers[a] * self.registers[b]

    def muli(self, a, b, c):
        self.registers[c] = self.registers[a] * b

    def banr(self, a, b, c):
        self.registers[c] = self.registers[a] & self.registers[b]

    def bani(self, a, b, c):
        self.registers[c] = self.registers[a] & b

    def borr(self, a, b, c):
        self.registers[c] = self.registers[a] | self.registers[b]

    def bori(self, a, b, c):
        self.registers[c] = self.registers[a] | b

    def setr(self, a, b, c):
        self.registers[c] = self.registers[a]

    def seti(self, a, b, c):
        self.registers[c] = a

    def gtir(self, a, b, c):
        if a > self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0
        # self.registers[c] = int(a > self.registers[b])

    def gtri(self, a, b, c):
        if self.registers[a] > b:
            self.registers[c] = 1
        else:
            self.registers[c] = 0
        # self.registers[c] = int(self.registers[a] > b)

    def gtrr(self, a, b, c):
        if self.registers[a] > self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0
        # self.registers[c] = int(self.registers[a] > self.registers[b])

    def eqir(self, a, b, c):
        if a == self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0
        # self.registers[c] = int(a == self.registers[b])

    def eqri(self, a, b, c):
        if self.registers[a] == b:
            self.registers[c] = 1
        else:
            self.registers[c] = 0
        # self.registers[c] = int(self.registers[a] == b)

    def eqrr(self, a, b, c):
        if self.registers[a] == self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0
        # self.registers[c] = int(self.registers[a] == self.registers[b])


def process_data(data):
    reg_checks = []
    test_code = []

    for line in data:
        if line.startswith('Before'):
            i = 0
            _, regs = line.split('Before: ')
            r1 = map(int, regs.strip('[]').split(', '))
        elif line.startswith('After'):
            i = 2
            _, regs = line.split('After:  ')
            r2 = map(int, regs.strip('[]').split(', '))
        elif i == 0:
            i = 1
            inputs = map(int, line.split())
        elif i == 2:
            reg_checks.append((r1, inputs, r2))
            i = 1
        elif line == '':
            i = 3
        elif i == 3:
            test_code.append(map(int, line.split()))

    return reg_checks, test_code


def sum_at_least_3(checks):
    r = OPR()
    c = 0
    for br, inputs, ar in checks[:]:
        v = r.run_check(br, inputs, ar)
        if v >= 3:
            c += 1
    return c


def id_codes(checks):
    r = OPR()
    d = {}
    for br, inputs, ar in checks[:]:
        u = r.run_check(br, inputs, ar, debug=True)
        for k, v in u.items():
            if k not in d:
                d[k] = set()
            d[k].add(v)

    mappings = {}

    while len(mappings) < 16:
        copy = {k: v for k, v in d.items()}
        for k, v in copy.items():
            if len(v) == 1:
                val = list(v)[0]
                mappings[val] = k
                for k1 in copy:
                    if val in d[k1]:
                        d[k1].remove(val)
                break

    return mappings

def get_answer(data, part2=False):
    # r = OPR()
    # print r.run_check([3, 2, 1, 1], [9, 2, 1, 2], [3, 2, 2, 1], debug=True)

    checks, test = process_data(data)

    if part2:
        mapping = id_codes(checks)
        r = OPR()
        return r.run_program(test, mapping)
    return sum_at_least_3(checks)


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))