from aoc_utilities import get_instructions
from pathlib import Path
from collections import deque


class Secret:
    def __init__(self, initial):
        self.secret = initial
        self.history = [self.secret]

    def __call__(self):
        self.mix(self.secret * 64)
        self.prune()
        self.mix(self.secret // 32)
        self.prune()
        self.mix(self.secret * 2048)
        self.prune()

    def mix(self, value):
        self.secret = self.secret ^ value

    def prune(self):
        self.secret = self.secret % 16777216

    def __str__(self):
        return str(self.secret)


def get_answer(data, part2=False):
    secrets = []
    bannanas = {}
    for num in data:
        secret = Secret(int(num))
        diff = deque(maxlen=4)
        seen = set()
        for _ in range(2000):
            prev_price = secret.secret % 10
            secret()
            cur_price = secret.secret % 10

            diff.append(cur_price - prev_price)

            if len(diff) == 4:
                last_4 = tuple(diff)

                # can only buy from a monkey once
                if last_4 not in seen:
                    seen.add(last_4)
                    bannanas[last_4] = bannanas.get(last_4, 0) + cur_price

        secrets.append(secret.secret)

    print(sum(secrets))
    return max(bannanas.values())


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''1
# 2
# 3
# 2024'''.split('\n')

    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
