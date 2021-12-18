from aoc_utilities import get_instructions
from pathlib import Path
from math import floor, ceil
from operator import add
from functools import reduce

class SnailFish:
    flip = {'left': 'right', 'right': 'left'}
    def __init__(self, val):
        assert len(val) == 2
        if isinstance(val[0], SnailFish) or isinstance(val[0], int):
            self.left = val[0]
        else:
            self.left = SnailFish(val[0])
        if isinstance(val[1], SnailFish) or isinstance(val[1], int):
            self.right = val[1]
        else:
            self.right = SnailFish(val[1])
        self.left_level = self._get_left_level()
        self.right_level = self._get_right_level()
        self.max_level = max(self.left_level, self.right_level)
        self.changed = False
        self.explode()
        # if self.max_level == 4:
        #     self.explode()
        # self.reduce()

    @property
    def child(self):
        if self.left_level > self.right_level:
            return self.left
        elif self.right_level > self.left_level:
            return self.right
        else:
            return self.left

    @property
    def magnitude(self):
        if isinstance(self.left, int):
            l = self.left
        else:
            l = self.left.magnitude
        if isinstance(self.right, int):
            r = self.right
        else:
            r = self.right.magnitude
        return (3 * l) + (2 * r)

    def _get_left_level(self):
        if not isinstance(self.left, SnailFish):
            return 0
        else:
            val = max(self.left.left_level, self.left.right_level)
            return val + 1

    def _get_right_level(self):
        if not isinstance(self.right, SnailFish):
            return 0
        else:
            val = max(self.right.left_level , self.right.right_level)
            return val + 1

    def __add__(self, other):
        return SnailFish([[self.left, self.right], other])

    def _get_level(self, l):
        cur = self
        for _ in range(l):
            cur = cur.child
        return cur

    def _get_extreme(self, level, which):
        check = getattr(level, which)
        while not isinstance(check, int):
            try:
                level = check
                check = getattr(check, which)
            except:
                print('did this happen')
        if isinstance(check, int):
            return level
        return None

    def _get_explode_number(self, which):
        cur = self._get_level(4)
        for l in range(3, -1, -1):
            pos = self._get_level(l)
            check = getattr(pos, which)
            if isinstance(check, int):
                return pos, 'n'
            elif check != cur:
                return self._get_extreme(check, self.flip[which]), 'f'
            else:
                cur = pos
        return None, 'n'

    def explode(self):
        if self.max_level == 4:
            self._explode()

    def _explode(self):
        cur = self._get_level(4)
        base = self._get_level(3)
        l, lw = self._get_explode_number('left')
        r, rw = self._get_explode_number('right')
        if l is not None:
            if lw == 'f':
                l.right += cur.left
            else:
                l.left += cur.left
        if r is not None:
            if rw == 'f':
                r.left += cur.right
            else:
                r.right += cur.right
        if cur == base.left:
            base.left = 0
        else:
            base.right = 0
        return self.__init__(eval(str([self.left, self.right])))

    def __iter__(self):
        if isinstance(self.left, int):
            yield self.left, self
        else:
            yield from self.left
        if isinstance(self.right, int):
            yield self.right, self
        else:
            yield from self.right

    def split(self):
        for val, level in self:
            if val > 9:
                nl = floor(val / 2)
                nr = ceil(val / 2)
                replacement = SnailFish([nl, nr])
                if val == level.left:
                    level.left = replacement
                else:
                    level.right = replacement
                return self.__init__(eval(str([self.left, self.right])))

    def __str__(self):
        return str([self.left, self.right])

    def __repr__(self):
        return str([self.left, self.right])


def get_fishes(data):
    out = []
    for line in data:
        out.append(SnailFish(eval(line)))
    return out


def add_fishes(fish1, fish2):
    f1c = SnailFish(eval(str(fish1)))
    f2c = SnailFish(eval(str(fish2)))
    r = f1c + f2c
    prev = None
    while str(r) != str(prev):
        prev = SnailFish(eval(str(r)))
        r.split()
        # print(r)
    return r


def get_answer(data, part2=False):
    fishes = get_fishes(data)
    if part2:
        largest = 0
        for f1 in fishes:
            for f2 in fishes:
                c = add_fishes(f1, f2).magnitude
                if c > largest:
                    largest = c
        return largest

    result = reduce(add_fishes, fishes)
    return result.magnitude


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
# [[[5,[2,8]],4],[5,[[9,9],0]]]
# [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
# [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
# [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
# [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
# [[[[5,4],[7,7]],8],[[8,3],8]]
# [[9,3],[[9,9],[6,[4,9]]]]
# [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
# [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
