from time import time
import requests, os

def get_data(day=1):
    f_name = 'day_{}_data'.format(day)
    if not os.path.isfile(f_name):
        with open(f_name, 'w') as f:
            url = 'http://adventofcode.com/2016/day/{}/input'.format(day)
            with open('cookie.env', 'r') as f1:
                cookie = {'session' : f1.read().strip()}
            response = requests.get(url, cookies=cookie)
            f.write(response.text)

    with open(f_name, 'r') as f:
        data = f.read().strip()

    return data


def timeit(function):
    def timed(*args, **kwargs):
        s_t = time()
        result = function(*args, **kwargs)
        e_t = time()
        out = '{} {} took {:.2f} sec'
        print out.format(function.__name__, kwargs, e_t - s_t)
        return result
    return timed
