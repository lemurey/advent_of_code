from aoc_utilities import get_instructions
import os


'''
trying to work through the number theory version of this.
idea is represent the deck by (a, b), N. a is the first postion, b is how big
to step, n is the length of the deck. So, the starting deck is (0, 1), 10007.
becuase we start at zero, go up 1 each time and it is 10007 cards.

** Important note, everything is mod n. so to use an example, a 10 card deck that
was
[0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
would be (0, 3), 10

okay, so now lets think about operations:
deal into new stack:
    this is pretty easy, we are just reversing the deck, so all we need to do
    is flip b (b = -b), but we also need to make the first card the last card,
    we can do this by adding the new b value to a
    so (0, 1) becomes (-1, -1) (note that offset an be negative, works like a python)
    list, where -1 means the last value

    for the example above
    [0, 3, 6, 9, 2, 5, 8, 1, 4, 7] becomes
    [7, 4, 1, 8, 5, 2, 9, 6, 3, 0]
    before it was (0, 3), now it is (-3, -3)

    in code:
    b = (b * -1) % N
    a = (a + b) % N

cut n cards:
    shift the list around, all we are doing here is modifying offset, specifially
    we are moving the nth card to the start of the list, the nth card is
    a + b * n, we are also modifying all cards by that new index (everything is
    just moving over, the wrapping comes about because of the modulus)

    [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
    if we cut by 3 becomes:
    [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]
    this is (9, 3), 10

    (0 + 3 * 3) % 10 = 9, so a (was 0) becomes 9

    in code:
    a = (a + b * n) % N

deal with increment n:
    this is the trickiest one. for this one a does not change, but b does.
    the 0th card stays the 0th (that's what i mean by a does not change) but
    then what was the 1st card becomes the nth, the 2nd becomes (2 * n)th and
    so on. so the ith card is now (i * n)th card (this seems simlar to the cut
    modification, but instead of modifying a by i * n, we are modifying
    the b this way)

    but, doing the operation this way iteratively is slow, we want something fast
    so lets think about it this way, we want to kno when i * n = 1 (when is the
    ith card the first card), so this becomes i = 1 / n

    one again we need to do all this in terms of the modulus, so we are now in
    the realm of modular inverses. because the numbers we are using
    10007 and 119315717514047 are prime we can use fermat's little thereom to
    help out. fermat's little therom says for a prime number then for any
    integer a ** p = a MOD p
    this means a ** (p - 1) = 1 mod p, this means we can calculate the modular
    inverse of n as n ** (N - 2) MOD N
    we are in luck that python has built in support for this so in code we just
    need pow(n, N-2, N)

    since we know that the first card became the MODINV(n)th card, the 2nd card
    became the (b * MODINV(n))th card so the end result of this operation
    is to set b = b * MODINV(n)

    in code:
    b *= MODINV(n)


for the large number of iterations:
    the first time you run through a series of steps you will have modified
    a and b.

    if you look at the code, b is only every multiplied by -1 or MODINV(n) where
    n is an input to the shuffle procedure. so b is modified by constants at each
    point and that cna pretty clearly be combined into one modification

    a is always modified by adding a multiple of b to it. but it is the value
    of b at each step, so in theory this is not reducible to a single operation:
    however, because b is modified by a constant at each step it is possible to
    collapse the change to a by adding some multiple of b at the starting point

    so, run through the shuffle once (starting with a=0 and b=1) and find the
    values of a and b at the end of that process (call them a_diff and b_mul).
    then for any given shuffle we can calculate the outcome by doing
    a = a + (b * a_diff) (so we multiple the current b by the a delta and add it
    back in)
    b = b * b_mul
    once again these are done MOD N. so now we can do a whole shuffle as one
    quick operation, but if we want to repeat 101741582076661 (~ 100 trillion times)
    we need to collapse more, (or wait hundreds to thousans of hours)

    well, b is fairly easy to collapse, we are multiplying by a constant n times,
    that is literally the definition of exponentition
    so b_n is b after n shuffles clearly:
    b_n = b ** b_mul % N
    once again python helps here by having built in exponentiation with
    mod
    b_n = pow(b_mul, n, N)

    for a lets look at the progression:
        a_0 = 0
        a_1 = 0 + 1 * a_diff
        a_2 = 0 + 1 * a_diff + b_mul * a_diff
        a_3 = 0 + 1 * a_diff + b_mul * a_diff + (b_mul * b_mul) * a_diff
        a_4 = 0 + 1 * a_diff + b_mul * a_diff + (b_mul * b_mul) * a_diff +
              (bmul * b_mul + b_mul) * a_diff

    this looks like a series:
    a_n = SUM[i = 0 to n-1](b_mul ** i * a_diff) = a_diff * SUM[i = 0 to n-1](b_mul ** i)
    not only does that look like a series it looks like the geometric series
    so we have

    SUM[i = 0 to n-1] (r ** i) = (1 - r ** n) / (1 - r)
    to do this in code (and with the moduls included) we need
    1 - pow(r, n, N) * MODINV(1 - r)

    so now we can collapse any number of shuffles into one calcualtion

    b_n = pow(b_mul, n, N)
    a_n = a_diff * (1 - pow(b_mul, n, N) * MODINV(1 - b_mul))

'''


