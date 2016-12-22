from utilities import timeit
from heapq import heappush, heappop
from itertools import count

'''mostly stolen from reddit, with some modifications after my search methods
failed part 2, my part1 methodology was to randomly generate sequences of 
spells and check for lowest mana used. that worked in ~ same amount of time, 
and with somewhat similar code to below'''
class Spell(object):
    def __init__(self, name, cost, effect=False, 
                       turns=None, damage=0, heal=0, armor=0, mana=0):
        self.name = name
        self.cost = cost
        self.effect = effect
        self.turns = turns
        self.damage = damage
        self.heal = heal
        self.armor = armor
        self.mana = mana


SPELLS = (Spell('Magic Missle', 53, damage=4),
          Spell('Drain', 73, damage=2, heal=2),
          Spell('Shield', 113, effect=True, turns=6, armor=7),
          Spell('Poison', 173, effect=True, turns=6, damage=3),
          Spell('Recharge', 229, effect=True, turns=5, mana=101))


class Game(object):
    def __init__(self, hp, mana, boss_hp, boss_damage, mana_used=0,
                       effects=None, hard=False, parent=None, spell_cast=None):
        self.hp = hp
        self.mana = mana
        self.boss_hp = boss_hp
        self.boss_damage = boss_damage
        self.mana_used = mana_used
        self.effects = effects or ()
        self.hard = hard

    def __hash__(self):
        temp = []
        for v in vars(self).values():
            temp.append(v)
        return reduce(lambda a, b: a ^ hash(b), temp, 0)

    def run_effects(self):
        armor = 0
        continuing = []
        for timer, spell in self.effects:
            self.hp += spell.heal
            self.mana += spell.mana
            self.boss_hp -= spell.damage
            armor += spell.armor
            if timer > 1:
                continuing.append((timer - 1, spell))
        return tuple(continuing), armor

    def boss(self):
        self.effects, armor = self.run_effects()
        if self.boss_hp > 0:
            self.hp -= max(1, self.boss_damage - armor)

    def round(self):
        self.effects, armor = self.run_effects()
        if self.hard:
            self.hp -= 1
        for spell in SPELLS:
            if spell.cost > self.mana or any(spell is s for _, s in self.effects):
                continue
            new_game = Game(self.hp, self.mana - spell.cost, self.boss_hp, 
                            self.boss_damage, self.mana_used + spell.cost,
                            self.effects, hard=self.hard, parent=self)
            if not spell.effect:
                new_game.hp += spell.heal
                new_game.boss_hp -= spell.damage
            else:
                new_game.effects = new_game.effects + ((spell.turns, spell),)

            new_game.boss()

            if new_game.hp > 0:
                yield new_game


def boss_stats(instructions):
    boss = {}
    for line in instructions.split('\n'):
        stat, value = line.split(': ')
        boss[stat] = int(value)

    return boss


def search(start, verbose=False):
    history = {start}
    visited = set()
    uid = count()
    pq = []
    heappush(pq, (0, uid.next(), start))
    iterations = 0
    while history:
        game = heappop(pq)[-1]
        if game.boss_hp < 1:
            return game
        history.remove(game)
        visited.add(game)
        for g in game.round():
            iterations += 1
            if verbose and iterations % 10000 == 0:
                print '{}, len of stack:{}'.format(iterations, len(history))
            if g in history or g in visited:
                print 'skipping'
                continue
            history.add(g)
            heappush(pq, (g.mana_used, uid.next(), g))


@timeit
def get_results(instructions, part2=False):
    boss = boss_stats(instructions)
    start_point = Game(50, 500, boss['Hit Points'], boss['Damage'], hard=part2)
    end = search(start_point)
    return end.mana_used


if __name__ == '__main__':
    with open('instructions_day22.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)
