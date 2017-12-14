from aoc_utilities import get_instructions
import os
from day10 import knothash
from collections import deque


def process_row(seed, row):
    hex_val = knothash('{}-{}'.format(seed, row))
    bin_string = '{:0>128}'.format(bin(int(hex_val, 16))[2:])
    return list(map(int, bin_string))


def neighbors(row, col):
    if col < 127:
        yield row, col + 1
    if col > 0:
        yield row, col - 1
    if row > 0:
        yield row - 1, col
    if row < 127:
        yield row + 1, col


def zero_process(row, col, q, regions):
    for neighbor in neighbors(row, col):
        if neighbor not in regions:
            q.append(neighbor)


def one_process(row, col, q, regions, grid):
    cur_region = regions[(row, col)]
    for n_row, n_col in neighbors(row, col):
        if (n_row, n_col) in regions:
            continue
        if grid[n_row][n_col] == 0:
            regions[(n_row, n_col)] = -1
            zero_process(n_row, n_col, q, regions)
            continue
        regions[(n_row, n_col)] = cur_region
        one_process(n_row, n_col, q, regions, grid)


def find_regions(grid):
    q = deque()
    q.append((0, 0))
    regions = {}
    cur_region = 1
    while q:
        row, col = q.popleft()
        if (row, col) in regions:
            continue
        if grid[row][col] == 0:
            regions[(row, col)] = -1
            zero_process(row, col, q, regions)
            continue
        regions[(row, col)] = cur_region
        one_process(row, col, q, regions, grid)
        cur_region += 1

    return max(regions.values())


def print_regions(regions):
    size = max(regions)[0]
    output = ''
    for i in range(size + 1):
        line = ''
        for j in range(size + 1):
            if regions[(i, j)] == -1:
                line += '.'
            else:
                line += str(regions[(i, j)])
        output += line + '\n'
    print(output)


def get_answer(data, part2=False):
    grid = []
    for row_num in range(128):
        grid.append(process_row(data, row_num))
    if part2:
        return find_regions(grid)
    return sum([sum(x) for x in grid])


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    # grid = [[0, 0, 1, 0, 1],
    #         [0, 1, 1, 0, 1],
    #         [0, 0, 0, 0, 1],
    #         [1, 1, 0, 1, 0],
    #         [1, 0, 0, 1, 0]]
    # print(find_regions(grid))
    # print(get_answer('flqrgnkx', part2=True))
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
