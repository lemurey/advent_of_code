from aoc_utilities import get_instructions
from utilities import timeit
import os


class Marble(object):
    def __init__(self, num, left=None, right=None):
        self.id = num
        self.left = left
        self.right = right
        self.is_current = False

    def get_left(self):
        if self.left is None:
            return self
        return self.left

    def get_right(self):
        if self.left is None:
            return self
        return self.right

    def set_current(self):
        self.is_current = True

    def unset_current(self):
        self.is_current = False

    def change_left(self, left):
        self.left = left

    def change_right(self, right):
        self.right = right

    def __mod__(self, other):
        return self.id % other

    def __eq__(self, other):
        if isinstance(other, Marble):
            return self.id == other.id
        elif isinstance(other, int):
            return self.id == other
        else:
            return False

    def __repr__(self):
        if self.is_current:
            return '({})'.format(self.id)
        else:
            return '{}'.format(self.id)

class MarbleGame(object):
    def __init__(self, num_players):
        self.scores = [0 for _ in range(num_players)]
        self.current = Marble(0)

    def __call__(self, player, marble):
        if marble % 23 == 0:
            self._run_23(marble, player)
        else:
            prev = self.current
            prev.unset_current()
            self.current = marble
            self.current.set_current()
            self.current.change_left(prev.get_right())
            self.current.change_right(prev.get_right().get_right())
            self.current.get_right().change_left(self.current)
            self.current.get_left().change_right(self.current)

    def _run_23(self, marble, player):
        # player gets that marble
        self.scores[player] += marble.id
        # find marble 7 to the left of current marble
        check = self.current
        for _ in range(7):
            check = check.get_left()
        # remove that marble from game
        check.get_left().change_right(check.get_right())
        check.get_right().change_left(check.get_left())
        # player gets removed marble as well
        self.scores[player] += check.id
        # marble to right of removed marble becomes current
        new = check.get_right()
        self.current.unset_current()
        self.current = new
        new.set_current()

    def _get_zero(self):
        check = self.current
        while True:
            if check == 0:
                return check
            check = check.get_right()

    def print_game(self):
        start = self._get_zero()
        out = str(start)
        test = start.get_right()
        while test != start:
            out += ' ' + str(test)
            test = test.get_right()
        print out


def play_game(num_players, num_rounds):
    game = MarbleGame(num_players)
    game.current.set_current()
    for cur_round in xrange(num_rounds):
        cur_player = cur_round % num_players
        cur_marble = Marble(cur_round + 1)
        game(cur_player, cur_marble)
    return max(game.scores)


@timeit
def get_answer(data, part2=False):
    temp = data[0].split()
    players = int(temp[0])
    rounds = int(temp[-2])
    if part2:
        return play_game(players, rounds*100)
    return play_game(players, rounds)


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    sample = '''10 players; last marble is worth 1618 points
13 players; last marble is worth 7999 points
17 players; last marble is worth 1104 points
21 players; last marble is worth 6111 points
30 players; last marble is worth 5807 points'''.split('\n')
    answers = [8317, 146373, 2764, 54718, 37305]
    for entry, answer in zip(sample, answers):
        a = get_answer([entry])
        assert a == answer
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))