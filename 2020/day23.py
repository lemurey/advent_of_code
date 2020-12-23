from aoc_utilities import get_instructions, timeit
from pathlib import Path


class Cup:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return f'{self.value}'

    def __str__(self):
        return self.__repr__()


def setup(data, part2=False):
    first = None
    last = None
    arr = [int(x) for x in data[0]]

    if part2:
        cups = [None] * 1000001
    else:
        cups = [None] * (len(arr) + 1)
    max_value = 0
    for val in arr:
        cup = Cup(val)
        max_value = max(val, max_value)
        cups[val] = cup

        if first is None:
            first = cup
        if last is not None:
            last.right = cup
            last.left = last
        last = cup

    if part2:
        while max_value < 1000000:
            max_value += 1
            cup = Cup(max_value)

            cups[max_value] = cup
            last.right = cup
            cup.left = last
            last = cup

    last.right = first
    first.left = last


    return cups, first, max_value


def run_game(cups, current, max_value, rounds):
    for round_num in range(rounds):
        if round_num % 2500000 == 0:
            print(f'On round {round_num}')

        # get next 3 values
        c1 = current.right
        c2 = c1.right
        c3 = c2.right
        store = {c1.value, c2.value, c3.value}

        # skip over the 3 removed values
        current.right = c3.right

        # find the destination
        destination = current.value
        while True:
            destination -= 1
            if destination < 1:
                destination = max_value
            if destination not in store:
                destination = cups[destination]
                break

        # put the removed values back in the ring
        c3.right = destination.right
        c3.right.left = c3
        destination.right = c1
        c1.left = current

        # advance 1
        current = current.right
    return cups


def get_answer(data, part2=False):

    cups, start, max_value = setup(data, part2)

    if part2:
        cups = run_game(cups, start, max_value, rounds=10000000)
        return cups[1].right.value * cups[1].right.right.value
    else:
        cups = run_game(cups, start, max_value, rounds=100)
        out = ''
        current = cups[1].right
        while current != cups[1]:
            out += str(current)
            current = current.right

        return out


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    # inputs = ['389125467']

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
