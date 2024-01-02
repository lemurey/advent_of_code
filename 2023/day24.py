from aoc_utilities import get_instructions
from pathlib import Path
from collections import namedtuple

Vec = namedtuple("Vec", "x,y,z", defaults=(0, 0, 0))


def get_hail(data):
    hail = []
    for row in data:
        p, v = row.split(' @ ')
        ps = Vec(*map(int, p.split(',')))
        vs = Vec(*map(int, v.split(',')))
        hail.append((ps, vs))
    return hail


def get_intersection(h1, h2):
    ph1, vh1 = h1
    ph2, vh2 = h2
    a1 = 1 / vh1.x
    b1 = -1 / vh1.y
    c1 = (ph1.y / vh1.y) - (ph1.x / vh1.x)
    a2 = 1 / vh2.x
    b2 = -1 / vh2.y
    c2 = (ph2.y / vh2.y) - (ph2.x / vh2.x)

    denom = (a1 * b2 - a2 * b1)
    if denom == 0:
        return 'no intersection'

    x_int = (b1 * c2 - b2 * c1) / denom
    y_int = (c1 * a2 - c2 * a1) / denom

    t1_int_x = (x_int - ph1.x) / vh1.x
    t2_int_x = (x_int - ph2.x) / vh2.x
    t1_int_y = (y_int - ph1.y) / vh1.y
    t2_int_y = (y_int - ph2.y) / vh2.y
    if any(t < 0 for t in (t1_int_x, t2_int_x, t1_int_y, t2_int_y)):
        return 'no intersection (paths intersect in past)'

    return x_int, y_int


def part1(hail):
    low_bound, high_bound = 200000000000000, 400000000000000

    c = 0
    for i, h1 in enumerate(hail):
        for h2 in hail[i+1:]:
            check = get_intersection(h1, h2)
            if isinstance(check, str):
                continue
            x, y = check
            if low_bound <= x <= high_bound:
                if low_bound <= y <= high_bound:
                    c += 1
    return c


def cross(v1, v2):
    '''
    get the cross product for two vectors
    '''
    t1 = v1.y * v2.z - v2.y * v1.z
    t2 = v2.x * v1.z - v1.x * v2.z
    t3 = v1.x * v2.y - v2.x * v1.y
    return Vec(t1, t2, t3)


def sub_vec(v1, v2):
    return Vec(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)


def dot(v1, v2):
    '''
    get the dot product for two vectors
    '''
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


def independent(v1, v2):
    return any(x != 0 for x in cross(v1, v2))


def get_lin_indep_hail(hail):
    p1, v1 = hail[0]
    for i in range(1, len(hail)):
        p2, v2 = hail[i]
        if independent(v1, v2):
            break
    for j in range(1, len(hail)):
        if j == i:
            continue
        p3, v3 = hail[j]
        if independent(v1, v3) and independent(v2, v3):
            break
    return p1, v1, p2, v2, p3, v3


def get_plane(p1, v1, p2, v2):
    '''
    get the plane from the vectors p1, v1, p2, v2 using
    C = (p1 - p2) . (v1 x v2)
    v = (p1-p2)x(v1-v2)
    '''
    p12 = sub_vec(p1, p2)
    v12 = sub_vec(v1, v2)
    v = cross(p12, v12)
    c = dot(p12, cross(v1, v2))
    return v, c


def make_w(a1, a2, a3, a, b, c):
    x = a1*a.x + a2*b.x + a3*c.x
    y = a1*a.y + a2*b.y + a3*c.y
    z = a1*a.z + a2*b.z + a3*c.z
    return Vec(x, y, z)


def part2(hail):
    '''
    use linear algebra (manually defined) to do all of this
    first find 3 hails that are linearly independent

    then note that the position of the rock at time t must be
    r = pi + (vi-w)*t (where w is rock velocity) for all the pi, vi
    this is becuase of the definition of the problem, cannot have the problem
    satisfied without this being true

    so we need to find intersections of the modified lines
    to have lines p1/p2 intersect we need (p1 - p2) . (v'1 x v'2) = 0
    where v'1 and v'2 are the modified velocities

    now define some constant C = (p1 - p2) . (v1 x v2)
    and note that the cross product for the modified velocities:
    (v'1 x v'2) = (v1 - w) x (v2 - w) = (v1 x v2) - ((v1 - v2) x w)
    (p1 - p2) . (v1 - w) x (v2 - w) = (p1 - p2) . (v1 x v2) - (p1 - p) . ((v1 - v2) x w)

    this reduces to
    (p1 - p2) . (v'1 x v'2) = C - (p1 - p) . ((v1 - v2) x w)

    so we get what we want so long as
    (p1 - p2) . ((v1 - v2) x w) = C
    the triple product a.(bxc) can be cycled without changing its value so this is
    w.((p1-p2)x(v1-v2)) = C
    which is an equation for a plane (w.v = C)

    if we repeat with additional vector combinations (p1, p3) and (p2, p3) we
    can get three planes (we need three to get the intersection to be a point)
    each would be (w.v = C) but with diffferent values for v, C. If we call the
    three vectors (a, b, c) then we can use these vectors to construct w

    w = a1 * (bxc) + a2 * (cxa) + a3 * (axb)

    now that we know w, we can calculate the intersection of p1 and p2, which will
    be the point r we are looking for
    '''
    p1, v1, p2, v2, p3, v3 = get_lin_indep_hail(hail)

    a, c1 = get_plane(p1, v1, p2, v2)
    b, c2 = get_plane(p1, v1, p3, v3)
    c, c3 = get_plane(p2, v2, p3, v3)

    w = make_w(c1, c2, c3, cross(b, c), cross(c, a), cross(a, b))
    mod = dot(a, cross(b, c))
    # get the integer valued w (using round to deal with floating point weirdness)
    w = Vec(round(w.x / mod), round(w.y / mod), round(w.z / mod))

    # now get the intersection, did this above for 2d, now need 3d version, easier
    # with dot/cross defined
    dif1 = sub_vec(v1, w)
    dif2 = sub_vec(v2, w)
    normal = cross(dif1, dif2)
    norm = dot(normal, normal)

    c1 = dot(normal, cross(p2, dif2))
    c2 = -1 * dot(normal, cross(p1, dif1))
    c3 = dot(normal, p1)
    # do the same plane construction that gives the vector defining the intersection point
    rock = make_w(c1, c2, c3, dif1, dif2, normal)
    return Vec(rock.x / norm, rock.y / norm, rock.z / norm)


def get_answer(data):
    hail = get_hail(data)
    p1 = part1(hail)
    print(p1)
    p2 = part2(hail)
    print(p2)
    return sum(p2)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''19, 13, 30 @ -2,  1, -2
# 18, 19, 22 @ -1, -1, -2
# 20, 25, 34 @ -2, -2, -4
# 12, 31, 28 @ -1, -2, -1
# 20, 19, 15 @  1, -5, -3'''.split('\n')
    print(get_answer(inputs))
    # print(get_answer(inputs, part2=True))
