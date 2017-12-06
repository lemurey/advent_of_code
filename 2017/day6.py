from aoc_utilities import get_instructions
import os
from utilities import timeit


def process_data(data):
    state = []
    for entry in data.split():
        state.append(int(entry))
    return state


def get_max_block(state):
    max_val = state[0]
    max_index = 0
    for i, block in enumerate(state):
        if block > max_val:
            max_val = block
            max_index = i
    return max_index, max_val


def run_cycle(state, n):
    index, values = get_max_block(state)
    state[index] = 0
    for _ in range(values):
        index = (index + 1) % n
        state[index] += 1
    return state


@timeit
def get_answer(data, mode):
    states = {}
    state = process_data(data)
    count = 0
    n = len(state)
    while True:
        check = tuple(state)
        if check in states:
            if mode == 'part1':
                return count
            else:
                return count - states[check]
        states[check] = count
        state = run_cycle(state, n)
        count += 1


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, mode='part1'))
    print(get_answer(inputs, mode='part2'))
