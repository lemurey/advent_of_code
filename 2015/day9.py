from itertools import permutations

def get_results(instructions):
    locations = set()
    distances = {}
    paths = {}
    for line in instructions.split('\n'):
        temp = line.split()
        distance, city1, city2 = int(temp[-1]), temp[0], temp[2]
        if city1 not in distances:
            distances[city1] = {city2 : distance}
        else:
            distances[city1][city2] = distance
        if city2 not in distances:
            distances[city2] = {city1 : distance}
        else:
            distances[city2][city1] = distance
        locations.add(city1)
        locations.add(city2)
    for cycle in permutations(locations):
        traveled = 0
        for i, city in enumerate(cycle[:-1]):
            traveled += distances[city][cycle[i + 1]]
        paths[cycle] = traveled

    temp = sorted(paths.iteritems(), key=lambda x: x[1])
    print temp[0][1]
    return temp[-1][1]


if __name__ == '__main__':
    with open('instructions_day9.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions)