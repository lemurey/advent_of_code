ID_NUM = 1


class Intcode():
    def __init__(self, program, input=ID_NUM, sep='|',
                 secondary=0, mode='single', parent=None,
                 indicator=None):
        self.program = program
        self.program += [0] * 10000
        self.input = input
        self.output_func = lambda x: print('{}{}'.format(x, self.sep), end='')
        if mode == 'debug':
            self.output_func = print
        self.orig = [x for x in program]
        self.sep = sep
        self.secondary = secondary
        self.mode = mode
        self.parent = parent
        self.indicator = indicator
        self.first = True
        self.cur_ind = 0
        self.relative_base = 0
        self.halted = False

        self.OPS = {
            1: self.__add,
            2: self.__mul,
            3: self.__input,
            4: self.__output,
            5: self.__jit,
            6: self.__jif,
            7: self.__lt,
            8: self.__eq,
            9: self.__adj_rel,
            99: self.__halt,
        }

        self.arg_details = {
            1: (None, None, 'write'),
            2: (None, None, 'write'),
            3: ('write', ),
            4: (None, ),
            5: (None, None),
            6: (None, None),
            7: (None, None, 'write'),
            8: (None, None, 'write'),
            9: (None, ),
            99: [],
        }

    def parse_opcode(self, val):
        c = '{:0>5}'.format(val)
        return [int(x) for x in (c[3:], c[2], c[1], c[0])]

    def step(self):
        opcode, *modes = self.parse_opcode(self.program[self.cur_ind])

        if opcode not in self.OPS:
            raise ValueError('invalid opcode: {}'.format(opcode))

        op = self.OPS[opcode]
        details = self.arg_details[opcode]
        self._call_op(op, modes, details)

    def run(self):
        while not self.halted:
            self.step()

    def _call_op(self, op, modes, details):
        saved_index = self.cur_ind

        raw_args = []
        arguments = []
        for offset, (mode, d) in enumerate(zip(modes, details)):
            raw_arg = self.program[self.cur_ind + offset + 1]
            arg = self._get_values(raw_arg, mode, d)
            raw_args.append(raw_arg)
            arguments.append(arg)

        self._print_op(op, raw_args, arguments, modes)
        op(*arguments)

        if self.cur_ind == saved_index:
            self.cur_ind += len(details) + 1

    def _get_values(self, c_val, mode, d):
        if mode == 0:
            if d == 'write':
                return c_val
            return self.program[c_val]
        elif mode == 1:
            return c_val
        elif mode == 2:
            if d == 'write':
                return c_val + self.relative_base
            return self.program[c_val + self.relative_base]

    def _print_op(self, op, raw, vals, modes):
        if self.mode != 'debug':
            return
        name = op.__name__[2:].upper()
        arg_strings = []
        for raw, mode in zip(raw, modes):
            if mode == 0:
                arg_strings.append(f'[{raw:4}]')
            elif mode == 1:
                arg_strings.append(f'{raw:6}')
            elif mode == 2:
                arg_strings.append(f'@{raw:<+4}')

        val_strings = [f'{v}' for v in vals]

        arg_disp = ' '.join(arg_strings)
        val_disp = ' '.join(val_strings)

        print(f'{self.cur_ind:4}: {name:4} {arg_disp} + ({val_disp})')

    # Ops
    def __halt(self):
        self.halted = True

    def __add(self, a1, a2, o):
        self.program[o] = a1 + a2

    def __mul(self, a1, a2, o):
        self.program[o] = a1 * a2

    def __input(self, o):
        if self.first:
            val = self.input
            self.first = False
        else:
            val = self.secondary
        self.program[o] = val

    def __output(self, a1):
        self.output_val = a1
        self.output_func(a1)

    def __jit(self, a1, a2):
        if a1 != 0:
            self.cur_ind = a2

    def __jif(self, a1, a2):
        if a1 == 0:
            self.cur_ind = a2

    def __lt(self, a1, a2, o):
        if a1 < a2:
            self.program[o] = 1
        else:
            self.program[o] = 0

    def __eq(self, a1, a2, o):
        if a1 == a2:
            self.program[o] = 1
        else:
            self.program[o] = 0

    def __adj_rel(self, a1):
        self.relative_base += a1
