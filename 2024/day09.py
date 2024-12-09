from aoc_utilities import get_instructions
from pathlib import Path


def make_filemap(data):
    file_map = []
    dots = []
    file_id = -1
    for i, char in enumerate(data[0]):
        if i % 2 == 0:
            file_id += 1
            to_add = (file_id, char)
        else:
            to_add = ('.', char)
        file_map.append(to_add)

    expanded = []
    index = 0
    for (char, length) in file_map:
        for _ in range(int(length)):
            expanded.append(char)
            if char == '.':
                dots.append(index)
            index += 1

    return file_map, dots, expanded


def _swap(arr, il, ir):
    vl = arr[il]
    vr = arr[ir]
    arr[il] = vr
    arr[ir] = vl
    return arr


def run_compress(expanded, dots):
    dot_index = 0
    first_dot = dots[dot_index]
    position = len(expanded) - 1

    count = 0
    while first_dot < position:
        count += 1
        if count > 100000:
            break
        # if postion is a dot, move left and loop
        # otherwise swap with first_dot, increment first_dot, decrease position
        if expanded[position] == '.':
            position -= 1
            continue
        else:
            expanded = _swap(expanded, first_dot, position)
            position -= 1
            dot_index += 1
            first_dot = dots[dot_index]

    return expanded


def _update(arr, start_index, id_num, length, position):
    for i in range(length):
        arr = _swap(arr, start_index+i, position-i)
    return arr


def run_compress_v2(file_map, expanded, dots):
    # make dots more useful
    d2 = []
    prev = None
    for val in dots:
        if prev is None:
            prev = val
            first = val
            length = 1
            continue
        if val - prev > 1:
            d2.append((first, length))
            prev = val
            first = val
            length = 1
            continue
        else:
            length += 1
        prev = val
    d2.append((first, length))

    # iterate over file backwards:
    compressed = expanded[:]
    position = len(expanded) - 1

    for (id_num, length) in file_map[::-1]:
        length = int(length)
        # for empty blocks move past them
        if id_num == '.':
            position -= length
            continue
        # iterate over d2, if there is enough space for the file, insert it
        # in the appropriate location and update the d2 entry to 
        for i, (start, dot_length) in enumerate(d2):
            # only move blocks to the left
            if start >= position:
                mod_index = None
                break
            if dot_length >= length:
                compressed = _update(compressed, start, id_num, length, position)
                position -= length
                mod_index = i
                break
        else:
            mod_index = None

        if mod_index is not None:
            if dot_length == length:
                d2.pop(mod_index)
            else:
                d2[mod_index] = (start + length, dot_length - length)
        else:
            position -= length

    return compressed


def get_answer(data, part2=False):
    file_map, dots, expanded = make_filemap(data)
    compressed = run_compress(expanded[:], dots)

    compressed_v2 = run_compress_v2(file_map, expanded, dots)

    with open('initial.txt', 'w') as f:
        f.write(','. join(str(x) for x in expanded))

    with open('temp.txt', 'w') as f:
        f.write(','. join(str(x) for x in compressed_v2))

    with open('f_map.txt', 'w') as f:
        for (id_num, length) in file_map:
            f.write(f'{id_num}, {length}\n')

    check_sum = 0
    for i, val in enumerate(compressed):
        if val != '.':
            check_sum += i * int(val)
    print(check_sum)
    check_sum = 0
    for i, val in enumerate(compressed_v2):
        if val != '.':
            check_sum += i * int(val)
    return check_sum


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

    # inputs = ['2333133121414131402']

    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
