from aoc_utilities import get_instructions
from pathlib import Path


class Circuit:
    def __init__(self):
        self.circuit = set()

    def add(self, p):
        self.circuit.add(p)

    def remove(self, p):
        if p in self.circuit:
            self.circuit.remove(p)

    def union(self, other):
        merged = self.circuit.union(other.circuit)
        self.circuit = merged
        other.circuit = merged

    def __eq__(self, other):
        return self.circuit == other.circuit

    def __len__(self):
        return len(self.circuit)

    def __contains__(self, other):
        return other in self.circuit

    def __gt__(self, other):
        return len(self) > len(other)

    def __str__(self):
        return str(self.circuit)

    def __hash__(self):
        return hash(frozenset(self.circuit))


def distance(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return (x2 - x1)**2 + (y2 - y1)**2 + (z2-z1)**2


def parse_input(lines):
    points = []
    for line in lines:
        x, y, z = map(int, line.split(','))
        points.append((x, y, z))
    return points


def check_circuits(p1, p2, circuits, return_merged=False):
    for c in circuits:
        if p1 in c:
            c1 = c
            break
    for c in circuits:
        if p2 in c:
            c2 = c
            break
    c1.union(c2)
    new = []
    for c in circuits:
        if c not in new:
            new.append(c)
    if return_merged:
        return new, c1
    return new


def run_part2(check, circuits):
    num = len(circuits)
    for i, entry in enumerate(check):
        if i % 1000 == 0:
            print(i)
        p1, p2 = entry[0]
        circuits, check = check_circuits(p1, p2, circuits, return_merged=True)
        if len(check) == num:
            print((p1, p2), i)
            return p1[0] * p2[0]


def get_answer(data, part2=False):
    boxes = parse_input(data)
    circuits = []
    for p in boxes:
        t = Circuit()
        t.add(p)
        circuits.append(t)

    distances = {}
    for i, p1 in enumerate(boxes):
        for p2 in boxes[i:]:
            if p1 == p2:
                continue
            distances[(p1, p2)] = distance(p1, p2)
    check = sorted(distances.items(), key=lambda x: x[1])

    if part2:
        return run_part2(check, circuits)

    num = 1000
    if len(circuits) < num:
        num = 10

    for i in range(num):
        p1, p2 = check[i][0]
        circuits = check_circuits(p1, p2, circuits)

    output = 1
    for entry in sorted(circuits, key=lambda x: len(x), reverse=True)[:3]:
        output *= len(entry)
    return output
    

if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''162,817,812
# 57,618,57
# 906,360,560
# 592,479,940
# 352,342,300
# 466,668,158
# 542,29,236
# 431,825,988
# 739,650,466
# 52,470,668
# 216,146,977
# 819,987,18
# 117,168,530
# 805,96,715
# 346,949,466
# 970,615,88
# 941,993,340
# 862,61,35
# 984,92,344
# 425,690,689'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
