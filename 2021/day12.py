from aoc_utilities import get_instructions
from pathlib import Path

from collections import deque


def get_caves(data):
    caves = {}
    r = {'start': 'START'}
    for line in data:
        c1, c2 = line.split('-')

        if c1 in r:
            c1 = r[c1]
        if c2 in r:
            c2 = r[c2]

        if c1 not in caves:
            caves[c1] = []
        if c2 not in caves:
            caves[c2] = []

        if c2 != 'START':
            caves[c1].append(c2)
        if c1 != 'START':
            caves[c2].append(c1)

    return caves



def search(caves, part2=False):

    Q = deque()
    Q.append(('START', ['START']))
    paths = []
    while Q:
        cave, path = Q.popleft()

        if cave == 'end':
            paths.append(path)
            continue

        for next_cave in caves[cave]:
            if next_cave.islower():
                if part2:
                    counts = {x: path.count(x) for x in path if x.islower()}
                    check1 = sum([x > 1 for x in counts.values()]) > 1
                    check2 = any([x > 2 for x in counts.values()])
                    if check1 or check2:
                        continue
                elif next_cave in path:
                    continue
            new_path = path[:]
            new_path.append(next_cave)

            Q.appendleft((next_cave, new_path))


    return paths





def get_answer(data, part2=False):
    caves = get_caves(data)
    paths = search(caves, part2)
    # for path in sorted(paths):
    #     print(','.join(path))
    return len(paths)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''start-A
# start-b
# A-c
# A-b
# b-d
# A-end
# b-end'''.split('\n')
#     inputs = '''dc-end
# HN-start
# start-kj
# dc-start
# dc-HN
# LN-dc
# HN-end
# kj-sa
# kj-HN
# kj-dc'''.split('\n')
#     inputs = '''fs-end
# he-DX
# fs-he
# start-DX
# pj-DX
# end-zg
# zg-sl
# zg-pj
# pj-he
# RW-he
# fs-DX
# pj-RW
# zg-RW
# start-pj
# he-WI
# zg-he
# pj-fs
# start-RW'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
