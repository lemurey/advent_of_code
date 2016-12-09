test_room = 'aaaaa-bbb-z-y-x-123[abxyz]'

with open('instructions_day4.txt', 'r') as f:
    instructions = f.read().strip()

def parse_room(room):
    pre, post = room.split('[')
    checksum = post[:-1]
    split_ind = -1 * pre[::-1].find('-')
    letters = pre[:split_ind]
    id_num = int(pre[split_ind:])
    return letters, id_num, checksum


def count_letters(letters):
    count = {}
    for char in letters:
        if char == '-':
            continue
        if char in count:
            count[char] += 1
        else:
            count[char] = 1
    return count


def check_room(room):
    letters, id_num, checksum = parse_room(room)
    count = count_letters(letters)
    sorted_count = sorted(count.iteritems(), key=lambda x: (-x[1], x[0]))[:5]
    check = ''.join(x[0] for x in sorted_count)
    if check == checksum:
        return letters, id_num
    else:
        return 0, 0


def get_name(encrypted, id_num):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    output = ''
    for char in encrypted:
        if char == '-':
            output += ' '
            continue
        cur_ind = alphabet.find(char)
        output += alphabet[(cur_ind + id_num) % 26]
    return output


def find_sector_id(letters, id_num):
    name = get_name(letters, id_num)
    if 'northpole' in name:
        print name, id_num


def get_results(instructions):
    valid = map(check_room, instructions)
    print sum(x[1] for x in valid)
    for encrypted, id_num in valid:
        if encrypted != 0:
            find_sector_id(encrypted, id_num)


if __name__ == '__main__':
    get_results(instructions.split('\n'))
