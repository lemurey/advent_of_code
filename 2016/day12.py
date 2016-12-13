class Process(object):
    def __init__(self, instructions, second_run = False, return_register='a'):
        self.lines = instructions.split('\n')
        self.lines.append('END')
        self.registers = {}
        if second_run:
            self.registers['c'] = 1
        self.return_register = return_register
        self.index = 0
        self.iteration = 0
        self.running = True
        self.o = 'at iteration {}, index is {}'

    def process_line(self, line):
        self.iteration += 1
        if self.iteration % 100000 == 0:
            print self.o.format(self.iteration, self.index)
        if line == 'END':
            return self.registers[self.return_register]
        elif line[2] == 'c':
            command, register = line.split()
            self._change_value(command, register)
        elif line[0] == 'c':
            _, value, register = line.split()
            self._copy_value(value, register)
        else:
            _, value, jump = line.split()
            self._jump(value, jump)

    def run(self):
        while self.running:
            val = self.process_line(self.lines[self.index])
            if val:
                return val

    def _change_value(self, command, register):
        if command[0] == 'i':
            self.registers[register] += 1
        else:
            self.registers[register] -= 1
        self.index += 1

    def _copy_value(self, value, register):
        if value.strip().isdigit():
            result = int(value)
        else:
            result = self.registers[value.strip()]
        self.registers[register] = result
        self.index += 1

    def _jump(self, value, jump):
        if value.strip().isdigit():
            result = int(value)
        else:
            if value.strip() in self.registers:
                result = self.registers[value.strip()]
            else:
                result = 0
        if result == 0:
            self.index += 1
        else:
            self.index += int(jump)


def get_results(instructions):
    test = Process(instructions)
    print test.run()
    test2 = Process(instructions, second_run=True)
    print test2.run()


if __name__ == '__main__':
    with open('instructions_day12.txt', 'r') as f:
        instructions = f.read().strip()
    get_results(instructions)