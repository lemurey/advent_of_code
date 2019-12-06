from aoc_utilities import get_instructions
import os

ID_NUM = 1

class Intcode():
    def __init__(self, program, input=ID_NUM, sep='|'):
        self.program = program
        self.input = input
        self.orig = [x for x in self.program]
        self.sep = sep

    def _get_values(self, c_val, mode):
        if mode == 0:
            return self.program[c_val]
        elif mode == 1:
            return c_val


    def code_01(self, index, mode1, mode2, mode3):
        a = self._get_values(self.program[index + 1], mode1)
        b = self._get_values(self.program[index + 2], mode2)
        c = self.program[index + 3]

        self.program[c] = a + b

    def code_02(self, index, mode1, mode2, mode3):
        a = self._get_values(self.program[index + 1], mode1)
        b = self._get_values(self.program[index + 2], mode2)
        c = self.program[index + 3]
        self.program[c] = a * b

    def code_03(self, index, mode1, mode2, mode3):
        loc = self.program[index + 1]
        val = self.input
        self.program[loc] = val

    def code_04(self, index, mode1, mode2, mode3):
        loc = self._get_values(self.program[index + 1], mode1)
        print('{}{}'.format(loc, self.sep), end='')

    def code_05(self, index, mode1, mode2, mode3):
        a = self._get_values(self.program[index + 1], mode1)
        b = self._get_values(self.program[index + 2], mode2)
        if a != 0:
            return b - index
        return 3

    def code_06(self, index, mode1, mode2, mode3):
        a = self._get_values(self.program[index + 1], mode1)
        b = self._get_values(self.program[index + 2], mode2)
        if a == 0:
            return b - index
        return 3

    def code_07(self, index, mode1, mode2, mode3):
        a = self._get_values(self.program[index + 1], mode1)
        b = self._get_values(self.program[index + 2], mode2)
        c = self.program[index + 3]
        if a < b:
            self.program[c] = 1
        else:
            self.program[c] = 0

    def code_08(self, index, mode1, mode2, mode3):
        a = self._get_values(self.program[index + 1], mode1)
        b = self._get_values(self.program[index + 2], mode2)
        c = self.program[index + 3]
        if a == b:
            self.program[c] = 1
        else:
            self.program[c] = 0

    def parse_opcode(self, val):
        c = '{:0>5}'.format(val)
        return [int(x) for x in (c[0], c[1], c[2], c[3:])]

    def run(self):
        cur_ind = 0
        while True:
            which = self.program[cur_ind]
            mode3, mode2, mode1, op = self.parse_opcode(which)

            if op == 1:
                self.code_01(cur_ind, mode1, mode2, mode3)
                advance = 4
            elif op == 2:
                self.code_02(cur_ind, mode1, mode2, mode3)
                advance = 4
            elif op == 3:
                self.code_03(cur_ind, mode1, mode2, mode3)
                advance = 2
            elif op == 4:
                self.code_04(cur_ind, mode1, mode2, mode3)
                advance = 2
            elif op == 5:
                advance = self.code_05(cur_ind, mode1, mode2, mode3)
            elif op == 6:
                advance = self.code_06(cur_ind, mode1, mode2, mode3)
            elif op == 7:
                self.code_07(cur_ind, mode1, mode2, mode3)
                advance = 4
            elif op == 8:
                self.code_08(cur_ind, mode1, mode2, mode3)
                advance = 4
            elif op == 99:
                print()
                return
            else:
                raise ValueError('incorrect value')
            cur_ind += advance

    def reset(self, noun, verb):
        self.program = [x for x in self.orig]
        self.program[1] = noun
        self.program[2] = verb


def parse_inputs(data):
    return list(map(int, data[0].split(',')))


def get_answer(data, part2=False):
    program = parse_inputs(data)
    if part2:
        comp = Intcode(program, input=5)
    else:
        comp = Intcode(program)
    comp.run()


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
