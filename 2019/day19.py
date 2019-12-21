import sys
sys.path.append('/Users/lee.murray/projects/advent_of_code/')
from aoc_utilities import get_instructions
import os
from intcode import Intcode


def check_single(x, y, comp):
    comp.reset()
    comp.secondary = [x, y]
    return comp.run()


def check_range(x_range, y_range, comp):
    grid = {}
    for x in x_range:
        for y in y_range:
            comp.reset()
            comp.secondary = [x, y]
            val = comp.run()
            grid[x, y] = val
    return grid


def check_square(comp, y, x, size=100):
    offset = size - 1
    xc = x - offset
    yc = y + offset
    if check_single(x, y, comp):
        return check_single(xc, yc, comp)
    return False


def search(comp, y, size=100):

    min_x = 0

    while True:
        print(y, end=', ')
        left, right = get_width(comp, y, min_x)
        if left > min_x:
            min_x = left

        if (right - left) < size:
            y += 1
            print()
            continue

        prev = False
        for check_x in range(right , left, -1):
            if not check_square(comp, y, check_x, size):
                if prev:
                    return y, check_x - 99
                else:
                    break
            else:
                prev = True

        print(left, right, check_x)
        y += 1


def get_width(comp, y_loc, low=0):

    high = y_loc

    # search for beam
    step = (high - low) // 5
    while True:
        step = step // 2
        options = []
        for x_val in range(low, high, step):
            if check_single(x_val, y_loc, comp) == 1:
                options.append(x_val)
        if len(options) > 0:
            break

    # search for left edge of beam
    high = min(options)
    while True:
        mid = (low + high) // 2
        val = check_single(mid, y_loc, comp)

        if val == 0: # out of beam, move back to right
            low = mid
        if val == 1: # in beam
            if check_single(mid - 1, y_loc, comp) == 0: # at left edge
                beam_left = mid
                break
            else: # not at edge current point is still in beam so it is new max
                high = mid

    # search for right edge of beam
    low = beam_left
    high = max(options) + step
    while low < high:
        mid = (low + high) // 2
        val = check_single(mid, y_loc, comp)

        if val == 0: # out of beam, move to left
            high = mid
        if val == 1: # in beam
            if check_single(mid + 1, y_loc, comp) == 0: # at right edge
                beam_right = mid
                break
            else: # not at edge move right
                low = mid + 1

    return beam_left, beam_right


def calc_min(row):
    for i, val in enumerate(reversed(row)):
        if val == '#':
            return i


def zero_row(row, min_s):
    out = ''
    s = 0
    for i, val in enumerate(reversed(row)):
        if val == '#' and i >= min_s:
            s += 1
        if s <= 100 and i >= min_s and val == '#':
            out += 'O'
        else:
            out += val
    return ''.join(reversed(out))


def plot_range(comp, ylow, size):
    grid = {}
    left = 0
    for y in range(ylow - 1, ylow + size + 1):
        left, right = get_width(comp, y, left)
        grid[left, y] = 1
        grid[left - 1, y] = check_single(left - 1, y, comp)
        grid[right, y] = 1
        grid[right + 1, y] = check_single(right + 1, y, comp)

    string = string_grid(grid)

    data = string.split('\n')
    min_val = calc_min(data[1])
    for j, row in enumerate(data):
        if j > 0 and j <= 100:
            print(zero_row(row, min_val))
        else:
            print(row)


def string_grid(grid):
    x_min = min(grid.keys(), key=lambda x: x[0])[0]
    x_max = max(grid.keys(), key=lambda x: x[0])[0]
    y_min = min(grid.keys(), key=lambda x: x[1])[1]
    y_max = max(grid.keys(), key=lambda x: x[1])[1]


    o = ''
    i = 0
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            if (x, y) not in grid:
                if i == 0:
                    o += '.'
                elif o[i - 1] == '#':
                    o += '#'
                else:
                    o += '.'
                i += 1
                continue
            elif grid[x, y] == 0:
                o += '.'
            else:
                o += '#'
            i += 1
        o += '\n'
        i += 1
    return o


def get_answer(data, part2=False):

    program = list(map(int, data[0].split(',')))
    comp = Intcode(program, mode='drone')


    left, right = get_width(comp, 10000)
    print(left, right)
    m1 = left / 10000
    m2 = right / 10000

    x2 = (m1 * 99) + 99 / (m2 - m1)
    y1 = m2 * x2 - 99
    print(x2, y1)

    # # return check_perimeter(comp, 1687, 1144)
    # # plot_range(comp, 1690, 100)
    # # return check_square(comp, 1690, 1020)
    # # return check_square(comp, 1680, 940)

    # y_low, x_low = search(comp, 1650)
    # print()

    # print(check_square(comp, 1666, 1130))
    # print(check_square(comp, 1666, 1129))
    # print(check_square(comp, 1665, 1129))

    # # plot_range(comp, y_low, 100)
    # # plot_range(comp, y_low + 3, 100)

    # return 10000 * x_low + y_low

    # # x_max = 50
    # # y_max = 50
    # # beam = check_range(range(x_max), range(y_max), comp)
    # # for y in range(y_max):
    #     # for x in range(x_max):
    # #         if beam[x, y] == 0:
    # #             print('.', end='')
    # #         else:
    # #             print('#', end='')
    # #     print()
    # # return sum(beam.values())


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
