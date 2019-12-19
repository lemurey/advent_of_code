from aoc_utilities import get_instructions
import os
from itertools import cycle


def get_ones(x):
    return int(str(x)[-1])

def phases():
    base = [0, 1, 0, -1]
    index = 0
    while True:
        vals = []
        for entry in base:
            vals.extend([entry] * (index + 1))
        yield cycle(vals)
        index += 1


def FFT(pattern):
    orig = list(map(int, pattern))
    spots = len(orig)

    output = orig[:]
    while True:
        phase = phases()
        new = [0] * spots
        for i in range(spots):
            p = next(phase)
            next(p) # skip the first entry in the new phase
            new[i] = get_ones(sum([a * b for a, b in zip(output, p)]))
        output = new[:]
        yield output


def after_100(pattern, offset=0, verbose=False):
    gen = FFT(pattern)
    for _ in range(100):
        o = next(gen)
        if verbose:
            t = [str(x) for x in o[-100:]]
            print(''.join(t))

    return o[offset:offset + 8]


class FastFFT:
    def __init__(self, pattern, message_size=8, offset_digits=7,
                 multiplier=10000):
        base = list(map(int, pattern))
        # get the offset
        message_offset = int(pattern[:offset_digits])
        full_length = len(base) * multiplier
        # to solve based on the pattern match, need to work in only second
        # half of pattern
        if message_offset < (full_length // 2):
            raise Exception('Cannot solve in fast way')
        length_needed = full_length - message_offset
        # math.ceil without importing math
        to_copy, rem = divmod(length_needed, len(base))
        if rem != 0:
            to_copy += 1
        # create a copy of the data
        input_data = base * to_copy
        # create the pattern to work from
        # self.pattern = base
        self.pattern = input_data[-length_needed:]
        self.message_size = message_size

    def _run_phases(self, num_to_run):
        '''
        for this we don't do the full calculation, instead rely on the
        pattern, last n digits only depend on the last n-1 digits of previous
        run. So we run over the data backwards, and each iteration update the
        nth from the last spot with the ones digit of the running total
        '''
        data = self.pattern[:]
        for _ in range(num_to_run):
            running_total = 0
            # iterate over the data backwards
            for index in range(len(data) - 1, -1, -1):
                running_total += data[index]
                # now replace data with the ones digit of the running total
                update = running_total % 10
                data[index] = update
        return data

    def __call__(self, num_to_run):
        output = self._run_phases(num_to_run)
        message = [str(x) for x in output[:self.message_size]]
        return ''.join(message)


# import math
# class FastFFT:
#     BASE_PATTERN = [1, 0, -1, 0]
#     MULTIPLIER = 10000
#     NUM_OFFSET_DIGITS = 7
#     MESSAGE_SIZE = 8

#     def __init__(self, input_data):
#         message_offset = int(input_data[:self.NUM_OFFSET_DIGITS])
#         input_data = [int(d) for d in input_data]
#         data_length = len(input_data) * self.MULTIPLIER
#         assert message_offset > data_length / 2,\
#         'There is no fast way to solve this'
#         necessary_length = data_length - message_offset
#         num_copies = math.ceil(necessary_length / len(input_data))
#         input_data = input_data * num_copies
#         self.input_data = input_data[-necessary_length:]
#         print(necessary_length, num_copies, len(self.input_data))


#     def get_message(self, num_phases):
#         output = self._calculate(num_phases)
#         message = ''.join([str(d) for d in output[:self.MESSAGE_SIZE]])
#         return message

#     def _calculate(self, num_phases):
#         data = self.input_data
#         for i in range(0, num_phases):
#             sum = 0
#             for j in range(len(data) - 1, -1, -1):
#                 sum += data[j]
#                 data[j] = sum % 10
#         return data


def get_answer(data, part2=False):
    pat = data[0]
    if part2:
        FFT = FastFFT(pat)
        return FFT(100)
    output = [str(x) for x in after_100(pat)]
    return ''.join(output)


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
