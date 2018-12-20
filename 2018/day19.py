from aoc_utilities import get_instructions
import os
from utilities import timeit
from day16 import OPR

class OPR2(OPR):
    def __init__(self, ip, num_registers=6):
        super(OPR2, self).__init__(num_registers)
        self.ip = ip
        self.ip_num = 0

    def run_command(self, op, a, b, c, debug):
        self.registers[self.ip] = self.ip_num
        if debug:
            p_reg = [x for x in self.registers]
        else:
            p_reg = []
        f = self.op_map[op]
        f(a, b, c)
        self.ip_num = self.registers[self.ip]
        self.ip_num += 1
        return p_reg

    def _run_program(self, codes, f=None):
        o_s = 'ip={} {} {} {} {} {} {}\n'
        while True:
            ind = self.ip_num
            if 0 <= ind < len(codes):
                op, a, b, c = codes[ind]
            else:
                return
            p_reg = self.run_command(op, a, b, c, debug=True)
            if f is not None:
                f.write(o_s.format(self.ip_num, p_reg,
                        op, a, b, c, self.registers))

    def run_program(self, codes, debug=False):
        if debug:
            with open('day19_debug.log', 'w') as f:
                self._run_program(codes, f)
        else:
            self._run_program(codes)

def process_codes(data):
    program = []
    for line in data:
        if line.startswith('#'):
            _, ip = line.split()
            ip = int(ip)
        else:
            op, a, b, c = line.split()
            program.append([op] + map(int, (a, b, c)))
    return ip, program


def factors(n):
    f = []
    for i in range(1, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            f.extend((i, n / i))
    return f


def my_decompiled(n):
    return sum(factors(n))


def get_answer(data, part2=False):
    if part2:
        n = 10551345
    else:
        n = 945
    return my_decompiled(n)


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])

    sample = '''#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5'''.split('\n')
    # get_answer(sample)
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))