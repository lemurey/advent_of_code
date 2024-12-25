from aoc_utilities import get_instructions
from pathlib import Path


def get_keys_and_locks(data):
    index = -1
    is_key = False
    is_lock = False
    keys = []
    locks = []
    for row in data:
        if row == '':
            index = -1
            if is_key:
                keys.append([v for k, v in sorted(thing.items())])
            elif is_lock:
                locks.append([v for k, v in sorted(thing.items())])
            continue
        index += 1
        if index == 0:
            if row == '#####':
                is_key = True
                is_lock = False
            elif row == '.....':
                is_lock = True
                is_key = False
            thing = {}
        for i, val in enumerate(row):
            if is_key and val == '.':
                if i not in thing:
                    thing[i] = index - 1
            if is_lock and val == '#':
                if i not in thing:
                    thing[i] = index
    if is_key:
        keys.append([v for k, v in sorted(thing.items())])
    elif is_lock:
        locks.append([v for k, v in sorted(thing.items())])
    return keys, locks


def fits(key, lock):
    for k, l in zip(key, lock):
        if k >= l:
            return False
    return True


def get_answer(data, part2=False):
    keys, locks = get_keys_and_locks(data)
    overlap = 0
    for key in keys:
        for lock in locks:
            if fits(key, lock):
                overlap += 1

    return overlap


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''#####
# .####
# .####
# .####
# .#.#.
# .#...
# .....

# #####
# ##.##
# .#.##
# ...##
# ...#.
# ...#.
# .....

# .....
# #....
# #....
# #...#
# #.#.#
# #.###
# #####

# .....
# .....
# #.#..
# ###..
# ###.#
# ###.#
# #####

# .....
# .....
# .....
# #....
# #.#..
# #.#.#
# #####'''.split('\n')

    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
