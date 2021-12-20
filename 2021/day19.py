from aoc_utilities import get_instructions
from pathlib import Path


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, other):
        return tuple(map(abs, self - other))

    def rotate(self):
        for nx, ny, nz in ((self.x, self.y, self.z),
                           (self.z, self.x, self.y),
                           (self.y, self.z, self.x)):
            for mx, my, mz in ((1, 1, 1), (1, -1, -1),
                               (-1, 1, -1), (-1, -1, 1)):
                yield Point(mx * nx, my * ny, mz * nz)

        for nx, ny, nz in ((self.x, self.z, self.y),
                           (self.z, self.y, self.x),
                           (self.y, self.x, self.z)):
            for mx, my, mz in ((-1, -1, -1), (1, -1, 1),
                               (1, 1, -1), (-1, 1, 1)):
                yield Point(mx * nx, my * ny, mz * nz)

    def __add__(self, other):
        return Point(self.x + other.x,
                     self.y + other.y,
                     self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x,
                     self.y - other.y,
                     self.z - other.z)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __lt__(self, other):
        if self.x < other.x:
            return True
        elif self.x > other.x:
            return False
        elif self.y < other.y:
            return True
        elif self.y > other.y:
            return False
        elif self.z < other.z:
            return True
        return False

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __str__(self):
        return str((self.x, self.y, self.z))

    def __repr__(self):
        return str(self)


def parse_data(data):
    points = []
    for line in data:
        if line.startswith('--'):
            num = int(''.join([x for x in line if x.isdigit()]))
            points.append([])
        elif line == '':
            pass
        else:
            x, y, z = map(int, line.split(','))
            points[-1].append(Point(x, y, z))
    return points


def get_distances(data):
    distances = {}
    for pos1 in data:
        distances[pos1] = set()
        for pos2 in data:
            if pos1 == pos2:
                continue
            d = tuple(sorted(pos1.distance(pos2)))
            distances[pos1].add(d)
    return distances


def get_max_overlap(fixed_distances, to_check):
    max_overlap = 0

    for scanner in to_check:
        d = get_distances(scanner)
        c = max([len(d1.intersection(d2)) for d1 in fixed_distances.values() for d2 in d.values()])
        if c > max_overlap:
            max_overlap = c
            max_scanner = scanner
            max_distances = d
    return max_scanner, max_distances


def align(fixed, checking):
    mapping = {}
    for p1 in fixed:
        biggest_overlap = 0
        for p2 in checking:
            p1d = fixed[p1]
            p2d = checking[p2]
            num_in_common = len(p1d.intersection(p2d))
            if num_in_common > biggest_overlap:
                biggest_overlap = num_in_common
                mapping[p1] = p2

    with open('check_19.txt', 'w') as f:
        for p1 in mapping:
            f.write(f'{p1} : {mapping[p1]}\n')

    store = [set() for _ in range(24)]

    for p1 in mapping:
        for i, rotated in enumerate(mapping[p1].rotate()):
            store[i].add(p1 - rotated)

    for i, row in enumerate(store):
        if len(row) == 1:
            offset = Point(*row.pop())
            break
    else:
        return None, None

    new_points = set()
    for p2 in checking:
        for count, new in enumerate(p2.rotate()):
            if count == i:
                new_points.add(offset + new)
                break

    return new_points, offset


def get_answer(data, part2=False):

    data = parse_data(data)

    fixed = set(data[0])
    scanner_locs = ({Point(0, 0, 0)})
    to_check = data[1:]

    while to_check:
        fixed_distances = get_distances(fixed)
        scanner, distances = get_max_overlap(fixed_distances, to_check)

        new_points, new_scanner = align(fixed_distances, distances)

        if new_points is None:
            continue

        fixed = fixed.union(new_points)
        scanner_locs.add(new_scanner)
        to_check.remove(scanner)
    print(len(fixed))
    return max(sum(p1.distance(p2)) for p1 in scanner_locs for p2 in scanner_locs)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''--- scanner 0 ---
# 404,-588,-901
# 528,-643,409
# -838,591,734
# 390,-675,-793
# -537,-823,-458
# -485,-357,347
# -345,-311,381
# -661,-816,-575
# -876,649,763
# -618,-824,-621
# 553,345,-567
# 474,580,667
# -447,-329,318
# -584,868,-557
# 544,-627,-890
# 564,392,-477
# 455,729,728
# -892,524,684
# -689,845,-530
# 423,-701,434
# 7,-33,-71
# 630,319,-379
# 443,580,662
# -789,900,-551
# 459,-707,401

# --- scanner 1 ---
# 686,422,578
# 605,423,415
# 515,917,-361
# -336,658,858
# 95,138,22
# -476,619,847
# -340,-569,-846
# 567,-361,727
# -460,603,-452
# 669,-402,600
# 729,430,532
# -500,-761,534
# -322,571,750
# -466,-666,-811
# -429,-592,574
# -355,545,-477
# 703,-491,-529
# -328,-685,520
# 413,935,-424
# -391,539,-444
# 586,-435,557
# -364,-763,-893
# 807,-499,-711
# 755,-354,-619
# 553,889,-390

# --- scanner 2 ---
# 649,640,665
# 682,-795,504
# -784,533,-524
# -644,584,-595
# -588,-843,648
# -30,6,44
# -674,560,763
# 500,723,-460
# 609,671,-379
# -555,-800,653
# -675,-892,-343
# 697,-426,-610
# 578,704,681
# 493,664,-388
# -671,-858,530
# -667,343,800
# 571,-461,-707
# -138,-166,112
# -889,563,-600
# 646,-828,498
# 640,759,510
# -630,509,768
# -681,-892,-333
# 673,-379,-804
# -742,-814,-386
# 577,-820,562

# --- scanner 3 ---
# -589,542,597
# 605,-692,669
# -500,565,-823
# -660,373,557
# -458,-679,-417
# -488,449,543
# -626,468,-788
# 338,-750,-386
# 528,-832,-391
# 562,-778,733
# -938,-730,414
# 543,643,-506
# -524,371,-870
# 407,773,750
# -104,29,83
# 378,-903,-323
# -778,-728,485
# 426,699,580
# -438,-605,-362
# -469,-447,-387
# 509,732,623
# 647,635,-688
# -868,-804,481
# 614,-800,639
# 595,780,-596

# --- scanner 4 ---
# 727,592,562
# -293,-554,779
# 441,611,-461
# -714,465,-776
# -743,427,-804
# -660,-479,-426
# 832,-632,460
# 927,-485,-438
# 408,393,-506
# 466,436,-512
# 110,16,151
# -258,-428,682
# -393,719,612
# -211,-452,876
# 808,-476,-593
# -575,615,604
# -485,667,467
# -680,325,-822
# -627,-443,-432
# 872,-547,-609
# 833,512,582
# 807,604,487
# 839,-516,451
# 891,-625,532
# -652,-548,-490
# 30,-46,-14
# '''.split('\n')

    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
