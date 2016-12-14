import md5, re

c1 = re.compile(r'(\w)\1\1')

def compute_hash(string, count):
    return md5.new('{}{}'.format(string, count)).hexdigest()


def advanced_hashes(string, count):
    temp_hash = compute_hash(string, count)
    for _ in xrange(2016):
        temp_hash = compute_hash(temp_hash, '')
    return temp_hash


def get_results(instructions, part2=False):
    hash_checks = {}
    keys = []
    count = 0
    while len(keys) < 64:
        to_remove = []
        skip = False
        if part2:
            hashed = advanced_hashes(instructions, count)
        else:
            hashed = compute_hash(instructions, count)
        for k, regex in hash_checks.iteritems():
            if count <= k + 1000 and count > k:
                if regex.search(hashed):
                    keys.append(k)
            elif count > k + 1000:
                to_remove.append(k)
        for index in to_remove:
            del hash_checks[index]
        match = c1.search(hashed)
        if match:
            string = r'({})\1{{4}}'.format(match.group(1))
            hash_checks[count] = re.compile(string)
        count += 1
    return sorted(keys)[63]



if __name__ == '__main__':
    with open('instructions_day14.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions)
    print get_results(instructions, True)
    # print get_results('abc')

