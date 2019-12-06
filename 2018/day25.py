from aoc_utilities import get_instructions
import os


def md(p1, p2):
    d = 0
    for a, b in zip(p1, p2):
        d += abs(a - b)
    return d


def get_answer(data, part2=False):
    points = []
    for line in data:
        p = tuple(map(int, line.split(',')))
        points.append(p)
    links = {}
    for i, p1 in enumerate(points):
        links[i] = set()
        for j, p2 in enumerate(points):
            if md(p1, p2) <= 3:
                links[i].add(j)

    seen = set()
    num_cons = 0
    for i, _  in enumerate(points):
        if i in seen:
            continue
        num_cons += 1
        vals = [i]
        while vals:
            cur = vals.pop()
            if cur in seen:
                continue
            seen.add(cur)
            for neighbor in links[cur]:
                vals.append(neighbor)

    return num_cons

if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))