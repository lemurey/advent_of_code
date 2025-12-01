from aoc_utilities import get_instructions
from pathlib import Path

from operator import add, sub


def parse_input(lines):
    output = []
    for line in lines:
        if line == '':
            continue
        if line[0] == 'R':
            output.append(int(line[1:]))
        elif line[0] == 'L':
            output.append(-1 * int(line[1:]))
    return output


def rotate_all(cur, rot, dial):
    count = 0
    if rot < 0:
        op = sub
    else:
        op = add
    for _ in range(abs(rot)):
        cur = op(cur, 1) % 100
        if cur == 0:
            count += 1
    return count, cur


def rotate(cur, rot, dial):
    index = (cur + rot)
    return dial[index % 100]


def get_answer(data, part2=False, debug=False):
    dial = list(range(100))
    rotations = parse_input(data)
    loc = 50
    password = 0
    history = [loc]
    for rot in rotations:
        if part2:
            count, loc = rotate_all(loc, rot, dial)
            password += count
        else:
            loc = rotate(loc, rot, dial)
            if loc == 0:
                password += 1
        history.append(loc)
    if debug:
        print(history)
    return password


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''L68
# L30
# R48
# L5
# R60
# L55
# L1
# L99
# R14
# L82'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
