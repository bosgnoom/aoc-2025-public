import math
from pathlib import Path
import pprint
from scipy.spatial import KDTree
import numpy as np
import logging
import coloredlogs
# Note to self: DSU (Union-Find) implementation
# This broke me...

# Started off with a dict of sets() --> does not work, since need to connect junction boxes, not make a collection
# of connected items. So, fell back into a dict of lists() --> does not work, since does not support branches.
# Although the first one could handle branches, in the sense that all items are connected (and the second one not),
# it lacked the stringed approach, where you could have a (idk) triple, or higher interval on connections.
# Internet inspired me to look into the DSU approach. Luckily wikipedia and youtube have enough pseudo code
# to finally finish this one...

coloredlogs.install(level='INFO')
logger = logging.getLogger(__name__)


class DSU():
    """Class for DSU calculations, so find and union are nicely written apart.
    Also has the advantage that the coordinates and parents are stored in this class as well.
    Yay for not having global variables
    """

    def __init__(self, coords):
        self.parent = list(range(len(coords)))
        self.size = [1] * len(coords)

    def find(self, x):
        # Look for "top" node in connections
        while x != self.parent[x]:
            x = self.parent[x]
            logger.debug(f'Looking for {x}, found parent: {self.parent[x]}')
        return x

    def union(self, a, b):
        # Connect two sets/branches by looking for their parents first,
        # then setting the parent of the smallest node to the parent of the
        # larger branch
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            # Already in the same component
            logger.debug(f'For union {a} and {b}, already having same parent {ra}')
            return self.size[ra]

        # Union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra

        # Change parent here
        logger.debug(f'For union {a} and {b}, setting parent {rb} to parent {ra} ')
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return self.size[ra]


def read_input(filename: Path) -> list:
    """Reads from input file, strips newline characters and splits by comma

    :param filename: Puzzle filename
    :type filename: Path
    :return: Puzzle input
    :rtype: list
    """
    with open(filename, "r") as f:
        data = f.readlines()

    puzzle = [
        [int(x) for x in line.strip().split(',')]
        for line in data
    ]

    return puzzle


def coords_to_distances(coords: list) -> list:
    # Build KD tree
    tree = KDTree(coords)

    # Calculate distances from tree
    dm = tree.sparse_distance_matrix(tree, max_distance=np.inf)

    # Convert to list of (index1, index2, distance), skipping duplicates
    # (read: A->B is ok, but then do not add B->A anymore)
    distances = [(n1, n2, dist) for (n1, n2), dist in dm.items() if dist > 0 and n1 < n2]

    # Sort by distance
    distances = sorted(distances, key=lambda x: x[2])

    return distances


def part1(coords: list, distances: list, n: int) -> int:
    """_summary_

    :param coords: _description_
    :type coords: list
    :param distances: _description_
    :type distances: list
    :param n: _description_
    :type n: int
    :return: _description_
    :rtype: int
    """
    # Set up the DSU approach here
    puzzle = DSU(coords)

    # Process n shortest connections
    for coord1, coord2, _ in distances[:n]:
        puzzle.union(coord1, coord2)

    # Convert DSU structure into dict of sets,
    # so we can easily add coord indexes to the circuits
    components = {}
    for node in range(len(coords)):
        root = puzzle.find(node)
        if root not in components:
            components[root] = set()
        components[root].add(node)

    # Show circuits
    for k, v in components.items():
        logger.debug(f'In circuit {k}: {v}')

    # check three largest groups and multiply
    lengths = sorted([len(v) for k, v in components.items()], reverse=True)
    logger.debug(f'Number of junctions in circuits sorted: {lengths}')

    answer = math.prod(lengths[0:3])
    logger.info(f'Answer part1: {answer}')

    return answer


def part2(coords: list, distances: list) -> int:
    """Keep on running part1 untill all coords are in a single circuit

    :param coords: Puzzle coordinates
    :type coords: _type_
    :param distances: _description_
    :type distances: _type_
    """

    # Set up the DSU approach here
    puzzle = DSU(coords)

    k = 0
    answer = 0
    while True:
        # Get new coordinate pair
        coord1, coord2, _ = distances[k]
        logger.debug(f'Processing coordinate pair {coord1}, {coord2}')

        new_size = puzzle.union(coord1, coord2)
        logger.debug(f'Amount of circuits: {new_size}')

        # Check if all nodes are connected
        if new_size == len(coords):
            x1 = coords[coord1][0]  # first coordinate of the last edge
            x2 = coords[coord2][0]  # first coordinate of the last edge
            logger.info(f"All nodes connected by last edge: {coords[coord1]} -> {coords[coord2]}")
            answer = x1 * x2
            logger.info(f"Multiplying x-coordinates: {x1} x {x2} = {answer}")
            return answer

        k += 1


if __name__ == "__main__":  # pragme: no cover
    coords = read_input(Path("08/input.txt"))
    dist = coords_to_distances(coords)
    part1(coords, dist, 10)
    part2(coords, dist)
