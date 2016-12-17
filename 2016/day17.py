from time import time
from hashlib import md5
from collections import deque

VALID = set(['b', 'c', 'd', 'e', 'f'])
MOVES = {'U' : (0, -1), 'D' : (0, 1), 'L' : (-1, 0), 'R' : (1, 0)}

def valid_moves(data):
    result = md5(data).hexdigest()[:4]
    for letter, direction in zip(result, 'UDLR'):
        if letter in VALID:
            yield direction


def update_node(node, direction):
    return (node[0] + MOVES[direction][0], node[1] + MOVES[direction][1])


def search(key, end):
    vertices = deque()
    vertices.append(((0, 0), ''))
    while vertices:
        prev, path = vertices.popleft()
        for direction in valid_moves(key + path):
            node = update_node(prev, direction)
            nx, ny = node
            if 0 > nx or nx > end[0] or 0 > ny or ny > end[1]:
                continue
            elif node == end:
                yield path + direction
            else:
                vertices.append((node, path + direction))


def timeit(function):
    def timed(*args, **kwargs):
        s_t = time()
        result = function(*args, **kwargs)
        e_t = time()
        out = '{} {} took {:.2f} sec'
        print out.format(function.__name__, kwargs, e_t - s_t)
        return result
    return timed


@timeit
def get_results(instructions, part2=False):
    end_point = (3, 3)
    t = list(search(instructions, end_point))
    if not part2:
        return t[0]
    else:
        return len(max(t, key=lambda x: len(x)))


if __name__ == '__main__':
    with open('instructions_day17.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)