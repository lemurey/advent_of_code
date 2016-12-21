from utilities import timeit

class Encoder(object):
    def __init__(self, instructions, string=''):
        self.moves = {'swap position'     : self._swap_position,
                      'swap letter'       : self._swap_letters,
                      'rotate left'       : self._rotate_left,
                      'rotate right'      : self._rotate_right,
                      'rotate based'      : self._rotate_by_x,
                      'reverse positions' : self._reverse,
                      'move position'     : self._move}
        self._parse_instructions(instructions)
        self.string = string

    def _parse_instructions(self, instructions):
        self.operations = []
        for line in instructions.split('\n'):
            words = line.split()
            action = self.moves[' '.join(words[:2])]
            first = int(words[2]) if words[2].isdigit() else words[2]
            second = int(words[-1]) if words[-1].isdigit() else words[-1]
            if len(words) != 7:
                self.operations.append((action, first, second))
            else:
                self.operations.append((action, second, first))

    def _swap_position(self, p1, p2):
        if p1 > p2:
            p1, p2 = p2, p1
        a = self.string[p2]
        b = self.string[p1]
        beginning = self.string[:p1]
        middle = self.string[p1 + 1:p2]
        end = self.string[p2 + 1:]
        self.string = '{}{}{}{}{}'.format(beginning, a, middle, b, end)

    def _swap_letters(self, a, b):
        self.string = self.string.replace(a, '#').replace(b, a).replace('#', b)

    def _rotate_left(self, r, *args):
        r = r % len(self.string)
        self.string = self.string[r:] + self.string[:r]

    def _rotate_right(self, r, *args):
        r = -1 * r % len(self.string)
        self.string = self.string[r:] + self.string[:r]

    def _rotate_by_x(self, a, *args):
        index = self.string.find(a)
        if index >= 4:
            index += 1
        index += 1
        self._rotate_right(index)

    def _reverse(self, p1, p2):
        begin = self.string[:p1]
        swapped = self.string[p1:p2 + 1]
        end = self.string[p2 + 1:]
        self.string = begin + swapped[::-1] + end

    def _move(self, p1, p2):
        a = self.string[p1]
        temp = self.string[:p1] + self.string[p1 + 1:]
        self.string = temp[:p2] + a + temp[p2:]

    def __str__(self):
        return self.string

    def __call__(self, string=None):
        if string:
            self.string = string
        for action, arg1, arg2 in self.operations:
            action(arg1, arg2)


class Decoder(Encoder):
    def __init__(self, instructions, string=None):
        super(Decoder, self).__init__(instructions, string)
        for i, (action, arg1, arg2) in enumerate(self.operations):
            if 'left' in action.__name__:
                self.operations[i] = (self._rotate_right, arg1, arg2)
            elif 'right' in action.__name__:
                self.operations[i] = (self._rotate_left, arg1, arg2)
            elif 'move' in action.__name__:
                self.operations[i] = (action, arg2, arg1)
        self.operations = self.operations[::-1]

    def _rotate_by_x(self, a, *args):
        self._rotate_left(1)
        index = self.string.find(a)
        if index % 2 == 0:
            self._rotate_left(index/2)
        else:
            self._rotate_right((len(self.string) - index)/2)


@timeit
def get_results(instructions, part2=False):
    if part2:
        string = 'fbgdceah'
        helper = Decoder(instructions, string)
    else:
        string = 'abcdefgh'
        helper = Encoder(instructions, string)
    helper()
    return helper


if __name__ == '__main__':
    with open('instructions_day21.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)
