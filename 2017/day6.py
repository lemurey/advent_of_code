from aoc_utilities import get_instructions
import os


def process_data(data):
    state = []
    for entry in data.split():
        state.append(int(entry))
    return tuple(state)


def get_max_block(state):
    max_val = state[0]
    max_index = 0
    for i, block in enumerate(state):
        if block > max_val:
            max_val = block
            max_index = i
    return max_index


def run_cycle(state):
    state = list(state)
    n = len(state)
    index = get_max_block(state)
    values = state[index]
    state[index] = 0
    count = 0
    for _ in range(values):
        index = (index + 1) % n
        state[index] += 1
    return tuple(state)


def get_answer(data, mode):
    states = {}
    state = process_data(data)
    count = 0
    while True:
        if state in states:
            if mode == 'part1':
                return count
            else:
                return count - states[state]
        states[state] = count
        state = run_cycle(state)
        count += 1


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, mode='part1'))
    print(get_answer(inputs, mode='part2'))
