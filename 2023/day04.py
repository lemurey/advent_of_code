from aoc_utilities import get_instructions
from pathlib import Path

def parse_data(data):
    outcomes = {}
    for line in data:
        num, base = line.split(':')
        num = int(num.strip().split()[-1])
        winners, haves = base.strip().split(' | ')
        winners = set(int(x) for x in winners.split())
        haves = set(int(x) for x in haves.split())

        my_winners = winners & haves
        outcomes[num] = len(my_winners)
    return outcomes


def get_answer(data, part2=False):
    outcomes = parse_data(data)
    total = 0
    winners = {k: 1 for k in outcomes}
    for k, v in outcomes.items():
        total += int(2 ** (v - 1))
        for i in range(k + 1, k + 1 + v):
            winners[i] += winners[k]

    return total, sum(winners.values())


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
