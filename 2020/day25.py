from aoc_utilities import get_instructions
from pathlib import Path


def one_loop(value, subject):
    value *= subject
    _, value = divmod(value, 20201227)
    return value


def sim_loops(num):
    loops = 0
    check = 1
    while True:
        loops += 1
        check = one_loop(check, 7)
        if check == num:
            return loops


def get_key(public_key, loop_num):
    output = 1
    for _ in range(loop_num):
        output = one_loop(output, public_key)
    return output


def get_answer(data, part2=False):
    card, door = tuple(map(int, data))
    # card, door = 5764801, 17807724

    card_loop = sim_loops(card)
    door_loop = sim_loops(door)

    return get_key(door, card_loop)



if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
