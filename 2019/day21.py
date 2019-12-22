from aoc_utilities import get_instructions
import os
from intcode import Intcode


def to_ascii(string):
        if not string.endswith('\n'):
            string += '\n'
        vals = []
        for char in string:
            vals.append(ord(char))
        return vals


def check_output(core):
    while True:
        core.waiting = False
        val = core.run()
        if val < 0 or val > 128:
            print(val)
            return
        else:
            print(chr(val), end='')
        if chr(val) in (':', '?'):
            return


def get_answer(data, part2=False):
    '''
    A: ground 1 tile away
    B: ground 2 tiles away
    C: ground 3 tiles away
    D: ground 4 tiles away

    jumps 4 spaces,
    so if there is ground 4 away and any holes in the next 3, jump
    THIS IS PART 1

    (!A OR !B OR !C) AND D
    NOT A T  #temp register is T if hole at 1
    NOT B J  #jump register is T if hole at 2
    OR T J   #jump register is T if hole at 1 or 2
    NOT C T  #temp register is T if hole at 3
    OR T J   #jump register is T if hole at 1, 2, or 3
    AND D J  #jump register is T if hole at 1, 2, or 3 and ground at 4


    for part 2

    if hole at a jump
    if hole at b jump
    if hole at d don't jump

    jump if there is a hole at 3 and 6 jump
    jump if there is a hole at 3 and no hole at 8

    (D AND (!A OR !B OR (!C AND (!F OR H)))

    NOT F T
    OR H T
    NOT C J
    AND T J
    NOT B T
    OR T J
    NOT A T
    OR T J
    AND D J
    '''
    program = list(map(int, data[0].split(',')))
    core = Intcode(program, mode='ascii robot')
    code1 = '''NOT A T
NOT B J
OR T J
NOT C T
OR T J
AND D J
WALK
'''
    code2 = '''NOT F T
OR H T
NOT C J
AND T J
NOT B T
OR T J
NOT A T
OR T J
AND D J
RUN
'''
    if part2:
        instruction = to_ascii(code2)
    else:
        instruction = to_ascii(code1)
    core.secondary = instruction
    check_output(core)
    check_output(core)
    check_output(core)


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
