from aoc_utilities import get_instructions
from pathlib import Path

OFFSETS = ((0, 0, 1), (0, 0, -1), (0, 1, 0),
           (0, -1, 0), (1, 0, 0), (-1, 0 ,0))


def get_neighbors(x, y, z):
    for dx, dy, dz in OFFSETS:
        yield (x + dx, y + dy, z + dz)


# I never would have thought of this, pulled from solutions again
# you can use a version of DFS to find all the exterior points including the
# hollows
def is_exposed(x, y, z, drops, x_range, y_range, z_range, exterior):
    # original data points are never outside
    if (x, y, z) in drops:
        return False

    checked = set()
    to_check = [(x, y, z)]

    while to_check:
        x, y, z = to_check.pop()

        if (x, y, z) in checked:
            continue
        checked.add((x, y, z))

        # if we find something we already know is outside
        # then add everything to exterior but make sure we don't
        # add any data points in (this is like the fill tool in images)
        if (x, y, z) in exterior:
            exterior.update(checked - drops)
            return True
        # if we are checking a point outside the big cube then we know
        # we are outside, so everything is exterior like above
        if (x not in x_range) or (y not in y_range) or (z not in z_range):
            exterior.update(checked - drops)
            return True
        # if we don't know whats going on yet, add all the neighbors for checking
        if (x, y, z) not in drops:
            for n in get_neighbors(x, y, z):
                to_check.append(n)

    # if we checked everything and didn't get outside then original point
    # wasn't on the outside
    return False


def get_answer(data, part2=False):
    drops = {tuple(map(int, row.split(','))) for row in data}

    min_x = min(x[0] for x in drops)
    max_x = max(x[0] for x in drops)
    x_range = set(range(min_x, max_x + 1))
    min_y = min(x[1] for x in drops)
    max_y = max(x[1] for x in drops)
    y_range = set(range(min_y, max_y + 1))
    min_z = min(x[2] for x in drops)
    max_z = max(x[2] for x in drops)
    z_range = set(range(min_z, max_z + 1))

    exterior = set()

    exposed = 0
    exposed_2 = 0
    for (x, y, z) in drops:
        for n in get_neighbors(x, y, z):
            if n not in drops:
                exposed += 1
            if is_exposed(*n, drops, x_range, y_range, z_range, exterior):
                exposed_2 += 1

    return exposed, exposed_2


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''2,2,2
# 1,2,2
# 3,2,2
# 2,1,2
# 2,3,2
# 2,2,1
# 2,2,3
# 2,2,4
# 2,2,6
# 1,2,5
# 3,2,5
# 2,1,5
# 2,3,5'''.split('\n')
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
