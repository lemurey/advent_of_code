from aoc_utilities import get_instructions
from pathlib import Path


class Comp:
    def __init__(self, A, B, C, instr):
        self.A = A
        self.B = B
        self.C = C
        self.instr = instr
        self.codes = {0: self.adv, 1: self.bxl, 2: self.bst, 3: self.jnz, 
                      4: self.bxc, 5: self.out, 6: self.bdv , 7: self.cdv}
        self.pointer = 0
        self.output = []

    def combo(self, operand):
        if operand <= 3:
            return operand
        elif operand == 4:
            return self.A
        elif operand == 5:
            return self.B
        elif operand == 6:
            return self.C
        else:
            raise ValueError(f'cannot use combo 7 in valid programs')

    def adv(self, operand):
        self.A = self.A // (2 ** self.combo(operand))
        self.pointer += 2

    def bxl(self, operand):
        self.B = self.B ^ operand
        self.pointer += 2

    def bst(self, operand):
        self.B = self.combo(operand) % 8
        self.pointer += 2

    def jnz(self, operand):
        if self.A == 0:
            self.pointer += 2
            return
        self.pointer = operand

    def bxc(self, operand):
         self.B = self.C ^ self.B
         self.pointer += 2

    def out(self, operand):
        self.output.append(self.combo(operand)%8)
        self.pointer += 2

    def bdv(self, operand):
        self.B = int(self.A / 2 ** self.combo(operand))
        self.pointer += 2

    def cdv(self, operand):
        self.C = int(self.A / 2 ** self.combo(operand))
        self.pointer += 2

    def run(self, verbose=False):
        # reset output and pointer
        self.output = []
        self.pointer = 0

        c = 0
        while self.pointer in range(len(self.instr)):
            c += 1
            if c % 1000 == 0:
                print(f'{c}: {self.output}, {(self.A, self.B, self.C)}, {self.pointer}')
            if c > 100000:
                return

            op = self.instr[self.pointer]
            operand = self.instr[self.pointer + 1]
            if verbose:
                print(f'{op}, {operand}', end=',')
            self.codes[op](operand)
            if verbose:
                print(f'{self.output}, {(self.A, self.B, self.C)}, {self.pointer}')
        return self.output


def run_with(comp, val):
    comp.A = val
    comp.B = 0
    comp.C = 0
    return ','.join(map(str, comp.run(verbose=False)))


def get_answer(data, part2=False):
    for row in data:
        if row == '':
            continue
        vals = row.split(': ')[1]
        if 'A:' in row:
            A = int(vals)
        elif 'B:' in row:
            B = int(vals)
        elif 'C:' in row:
            C = int(vals)
        else:
            instructions = list(map(int, vals.split(',')))

    comp = Comp(A, B, C, instructions)
    if part2:
        # each time you add a number to output a needs to go up by a
        # factor of 8
        # so going from right to left, match outputs, then go up a factor of 8
        # and do it again
        check_seq = '2,4,1,7,7,5,4,1,1,4,5,5,0,3,3,0'
        checks = [0]
        for ol in range(1, 33, 2):
            prev_checks = checks
            checks = []
            for num in prev_checks:
                for offset in range(8):
                    val = 8*num + offset
                    check = run_with(comp, val)
                    if check == check_seq[-ol:]:
                        print(val, check)
                        checks.append(val)
        return min(checks)

    else:
        return ','.join(map(str, comp.run(verbose=True)))


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''Register A: 729
# Register B: 0
# Register C: 0

# Program: 0,1,5,4,3,0'''.split('\n')
    # print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
