from aoc_utilities import get_instructions
from pathlib import Path


class Card:
    ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
             '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    def __init__(self, value, wild=False):
        if wild:
            self.ranks['J'] = 1
        self.value = value
        self.rank = self.ranks[self.value]

    def __lt__(self, other):
        if self.rank >= other.rank:
            return False
        return True

    def __ge__(self, other):
        return not self.__lt__(other)

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)


class Hand:
    orders = {(5, ): '7-5oak',
              (1, 4): '6-4oak',
              (2, 3): '5-full',
              (1, 1, 3): '4-3oak',
              (1, 2, 2): '3-2pair',
              (1, 1, 1, 2): '2-1pair',
              (1, 1, 1, 1, 1): '1-high',}
    def __init__(self, cards, winnings, wild=False):
        self.wild = wild
        self.cards = [Card(c, wild) for c in cards]
        self.order = self.orders[self.count(self.cards)]
        self.winnings = winnings

    def __str__(self):
        return ''.join(str(c) for c in self.cards)

    def __repr__(self):
        return str(self)

    def count(self, hand):
        count = {}
        for val in hand:
            if val not in count:
                count[val] = 0
            count[val] += 1
        if self.wild and Card('J') in count:
            add_val = count[Card('J')]
            del count[Card('J')]
            r = {v: k for k, v in count.items()}
            if len(r) == 0:
                count[Card('J')] = 5
            else:
                count[r[max(count.values())]] += add_val

        return tuple(sorted(count.values()))

    def __lt__(self, other):
        if self.order > other.order:
            return False
        if self.order < other.order:
            return True
        for c1, c2 in zip(self.cards, other.cards):
            if c1 > c2:
                return False
            if c2 > c1:
                return True

    def __ge__(self, other):
        return not self.__lt__(other)

    def __eq__(self, other):
        return all([x == y for (x, y) in zip(self.cards, other.cards)])


def rank_hands(hands):
    store = {'7-5oak': [], '6-4oak': [], '5-full': [],
             '4-3oak': [], '3-2pair': [], '2-1pair': [],
             '1-high': []}
    ranked = []
    for hand in hands:
        store[hand.order].append(hand)
    with open('log.txt', 'w') as f:
        for key, sub_hands in sorted(store.items()):
            for hand in sorted(sub_hands):
                f.write(str(hand) + ', ')
                ranked.append(hand)
            f.write('\n')
    return ranked


def get_answer(data, part2=False):
    hands = []
    for row in data:
        hand, winnings = row.split()
        hand = Hand(hand, int(winnings), wild=part2)
        hands.append(hand)
    out = 0
    for i, hand in enumerate(rank_hands(hands), start=1):
        with open('l2.txt', 'a') as f:
            f.write(str(hand) + '\n')
        out += i * hand.winnings
    return out


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''32T3K 765
# T55J5 684
# KK677 28
# KTJJT 220
# QQQJA 483'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
