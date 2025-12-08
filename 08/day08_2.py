import math
import time
import numpy as np
from pathlib import Path
import logging
import coloredlogs
import pprint
from scipy.spatial import KDTree

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

    # logger.debug(pprint.pformat(puzzle))

    return puzzle


if __name__ == "__main__":
    # coords = read_input(Path("08/input.txt"))
    coords = read_input(Path("08/sample01.txt"))

    # Buidl KD tree (yay, there's a function to calculate all distances in one go)
    tree = KDTree(coords)

    # Calculate distances from tree
    dm = tree.sparse_distance_matrix(tree, max_distance=np.inf)

    # scipy thinggy into something I understand (list), skipping inverted pairs
    distances = [(int(n1), int(n2), dist) for (n1, n2), dist in dm.items() if dist > 0 and n1 < n2]

    # Sort distances, lowerst first
    distances = sorted(distances, key=lambda x: x[2])

    # Convert the list into a dict of lists
    circuits = {0: list([distances[0][0], distances[0][1]])}
    circuit_id = 1

    # Loop over n shortest distances
    for i in range(1, 4):  # len(distances)):
        coord1, coord2, _ = distances[i]
        print(f'[{i:5}] Processing coords {coords[coord1]} and {coords[coord2]}')

        # try to find in circuits
        found_in_circuits = []
        for circ in circuits.items():
            k, v = circ
            if coord1 == v[0]:
                print(f'    Found {coords[coord1]} at the start in circuits {k}, adding before')
                circuits[k] = [coord2, *v]
                found_in_circuits.append(k)
            elif coord2 == v[0]:
                print(f'    Found {coords[coord2]} at the start in circuits {k}, adding before')
                circuits[k] = [coord1, *v]
                found_in_circuits.append(k)
            elif coord1 == v[-1]:
                print(f'    Found {coords[coord1]} at the end in circuits {k}, adding after')
                circuits[k] = [*v, coord2]
                found_in_circuits.append(k)
            elif coord2 == v[-1]:
                print(f'    Found {coords[coord2]} at the end in circuits {k}, adding after')
                circuits[k] = [*v, coord1]
                found_in_circuits.append(k)
            else:
                print(f'    Coords not found in circuits')

        # link can be in multiple circuits, make union here
        if len(found_in_circuits) > 1:
            alles = set()
            for t in found_in_circuits:
                alles.update(circuits[t])
                del circuits[t]
            print(f'    Union, here is {alles=}')
            circuits[found_in_circuits[0]] = alles
        elif found_in_circuits == []:
            # Add to circuits
            print(f'    coords not in circuits, making new one {circuit_id}')
            circuits[circuit_id] = {coord1, coord2}
            circuit_id += 1

        print('Circuits:')
        for circ in circuits.items():
            k, v = circ
            print(f'{k}: {[coords[x] for x in v]}')
        print(f'    Length of circuits: {len(circuits)}')

        print('------------------------------')
        if i > 2 and len(circuits) == 1:
            break

    pprint.pprint(circuits)

    lengths = sorted([len(v) for k, v in circuits.items()], reverse=True)
    print(lengths)
    print(math.prod(lengths[0:3]))  # part1: 79056
