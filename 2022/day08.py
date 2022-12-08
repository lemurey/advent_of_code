from aoc_utilities import get_instructions
from pathlib import Path


def parse_instructions(data):
    grid = {}
    for j, row in enumerate(data):
        for i, val in enumerate(row):
            grid[(i, j)] = val
    return grid, i, j


def is_visible(i, j, max_x, max_y, grid):
    val = grid[(i, j)]
    if (i == 0) or (j == 0):
        return True
    for c in range(0, i):
        if grid[(c, j)] >= val:
            break
    else:
        return True
    for c in range(0, j):
        if grid[(i, c)] >= val:
            break
    else:
        return True
    for c in range(i + 1, max_x + 1):
        if grid[(c, j)] >= val:
            break
    else:
        return True
    for c in range(j + 1, max_y + 1):
        if grid[(i, c)] >= val:
            break
    else:
        return True

    return False


def get_score(i, j, max_x, max_y, grid):
    val = grid[(i, j)]
    scores = [0, 0, 0, 0]
    def _look(low, high, which, reverse=True):
        seen = 0
        if reverse:
            checks = range(high, low, -1)
        else:
            checks = range(low, high)
        for c in checks:
            seen += 1
            if which == 'row':
                c_val = grid[(c, j)]
            else:
                c_val = grid[(i, c)]
            if c_val >= val:
                break
        return seen


    if (i == 0) or (j == 0):
        return 0
    if (i == max_x) or (j == max_y):
        return 0
    # up
    scores[0] = _look(-1, j-1, 'col')
    # left
    scores[1] = _look(-1, i-1, 'row')
    # right
    scores[2] = _look(i + 1, max_x + 1, 'row', False)
    # down
    scores[3] = _look(j + 1, max_y + 1, 'col', False)

    return scores[0] * scores[1] * scores[2] * scores[3]


def get_visible(grid, max_x, max_y):
    visible = {}
    for (i, j) in grid:
        visible[(i, j)] = is_visible(i, j, max_x, max_y, grid)
    return visible


def get_scores(grid, max_x, max_y):
    scores = {}
    for (i, j) in grid:
        scores[(i, j)] = get_score(i, j, max_x, max_y, grid)
    return scores


def show_grid(grid, max_x, max_y):
    row = ''
    for j in range(max_y + 1):
        for i in range(max_x + 1):
            row += str(int(grid[(i, j)]))
        print(row)
        row = ''

def get_answer(data, part2=False):
    grid, max_x, max_y = parse_instructions(data)
    if part2:
        scores = get_scores(grid, max_x, max_y)
        # show_grid(scores, max_x, max_y)
        return max(scores.values())
    visible = get_visible(grid, max_x, max_y)
    return sum(visible.values())



if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''30373
# 25512
# 65332
# 33549
# 35390'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
