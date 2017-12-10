from aoc_utilities import get_instructions
from functools import reduce
import os


class Knothash:
    def __init__(self, length=256):
        self.list = list(range(length))
        self.skip_size = 0
        self.current_position = 0

    def _get_index(self, index):
        return (self.current_position + index) % len(self.list)

    def _reverse(self, length):
        if self.current_position + length >= len(self.list):
            new_vals = self.list[self.current_position:]
            new_vals += self.list[:self._get_index(length)]
        else:
            new_vals = self.list[self.current_position:self._get_index(length)]

        assert len(new_vals) == length, '{}'.format(self.skip_size)

        new_vals = new_vals[::-1]

        for index in range(length):
            replace = self._get_index(index)
            self.list[replace] = new_vals[index]

    def __call__(self, length):
        self._reverse(length)
        self.current_position = self._get_index(length + self.skip_size)
        self.skip_size += 1

    def check_result(self, part2=False):
        if part2:
            return self._make_dense_hash()
        return self.list[0] * self.list[1]

    def _make_dense_hash(self):
        hash_list = []
        prev_index = 0
        for index in range(16, len(self.list) + 1, 16):
            vals = self.list[prev_index:index]
            hash_list.append(self._xor(vals))
            prev_index = index
        return ''.join('{:02X}'.format(d) for d in hash_list).lower()

    def _xor(self, sub_list):
        return reduce(lambda x, y: x ^ y, sub_list)


def print_list(kh):
    p_string = ''
    for i, val in enumerate(kh.list):
        if i == kh.current_position:
            o = '[{}]'.format(val)
        else:
            o = str(val)
        p_string += '{} '.format(o)
    return p_string


def update_data(data):
    output = []
    for character in data:
        output.append(ord(character))
    output += [17, 31, 73, 47, 23]
    output_string = ('{},' * len(output)).strip(',')
    return output_string.format(*output)


def get_answer(data, part2=False):
    kh = Knothash()
    if part2:
        data = update_data(data)
        num_rounds = 64
    else:
        num_rounds = 1
    for _ in range(num_rounds):
        for entry in data.split(','):
            length = int(entry)
            kh(length)

    return kh.check_result(part2)


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
