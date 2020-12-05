from aoc_utilities import get_instructions
from pathlib import Path


class Seats:
    def __init__(self, string, verbose=False):
        self.string = string
        self.row_low = 0
        self.row_high = 127
        self.col_high = 7
        self.col_low = 0
        self.row = None
        self.col = None
        self.verbose = verbose

    def split_rows(self):
        for char in self.string[:6]:
            mod = (self.row_high - self.row_low) // 2

            if char == 'F':
                self.row_high = self.row_low + mod
            elif char == 'B':
                self.row_low = self.row_high - mod

            if self.verbose:
                print(char, mod, self.row_low, self.row_high)
        if self.string[6] == 'F':
            self.row = self.row_low
        elif self.string[6] == 'B':
            self.row = self.row_high

        if self.verbose:
            print(self.row)

    def split_cols(self):
        for char in self.string[7:-1]:
            mod = (self.col_high - self.col_low) // 2
            if char == 'L':
                self.col_high = self.col_low + mod
            elif char == 'R':
                self.col_low = self.col_high - mod

            if self.verbose:
                print(char, mod, self.col_low, self.col_high)

        if self.string[-1] == 'L':
            self.col = self.col_low
        elif self.string[-1] == 'R':
            self.col = self.col_high
        if self.verbose:
            print(self.col)

    def pid(self):
        if self.row is None:
            self.split_rows()
        if self.col is None:
            self.split_cols()
        return self.row * 8 + self.col


def get_answer(data, part2=False):
    max_id = 0
    ids = set()
    for row in data:
        seat = Seats(row)
        pid = seat.pid()
        ids.add(pid)
        if pid > max_id:
            max_id = pid
    print(max_id)
    if part2:
        for pid in range(max_id):
            if ((pid - 1) in ids) and ((pid + 1) in ids) and (pid not in ids):
                return pid
    # return max_id


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

    # inputs = ['FBFBBFFRLR', 'BFFFBBFRRR', 'FFFBBBFRRR', 'BBFFBBFRLL']

    # print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
