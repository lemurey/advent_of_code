from utilities import timeit

class Process(object):
    def __init__(self):
        self.registers = {'a' : 0, 'b' : 0}
        self.index = 0
        self.instructions = []
        self.commands = {'inc' : self._inc,
                         'hlf' : self._hlf,
                         'tpl' : self._tpl,
                         'jmp' : self._jmp,
                         'jie' : self._jie,
                         'jio' : self._jio}

    def read_program(self, lines):
        for line in lines.split('\n'):
            cmd, rest = line.split(' ', 1)
            if cmd in ['jio', 'jie']:
                r, o = rest.split(', ')
                o = int(o)
            elif cmd == 'jmp':
                r = ''
                o = int(rest)
            else:
                r = rest
                o = 0
            self.instructions.append((cmd, r, o))

    def _inc(self, register, **kwargs):
        self.registers[register] += 1

    def _hlf(self, register, **kwargs):
        self.registers[register] /= 2

    def _tpl(self, register, **kwargs):
        self.registers[register] *= 3

    def _jmp(self, offset, **kwargs):
        self.index += offset - 1

    def _jie(self, register, offset):
        if self.registers[register] % 2 == 0:
            self._jmp(offset)

    def _jio(self, register, offset):
        if self.registers[register] == 1:
            self._jmp(offset)

    def run(self):
        while self.index < len(self.instructions):
            cmd, r, o = self.instructions[self.index]
            self.commands[cmd](register=r, offset=o)
            self.index += 1


@timeit
def get_results(instructions, part2=False):
    computer = Process()
    computer.read_program(instructions)
    if part2:
        computer.registers['a'] = 1
    computer.run()
    return computer.registers['b']


if __name__ == '__main__':
    with open('instructions_day23.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)
