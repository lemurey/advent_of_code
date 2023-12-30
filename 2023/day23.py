from aoc_utilities import get_instructions
from pathlib import Path
from collections import deque


def get_neighbors(grid, loc):
    cur = grid[loc]
    checks = {'>': 1, '<': -1, 'v': 1j, '^': -1j}
    for d in (1j, -1j, 1, -1):
        n = grid.get(loc + d, '#')
        if n == '#':
            continue
        if cur in checks and checks[cur] != d:
            continue
        yield loc + d


def parse_grid(data, part2=False):
    grid = {}
    for j, row in enumerate(data):
        for i, val in enumerate(row):
            c = i + 1j*j
            if part2 and val in '><v^':
                val = '.'
            grid[c] = val
            if j == 0 and val == '.':
                start = c
            if val == '.':
                end = c
    return grid, start, end


def find_vertices(data, grid):
    vertices = set()
    for j, row in enumerate(data):
        for i, val in enumerate(row):
            c = i + 1j*j
            if val == '#':
                continue
            n = len(list(get_neighbors(grid, c)))
            if n > 2:
                vertices.add(c)
    return vertices


def search_vertices(grid, vertices):
    outcomes = {}
    for v in vertices:
        Q = deque([(v, 0)])
        seen = set()
        outcomes[v] = []
        while Q:
            loc, dist = Q.popleft()
            if loc in seen:
                continue
            seen.add(loc)
            for n in get_neighbors(grid, loc):
                if n in vertices and n != v:
                    outcomes[v].append((n, dist + 1))
                    continue
                Q.append((n, dist + 1))
    return outcomes


def get_walk_from_vertices(grid, start, end, edges):
    Q = deque([(start, set(), 0)])
    all_lengths = []
    while Q:
        loc, path, dist = Q.pop()
        if loc == end:
            all_lengths.append(dist)

        for n, d in edges[loc]:
            if n in path:
                continue
            n_path = path.union(set([n]))
            Q.append((n, n_path, dist + d))
    return all_lengths


def get_walk(grid, start, end):
    Q = [(start, set([start]))]
    paths = []

    while Q:
        loc, path = Q.pop()

        if loc == end:
            paths.append(path)
            continue

        for n in get_neighbors(grid, loc):
            if n in path:
                continue
            n_path = path.union(set([n]))
            Q.append((n, n_path))
    return paths


def get_answer(data, part2=False):
    grid, start, end = parse_grid(data, part2)

    vertices = find_vertices(data, grid)
    vertices.add(start)
    vertices.add(end)
    distances = search_vertices(grid, vertices)
    all_walks = get_walk_from_vertices(grid, start, end, distances)
    return max(all_walks)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''#.#####################
# #.......#########...###
# #######.#########.#.###
# ###.....#.>.>.###.#.###
# ###v#####.#v#.###.#.###
# ###.>...#.#.#.....#...#
# ###v###.#.#.#########.#
# ###...#.#.#.......#...#
# #####.#.#.#######.#.###
# #.....#.#.#.......#...#
# #.#####.#.#.#########v#
# #.#...#...#...###...>.#
# #.#.#v#######v###.###v#
# #...#.>.#...>.>.#.###.#
# #####v#.#.###v#.#.###.#
# #.....#...#...#.#.#...#
# #.#########.###.#.#.###
# #...###...#...#...#.###
# ###.###.#.###v#####v###
# #...#...#.#.>.>.#.>.###
# #.###.###.#.###.#.#v###
# #.....###...###...#...#
# #####################.#'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
