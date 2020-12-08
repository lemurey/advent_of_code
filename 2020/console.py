class Console:
    def __init__(self, instructions):
        self.accumulator = 0
        self.run_instructions = set()
        self.instructions = []
        self._lookups = {
            'nop': self.nop,
            'jmp': self.jmp,
            'acc': self.acc,
                         }
        self._reverse_lookups = {
            self.nop: 'nop',
            self.jmp: 'jmp',
            self.acc: 'acc',
                                }

        self.parse_instructions(instructions)
        self.index = 0
        self.max_instruction = len(self.instructions)

        self.backup = self.instructions[:]

    def parse_instructions(self, instructions):
        for row in instructions:
            cmd, val = row.split()
            val = int(val)
            self.instructions.append((self._lookups[cmd], val))

    def jmp(self, val):
        self.index += val

    def nop(self, val):
        self.index += 1

    def acc(self, val):
        self.accumulator += val
        self.index += 1

    def reset(self):
        self.instructions = self.backup[:]
        self.index = 0
        self.accumulator = 0
        self.run_instructions = set()

    def run(self):
        while True:
            if self.index >= self.max_instruction:
                self.log = 'no infinite loop'
                return self.accumulator

            next_op, val = self.instructions[self.index]

            if self.index in self.run_instructions:
                self.log = 'infinite loop'
                return self.accumulator

            self.run_instructions.add(self.index)
            next_op(val)

    def __str__(self):
        out = ''
        for op, val in self.instructions:
            out += f'{self._reverse_lookups[op]}: {val}\n'
        return out
