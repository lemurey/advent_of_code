from aoc_utilities import get_instructions
from pathlib import Path

'''
if y velocity starts more negative than y_min then will never hit target
but what is maximum y velocity, it is one that results in the probe going so
fast on the descent after peaking that it bypasses the target

for x, has to have velocity >0 and if velocity is >x_max it will always
be too fast
'''


def get_target(data):
    _, vals = data[0].split(':')
    x_vals, y_vals = vals.split(',')
    x_vals = x_vals.strip().lstrip('x=')
    y_vals = y_vals.strip().lstrip('y=')

    x_min, x_max = tuple(map(int, x_vals.split('..')))
    y_min, y_max = tuple(map(int, y_vals.split('..')))

    target = set()

    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            target.add((x, y))

    return target, x_min, x_max, y_min, y_max


def run_step(xv, yv, x_pos, y_pos):
    x_pos += xv
    y_pos += yv

    if xv > 0:
        xv -=1
    elif xv < 0:
        xv += 1

    yv -= 1
    return xv, yv, x_pos, y_pos


def check_x(xv, pos, x_min, x_max):
    yv = 0
    (xp, yp) = pos
    count = 0
    while True:
        count += 1
        xv, yv, xp, yp = run_step(xv, yv, xp, yp)
        if (xp >= x_min) and (xp <= x_max):
            return count
        elif (xp > x_max):
            return 'too fast'
        elif (xv == 0) and (xp < x_min):
            return 'too slow'


def check_y(xv, yv, target, x_min, x_max, y_min, y_max):
    xp, yp = 0, 0
    highest = yp
    initial = yv
    while True:
        xv, yv, xp, yp = run_step(xv, yv, xp, yp)
        if yp > highest:
            highest = yp
        if (xp, yp) in target:
            return highest
        ## fail conditions
        ## - no x speed and in front of target
        ## - to right of target
        ## - below target and negative yv
        if (((xv == 0) and (xp < x_min)) or
            ((yv < 0) and (yp < y_min)) or
            (xv > x_max)):
            return 'failure'


def x_search(x_min, x_max):
    prev = None
    for cx in range(x_min, 0, -1):
        check = check_x(cx, (0, 0), x_min, x_max)
        if check == 'too slow':
            return prev, cx + 1
        prev = check


def y_search(cx, target, x_min, x_max, y_min, y_max):
    highest = 0
    highest_speed = 0

    cy = 0
    while True:
        cy += 1

        check = check_y(cx, cy, target, x_min, x_max, y_min, y_max)
        if check != 'failure':
            print(f'{check: >5}', f'{cy: >4}', end=' -- ')
        else:
            print('    f', f'{cy: >4}', end=' -- ')
        if cy % 8 == 0:
            print()

        if cy > 500:
            break


def y_verify(yv, y_min, y_max):
    xv = 0
    xp, yp = 0, 0
    count = 0

    while True:
        xv, yv, xp, yp = run_step(xv, yv, xp, yp)
        count += 1

        delta = abs(yp - y_min)
        if (yp > y_max) and (abs(yv) > delta) and (yv < 0):
            return 'too fast'
        if (yp >= y_min) and (yp <= y_max):
            return count
        if (yp < y_min) and (yv < 0):
            return 'fail'


def find_y_max(y_min, y_max):
    yv = 0
    while True:
        yv += 1
        if yv % 100 == 0:
            print(yv)
        check = y_verify(yv, y_min, y_max)
        if check == 'too fast':
            return yv


def check_velocity(xv, yv, target, x_min, x_max, y_min, y_max):
    xp, yp = 0, 0
    highest = yp
    while True:
        xv, yv, xp, yp = run_step(xv, yv, xp, yp)
        if yp > highest:
            highest = yp
        if (xp, yp) in target:
            return highest
        ## fail conditions
        ## - no x speed and in front of target
        ## - to right of target
        ## - below target and negative yv
        if (((xv == 0) and (xp < x_min)) or
            ((yv < 0) and (yp < y_min)) or
            (xv > x_max)):
            return 'failure'


def get_answer(data, part2=False):
    target, x_min, x_max, y_min, y_max = get_target(data)

    highest = 0
    count = 0
    for x in range(0, x_max + 1):
        for y in range(y_min, abs(y_min)):
            check = check_velocity(x, y, target, x_min, x_max, y_min, y_max)
            if check != 'failure':
                count += 1
                if check > highest:
                    highest = check

    return highest, count


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    # inputs=['target area: x=20..30, y=-10..-5']
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
