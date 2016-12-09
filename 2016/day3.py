


def valid_triangle(s1, s2, s3):
    if s1 + s2 <= s3:
        return False
    if s1 + s3 <= s2:
        return False
    if s2 + s3 <= s1:
        return False
    return True


def make_triangles_1(path):
    with open(path, 'r') as f:
        instructions = f.read().strip()
    return [(int(x) for x in line.split()) for line in instructions.split('\n')]


def get_sides(line, cur_triangles):
    for j, side in enumerate(line.split()):
        cur_triangles[j].append(int(side))
    return cur_triangles


def make_triangles_2(path):
    triangles = []
    with open(path, 'r') as f:
        first_line = f.readline()
        num_triangles = len(first_line.split())
        cur_triangles = [[] for _ in xrange(num_triangles)]
        cur_triangles = get_sides(first_line, cur_triangles)
        for i, line in enumerate(f, 1):
            if i % 3 == 0:
                triangles.extend(tuple(x) for x in cur_triangles)
                cur_triangles = [[] for _ in xrange(num_triangles)]
            cur_triangles = get_sides(line, cur_triangles)
    triangles.extend(tuple(x) for x in cur_triangles)
    return triangles


def check_triangles(path, function=make_triangles_1):
    all_triangles = function(path)
    return sum(valid_triangle(*triangle) for triangle in all_triangles)


if __name__ == '__main__':
    print check_triangles('instructions_day3.txt')
    print check_triangles('instructions_day3.txt', make_triangles_2)
