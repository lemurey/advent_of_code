from aoc_utilities import get_instructions
from pathlib import Path


def check_fuel(positions, spot, part2):
    cost = 0
    for x in positions:
        delta = abs(x - spot)
        if part2:
            # cost += sum(range(delta + 1))
            cost += int(delta * (delta + 1) / 2)
        else:
            cost += delta
    return cost


def get_answer(data, part2=False):

    positions = list(map(int, data[0].split(',')))
    min_fuel = None

    for val in range(min(positions), max(positions)):
        cost = check_fuel(positions, val, part2)

        if min_fuel is None:
            min_fuel = cost
            min_spot = val

        if cost < min_fuel:
            min_fuel = cost
            min_spot = val

    return min_fuel



if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

    # inputs = ['16,1,2,0,4,2,7,1,2,14']

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
