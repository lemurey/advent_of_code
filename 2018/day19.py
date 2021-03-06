from aoc_utilities import get_instructions
import os
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

    def _run_program(self, codes, f=None, early_stop=None):
        o_s = 'ip={} {} {} {} {} {} {}\n'
        count = 0
        if early_stop is not None:
            cond = lambda x: x < early_stop
        else:
            cond = lambda x: True
        while cond(count):
            count += 1
            ind = self.ip_num
            if 0 <= ind < len(codes):
                op, a, b, c = codes[ind]
            else:
                return
            p_reg = self.run_command(op, a, b, c, debug=True)
            if f is not None:
                f.write(o_s.format(self.ip_num, p_reg,
                        op, a, b, c, self.registers))
        self.count = count

    def run_program(self, codes, debug=False, early_stop=None, day=19):
        if debug:
            with open('day{}_debug.log'.format(day), 'a') as f:
                self._run_program(codes, f, early_stop=early_stop)
        else:
            self._run_program(codes, early_stop=early_stop)

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
    ip, program = process_codes(data)
    r = OPR2(ip)
    if part2:
        r.registers[0] = 1
    r.run_program(program, debug=True, early_stop=20)
    n = r.registers[5]
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