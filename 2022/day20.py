from aoc_utilities import get_instructions
from pathlib import Path
from collections import deque


def parse_instructions(data):
    encrypted = deque([])
    encrypted_2 = deque([])
    raw = []
    raw_2 = []
    for i, row in enumerate(data):
        val = int(row)
        encrypted.append((val, i))
        encrypted_2.append((val * 811589153, i))
        raw.append(val)
        raw_2.append(val * 811589153)

    return encrypted, encrypted_2, raw, raw_2


def decrypt_pass(data, raw):
    for i, val in enumerate(raw):
        # rotate the data so the entry at original index
        # i is the leftmost entry
        data.rotate(-data.index((val, i)))
        # remove the entry
        data.popleft()
        # rotate by the number. we need left for positive and
        # right for negative so negate the value
        data.rotate(-val)
        # add the number back in
        data.appendleft((val, i))
    return data


def decrypt(data, raw, n=1):
    for _ in range(n):
        data = decrypt_pass(data, raw)

    decrypted = [x[0] for x in data]
    total = 0
    for offset in (1, 2, 3):
        loc = (decrypted.index(0) + offset * 1000) % len(data)
        total += decrypted[loc]
    return total


def get_answer(data, part2=False):
    encrypted, encrypted_2, raw, raw_2 = parse_instructions(data)
    if part2:
        return decrypt(encrypted_2, raw_2, 10)
    return decrypt(encrypted, raw)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    # inputs = '1, 2, -3, 3, -2, 0, 4'.split(', ')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
