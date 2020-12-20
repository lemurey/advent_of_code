from aoc_utilities import get_instructions, timeit
from pathlib import Path
import numpy as np

OFFSETS = {'up': (0, -1), 'left': (-1, 0),
           'down': (0, 1), 'right': (1, 0)}

def image_to_array(image):
    holding = []
    for row in image:
        holding.append([1 if x == '#' else 0 for x in row])
    return np.array(holding)


def array_to_image(array):
    return (str(array).replace('[', '')
                      .replace(']', '')
                      .replace('1', '#')
                      .replace('0', '.')
                      .replace(' ', ''))


class Tile:
    def __init__(self, header, image):
        self.id = int(header.split()[1][:-1])
        self.array = image_to_array(image)
        self.image = array_to_image(self.array)
        self.fixed = False

    def align(self, other):
        for a1 in self:
            for a2 in other:
                c = compare(a1, a2)
                if c in ('up', 'left', 'down', 'right'):
                    break
            else:
                continue
            break
        else:
            return False

        # set this tile and other as fixed
        self.fixed = True
        other.fixed = True

        # update the arrays to the aligned version
        self.array = a1
        other.array = a2

        # update the images based on the array
        self.image = array_to_image(self.array)
        other.image = array_to_image(other.array)

        # set the x and y cooordinate of the other tile
        dx, dy = OFFSETS[c]
        other.x = self.x + dx
        other.y = self.y + dy
        return True

    def __iter__(self):
        if self.fixed:
            yield self.array
            return
        for rot in range(4):
            yield np.rot90(self.array, rot)
            yield np.flipud(np.rot90(self.array, rot))
            yield np.fliplr(np.rot90(self.array, rot))

    def __str__(self):
        return self.image


class Image:
    def __init__(self, data):
        self.tiles = self._make_tiles(data)
        self.image = None

    def _make_tiles(self, data):
        tiles = {}
        for row in data:
            rows = row.split('\n')
            tile = Tile(rows[0], rows[1:])
            tiles[tile.id] = tile

        self.keys = list(tiles.keys())
        return tiles

    def _crawl_tiles(self):
        # grab the first tile and define it at 0, 0
        start = self[0]
        start.x = 0
        start.y = 0

        q = [start]

        num_aligned = 1
        while num_aligned < len(self.tiles):
            current = q.pop()

            for tile in self:
                if (tile.id == current.id) or (current.fixed and tile.fixed):
                    continue

                if current.align(tile):
                    num_aligned += 1
                    q.append(tile)

    def _reconstruct(self):
        outer = None
        temp = None
        prev = None
        for tile in sorted(self, key=lambda t: (t.y, t.x)):
            if tile.y != prev:
                if outer is None:
                    outer = temp
                else:
                    outer = np.append(outer, temp, axis=0)
                temp = None

            if temp is None:
                temp = tile.array[1:-1, 1:-1]
            else:
                temp = np.append(temp, tile.array[1:-1, 1:-1], axis=1)
            prev = tile.y

        outer = np.append(outer, temp, axis=0)

        image = array_to_image(outer)
        self.image = Tile('Tile -1:', image.split('\n'))
        ## calling string on a large array yields truncated arrays by default
        ## so my array_to_image function fails on the full size image, manually
        ## convert it instead
        self.image.array = outer
        im = []
        for row in outer:
            im.append(''.join(['#' if x == 1 else '.' for x in row]))
        self.image.image = '\n'.join(im)

    def get_corners(self):
        if self.image is None:
            self.reconstruct

        min_x = min(self, key=lambda t: t.x).x
        max_x = max(self, key=lambda t: t.x).x
        min_y = min(self, key=lambda t: t.y).y
        max_y = max(self, key=lambda t: t.y).y

        corners = []
        for tile in self:
            if ((tile.x == min_x or tile.x == max_x) and
                (tile.y == min_y or tile.y == max_y)):
                corners.append(tile)
        return corners

    def reconstruct(self):
        self._crawl_tiles()
        self._reconstruct()

    def __str__(self):
        if self.image is None:
            return 'Image reconstruction has not been run'
        return self.image.image

    def __iter__(self):
        for k in self.keys:
            yield self.tiles[k]

    def __getitem__(self, index):
        if index in self.tiles:
            return self.tiles[index]
        else:
            return self.tiles[self.keys[index]]


def get_edges(image):
    top = image[0, :]
    bottom = image[-1, :]
    left = image[:, 0]
    right = image[:, -1]
    return top, bottom, left, right


def compare(tile1, tile2):
    t1, b1, l1, r1 = get_edges(tile1)
    t2, b2, l2, r2 = get_edges(tile2)

    if np.all(t1 == b2):
        return 'up'
    if np.all(r1 == l2):
        return 'right'
    if np.all(l1 == r2):
        return 'left'
    if np.all(b1 == t2):
        return 'down'


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
            sub = image[x:x + x_offset, y: y + y_offset]
            if np.all((sub * mask) == mask):
                matches += 1
    return matches


def get_answer(inputs, part2=False):
    image = Image(inputs)
    image.reconstruct()

    corners = [x.id for x in image.get_corners()]

    print(np.prod(corners))

    mask = image_to_array(['                  # ',
                           '#    ##    ##    ###',
                           ' #  #  #  #  #  #   '])

    max_serpents = 0
    for i in image.image:
        num_serpents = convolve(mask, i)
        if num_serpents > max_serpents:
            max_serpents = num_serpents

    return image.image.array.sum() - max_serpents * mask.sum()


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

    # print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
