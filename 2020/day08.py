from aoc_utilities import get_instructions
from pathlib import Path
from console import Console


def _run_alternates(c, arr, which):
    if which == 'nop':
        new_func = c.jmp
    else:
        new_func = c.nop

    for index in arr:
        _, val = c.instructions[index]
        c.instructions[index] = new_func, val

        result = c.run()

        if c.log == 'no infinite loop':
            return result
        c.reset()
    return 'fail'


def brute_force(c):
    nops = [i for i, (r, _) in enumerate(c.instructions) if r == c.nop]
    jmps = [i for i, (r, _) in enumerate(c.instructions) if r == c.jmp]

    check = _run_alternates(c, nops, 'nop')
    if check != 'fail':
        return check
    check = _run_alternates(c, jmps, 'jmp')

    if check != 'fail':
        return check

    return 'failed'


def get_answer(data, part2=False):
    c = Console(data)

    if part2:
        return brute_force(c)
    else:
        return c.run()


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''nop +0
# acc +1
# jmp +4
# acc +3
# jmp -3
# acc -99
# acc +1
# jmp -4
# acc +6'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
