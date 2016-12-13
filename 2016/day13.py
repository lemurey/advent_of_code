from collections import deque

def get_results(instructions):
    favorite = int(instructions)
    t = search(favorite, (31, 39))
    if type(t) is dict:
        print t
    print len(t)
    t = search(favorite, None)
    paths = 0
    for path in t.itervalues():
        if len(path) <= 50:
            paths += 1
    print paths
    show_solution(set(t.keys()), favorite, 25, 25)


def show_solution(path, num, x_size=40, y_size=40):
    grid = [[0 for _ in xrange(x_size)] for __ in xrange(y_size)]
    for y in range(x_size):
        for x in range(y_size):
            if (x, y) in path:
                value = 'O'
            elif is_open(f1(x, y, num)):
                value = '.'
            else:
                value = '#'
            grid[y][x] = value
    print_grid(grid)


def print_grid(grid):
    output = '{: <2}' * len(grid[0])
    for row in grid:
        print output.format(*row)


def f1(x, y, num):
    return (x * x) + (3 * x) + (2 * x * y) + y + (y * y) + num


def memoize(f):
    memo = {}
    def helper(num):
        if num not in memo:
            memo[num] = f(num)
        return memo[num]
    return helper


@memoize
def is_open(num):
    return sum(map(int, bin(num)[2:])) % 2 == 0


def score(x, y, end_x, end_y):
    return end_x - x + end_y - y


def search(num, endpoint):
    Q = deque([(1, 1)])
    path = {(1, 1) : []}
    while Q:
        item = Q.popleft()
        if endpoint:
            if item == endpoint:
                return path[item]
        lengths = []
        for neighbor in get_neighbors(item, num):
            if neighbor in path:
                continue
            path[neighbor] = path[item] + [neighbor]
            lengths.append(len(path[neighbor]))
            if not endpoint and all(x > 50 for x in lengths):
                return path
            Q.append(neighbor)
    return path


def get_neighbors(point, num):
    scores = []
    x, y = point
    for i in (-1, 1):
        if is_open(f1(x + i, y, num)) and x + i >= 0:
            yield (x + i, y)
        if is_open(f1(x, y + i, num)) and y + i >= 0:
            yield (x, y + i)


if __name__ == '__main__':
    with open('instructions_day13.txt', 'r') as f:
        instructions = f.read().strip()
    get_results(instructions)
