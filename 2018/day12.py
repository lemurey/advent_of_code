from aoc_utilities import get_instructions
import os


def sum_state(state, zero_pot):
    total = 0
    for i, c in enumerate(state, start=-zero_pot):
        if c == '#':
            total += i
    return total


def pad_state(state):
    updates = []
    fills = {0: '....', 1: '...', 2: '..', 3: '.', 4: ''}
    for sub in (state[:5], state[-5:][::-1]):
        for i, c in enumerate(sub):
            if c == '#':
                break
        updates.append(fills[i])
    state = updates[0] + state + updates[1]
    return state, updates[0]


def update_state(state, rules, zero_pot=0):
    state, update = pad_state(state)
    replace = '..'
    zero_pot += len(update)
    count = 0
    for i in xrange(2, len(state) - 2):
        check = state[i-2:i+3]
        if check in rules:
            replace += rules[check]
        else:
            replace += '.'
    return replace, zero_pot


def align_state(state, zero_pot):
    return state[:zero_pot], state[zero_pot:]


def run_generations(state, rules, n):
    zero_pot = 0
    prev_state = sum_state(state, zero_pot)
    diffs = tuple(range(5))
    for i in xrange(1, n + 1):
        state, zero_pot = update_state(state, rules, zero_pot)
        new_state = sum_state(state, zero_pot)
        diff = new_state - prev_state
        diffs = diffs[1:] + (diff, )
        if all((x == diffs[0] for x in diffs)):
            current_iter = i
            return ((n - i) * diffs[0]) + new_state
        prev_state = new_state
    return new_state


def get_answer(data, part2=False):
    if part2:
        n = 50000000000
    else:
        n = 20
    rules = {}
    for line in data:
        if line.startswith('i'):
            temp = line.split(':')
            state = temp[1].strip()
        elif '=>' in line:
            reg, result = map(lambda x: x.strip(), line.split('=>'))
            rules[reg] = result
    return run_generations(state, rules, n)


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
#     sample = '''initial state: #..#.#..##......###...###

# ...## => #
# ..#.. => #
# .#... => #
# .#.#. => #
# .#.## => #
# .##.. => #
# .#### => #
# #.#.# => #
# #.### => #
# ##.#. => #
# ##.## => #
# ###.. => #
# ###.# => #
# ####. => #'''.split('\n')
#     print(get_answer(sample))
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
