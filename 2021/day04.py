from aoc_utilities import get_instructions
from pathlib import Path


def get_boards(data):
    boards = []
    board = []
    for row in data:
        if row == '':
            if len(board) == 0:
                continue
            boards.append(board)
            board = []
            continue
        board.append(list(map(int, row.split())))
    boards.append(board)
    return boards


def run_board(board, num):
    new = []
    for row in board:
        nr = []
        for val in row:
            if val == num:
                nr.append('X')
            else:
                nr.append(val)
        new.append(nr)
    return new


def check_board(board):
    cols = [0, 0, 0, 0, 0]
    for row in board:
        if all([True if x == 'X' else False for x in row]):
            return 1
        for i, val in enumerate(row):
            if val == 'X':
                cols[i] += 1
            if cols[i] == 5:
                return 1
    return 0


def score_board(board):
    total = 0
    for row in board:
        for val in row:
            if val == 'X':
                continue
            total += val
    return total


def run_game(boards, nums, part2=False):
    check_val = 1
    if part2:
        check_val = len(boards)
    win_count = 0
    for num in nums:
        replacement = []
        for board in boards:
            new = run_board(board, num)
            if check_board(new):
                win_count += 1
                if win_count == check_val:
                    return score_board(new) * num
                else:
                    new = [[-1] * 5 for _ in range(5)]
            replacement.append(new)
        boards = replacement[:]


def get_answer(data, part2=False):
    nums = list(map(int, data[0].split(',')))
    boards = get_boards(data[1:])
    if part2:
        return run_game(boards, nums, part2)
    return run_game(boards, nums)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
