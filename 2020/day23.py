from aoc_utilities import get_instructions, timeit
from pathlib import Path


class Cup:
    def __init__(self, value, right=None):
        self.value = value
        self.right = right

    def __str__(self):
        return f'{self.value}'


class Cups:
    def __init__(self, start, max_value=None):
        self._setup(start, max_value)
        self._write_start = int(start[0])

    def _setup(self, start, max_value):
        arr = [int(x) for x in start]
        if max_value is None:
            max_value = max(arr)

        self.cups = [None] * (max_value + 1)

        first = Cup(arr[0])
        last = first
        self.cups[arr[0]] = first

        current = 0

        for val in arr[1:]:
            if val > current:
                current = val
            cup = Cup(val)
            self.cups[val] = cup
            last.right = cup
            last = cup

        while self.cups[-1] is None:
                current += 1
                cup = Cup(current)
                self.cups[current] = cup

                last.right = cup
                last = cup

        last.right = first

        self.max_value = max_value
        self.current = first

    def run_round(self):
        # get the next three cups in ring
        c1 = self.current.right
        c2 = c1.right
        c3 = c2.right
        store = {c1.value, c2.value, c3.value}

        # find destination
        dest_value = self.current.value
        destination = None
        while destination is None:
            dest_value -= 1
            if dest_value < 1:
                dest_value = self.max_value
            if dest_value not in store:
                destination = self.cups[dest_value]

        # snip ring
        self.current.right = c3.right
        # right of destination is now right of c3
        c3.right = destination.right
        # right of destination is now c1
        destination.right = c1
        # move forward one in ring
        self.current = self.current.right

    def __getitem__(self, index):
        return self.cups[index]

    def _write(self, cup):
        if cup == self.current:
            return f'({cup}) '
        return f'{cup} '

    def __str__(self):
        start = self.cups[self._write_start]
        out = self._write(start)
        current = start.right
        while current != start:
            out += self._write(current)
            current = current.right
        return out


def run_game(cups, rounds):
    for round_num in range(rounds):
        if round_num % 2500000 == 0 and round_num != 0:
            print(f'On round {round_num}')
        cups.run_round()

def get_answer(data, part2=False):
    if part2:
        cups = Cups(data[0], 1000000)
    else:
        cups = Cups(data[0])

    if part2:
        run_game(cups, 10000000)
        return cups[1].right.value * cups[1].right.right.value
    else:
        run_game(cups, 100)
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
