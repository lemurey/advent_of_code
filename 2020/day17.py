from aoc_utilities import get_instructions
from pathlib import Path


DIRECTIONS = ((0, 0, 1), (1, 0, 1), (0, 1, 1), (1, 1, 1), (-1, 0, 1),
              (0, -1, 1), (-1, -1, 1), (1, -1, 1), (-1, 1, 1), (1, 0, 0),
              (0, 1, 0), (1, 1, 0), (-1, 0 ,0), (0, -1, 0), (-1, -1, 0),
              (1, -1, 0), (-1, 1, 0), (0, 0, -1), (1, 0, -1), (0, 1, -1),
              (1, 1, -1), (-1, 0 ,-1), (0, -1, -1), (-1, -1, -1),
              (1, -1, -1), (-1, 1, -1))


DIRECTIONS_2 = [(0, 0, 0, -1), (0, 0, 0, 1)]
for (x, y, z) in DIRECTIONS:
    DIRECTIONS_2.extend(((x, y, z, 1), (x, y, z, 0), (x, y, z, -1)))


def make_state(data):
    state = {}
    z = 0
    for y, row in enumerate(data):
        for x, val in enumerate(row):
            state[(x, y, z)] = val
    return state


def get_neighbors(p, which):
    if which == 1:
        for dx, dy, dz in DIRECTIONS:
            np = (p[0] + dx, p[1] + dy, p[2] + dz)
            yield np
    else:
        for dx, dy, dz, dw in DIRECTIONS_2:
            np = (p[0] + dx, p[1] + dy, p[2] + dz, p[3] + dw)
            yield np


def expand(state, which):
    new_state = {}
    for p in state:
        for np in get_neighbors(p, which):
            if np in state:
                new_state[np] = state[np]
            else:
                new_state[np] = '.'
    return new_state


def run_cycle(state, which=1):
    expanded = expand(state, which)
    new_state = {}

    for p in expanded:
        num_active = 0
        current = expanded[p]
        for np in get_neighbors(p, which):
            if np not in expanded:
                pass
            elif expanded[np] == '#':
                num_active += 1

        if (current == '#') and (num_active in (2, 3)):
            new_state[p] = '#'
        elif current == '#':
            new_state[p] = '.'
        elif num_active == 3:
            new_state[p] = '#'
        else:
            new_state[p] = '.'

    return new_state


def show_state(state, add_on=''):

    slices = {}
    for x, y, z in sorted(state):
        if z not in slices:
            slices[z] = []
        slices[z].append((x, y))

    for z in sorted(slices):
        print(f'z={z}{add_on}')
        grid = ''
        prev_y = None
        for x, y in sorted(slices[z], key=lambda x: x[1]):
            if y != prev_y and prev_y is not None:
                grid += '\n'
            grid += state[x, y, z]
            prev_y = y
        print(grid)


def show_state_2(state):
    w_states = {}
    for x, y, z, w in sorted(state):
        if w not in w_states:
            w_states[w] = {}
        w_states[w][(x, y, z)] = state[(x, y, z, w)]

    for w in sorted(w_states):
        sub_state = w_states[w]
        show_state(sub_state, add_on=f', w={w}')


def count_active(state):
    num_active = 0
    for val in state.values():
        if val == '#':
            num_active += 1
    return num_active


def get_answer(data, part2=False):
    state = make_state(data)
    if part2:
        new_state = {}
        for (x, y, z), v in state.items():
            new_state[(x, y, z, 0)] = v
        state = new_state

    for i in range(6):
        if part2:
            state = run_cycle(state, 2)
        else:
            state = run_cycle(state)

    return count_active(state)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''.#.
# ..#
# ###'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
