from aoc_utilities import get_instructions
import os


class Dance:
    def __init__(self, data=None, length=16):
        self.letters = list('abcdefghijklmnopqrstuvwxyz'[:length])
        self.moves = []
        self.period = None
        self.rotations = []
        if data is not None:
            self._process(data)

    def _spin(self, x):
        self.letters = self.letters[-x:] + self.letters[:-x]

    def _exchange(self, x, y):
        self.letters[x], self.letters[y] = self.letters[y], self.letters[x]

    def _partner(self, a, b):
        ia, ib = 0, 0
        for index, letter in enumerate(self.letters):
            if letter == a:
                ia = index
            if letter == b:
                ib = index
        self._exchange(ia, ib)

    def _process(self, data):
        for move in data.split(','):
            if move[0] == 's':
                func = self._spin
                arg = {'x': int(move[1:])}
            elif move[0] == 'x':
                func = self._exchange
                x, y = map(int, move[1:].split('/'))
                arg = {'x': x, 'y': y}
            elif move[0] == 'p':
                func = self._partner
                a, b = move[1:].split('/')
                arg = {'a': a, 'b': b}
            self.moves.append((func, arg))

    def _calc_period(self):
        seen = set()
        i = 0
        while True:
            current = ''.join(self.letters)
            if current not in seen:
                seen.add(current)
            else:
                self.period = i
                return i
            self._dance()
            i += 1

    def _dance(self):
        for f, d in self.moves:
            f(**d)

    def __getitem__(self, key):
        if self.period is None:
            self._calc_period()
            self.letters = sorted(self.letters)
        if len(self.rotations) == 0:
            for _ in range(self.period):
                self.rotations.append(''.join(self.letters))
                self._dance()
            self.rotations.append(''.join(self.letters))
        return self.rotations[key % self.period]

    def __str__(self):
        return ''.join(self.letters)


def get_answer(data, part2=False):
    d = Dance(data)
    if part2:
        return d[1000000000]
    return d[1]


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
