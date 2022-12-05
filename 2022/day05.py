from aoc_utilities import get_instructions
from pathlib import Path


def parse_instructions(data):
    crate_holder = []
    instructions = []
    for line in data:
        if line == '':
            crates = [list(x)[::-1] for x in zip(*crate_holder)]
            continue

        if ']' in line:
            temp = line.split(']')
            cur = []
            for entry in temp:
                if '[' not in entry:
                    gap = entry
                    val = None
                else:
                    gap, val = entry.split('[')
                cur.extend([' ' for x in range(len(gap) // 4)])
                if val:
                    cur.append(val)
            if cur.count(' ') != len(cur):
                crate_holder.append(cur)
        elif 'move' in line:
            temp = []
            for group in line.split():
                if group.isdigit():
                    temp.append(int(group))
            instructions.append(temp)

    cleaned = []
    for row in crates:
        cleaned.append([x for x in row if x != ' '])

    return cleaned, instructions


def run_instructions(crates, instructions):
    for n, f, t in instructions:
        cur = crates[f - 1]
        new = crates[t - 1]
        to_move = []

        for _ in range(n):
            to_move.append(cur.pop())
        new.extend(to_move)
    return crates


def run_instructions_2(crates, instructions):
    for n, f, t in instructions:
        cur = crates[f - 1]
        new = crates[t - 1]
        to_move = cur[-n:]
        crates[f - 1] = cur[:-n]
        new.extend(to_move)
    return crates


def get_answer(data, part2=False):
    crates, instructions = parse_instructions(data)

    if part2:
        crates = run_instructions_2(crates, instructions)
    else:
        crates = run_instructions(crates, instructions)

    return ''.join(x[-1] for x in crates)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = ['    [D]    ', '[N] [C]    ', '[Z] [M] [P]', ' 1   2   3 ', '']
#     inputs = inputs + '''move 1 from 2 to 1
# move 3 from 1 to 3
# move 2 from 2 to 1
# move 1 from 1 to 2'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
