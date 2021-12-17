from aoc_utilities import get_instructions
from pathlib import Path

from operator import mul
from functools import reduce

CONVERT = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}

OPS = {0: sum,
       1: lambda x: reduce(mul, x),
       2: min,
       3: max,
       5: lambda x: int(x[0] > x[1]),
       6: lambda x: int(x[0] < x[1]),
       7: lambda x: int(x[0] == x[1]),
      }

'''
my original version is commented below
it works on all test cases provided in instructions but fails on
my actual input, I am not sure where it is failing. No errors occur, but
I get the incorrect result. I looked at some solutions and
saw a version similar to the class I wrote below, in particular
keeping track of the global postion and using the read()
operations to update and return the values made the book-keeping
much easier and got me to the correct solution.

It is possible the issue is in how I am doing the conversions
between hex, binary, and base10. I found that calling bin(int(x, 16))
on the main input fails because python removes some zero padding, this
is why I use the CONVERT dictionary instead. it is possible something
similar is happening when I read the values for literals

it is also possible my book-keeping is wrong somehow in the operators
I honestly had some difficulty parsing what I was doing there, I
vastly prefer the class based approach
(actually my original version, long since deleted, was a class,
attempting to use a position tracker, but I couldn't get the recursion
right)
'''

class Packet:
    def __init__(self, string):
        self.bin_val = ''.join(CONVERT[x] for x in string)
        self.pos = 0
        self.versions = []

    def read(self, n):
        return int(self.read_raw(n), 2)

    def read_raw(self, n):
        self.pos += n
        return self.bin_val[self.pos-n:self.pos]

    def get_literal(self):
        val = ''
        while True:
            flag = self.read(1)
            val += self.read_raw(4)
            if flag == 0:
                return int(val, 2)

    def get_operator(self, id_num):
        store = []
        if self.read(1) == 0:
            n = self.read(15)
            limit = self.pos + n
            while self.pos < limit:
                store.append(self.parse())
        else:
            store = [self.parse() for _ in range(self.read(11))]

        return OPS[id_num](store)

    def parse(self):
        version = self.read(3)
        self.versions.append(version)
        id_num = self.read(3)
        if id_num == 4:
            return self.get_literal()
        return self.get_operator(id_num)


# def get_versions(string, convert=False, end=None, versions=None,
#                  num_remain=None, values=None):
#     if convert:
#         bin_val = ''.join(CONVERT[x] for x in string)
#     else:
#         bin_val = string
#     if versions is None:
#         versions = []
#     if values is None:
#         values = []
#     if end is None:
#         end = len(bin_val)

#     pos = 0

#     while True:
#         sub = bin_val[pos:]
#         if sub.strip('0') == '':
#             break

#         version = get_version(sub)
#         id_num = get_id(sub)

#         versions.append(version)

#         if id_num == 4:
#             value, step = get_literal(sub)
#             pos += step
#             if num_remain is not None:
#                 num_remain -= 1
#             values.append(value)
#         else:
#             sub_values, step = get_operator(sub, versions)
#             pos += step

#             value = OPS[id_num](sub_values)
#             values.append(value)

#         if pos >= end:
#             break

#         if num_remain == 0:
#             break

#     return versions, pos, values


# def get_operator(string, versions):
#     start = 6
#     if string[start] == '0':
#         length = int(string[7:22], 2)
#         _, step, values = get_versions(string[22:], end=length,
#                                        versions=versions)
#         start += 22 + step
#     else:
#         num_subs = int(string[7:18], 2)
#         step = 0
#         _, step, values = get_versions(string[18:], versions=versions,
#                                        num_remain=num_subs)
#         start += 18 + step
#     return values, start


# def get_version(string):
#     return int(string[:3], 2)


# def get_id(string):
#     return int(string[3:6], 2)


# def get_literal(string):
#     val = ''
#     for start in range(6, len(string), 5):
#         group = string[start:start + 5]
#         val += group[1:]
#         if group[0] == '0':
#             break
#     return int(val, 2), start


def get_answer(data, part2=False):
    # versions, _, value  = get_versions(data[0], convert=True)
    # return sum(versions), value
    p = Packet(data[0])
    result = p.parse()
    return sum(p.versions), result


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
