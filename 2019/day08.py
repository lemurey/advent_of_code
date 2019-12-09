from aoc_utilities import get_instructions
import os
from itertools import zip_longest

def grouper(string, n):
    args = [iter(string)] * n
    return zip_longest(*args, fillvalue='')


def parse_data(data, x_dim=25, y_dim=6):
    image = {}
    layer_num = 0
    array = []
    for i, sub in enumerate(grouper(data[0], x_dim), start=1):
        array.append([int(x) for x in sub])
        if i % y_dim == 0:
            image[layer_num] = array
            array = []
            layer_num +=1
    return image

def write_image(image, f_name, show=False):
    with open(f_name, 'w') as f:
        for array in image.values():
            f.write('\n')
            z_count = 0
            for row in array:
                if show:
                    out = ''.join(['█' if x == 0 else ' ' for x in row])
                    f.write(out)
                else:
                    f.write(''.join([str(x) for x in row]))
                f.write('\n')
                z_count += row.count(0)
            f.write(str(z_count))
            f.write('\n')


def decode(image, final_num):
    final = [[2] * 25 for _ in range(6)]
    for i in range(25):
        for j in range(6):
            for k in range(final_num + 1):
                check = image[k][j][i]
                if check == 2:
                    continue
                final[j][i] = check
                break
    return final

def get_answer(data, part2=False):
    image = parse_data(data)


    # write_image(image, 'day_8_test.txt')

    if part2:
        final_num = max(image.keys())
        im = decode(image, final_num)
        write_image({0: im}, 'day_08_part2.txt', show=True)
        return
    min_zeros = len(data[0])
    for layer_num, array in image.items():
        z_count = 0
        for row in array:
            z_count += row.count(0)
        if z_count < min_zeros:
            min_zeros = z_count
            min_layer = layer_num

    ones = 0
    twos = 0
    for row in image[min_layer]:
        ones += row.count(1)
        twos += row.count(2)

    return ones * twos


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