def deal(deck, n):
    to_place = len(deck)
    placed = 0
    cards = (x for x in deck)
    start = 0
    new = {}
    while placed < to_place:
        for index in range(start, to_place, n):
            new[index] = next(cards)
            placed += 1

        start = (index + n) % to_place
    return [new[k] for k in range(to_place)]


def stack(deck, n):
    return list(reversed(deck))


def cut(deck, n):
    return deck[n:] + deck[:n]


def parse(data):
    operations = []
    for line in data:
        val = line.split()[-1]
        if line.startswith('cut'):
            operations.append((cut, int(val)))
        elif val == 'stack':
            operations.append((stack, None))
        else:
            operations.append((deal, int(val)))
    return operations


class Deck:
    '''
    class to do the fast version, the functions above do the slow version
    '''
    def __init__(self, N):
        self.N = N
        self.a = 0
        self.b = 1
        self.ops = None
        self.a_diff = None
        self.b_mul = None

    def parse(self, data):
        ops = []
        for line in data:
            val = line.split()[-1]
            if line.startswith('cut'):
                ops.append((self.cut, int(val)))
            elif val == 'stack':
                ops.append((self.stack, 0))
            else:
                ops.append((self.deal, int(val)))
        self.ops = ops

    def deal(self, n):
        self.b = (self.b * self._modinv(n)) % self.N

    def stack(self, n=0):
        self.b = (self. b * -1) % self.N
        self.a = (self. a + self.b) % self.N

    def cut(self, n):
        self.a = (self.a + self.b * n) % self.N

    def _modinv(self, n):
        return pow(n, self.N-2, self.N)

    def _get_loc(self, n):
        '''get the card at location n'''
        return (self.a + n * self.b) % self.N

    def _make_deck(self):
        return [self._get_loc(i) for i in range(self.N)]

    def _single_shuffle(self):
        if self.ops is None:
            raise Exception('need to provide shuffle operations first')
        for f, n in self.ops:
            f(n)
        self.a_diff = self.a
        self.b_mul = self.b
        self.reset()

    def reset(self):
        self.a = 0
        self.b = 1

    def shuffle(self, n):
        if self.a_diff is None:
            self._single_shuffle()
        v = pow(self.b_mul, n, self.N)
        self.b = v
        v2 = (1 - self.b_mul) % self.N
        self.a = (self.a_diff * (1 - v) * self._modinv(v2)) % self.N

    def __call__(self, n=1):
        self.shuffle(n)

    def __getitem__(self, n):
        return self._get_loc(n)


def get_answer(data, part2=False):

    if part2:
        cards = 119315717514047
        deck = Deck(cards)
        deck.parse(data)

        deck.shuffle(101741582076661)
        return deck[2020]


    deck = Deck(10007)
    deck.parse(data)
    deck()
    for i, val in enumerate(deck._make_deck()):
        if val == 2019:
            return i


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
