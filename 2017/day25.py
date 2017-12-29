from aoc_utilities import get_instructions
from collections import deque
import os


class TuringMachine:
    def __init__(self, rules, state):
        self.tape = deque([0])
        self.index = 0
        self.end = 0
        self.steps = 0
        self.state = state
        self.rules = rules

    def run(self, checksum):
        while self.steps < checksum:
            current_value = self.tape[self.index]
            write, step, state = self.rules[self.state][current_value]
            self.tape[self.index] = write
            self.index += step
            self.state = state
            if self.index > self.end:
                self.tape.append(0)
                self.end += 1
            elif self.index < 0:
                self.tape.appendleft(0)
                self.index = 0

            self.steps += 1


def parse_rules(data):
    rules = {}
    state = None
    for i, line in enumerate(data.split('\n')):
        if i == 0:
            start_state = line[-2]
            continue
        if i == 1:
            checksum = int(line.split()[-2])
            continue
        if line == '':
            if state is not None:
                rules[state] = tuple(tuple(x) for x in cur_rules)
            continue
        if line[0] != ' ':
            state = line[-2]
            cur_rules = [[0, 0, 0], [0, 0, 0]]
        elif line[-1] == ':':
            place = int(line[-2])
            index = 0
        else:
            if line[-2].isdigit():
                value = int(line[-2])
            elif line[-2].isupper():
                value = line[-2]
            else:
                if line[-6:-1] == 'right':
                    value = 1
                else:
                    value = -1
            cur_rules[place][index] = value
            index += 1
    rules[state] = tuple(tuple(x) for x in cur_rules)

    return start_state, rules, checksum


def get_answer(data, part2=False):
    state, rules, checksum = parse_rules(data)
    tm = TuringMachine(rules, state)
    tm.run(checksum)
    return sum(tm.tape)


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
#     inputs = '''Begin in state A.
# Perform a diagnostic checksum after 6 steps.

# In state A:
#   If the current value is 0:
#     - Write the value 1.
#     - Move one slot to the right.
#     - Continue with state B.
#   If the current value is 1:
#     - Write the value 0.
#     - Move one slot to the left.
#     - Continue with state B.

# In state B:
#   If the current value is 0:
#     - Write the value 1.
#     - Move one slot to the left.
#     - Continue with state A.
#   If the current value is 1:
#     - Write the value 1.
#     - Move one slot to the right.
#     - Continue with state A.'''
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
