from utilities import timeit
from day12 import Process


def is_num(x):
    if x.lstrip('-').isdigit():
        return True
    return False


class Process(object):
    def __init__(self, instructions, a=7):
        self.registers = {'a' : a, 'b' : 0, 'c' : 0, 'd' : 0}
        self.lines = instructions.split('\n')
        self.index = 0
        self.o_line = 'iteration: {}, index: {}, registers: {}'

    def get_val(self, x):
        if is_num(x):
            return int(x)
        else:
            return self.registers[x]

    def process_line(self):
        line = self.lines[self.index]
        if len(line.split()) > 1:
            command, rest = line.split(' ', 1)
        else:
            return
        if command == 'cpy':
            first, second = rest.split(' ')
            first = self.get_val(first)
            if second in self.registers:
                self.registers[second] = first
        elif command == 'dec':
            if rest in self.registers:
                self.registers[rest] -= 1
        elif command == 'jnz':
            value, jump = map(self.get_val, rest.split())
            if value != 0:
                self.index += jump - 1
        elif command == 'tgl':
            jump = self.get_val(rest)
            new_index = self.index + jump
            if new_index > 0 and new_index < len(self.lines):
                self._toggle(new_index)
        elif command == 'inc':
            if self.index + 4 < len(self.lines):
                self._increment(rest)
            else:
                a = self.get_val(rest)
                if a in self.registers:
                    self.registers[a] += 1
        
        self.index += 1

    def _increment(self, a):
        # convert series of add/decrement loops to a multiplication
        if self.lines[self.index + 1].startswith('dec') and \
           self.lines[self.index + 2].startswith('jnz') and \
           self.lines[self.index + 3].startswith('dec') and \
           self.lines[self.index + 4].startswith('jnz') and \
           self.lines[self.index - 1].startswith('cpy'):

            copy_source, copy_dest = self.lines[self.index - 1].split()[1:]
            first_dec = self.lines[self.index + 1].split()[1]
            jump_cond_1, jump_dist_1 = self.lines[self.index + 2].split()[1:]
            second_dec = self.lines[self.index + 3].split()[1]
            jump_cond_2, jump_dist_2 = self.lines[self.index + 4].split()[1:]

            if copy_dest == first_dec and \
                first_dec == jump_cond_1 and second_dec == jump_cond_2 and \
                int(jump_dist_1) == -2 and int(jump_dist_2) == -5:

                update = self.get_val(copy_source) * self.get_val(second_dec)
                self.registers[a] += update # a = c * d
                self.registers[first_dec] = 0 # c <- 0
                self.registers[second_dec] = 0 # d <- 0
                self.index += 4 #skip loop
        else:
            self.registers[a] += 1

    def _toggle(self, index):
        line = self.lines[index]
        command, rest = line.split(' ', 1)


        if command == 'inc':
            new = 'dec ' + rest
        elif command == 'dec' or command == 'tgl':
            new = 'inc ' + rest
        elif command == 'jnz':
            new = 'cpy ' + rest
        elif command == 'cpy':
            new = 'jnz ' + rest
        else:
            return

        self.lines[index] = new

    def run(self):
        iterations = 0
        while self.index < len(self.lines):
            iterations += 1
            self.process_line()
            if iterations % 100000 == 0:
                print self.o_line.format(iterations, self.index, self.registers)



@timeit
def get_results(instructions, part2=False):
    test = Process(instructions)
    if part2:
        test.registers['a'] = 12
    test.run()
    for line in test.lines:
        print line
    return test.registers


if __name__ == '__main__':
    with open('instructions_day23.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)
