import regex as re

with open('instructions_day7.txt', 'r') as f:
    instructions = f.read().strip()

breaker = re.compile(r'(\[\w*\])')
check_string = re.compile(r'(\w)(?!\1)(.)\2\1')
check_three = re.compile(r'(\w)(?!\1)(.)\1')

def checker(line, check=check_string, breaker=breaker):
    groups = breaker.split(line)
    found = False
    for group in groups:
        if group[0] == '[':
            if check.search(group[1:-1]):
                return False
        else:
            if check.search(group):
                found = True
    return found


def advanced_checker(line, check=check_three, breaker=breaker):
    groups = breaker.split(line)
    interior = []
    exterior = []
    for group in groups:
        if group[0] == '[':
            interior.append(group[1:-1])
        else:
            exterior.append(group)
    for sub in exterior:
        test = check_three.findall(sub, overlapped=True)
        # print test, sub,
        if test:
            for group in test:
                bab = re.compile(r''.join((group[1], group[0], group[1])))
                for sub2 in interior:
                    if bab.search(sub2):
                        return True
    return False


def get_result(instructions):
    print sum(map(checker, instructions.split('\n')))
    return sum(map(advanced_checker, instructions.split('\n')))

    
if __name__ == '__main__':
    print get_result(instructions)
    print advanced_checker('aba[bab]xyz')
    print advanced_checker('xyx[xyx]xyx')
    print advanced_checker('aaa[kek]eke')
    print advanced_checker('zazbz[bzb]cdb')

