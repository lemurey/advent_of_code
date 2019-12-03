from aoc_utilities import get_instructions
import os


def run_line(line, which, points=None):
    directions = {'R': 1, 'L': -1,
                  'U': 1j, 'D': -1j}
    if points is None:
        points = {}
        points[0 + 0j] = set()
    cur = 0 + 0j
    steps = {}
    steps[cur] = 0
    num_steps = 0
    for entry in line.split(','):

        d = entry[0]
        num = int(entry[1:])
        mod = directions[d]
        for _ in range(num):
            num_steps += 1
            cur += mod
            if cur not in points:
                points[cur] = set()
            points[cur].add(which)
            steps[cur] = num_steps
    return points, steps


def parse_instructions(data):
    p_set = None
    all_steps = []
    for i, instructions in enumerate(data):
        p_set, steps = run_line(instructions, i, p_set)
        all_steps.append(steps)
    return p_set, all_steps


def get_answer(data, part2=False):
    points, steps = parse_instructions(data)
    distances = []
    for k, v in points.items():
        # print('{}: {}'.format(k, v))
        if len(v) > 1:
            if part2:
                distance = steps[0][k] + steps[1][k]
            else:
                distance = abs(k.imag) + abs(k.real)
            if distance != 0:
                distances.append(distance)

    return min(distances)


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))