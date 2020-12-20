from aoc_utilities import get_instructions
from pathlib import Path
import numpy as np
from collections import defaultdict, deque

import json


def image_to_array(image):
    holder = []
    for row in image:
        converted = [1 if x == '#' else 0 for x in row]
        holder.append(converted)
    return np.array(holder)


def array_to_image(array):
    return (str(array).replace('[', '')
                      .replace(']', '')
                      .replace('1', '#')
                      .replace('0', '.')
                      .replace(' ', '')
                      .replace('3', ' '))


def get_images(data):
    images = {}
    for raw in data:
        rows = raw.split('\n')
        header = rows[0]
        tile = int(header.split()[1][:-1])
        images[tile] = image_to_array(rows[1:])
    return images


def _gen_edges(image):
    top = image[0, :]
    bottom = image[-1, :]
    left = image[:, 0]
    right = image[:, -1]
    return top, bottom, left, right


def _comp_images(image1, image2):
    top1, bottom1, left1, right1 = _gen_edges(image1)
    top2, bottom2, left2, right2 = _gen_edges(image2)

    if (np.all(top1 == bottom2) or np.all(right1 == left2) or
        np.all(bottom1 == top2) or np.all(left1 == right2) or
        np.all(top2 == bottom1) or np.all(right2 == left1) or
        np.all(bottom2 == top1) or np.all(left2 == right1)) and not orientation:
        return True

    return False


def run_checks(image1, image2, tile1, tile2, neighbors):
     # check raw images
    if _comp_images(image1, image2):
        neighbors[tile1].add(tile2)
        neighbors[tile2].add(tile1)
    # rotate up down
    elif _comp_images(np.flipud(image1), image2):
        neighbors[tile1].add(tile2)
        neighbors[tile2].add(tile1)
    # rotate left right
    elif _comp_images(np.fliplr(image1), image2):
        neighbors[tile1].add(tile2)
        neighbors[tile2].add(tile1)


def find_neighbors(images):
    neighbors = defaultdict(set)

    for tile1, image1 in images.items():
        for tile2, image2 in images.items():
            if tile1 == tile2:
                continue

            if (len(neighbors[tile1]) == 4) and (len(neighbors[tile2]) == 4):
                continue

            for rot in range(4):
                run_checks(np.rot90(image1, rot), image2, tile1, tile2, neighbors)
                run_checks(np.rot90(image2, rot), image1, tile1, tile2, neighbors)

    return neighbors


def alterations(image, fixed=False):
    if fixed:
        yield image
        return
    for rot in range(4):
        yield np.rot90(image, rot)
        yield np.flipud(np.rot90(image, rot))
        yield np.fliplr(np.rot90(image, rot))


def _find_direction(image1, image2):
    top1, bottom1, left1, right1 = _gen_edges(image1)
    top2, bottom2, left2, right2 = _gen_edges(image2)

    if np.all(top1 == bottom2):
        return 'up'
    if np.all(right1 == left2):
        return 'right'
    if np.all(bottom1 == top2):
        return 'down'
    if np.all(left1 == right2):
        return 'left'


def align_images(image1, image2, image1_fixed, image2_fixed):
    for i1 in alterations(image1, image1_fixed):
        for i2 in alterations(image2, image2_fixed):
            c = _find_direction(i1, i2)
            if c in ('up', 'left', 'down', 'right'):
                return i1, i2, c


def crawl_neighbors(neighbors, images):
    for k, v in neighbors.items():
        if len(v) == 2:
            start = k
            break

    fixed = {}
    reconstruction = {start: (0, 0)}
    q = [start]

    dirs = {'up': (0, -1), 'left': (-1, 0),
            'down': (0, 1), 'right':(1, 0)}

    while len(fixed) < len(images):

        current = q.pop()
        for neighbor in neighbors[current]:

            if (current in fixed) and (neighbor in fixed):
                continue

            fixed_1 = current in fixed
            image_1 = fixed.get(current, images[current])
            fixed_2 = neighbor in fixed
            image_2 = fixed.get(neighbor, images[neighbor])

            image_1, image_2, direction = align_images(image_1, image_2,
                                                       fixed_1, fixed_2)
            x, y = reconstruction[current]
            dx, dy = dirs[direction]
            nx = x + dx
            ny = y + dy
            reconstruction[neighbor] = (nx, ny)
            fixed[current] = image_1
            fixed[neighbor] = image_2

            q.append(neighbor)

    return fixed, reconstruction


