from utilities import timeit
from itertools import permutations
from collections import  deque
import sys, time, os


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


def print_map(duct_map, path=None):
    os.system('clear')
    if not path:
        path = []
    path_color = '\033[31m{}\033[0m'
    wall_color = '\033[30m{}\033[0m'
    digit_color = '\033[37m{}\033[0m'
    o = ''
    for i, row in enumerate(duct_map):
        for j, point in enumerate(row):
            if (i, j) in path:
                o += path_color.format(point)
            elif point == '#':
                o += wall_color.format(point)
            elif point.isdigit():
                o += digit_color.format(point)
            else:
                o += point
        o += '\n'
    sys.stdout.write(o)
    sys.stdout.flush()
    time.sleep(0.3)


def search(start, end, duct_map):
    Q = deque([start])
    path = {start : [start]}
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


def build_0_y(start, rest, d_map, animate):
    start_d = [None for point in rest]    
    start_paths = start_d[:]
    for i, point in enumerate(rest):
        path = search(start, point, d_map)
        start_d[i] = len(path) - 1
        start_paths[i] = path
        if animate:
            print_map(d_map, path)

    return start_paths, start_d


def build_x_y(rest, d_map, animate):
    K = len(rest)
    other_d = [[None for j in xrange(K)] for i in xrange(K)]
    other_paths = [[None for j in xrange(K)] for i in xrange(K)]
    
    for i in xrange(K):
        for j in xrange(K):
            if j > i:
                continue
            path = search(rest[i], rest[j], d_map)
            if animate and path:
                print_map(d_map, path)
            other_d[i][j] = other_d[j][i] = len(path) - 1
            other_paths[i][j] = other_paths[j][i] = path

    return other_paths, other_d


def get_min_distance(start, rest, d_map, animate, part2):

    start_paths, start_distances = build_0_y(start, rest, d_map, animate)
    other_paths, other_distances = build_x_y(rest, d_map, animate)

    min_distance = 100000000000
    final_path = []
    for test_path in permutations(range(len(rest))):
        d = start_distances[test_path[0]]

        for i, p in enumerate(test_path[:-1]):
            d += other_distances[p][test_path[i + 1]]
        if part2:
            d += start_distances[test_path[-1]]

        if d < min_distance:
            min_distance = d
            if animate:
                final_path = start_paths[test_path[0]]
                for i, p in enumerate(test_path[:-1]):
                    final_path.extend(other_paths[p][test_path[i + 1]])

    return min_distance, final_path


def navigate_points(points, d_map, animate=False, part2=False):
    start = points[0]
    rest = points[1:]

    min_d, final_path = get_min_distance(start, rest, d_map, animate, part2)
    
    if animate:
        print_map(d_map, final_path)

    return min_d

    
@timeit
def get_results(instructions, part2=False):
    duct_map = make_duct_map(instructions)
    points = find_points(duct_map)
    locations = [points[x] for x in sorted(points.keys())]
    animate = True
    return navigate_points(locations, duct_map, animate, part2)


if __name__ == '__main__':
    with open('instructions_day24.txt', 'r') as f:
        instructions = f.read().strip()
    # print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)
