from itertools import islice
from collections import deque
import time
from itertools import permutations
from day11 import read_input
from pathlib import Path
import pprint
import networkx as nx

data = read_input(Path('11/input.txt'))


cache = {}


def solve(start, end, skip):
    result = 0
    if start == end:
        return 1
    else:
        for i in data[start]:
            if (i, end, skip) in cache:
                result += cache[(i, end, skip)]
            elif i not in skip:
                result += solve(i, end, skip)
    cache[(start, end, skip)] = result
    return result


a = solve("svr", "dac", ("out", "fft"))
b = solve("dac", "fft", ("out", "svr"))
c = solve("fft", "out", ("svr", "dac"))

print(a, b, c, a * b * c)
print(len(cache))

a = solve("svr", "fft", ("out", "dac"))
b = solve("fft", "dac", ("out", "svr"))
c = solve("dac", "out", ("svr", "fft"))

print(a, b, c, a * b * c)
print(len(cache))
