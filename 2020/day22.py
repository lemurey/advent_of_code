from aoc_utilities import get_instructions, cacheit
from pathlib import Path

import sys
sys.setrecursionlimit(10000)


class Deck:
    def __init__(self, cards, name):
        self.deck = cards
        self.name = name

    def draw(self):
        return self.deck.pop()

    def collect(self, cards):
        if not isinstance(cards, (list, tuple)):
            cards = [cards]
        for card in cards:
            self.deck = [card] + self.deck

    def __str__(self):
        return ', '.join([f'{x}' for x in self.deck][::-1])

    def __len__(self):
        return len(self.deck)

    def __eq__(self, other):
        return self.deck == other.deck

    def __hash__(self):
        return hash(tuple(self.deck))


def play_round(player1, player2):
    c1 = player1.draw()
    c2 = player2.draw()

    if c1 > c2:
        player1.collect((c1, c2))
    elif c2 > c1:
        player2.collect((c2, c1))


def recursive_combat(player1, player2, cache=None, offset=0):

    if cache is None:
        cache = {}

    if (tuple(player1.deck), tuple(player2.deck)) in cache:
        return player1

    cache[(tuple(player1.deck), tuple(player2.deck))] = len(cache)

    if len(player1) == 0:
        return player2
    if len(player2) == 0:
        return player1

    c1 = player1.draw()
    c2 = player2.draw()

    if (c1 <= len(player1)) and c2 <= (len(player2)):
        p1d = player1.deck[-1 * c1:]
        p2d = player2.deck[-1 * c2:]

        sub_winner = recursive_combat(Deck(p1d, 'p1'), Deck(p2d, 'p2'))

        if sub_winner.name == "p1":
            player1.collect((c1, c2))
        else:
            player2.collect((c2, c1))

    else:
        if c1 > c2:
            player1.collect((c1, c2))
        elif c2 > c1:
            player2.collect((c2, c1))


    return recursive_combat(player1, player2, cache=cache)


def get_answer(data, part2=False):
    player1_cards = []
    player2_cards = []
    for row in data:
        if row == 'Player 1:':
            current = player1_cards
            continue
        elif row == 'Player 2:':
            current = player2_cards
            continue
        elif row == '':
            continue
        current.append(int(row))
    player1 = Deck(player1_cards[::-1], 'p1')
    player2 = Deck(player2_cards[::-1], 'p2')

    if part2:
        winner = recursive_combat(player1, player2)
    else:
        while ((len(player1) > 0) and (len(player2) > 0)):
            play_round(player1, player2)

        if len(player2) > len(player1):
            winner = player2
        else:
            winner = player1

    return sum([i * x for i, x in enumerate(winner.deck, start=1)])


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''Player 1:
# 9
# 2
# 6
# 3
# 1

# Player 2:
# 5
# 8
# 4
# 7
# 10'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
