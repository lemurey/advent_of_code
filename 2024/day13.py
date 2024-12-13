from aoc_utilities import get_instructions
from pathlib import Path
import re


def get_mats(data):
    mats = []
    mat = [[None, None], [None, None]]
    for row in data:
        if row == '':
            mats.append((mat, vec))
            mat = [[None, None], [None, None]]
            continue
        if 'A:' in row:
            a, c = map(int, re.findall(r'X\+(\d+), Y\+(\d+)', row)[0])
            mat[0][0] = a
            mat[1][0] = c
        if 'B:' in row:
            b, d = map(int, re.findall(r'X\+(\d+), Y\+(\d+)', row)[0])
            mat[0][1] = b
            mat[1][1] = d
        if 'Prize:' in row:
            vec = list(map(int, re.findall(r'X=(\d+), Y=(\d+)', row)[0]))
    mats.append((mat, vec))

    return mats


def determinant(mat):
    a = mat[0][0]
    b = mat[0][1]
    c = mat[1][0]
    d = mat[1][1]
    return (a * d) - (b * c)


def solve_system(mat, vec):
    '''
    [[a, b], [c, d]], [A, B]
    '''
    denom = determinant(mat)
    A = determinant([[vec[0], mat[0][1]], [vec[1], mat[1][1]]]) / denom
    B = determinant([[mat[0][0], vec[0]], [mat[1][0], vec[1]]]) / denom
    return A, B


def get_answer(data, part2=False):
    mats = get_mats(data)

    tokens = 0
    for mat, vec in mats:
        if part2:
            vec = [vec[0]+10000000000000, vec[1]+10000000000000]
        A, B = solve_system(mat, vec)
        if (int(A) == A) and (int(B) == B):
            tokens += 3 * A + B

    return tokens


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400

# Button A: X+26, Y+66
# Button B: X+67, Y+21
# Prize: X=12748, Y=12176

# Button A: X+17, Y+86
# Button B: X+84, Y+37
# Prize: X=7870, Y=6450

# Button A: X+69, Y+23
# Button B: X+27, Y+71
# Prize: X=18641, Y=10279'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
