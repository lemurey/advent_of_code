from aoc_utilities import get_instructions
import os


class Recipes(object):
    def __init__(self):
        self.elf1 = 0
        self.elf2 = 1
        self.recipes = [3, 7]
        self.count = 0

    def get_next(self):
        e1 = self.recipes[self.elf1]
        e2 = self.recipes[self.elf2]
        num = e1 + e2
        tens = (num / 10) % 10
        ones = num % 10
        if tens != 0:
            self.recipes.append(tens)
        self.recipes.append(ones)

        self.elf1 += (1 + e1)
        self.elf1 %= len(self.recipes)
        self.elf2 += (1 + e2)
        self.elf2 %= len(self.recipes)
        self.count += 1

    def __str__(self):
        out = ''
        for i, val in enumerate(self.recipes):
            if i == self.elf1:
                out += '({})'.format(val)
            elif i == self.elf2:
                out += '[{}]'.format(val)
            else:
                out += ' {} '.format(val)
        return out


def get_answer(data, part2=False):
    r = Recipes()
    d = int(data[0])
    vals = map(int, data[0])
    c = len(vals)
    while True:
        r.get_next()
        if len(r.recipes) >= (d + 10) and (not part2):
            return ''.join(map(str, r.recipes[d:d + 10]))
        elif part2 and (r.recipes[-c:] == vals):
            return len(r.recipes[:-c])
        elif part2 and (r.recipes[(-c - 1):-1] == vals):
            return len(r.recipes[:(-c - 1)])
        if r.count % 1000000 == 0:
            print 'at run {}'.format(r.count)



if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))