from aoc_utilities import get_instructions
from pathlib import Path

## A -- rock, B -- paper, C -- scissors
## X -- lose, Y -- tie, Z -- win

SCORES = {'A': 1, 'B': 2, 'C': 3,
          'X': 1, 'Y': 2, 'Z': 3}
OUTCOMES = {('A', 'X'): 3,
            ('B', 'Y'): 3,
            ('C', 'Z'): 3,
            ('A', 'Y'): 6,
            ('A', 'Z'): 0,
            ('B', 'X'): 0,
            ('B', 'Z'): 6,
            ('C', 'X'): 6,
            ('C', 'Y'): 0
            }
CONVERSIONS = {('A', 'X'): 'Z',
               ('A', 'Y'): 'X',
               ('A', 'Z'): 'Y',
               ('B', 'X'): 'X',
               ('B', 'Y'): 'Y',
               ('B', 'Z'): 'Z',
               ('C', 'X'): 'Y',
               ('C', 'Y'): 'Z',
               ('C', 'Z'): 'X',
               }

def parse_instructions(data):
    pairs = []
    for row in data:
        pairs.append(tuple(row.split()))
    return pairs


def single_round(them, me, p2=False):
    if p2:
        me = CONVERSIONS[(them, me)]
    return SCORES[me] + OUTCOMES[(them, me)]


def total_score(rounds, p2=False):
    total = 0
    for t, m in rounds:
        total += single_round(t, m, p2)
    return total


def get_answer(data, part2=False):
    rounds = parse_instructions(data)
    return total_score(rounds, part2)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
