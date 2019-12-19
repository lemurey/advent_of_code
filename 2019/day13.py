from aoc_utilities import get_instructions
import os, sys, time
from intcode import Intcode
from random import randint


class Tile:
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.type = self._set_type(num)

    def _set_type(self, num):
        if num == 0:
            return ' '
        if num == 1:
            return '|'
        if num == 2:
            return 'B'
        if num == 3:
            return '_'
        if num == 4:
            return 'o'

    def __eq__(self, other):
        return (self.type == other.type and
                self.x == other.x and
                self.y == other.y
               )


class Cabinet:
    def __init__(self, program, mode='fixed', show=False):
        self.core = Intcode(program=program, mode='robot')
        self.mode = mode
        self.grid = {}
        self.score = 0
        self.direction = 0
        self.num_blocks = 0
        self.pred_dir = 0
        self.draw = False
        self.show = show
        self.min_y = None
        self.iters = 0
        self.score_deltas = set()

    def _get_three(self):
        num_ = 0
        outs = []
        while num_ < 3:
            out = self.core.run()
            self.core.waiting = False
            outs.append(out)
            num_ += 1
        return outs

    def run(self):
        while not self.core.halted:
            self.step()

    def test(self, num_iters):
        # self.core.debug = True
        self.iters = 0
        while not self.core.halted:
            self.step()
            self.iters += 1
            if self.iters == num_iters:
                break

    def step(self):
        if self.mode == 'random':
            self.core.secondary = randint(-1, 1)
        if self.mode == 'fixed':
            self.core.secondary = 0
        if self.mode == 'ai':
            self.core.secondary = self.pred_dir

        x, y, num = self._get_three()
        if x == -1 and y == 0:
            prev_score = self.score
            self.score = num
            score_delta = num - prev_score
            self.score_deltas.add(score_delta)
        elif (x, y) in self.grid:
            self._update(x, y, num)
            self.draw = True
        else:
            self.grid[(x, y)] = Tile(x, y, num)
            if self.grid[(x, y)].type == 'B':
                self.num_blocks += 1
            elif self.grid[(x, y)].type == 'o':
                self.ball_pos = (x, y)
            elif self.grid[(x, y)].type == '_':
                self.paddle_pos = (x, y)
        if self.draw and self.show:
            self.show_grid()

    def _get_velocity(self, x, y):
        self.vx = x - self.ball_pos[0]
        self.vy = y - self.ball_pos[1]

    def _calc_move(self, x, y):
        if self.vy < 0:
            mod = 2
        else:
            mod = 1
        height_dif = self.paddle_pos[1] - self.ball_pos[1]
        pred_x = self.ball_pos[0] + (height_dif * self.vx * mod)
        if self.paddle_pos[0] < pred_x:
            return 1
        if self.paddle_pos[0] > pred_x:
            return -1
        if self.paddle_pos[0] > 20:
            return -1
        if self.paddle_pos[1] < 20:
            return 1
        return 0

    def _update(self, x, y, num):
        new = Tile(x, y, num)
        prev = self.grid[(x, y)]
        if new == prev:
            return
        if new.type == 'o':
            self._get_velocity(x, y)
            self.pred_dir = self._calc_move(x, y)
            self.ball_pos = (x, y)
        if new.type == '_':
            self.paddle_pos = (x, y)
        if prev.type == 'B':
            if new.type != 'B':
                self.num_blocks -= 1
        self.grid[(x, y)] = new

    def show_grid(self):
        os.system('clear')
        if self.min_y is None:
            self.min_y = int(min(self.grid, key=lambda x: x[1])[1])
            self.max_y = int(max(self.grid, key=lambda x: x[1])[1])
            self.min_x = int(min(self.grid, key=lambda x: x[0])[0])
            self.max_x = int(max(self.grid, key=lambda x: x[0])[0])
        out = ''
        for y in range(self.min_y, self.max_y + 1):
            row = ''
            for x in range(self.min_x, self.max_x + 1):
                position = (x, y)
                if position in self.grid:
                    val = self.grid[position]
                else:
                    val = ' '
                row += val.type
            out += row
            out += '\n'
        out += '{}, {}'.format(self.score, self.num_blocks)
        if self.iters > 0:
            out += ', {}'.format(self.iters)
        out += '\n'
        sys.stdout.write(out)
        sys.stdout.flush()
        return



def get_answer(data, part2=False):
    program = list(map(int, data[0].split(',')))
    arcade = Cabinet(program, mode='ai', show=False)
    if part2:
        arcade.core.program[0] = 2
        arcade.run()
        return arcade.score
    arcade.run()
    return arcade.num_blocks


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
