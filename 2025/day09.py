from aoc_utilities import get_instructions
from pathlib import Path
from time import time


def parse_input(lines):
    red = []
    for line in lines:
        x, y = map(int, line.split(','))
        red.append((x, y))
    return red


def rectangle(c1, c2):
    x1, y1 = c1
    x2, y2 = c2
    return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)


def is_inside(c1, c2, red):
    x1, y1 = c1
    x2, y2 = c2
    xmin, xmax = sorted((x1, x2))
    ymin, ymax = sorted((y1, y2))
    for i, (xp1, yp1) in enumerate(red):
        xp2, yp2 = red[(i + 1) % len(red)] # get next point with looping
        if yp1 == yp2:
            xcl = min(xp1, xp2)
            xch = max(xp1, xp2)
            # if we are between (non-inclusive) the y values of our corners
            if ymin < yp1 < ymax:
                # if our x values are in the range of x values covered by the line
                # then this line crosses our rectangle, and thus our rectangle
                # contains some invalid tiles
                if (xcl <= xmin < xch) or (xcl < xmax <= xch):
                    return False
        else: # problem says all points share x or y with next point
            ycl = min(yp1, yp2)
            ych = max(yp1, yp2)
            # same condition as above, just x/y flipped
            if xmin < xp1 < xmax:
                if (ycl <= ymin < ych) or (ycl < ymax <= ych):
                    return False
    return True


def get_answer(data, part2=False):
    red = parse_input(data)
    sizes = []
    for c1 in red:
        for c2 in red:
            if part2 and not is_inside(c1, c2, red):
                continue
            sizes.append(rectangle(c1, c2))
    return max(sizes)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''7,1
# 11,1
# 11,7
# 9,7
# 9,5
# 2,5
# 2,3
# 7,3'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
