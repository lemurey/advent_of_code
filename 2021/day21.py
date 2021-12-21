from aoc_utilities import get_instructions
from pathlib import Path

from collections import Counter
from itertools import cycle


def universes(p1, p2):
    state = (p1['position'], p2['position'], 0, 0, 1)
    running = Counter()
    finished = Counter()
    running[state] += 1

    while len(running) > 0:
        fractures = Counter()
        for state, count in running.items():
            p1p, p2p, p1s, p2s, which = state
            if which == 1:
                for r1 in range(1, 4):
                    for r2 in range(1, 4):
                        for r3 in range(1, 4):
                            np1p = ((p1p + r1 + r2 + r3 - 1) % 10) + 1
                            np1s = p1s + np1p
                            new_state = np1p, p2p, np1s, p2s, 2
                            if np1s >= 21:
                                finished[new_state] += count
                            else:
                                fractures[new_state] += count
            else:
                for r1 in range(1, 4):
                    for r2 in range(1, 4):
                        for r3 in range(1, 4):
                            np2p = ((p2p + r1 + r2 + r3 - 1) % 10) + 1
                            np2s = p2s + np2p
                            new_state = p1p, np2p, p1s, np2s, 1
                            if np2s >= 21:
                                finished[new_state] += count
                            else:
                                fractures[new_state] += count
            running = fractures.copy()

    p1_wins = 0
    p2_wins = 0
    for state, count in finished.items():
        _, _, p1s, p2s, _ = state
        if p1s >= 21:
            p1_wins += count
        else:
            p2_wins += count
    return max((p1_wins, p2_wins))


def dirac(p1, p2, win_score=1000, max_die=100):
    dice = cycle(range(1, max_die))
    players = cycle((p1, p2))
    num_rolls = 0
    while (p1['score'] < win_score) and (p2['score'] < win_score):
        player = next(players)
        r1, r2, r3 = (next(dice) for _ in range(3))
        player['position'] = ((player['position'] + r1 + r2 + r3 - 1) % 10) + 1
        player['score'] += player['position']
        num_rolls += 3

    if p1['score'] >= win_score:
        return p2['score'] * num_rolls
    return p1['score'] * num_rolls


def get_answer(data, part2=False):
    pos1 = int(data[0].split(':')[1].strip())
    pos2 = int(data[1].split(':')[1].strip())
    p1 = {'score': 0, 'position': pos1, 'name': '1'}
    p2 = {'score': 0, 'position': pos2, 'name': '2'}
    if part2:
        return universes(p1, p2)
    return dirac(p1, p2)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
