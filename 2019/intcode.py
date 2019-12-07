ID_NUM = 1

class Intcode():
    def __init__(self, program, input=ID_NUM, sep='|',
                 secondary=0, mode='single', parent=None,
                 indicator=None):
        self.program = program
        self.input = input
        self.orig = [x for x in self.program]
        self.sep = sep
        self.secondary = secondary
        self.mode = mode
        self.parent = parent
        self.indicator = indicator
        self.first = True
        self.cur_ind = 0

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
        if self.first:
            val = self.input
            self.first = False
        else:
            val = self.secondary
        self.program[loc] = val

    def code_04(self, index, mode1, mode2, mode3):
        loc = self._get_values(self.program[index + 1], mode1)
        self.output_val = loc
        return loc
        # print('{}{}'.format(loc, self.sep), end='')

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
        while True:
            which = self.program[self.cur_ind]
            mode3, mode2, mode1, op = self.parse_opcode(which)

            if op == 1:
                self.code_01(self.cur_ind, mode1, mode2, mode3)
                advance = 4
            elif op == 2:
                self.code_02(self.cur_ind, mode1, mode2, mode3)
                advance = 4
            elif op == 3:
                self.code_03(self.cur_ind, mode1, mode2, mode3)
                advance = 2
            elif op == 4:
                val = self.code_04(self.cur_ind, mode1, mode2, mode3)
                advance = 2
                if self.mode != 'single':
                    self.cur_ind += advance
                    return val
            elif op == 5:
                advance = self.code_05(self.cur_ind, mode1, mode2, mode3)
            elif op == 6:
                advance = self.code_06(self.cur_ind, mode1, mode2, mode3)
            elif op == 7:
                self.code_07(self.cur_ind, mode1, mode2, mode3)
                advance = 4
            elif op == 8:
                self.code_08(self.cur_ind, mode1, mode2, mode3)
                advance = 4
            elif op == 99:
                # print()
                if self.mode != 'single':
                    self.parent.final[self.indicator] = True
                return self.output_val
            else:
                raise ValueError('incorrect value')
            self.cur_ind += advance

    def reset(self, noun, verb):
        self.program = [x for x in self.orig]
        self.program[1] = noun
        self.program[2] = verb