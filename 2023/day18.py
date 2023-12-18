from aoc_utilities import get_instructions
from pathlib import Path

'''
based on a brief perusal of solutions I saw mentions of pick's theorem
and the shoelace theorem, both of which I was previously completely unfamiliar.
But it lets us get the answer fairly quickly

to get the area we can use shoelace theorem which says for a series of x, y
coordinates the area is
A = 1/2 * SUM(y_i * (x_i-1 - x_i+1))
if you think about this you are creating a series of squares around each set of
three vertices and adding them together. I am not smart enough to be sure that
this all cancels correctly, but there is apparently a proof somewhere that they do

we can use this to get the number of interior points from pick's theorem
(this is the filled area in the problem description)
A = i + b/2 - 1
i = A + 1 - b/2
b is the boundary which we can get from counting our steps as we construct the
set of vertices

since we want the fill + boundary
i + b = A + 1 + b/2
'''

def get_digs(data, part2=False):
    instructions = []
    turns = {'R': 1, 'L': -1, 'U': 1j, 'D': -1j,
             '0': 1, '2': -1, '3': 1j, '1': -1j}
    for row in data:
        d, v, c = row.split()
        if part2:
            d = c.strip()[-2]
            v = int(c.strip()[2:-2], 16)
        instructions.append((turns[d], int(v)))

    return instructions


def get_area(instructions):
    cur = complex(0)
    vertices = []
    count = 0
    for d, v in instructions:
        count += v
        cur += d * v
        vertices.append(cur)

    area = 0
    for i, cur_vertex in enumerate(vertices):
        prev_vertex = vertices[(i - 1) % len(vertices)]
        next_vertex = vertices[(i + 1) % len(vertices)]
        area += cur_vertex.imag * (prev_vertex.real - next_vertex.real)
    area = abs(area // 2)
    # return the total using pick's theorem adjustment
    return area + count // 2 + 1


def get_answer(data, part2=False):
    return get_area(get_digs(data, part2))


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''R 6 (#70c710)
# D 5 (#0dc571)
# L 2 (#5713f0)
# D 2 (#d2c081)
# R 2 (#59c680)
# D 2 (#411b91)
# L 5 (#8ceee2)
# U 2 (#caa173)
# L 1 (#1b58a2)
# U 2 (#caa171)
# R 2 (#7807d2)
# U 3 (#a77fa3)
# L 2 (#015232)
# U 2 (#7a21e3)'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
