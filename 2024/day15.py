from aoc_utilities import get_instructions
from pathlib import Path
# import sys
# print(sys.getrecursionlimit())
# sys.setrecursionlimit(int(1e6))


class Thing:
    dirs = {'<': -1, '>': 1, '^': -1j, 'v': 1j}

    def move(self, direction, grid):
        next_spot = self.loc + self.dirs[direction]
        # if next spot doesn't exist or is a wall do nothing
        if next_spot not in grid or grid[next_spot] == '#':
            return -1
        # if next spot is empty, move into it mark current spot empty
        if grid[next_spot] == '.':
            grid[next_spot] = self
            grid[self.loc] = '.'
            self.loc = next_spot
            return 1
        # if next spot is a box, try to move it, then try to move yourself
        if isinstance(grid[next_spot], Box):
            check = grid[next_spot].move(direction, grid)
            if check == -1: # next object cannot be moved
                return -1
            return self.move(direction, grid)

    def __eq__(self, other):
        if not isinstance(other, Thing):
            return False
        return self.loc == other.loc

    def __hash__(self):
        return hash((self.loc, self.symbol))


class Robot(Thing):
    def __init__(self, loc):
        self.loc = loc
        self.symbol = '@'

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.symbol


class Box(Thing):
    def __init__(self, loc):
        self.loc = loc
        self.symbol = 'O'

    def value(self):
        return int(self.loc.real) + 100 * int(self.loc.imag)

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.symbol


class Boxl(Box):
    def __init__(self, loc):
        self.loc = loc
        self.symbol = '['
        self.partner = None

    def set_partner(self, other):
        self.partner = other

    def _basic_check(self, spot, grid):
        if spot not in grid or grid[spot] == '#':
            return -1
        if grid[spot] == '.':
            return 1
        return 0

    def check_move(self, direction, grid, moves):
        next_spot = self.loc + self.dirs[direction]
        last_spot = self.loc - self.dirs[direction]
        partner_spot = self.partner.loc + self.dirs[direction]

        next_check = self._basic_check(next_spot, grid)
        partner_check = self._basic_check(partner_spot, grid)
        if next_check == -1:
            return moves + [-1]
        elif next_check == 1:
            # if partner is right behind you you can both move
            if last_spot in grid and grid[last_spot] == self.partner:
                return moves + [self.loc, self.partner.loc]
            # check partner movement
            if partner_check == -1:
                return moves + [-1]
            elif partner_check == 1:
                moves = moves + [self, self.partner]
            else:
                moves = grid[partner_spot].check_move(direction, grid, moves)
                if moves[-1] == -1:
                    return moves
                else:
                    moves = moves + [self, self.partner]

        # if the next spot is your partner check it's spot
        elif grid[next_spot] == self.partner:
            if partner_check == -1:
                return moves + [-1]
            elif partner_check == 1:
                moves = moves + [self, self.partner]
            else:
                moves = grid[partner_spot].check_move(direction, grid, moves)
                if moves[-1] == -1:
                    return moves
                else:
                    moves = moves + [self, self.partner]
        else:
            # we can get here an not have checked the partner
            if partner_check == -1:
                return moves + [-1]
            elif partner_check == 1:
                moves = moves + [self, self.partner]
            else:
                moves = grid[partner_spot].check_move(direction, grid, moves)
                if moves[-1] == -1:
                    return moves
                else:
                    moves = moves + [self, self.partner]
            moves = grid[next_spot].check_move(direction, grid, moves)
            if moves[-1] == -1:
                return moves
            else:
                moves = moves + [self, self.partner]
        return moves

    def run_moves(self, direction, grid, moves):
        moves = set(moves)
        # if any moves were invalid, cancel all of them
        if any([x == -1 for x in moves]):
            return -1

        # if any([isinstance(x, complex) for x in moves]):
        #     print_grid(grid)
        # print(direction, [x.loc for x in moves])

        # sort the moves based on direction
        if direction == '<':
            to_move = sorted(moves, key=lambda move: move.loc.real)
        elif direction == '>':
            to_move = sorted(moves, key=lambda move: -move.loc.real)
        elif direction == '^':
            to_move = sorted(moves, key=lambda move: move.loc.imag)
        else:
            to_move = sorted(moves, key=lambda move: -move.loc.imag)

        # print(direction, [x.loc for x in to_move])

        for box in to_move:
            next_spot = box.loc + self.dirs[direction]
            grid[next_spot] = box
            grid[box.loc] = '.'
            box.loc = next_spot
        return 1

    def move(self, direction, grid, moves=None):
        if moves is None:
            moves = []
        moves = self.check_move(direction, grid, moves)
        return self.run_moves(direction, grid, moves)


class Boxr(Boxl):
    def __init__(self, loc):
        self.loc = loc
        self.symbol = ']'


def make_grid(data, part2=False):
    grid = {}
    moves = []
    boxes = []
    for y, row in enumerate(data):
        offset = 0
        for x, val in enumerate(row):
            if val == '\n':
                continue
            if val in '<^>v':
                moves.append(val)
                continue
            p = x + offset + y*1j
            if val == '@':
                robot = Robot(p)
                to_add = robot
            elif val == 'O':
                if part2:
                    box = Boxl(p)
                else:
                    box = Box(p)
                boxes.append(box)
                to_add = box
            else:
                to_add = val

            grid[p] = to_add
            if part2:
                if isinstance(to_add, Robot):
                    grid[p + 1] = '.'
                elif isinstance(to_add, Box):
                    boxr = Boxr(p + 1)
                    box.set_partner(boxr)
                    boxr.set_partner(box)
                    grid[p + 1] = boxr
                else:
                    grid[p + 1] = to_add
                offset += 1
    return grid, moves, boxes, robot


def print_grid(grid):
    max_x = int(max(x.real for x in grid))
    max_y = int(max(y.imag for y in grid))
    out = ''
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            p = x + y*1j
            out += str(grid[p])
        out += '\n'
    print(out)


def get_answer(data, part2=False):

    grid, moves, boxes, robot = make_grid(data, part2)

    # print_grid(grid)

    for move in moves:
        # print(move)
        robot.move(move, grid)
        # print_grid(grid)
        # break


    return sum(b.value() for b in boxes)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''##########
# #..O..O.O#
# #......O.#
# #.OO..O.O#
# #..O@..O.#
# #O#..O...#
# #O..O..O.#
# #.OO.O.OO#
# #....O...#
# ##########

# <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
# vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
# ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
# <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
# ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
# ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
# >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
# <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
# ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
# v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^'''.split('\n')

#     inputs = '''#######
# #...#.#
# #.....#
# #..OO@#
# #..O..#
# #.....#
# #######

# <vv<<^^<<^^'''.split('\n')

    # print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
