from aoc_utilities import get_instructions
from pathlib import Path


def get_games(line):
    outcomes = {}
    id_num, rest = line.split(':')
    id_num = int(id_num.split()[-1])
    for g in rest.split(';'):
        for p in g.strip().split(', '):
            num, col = p.split()
            if col not in outcomes:
                outcomes[col] = []
            outcomes[col].append(int(num))
    return id_num, outcomes


def get_answer(data, part2=False):
    possible = 0
    power = 0
    thresh = {'red': 12, 'green': 13, 'blue': 14}
    for line in data:
        id_num, o = get_games(line)
        temp = 1
        for color in ('red', 'blue', 'green'):
            v = o.get(color, 0)
            temp *= max(v)
            if any(x > thresh[color] for x in v):
                id_num = 0
        possible += id_num
        power += temp
    return possible, power


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
# Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
# Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
# Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''.split('\n')
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
