from aoc_utilities import get_instructions
import os


def parse_line(line):
    id_num, _, edges, size = line.split()
    left, top = map(int, edges.strip(':').split(','))
    width, height = map(int, size.split('x'))
    return id_num, left, top, width, height


def parse_file(data):
    max_width = 0
    max_height = 0
    output = {}
    for line in data:
        id_num, left, top, width, height = parse_line(line)
        total_width = left + width
        total_height = top + height
        output[id_num] = (left, top, width, height)
        if total_height > max_height:
            max_height = total_height
        if total_width > max_width:
            max_width = total_width
    return output, max_width + 1, max_height + 1


def get_answer(data, part2=False):
    sizes, max_width, max_height = parse_file(data)
    grid = [[0 for _ in range(max_width)] for _ in range(max_height)]
    for left, top, width, height in sizes.values():
        for x in range(width):
            for y in range(height):
                grid[top + y][left + x] += 1
    multiples = 0
    for row in grid:
        for value in row:
            if value > 1:
                multiples += 1
    for id_num, (left, top, width, height) in sizes.iteritems():
        total = 0
        sub = grid[top:(top + height)]
        for row in sub:
            sub2 = row[left: left + width]
            total += sum(sub2)
        if total == (width * height):
            no_overlap = id_num
            break
    return multiples, no_overlap


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    test_file = '''#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2'''.split('\n')
    print get_answer(test_file)
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))