def recreate(neighbors, images, fname):

    if Path(fname).exists():
        with open(fname, 'r') as f:
            d = json.load(f)
            of = d['fixed']
            fixed = {}
            for k, v in of.items():
                fixed[k] = image_to_array(v.split('\n'))
            reconstruction = d['reconstruction']
    else:
        fixed, reconstruction = crawl_neighbors(neighbors, images)

        with open(fname, 'w') as f:
            nf = {}
            for k, v in fixed.items():
                nf[k] = array_to_image(v)

            d = {'fixed': nf, 'reconstruction': reconstruction}
            json.dump(d, f, indent=2)

    outer = None
    temp = None
    prev = 0

    for k, v in sorted(reconstruction.items(), key=lambda x: (x[1][1],x[1][0])):

        if v[1] != prev:
            if outer is None:
                outer = temp
            else:
                outer = np.append(outer, temp, axis=0)
            temp = None

        img = fixed[k][1:-1, 1:-1]

        if temp is None:
            temp = img
        else:
            temp = np.append(temp, img, axis=1)

        prev = v[1]
    outer = np.append(outer, temp, axis=0)

    return outer


def initialize(data):
    images = get_images(data)

    if len(images) == 9:
        fname = 'test_data_neighbors.json'
    else:
        fname = 'day20_neighbors.json'

    if Path(fname).exists():
        with open(fname, 'r') as f:
            nn = json.load(f)
        neighbors = {}
        for k, v in nn.items():
            neighbors[int(k)] = set([int(x) for x in v])
    else:
        neighbors = find_neighbors(images)
        nn = {}
        for k, v in neighbors.items():
            nn[k] = list(v)
        with open(fname, 'w') as f:
            json.dump(nn, f)

    return images, neighbors, fname


def convolve(mask, image):
    x_offset = mask.shape[0]
    y_offset = mask.shape[1]

    y_steps = (image.shape[1] - y_offset) + 1
    x_steps = (image.shape[0] - x_offset) + 1
    if (x_steps <= 0) or (y_steps <= 0):
        raise AttributeError('your mask is bigger than your image')

    matches = 0
    for y in range(y_steps):
        for x in range(x_steps):
            # print(f'{x}:{x + x_offset}, {y}:{y + y_offset}')
            sub = image[x:x + x_offset, y: y + y_offset]
            if np.all((sub * mask) == mask):
                matches += 1
    return matches

def get_answer(data, part2=False):
    images, neighbors, fname = initialize(data)

    if not part2:
        corners = []
        for k, v in neighbors.items():
            if len(v) == 2:
                corners.append(k)
        return np.prod(corners)

    aligned_fname = Path(fname).stem +'_reconstruction.json'
    image = recreate(neighbors, images, aligned_fname)

    mask_template = ['                  # ',
                     '#    ##    ##    ###',
                     ' #  #  #  #  #  #   ']
    mask = image_to_array(mask_template)

    max_serpents = 0
    for i in alterations(image):
        num_serpents = convolve(mask, i)
        if num_serpents > max_serpents:
            max_serpents = num_serpents

    return image.sum() - max_serpents * mask.sum()


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    with open(f'instructions_day_{day}.txt', 'r') as f:
        inputs = f.read().split('\n\n')
    # inputs = get_instructions(year, day)

#     inputs = '''Tile 2311:
# ..##.#..#.
# ##..#.....
# #...##..#.
# ####.#...#
# ##.##.###.
# ##...#.###
# .#.#.#..##
# ..#....#..
# ###...#.#.
# ..###..###

# Tile 1951:
# #.##...##.
# #.####...#
# .....#..##
# #...######
# .##.#....#
# .###.#####
# ###.##.##.
# .###....#.
# ..#.#..#.#
# #...##.#..

# Tile 1171:
# ####...##.
# #..##.#..#
# ##.#..#.#.
# .###.####.
# ..###.####
# .##....##.
# .#...####.
# #.##.####.
# ####..#...
# .....##...

# Tile 1427:
# ###.##.#..
# .#..#.##..
# .#.##.#..#
# #.#.#.##.#
# ....#...##
# ...##..##.
# ...#.#####
# .#.####.#.
# ..#..###.#
# ..##.#..#.

# Tile 1489:
# ##.#.#....
# ..##...#..
# .##..##...
# ..#...#...
# #####...#.
# #..#.#.#.#
# ...#.#.#..
# ##.#...##.
# ..##.##.##
# ###.##.#..

# Tile 2473:
# #....####.
# #..#.##...
# #.##..#...
# ######.#.#
# .#...#.#.#
# .#########
# .###.#..#.
# ########.#
# ##...##.#.
# ..###.#.#.

# Tile 2971:
# ..#.#....#
# #...###...
# #.#.###...
# ##.##..#..
# .#####..##
# .#..####.#
# #..#.#..#.
# ..####.###
# ..#.#.###.
# ...#.#.#.#

# Tile 2729:
# ...#.#.#.#
# ####.#....
# ..#.#.....
# ....#..#.#
# .##..##.#.
# .#.####...
# ####.#.#..
# ##.####...
# ##..#.##..
# #.##...##.

# Tile 3079:
# #.#.#####.
# .#..######
# ..#.......
# ######....
# ####.#..#.
# .#...#.##.
# #.#####.##
# ..#.###...
# ..#.......
# ..#.###...'''.split('\n\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
