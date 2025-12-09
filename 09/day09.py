import matplotlib.cm as cm
import random
from matplotlib.patches import Polygon as MplPolygon, Rectangle
from matplotlib.collections import PatchCollection
from shapely import box
from math import comb
from shapely import Polygon
import itertools
import math
import time
import numpy as np
from pathlib import Path
import logging
import coloredlogs
import pprint
from scipy.spatial import KDTree
from tqdm import tqdm
import matplotlib.pyplot as plt
coloredlogs.install(level='DEBUG')
logger = logging.getLogger(__name__)


def read_input(filename: Path) -> list:
    """Reads from input file, strips newline characters

    :param filename: filename to read
    :type filename: Path
    :return: list of lists (each line as separate characters)
    :rtype: list
    """
    with open(filename, "r") as f:
        data = f.readlines()

    puzzle = [
        [int(x) for x in line.strip().split(',')]
        for line in data
    ]

    logger.debug(pprint.pformat(puzzle))

    return puzzle


def area(a: list[int], b: list[int]) -> int:
    """Calculates area from two 2d-coordinates

    Basically length * width, but
    accounting for zero starts and having first coordinate to the right
    of the second coordinate

    :param a,b: coordinate (x,y)
    :type a: list[int]
    :return: area
    :rtype: int
    """
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


def part1(data):
    # data = read_input(filename)

    # data = [[2, 5], [9, 7]]
    # data = [[7, 1], [11, 7]]
    # data = [[7, 3], [2, 3]]
    n_combinations = math.comb(len(data), 2)
    max_square = 0

    with tqdm(total=n_combinations) as pbar:
        for (a, b) in itertools.combinations(data, 2):

            ans = area(a, b)

            # print(f'{a} x {b} = {ans}')

            max_square = max(ans, max_square)
            pbar.set_postfix({"max_square": f'{max_square:>10d}'})
            pbar.update(1)
    print(f'{max_square=}')
    return max_square


def part2(data):

    polygon = Polygon(data)

    n_combinations = math.comb(len(data), 2)
    max_square = 0
    with tqdm(total=n_combinations) as pbar:
        for (a, b) in itertools.combinations(data, 2):
            x1, y1 = a
            x2, y2 = b

            rect = box(min(x1, x2), min(y1, y2),
                       max(x1, x2), max(y1, y2))

            if polygon.contains(rect):
                ans = area(a, b)

                max_square = max(ans, max_square)

                pbar.set_postfix({"max_square": f'{max_square:>10d}'})

            pbar.update(1)
    print(f'{max_square=}')

    return max_square


if __name__ == "__main__":  # pragma: no cover
    filename = Path('09/sample01.txt')
    data = read_input(filename)
    part1(data)
    part2(data)
