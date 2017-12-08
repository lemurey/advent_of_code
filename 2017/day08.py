from aoc_utilities import get_instructions
from operator import add, sub, lt, le, eq, ne, ge, gt
import os

OPERATIONS = {'>': gt,
              '<': lt,
              '<=': le,
              '>=': ge,
              '==': eq,
              '!=': ne,
              'inc': add,
              'dec': sub}

def parse_instructions(instruction):
    register, operand, value = instruction.split()
    return register, OPERATIONS[operand], int(value)


def get_answer(data, part2=False):
    registers = {}
    max_val = 0
    for line in data.split('\n'):
        operand, condition = line.split(' if ')
        register, function, value = parse_instructions(operand)
        check, comparison, value_check = parse_instructions(condition)
        if register not in registers:
            registers[register] = 0
        if check not in registers:
            registers[check] = 0

        if comparison(registers[check], value_check):
            temp = function(registers[register], value)
            if temp > max_val:
                max_val = temp
            registers[register] = temp

    if part2:
        return max_val
    return max(registers.values())


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
