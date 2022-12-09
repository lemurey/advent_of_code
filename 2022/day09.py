from aoc_utilities import get_instructions
from pathlib import Path

DIRECTIONS = {'R': 1, 'L': -1, 'U': 1j, 'D': -1j}

def get_distance(head, tail, absolute=True):
    v1 = head.real - tail.real
    v2 = head.imag - tail.imag
    if absolute:
        return int(abs(v1)), int(abs(v2))
    if v1 != 0:
        v1 = int(v1 / abs(v1))
    if v2 != 0:
        v2 = int(v2 / abs(v2)) * 1j

    return v1, v2


def is_seperated(head, tail):
    c1, c2 = get_distance(head, tail)
    if (c1 in (0, 1) and c2 in (0, 1)):
        return False
    return True


def step(d, v, h, t):
    seen = set()
    for _ in range(int(v)):
        h = h + DIRECTIONS[d]
        if is_seperated(h, t):
            r, c = get_distance(h, t, False)
            t = t + r + c
        seen.add(t)
    return seen, h, t


def step_rope(d, v, rope):
    head = rope[0]
    seen = set()
    temp_rope = rope[:]
    for _ in range(int(v)):
        head = head + DIRECTIONS[d]
        temp_rope[0] = head
        cur_head = head
        for i, tail in enumerate(rope[1:], start=1):
            if is_seperated(cur_head, tail):
                r, c = get_distance(cur_head, tail, False)
                tail = tail + r + c
            temp_rope[i] = tail
            cur_head = tail
        seen.add(tail)
        rope = temp_rope[:]
    return seen, rope


def run_instructions(instructions):
    tail_visits = set((0 + 0j,))
    head = 0 + 0j
    tail = 0 + 0j
    for row in instructions:
        cur_dir, val = row.split()
        new_visits, head, tail = step(cur_dir, val, head, tail)
        tail_visits = tail_visits | new_visits
    return tail_visits


def run_part2(instructions):
    rope = [0 + 0j for x in range(10)]
    tail_visits = set((0 + 0j,))
    for row in instructions:
        cur_dir, val = row.split()
        new_visits, rope = step_rope(cur_dir, val, rope)
        # display(rope)
        tail_visits = tail_visits | new_visits
    return tail_visits


def display(rope):
    for j in range(10, -10, -1):
        row = ''
        for i in range(-13, 13):
            val = i + j*1j
            if val == 0:
                row += 's'
                continue
            if val in rope:
                c = rope.index(val)
                if c == 0:
                    row += 'H'
                else:
                    row += str(c)
            else:
                row += '.'
            if val == 0:
                row
        print(row)
    print()
    print('-' * 20)


def get_answer(data, part2=False):
    if part2:
        tail_visits = run_part2(data)
    else:
        tail_visits = run_instructions(data)
    return len(tail_visits)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''R 5
# U 8
# L 8
# D 3
# R 17
# D 10
# L 25
# U 20'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
