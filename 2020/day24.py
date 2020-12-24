from aoc_utilities import get_instructions
from pathlib import Path


DIRECTIONS = {'nw': (0, 1, -1),
              'ne': (1, 0, -1),
              'e': (1, -1, 0),
              'se': (0, -1, 1),
              'sw': (-1, 0, 1),
              'w': (-1, 1, 0)}


class Tile:
    def __init__(self, x, y, z, color='w', id=None):
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        self.location = (x, y, z)
        self.id = id

    def visit(self):
        if self.color == 'w':
            self.color = 'b'
        else:
            self.color = 'w'

    def get_neighbor(self, direction):
        dx, dy, dz = DIRECTIONS[direction]
        nx = self.x + dx
        ny = self.y + dy
        nz = self.z + dz
        return (nx, ny, nz)

    def neighbors(self):
        for dx, dy, dz in DIRECTIONS.values():
            nx = self.x + dx
            ny = self.y + dy
            nz = self.z + dz
            yield (nx, ny, nz)

class Grid:
    def __init__(self, instructions):
        self.instructions = instructions
        self.grid = {(0, 0, 0): Tile(0, 0, 0)}
        self.max_id = 0

    def count(self):
        count = 0
        for tile in self.grid.values():
            if tile.color == 'b':
                count += 1
        return count

    def setup(self):
        for row in self.instructions:
            tile = self.grid[(0, 0, 0)]
            for direction in row:
                location = tile.get_neighbor(direction)
                if location not in self.grid:
                    self.grid[location] = Tile(*location, id=self.max_id)
                    self.max_id += 1
                tile = self.grid[location]
            tile.visit()

    def _expand_grid(self):
        adds = []
        for tile in self.grid.values():
            for location in tile.neighbors():
                if location not in self.grid:
                    adds.append(location)

        for location in adds:
            self.grid[location] = Tile(*location, id=self.max_id)
            self.max_id += 1

    def run(self):
        self._expand_grid()
        flips = []
        for tile in self.grid.values():
            n_count = 0
            for location in tile.neighbors():
                if location not in self.grid:
                    continue
                neighbor = self.grid[location]
                if neighbor.color == 'b':
                    n_count += 1
            if ((tile.color == 'b' and ((n_count == 0) or (n_count > 2))) or
                ((tile.color == 'w') and (n_count == 2))):
                flips.append(tile)

        for tile in flips:
            tile.visit()


def parse_inputs(data):
    instructions = []
    for line in data:
        current = []
        skip = False
        for i in range(len(line)):
            if skip:
                skip = False
                continue
            if line[i] in 'sn':
                direction = line[i: i+2]
                skip = True
            else:
                direction = line[i]
            current.append(direction)
        instructions.append(current)
    return instructions


def get_answer(data, part2=False):
    instructions = parse_inputs(data)
    grid = Grid(instructions)
    grid.setup()

    print(grid.count())

    for i in range(100):
        grid.run()

    return grid.count()


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''sesenwnenenewseeswwswswwnenewsewsw
# neeenesenwnwwswnenewnwwsewnenwseswesw
# seswneswswsenwwnwse
# nwnwneseeswswnenewneswwnewseswneseene
# swweswneswnenwsewnwneneseenw
# eesenwseswswnenwswnwnwsewwnwsene
# sewnenenenesenwsewnenwwwse
# wenwwweseeeweswwwnwwe
# wsweesenenewnwwnwsenewsenwwsesesenwne
# neeswseenwwswnwswswnw
# nenwswwsewswnenenewsenwsenwnesesenew
# enewnwewneswsewnwswenweswnenwsenwsw
# sweneswneswneneenwnewenewwneswswnese
# swwesenesewenwneswnwwneseswwne
# enesenwswwswneneswsenwnewswseenwsese
# wnwnesenesenenwwnenwsewesewsesesew
# nenewswnwewswnenesenwnesewesw
# eneswnwswnwsenenwnwnwwseeswneewsenese
# neswnwewnwnwseenwseesewsenwsweewe
# wseweeenwnesenwwwswnew'''.split('\n')

    print(get_answer(inputs))
