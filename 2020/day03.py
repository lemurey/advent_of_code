from aoc_utilities import get_instructions
from pathlib import Path


def parse_inputs(data):
    output = {}

    for y, row in enumerate(data):
        for x, square in enumerate(row):
            output[(x, y)] = square
        width = x
    height = y
    return output, width, height


def run_tobogan(trees, slope_x, slope_y, width, height):
    cur_y = 0
    cur_x = 0

    tree_count = 0
    while cur_y < height:
        cur_y += slope_y
        cur_x = (cur_x + slope_x) % (width + 1)
        if trees[(cur_x, cur_y)] == '#':
            tree_count += 1
    return tree_count



def get_answer(data, part2=False):
    tree_map, width, height = parse_inputs(data)
    if part2:
        answer = 1
        for (slope_x, slope_y) in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
            answer *= run_tobogan(tree_map, slope_x, slope_y, width, height)
        return answer

    return run_tobogan(tree_map, 3, 1, width, height)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''..##.......
# #...#...#..
# .#....#..#.
# ..#.#...#.#
# .#...##..#.
# ..#.##.....
# .#.#.#....#
# .#........#
# #.##...#...
# #...##....#
# .#..#...#.#'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
