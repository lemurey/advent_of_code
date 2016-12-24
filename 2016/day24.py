from utilities import timeit
from heapq import heappush, heappop
from itertools import count, combinations, permutations
from collections import defaultdict, deque
import sys, time, os

# my initial attempt was to make an animated version of this, it mostly worked
# but i used BFS with start point on the path, which led to an answer exactly
# 7 higher than the correct one fro part 1, i then redid to remove the fancy stuff
# during this process i noticed the problem with start on the path


def find_points(duct_map):
    points = {}
    for i, line in enumerate(duct_map):
        for j, point in enumerate(line):
            if point.isdigit():
                points[point] = (i, j)
    return points


def make_duct_map(instructions):
    temp = instructions.split('\n')
    duct_map = []
    for line in temp:
        row = []
        for char in line:
            row.append(char)
        duct_map.append(row)
    return duct_map


def add_nodes(n1, n2):
    return n1[0] + n2[0], n1[1] + n2[1]


def get_neighbors(node, duct_map):
    for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        x, y = add_nodes(node, direction)
        if duct_map[x][y] != '#':
            yield x, y


def distance(n1, n2):
    return abs(n1[0] - n2[0]) + abs(n1[1] - n2[1])


def print_map(duct_map, path=None):
    if not path:
        path = []
    colored = '\033[31m{}\033[0m'
    for i, row in enumerate(duct_map):
        o = ''
        for j, point in enumerate(row):
            if (i, j) in path:
                o += colored.format(point)
            else:
                o += str(point)
        sys.stdout.write(o)
    sys.stdout.flush()
    time.sleep(0.5)


def search(start, end, duct_map):
    Q = deque([start])
    path = {start : []}
    while Q:
        node = Q.popleft()
        if node == end:
            return path[node]
        for neighbor in get_neighbors(node, duct_map):
            if neighbor in path:
                continue
            path[neighbor] = path[node] + [neighbor]
            Q.append(neighbor)
    return 'path not found'

    # history = {start}
    # visited = set()
    # uid = count()
    # pq = []
    # heappush(pq, (0, uid.next(), start))
    # iterations = 0
    # while history:
    #     cur_point = heappop(pq)[-1]
    #     if cur_point == end:
    #         return path[cur_point]
    #     history.remove(cur_point)
    #     visited.add(cur_point)
    #     for neighbor in get_neighbors(cur_point, duct_map):
    #         if neighbor in history or neighbor in visited:
    #             continue
    #         iterations += 1
    #         # if iterations % 10000 == 0:
    #         #     print '{}, len of stack:{}'.format(iterations, len(history))
    #         path[neighbor] = path[cur_point] + [neighbor]
    #         history.add(neighbor)
    #         d = distance(neighbor, end)
    #         heappush(pq, (d, uid.next(), neighbor))
    # return 'path not found'


def navigate_points(points, duct_map, animate=False):
    pairs = []
    paths = {}
    for p1 in points:
        for p2 in points:
            if p1 == p2:
                break
            pairs.append((p1, p2))
    for pair in pairs:
        p1, p2 = points[pair[0]], points[pair[1]]
        path = search(p1, p2, duct_map)
        if animate:
            os.system('clear')
            print_map(duct_map, path)
        paths[(pair[0], pair[1])] = path
    return paths


def finalize_path(paths):
    search_space = sorted(paths.items(), key=lambda x: len(x[1]))
    visited = {}
    history = set()
    options = combinations
    min_distance = 10000000000
    cur_path = []
    for path in possible_paths():
        d = 0
        cur_path = []
        o = ''
        for point in path:

            if point not in paths:
                point = point[1], point[0]

            d += len(paths[point])
            cur_path.extend(paths[point])
            o += point[0] + point[1]
        if d < min_distance:
            print o, d
            min_distance = d
            min_path = cur_path
    return min_distance, cur_path


def make_group(values):
    prev = values[0]
    output = []
    for value in values[1:]:
        output.append((prev, value))
        prev = value
    return tuple(output)


def possible_paths():
    combos = set()
    for combo in permutations('01234567', 8):
        c = make_group(combo)
        if c not in combos:
            combos.add(c)
            yield c


def search_no_animation(points, d_map, part2):
    start = points[0]
    other = points[1:]
    K = len(other)
    start_d = [len(search(start, point, d_map)) for point in other]

    other_d = [[None for j in xrange(K)] for i in xrange(K)]
    for i in xrange(K):
        for j in xrange(K):
            other_d[i][j] = other_d[j][i] = len(search(other[i], other[j], d_map))

    min_distance = 100000000000
    for path in permutations(range(K)):
        # print path
        d = start_d[path[0]]
        for i, p in enumerate(path[:-1]):
            d += other_d[p][path[i + 1]]
        if part2:
            d += start_d[path[-1]]
        min_distance = min(d, min_distance)

    return min_distance


@timeit
def get_results(instructions, part2=False):
    duct_map = make_duct_map(instructions)
    points = find_points(duct_map)
    locations = [points[x] for x in sorted(points.keys())]
    return search_no_animation(locations, duct_map, part2)
    # paths = navigate_points(points, duct_map, False)
    # start_distances = [None for i in xrange(K)]
    # other_distances = [[None for j in xrange(K)] for i in xrange(K)]
    # for x, y in paths:
    #     index = 0
    #     d = len(paths[(x, y)])
    #     if x == 0:
    #         index = int(y)
    #     elif y == 0:
    #         index = int(x)
    #     else:
    #         i = int(x)
    #         j = int(y)
    #         i, j = min(i, j), max(i, j)
    #     if index:
    #         start_distances[index - 1] = d
    #     else:
    #         other_distances[i - 1][j - 1] = other_distances[j - 1][i - 1] = d
    # for row in other_distances:
    #     print row
    # for entry in paths:
    #     print entry
    # distance, path = finalize_path(paths)
    # test_path = [('0', '1'), ('1', '7'), ('7', '6'), ('6', '5'), ('5', '4'), ('4', '2'), ('2', '3')]
    # test_path = [('0', '1'), ('1', '7'), ('7', '3'), ('3', '6'), ('6', '5'), ('5', '4'), ('4', '2')]
    # f_path = []
    # d = 0
    # for point in test_path:
    #     if point not in paths:
    #         p1, p2 = point
    #         point = p2, p1
    #     d += len(paths[point])
    #     f_path.extend(paths[point])

    # print_map(duct_map, f_path)
    # print d

    # print
    # print distance


if __name__ == '__main__':
    with open('instructions_day24.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)
