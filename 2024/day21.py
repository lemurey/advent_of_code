from aoc_utilities import get_instructions
from pathlib import Path
from functools import cache
from heapq import heappush, heappop


DOORPAD = {(0, 0): '7', (1, 0): '8', (2, 0): '9', 
           (0, 1): '4', (1, 1): '5', (2, 1): '6', 
           (0, 2): '1', (1, 2): '2', (2, 2): '3', 
           (1, 3): '0', (2, 3): 'A', }
MOVEPAD = {(1, 0): '^', (2, 0): 'A',
           (0, 1): '<', (1, 1): 'v', (2, 1): '>'}
LOOKUP = {'A': (2, 0), 'v': (1, 1), '^': (1, 0), '>': (2, 1), '<': (0, 1)}
MOVES = {'A': (0, 0), 'v': (0, 1), '^': (0, -1), '>': (1, 0), '<': (-1, 0)}


def run_move(loc, move, pad):
    dx, dy = MOVES[move]
    new_loc = loc[0] + dx, loc[1] + dy
    if new_loc not in pad:
        return None, None
    if move == 'A':
        val = pad[new_loc]
    else:
        val = None
    return new_loc, val


@cache
def get_path(target_move, prev_move, num_pads):
    # need to stop the recursion, if no intermediate pads
    # moving is a 1 step thing
    if num_pads == 0:
        return 1
    start = LOOKUP[prev_move]
    Q = []
    heappush(Q, (0, start, 'A', ''))
    seen = {}

    while Q:
        cost, loc, prev, presses = heappop(Q)

        if presses == target_move:
            return cost

        if (loc, prev) in seen:
            continue
        seen[(loc, prev)] = cost

        for move in '^<v>A':
            new_loc, new_press = run_move(loc, move, MOVEPAD)
            # if we are not in the pad, stop the search
            if new_loc is None:
                continue
            cost_move = get_path(move, prev, num_pads-1)
            if new_press is not None:
                update = new_press
            else:
                update = ''
            heappush(Q, (cost + cost_move, new_loc, move, presses+update))


def get_code_sequence(code, num_pads):
    Q = []
    heappush(Q, (0, (2, 3), 'A', '', 0))

    seen = {}
    while Q:
        cost, loc, prev_move, sequence, code_index = heappop(Q)

        if sequence == code:
            return cost

        if (loc, prev_move, sequence) in seen:
            continue
        seen[(loc, prev_move, sequence)] = cost

        for move in '^<v>A':
            new_loc, new_press = run_move(loc, move, DOORPAD)
            if new_loc is None:
                continue
            if new_press is not None:
                # only keep looking if we are pushing the correct button
                if new_press != code[code_index]:
                    continue
                new_seq = sequence + new_press
                new_index = code_index + 1
            else:
                new_seq = sequence
                new_index = code_index

            cost_move = get_path(move, prev_move, num_pads)
            heappush(Q, (cost+cost_move, new_loc, move, new_seq, new_index))


def get_answer(data, part2=False):

    total_complexity = 0
    if part2:
        num_pads = 25
    else:
        num_pads = 2
    for code in data:
        seq_val = get_code_sequence(code, num_pads)

        print(f"{seq_val} * {int(code.strip('A'))}")
        total_complexity += (seq_val * int(code.strip('A')))
    return total_complexity


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''029A
# 980A
# 179A
# 456A
# 379A'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
