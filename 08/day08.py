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

    tree = KDTree(coords)

    dm = tree.sparse_distance_matrix(tree, max_distance=np.inf)  # , output_type="ndarray")

    distances = [(int(n1), int(n2), float(dist)) for (n1, n2), dist in dm.items() if dist > 0 and n1 < n2]
    distances = sorted(distances, key=lambda x: x[2])

    circuits = {}
    n_circuits = 0
    connected = set()

    for dist in distances:  # [0:10]:
        # unpack
        coord1, coord2, _ = dist

        print(f'Processing coords {coords[coord1]} and {coords[coord2]}')
        if coord1 not in connected and coord2 not in connected:
            print(f'    Coords {coords[coord1]} and {coords[coord2]} not in connected, adding as circuit')
            circuits[n_circuits] = set([coord1, coord2])
            n_circuits += 1
            connected.add(coord1)
            connected.add(coord2)
        else:
            # try to find in circuits
            found_in_circuits = []
            for circ in circuits.items():
                k, v = circ
                if coord1 in v:
                    print(f'    Found {coords[coord1]} in circ {k}, adding...')
                    circuits[k].add(coord1)
                    circuits[k].add(coord2)
                    connected.add(coord1)
                    connected.add(coord2)
                    found_in_circuits.append(k)
                elif coord2 in v:
                    print(f'    Found {coords[coord2]} in circ {k}, adding...')
                    circuits[k].add(coord1)
                    circuits[k].add(coord2)
                    connected.add(coord1)
                    connected.add(coord2)
                    found_in_circuits.append(k)
                else:
                    print(f'    Coords not found in circuit nr {k}')

            if len(found_in_circuits) > 1:
                # link can be in multiple circuits, make union here
                alles = set()
                for t in found_in_circuits:
                    alles.update(circuits[t])
                    del circuits[t]
                print(f'    Union, here is {alles=}, for circuit {n_circuits}')
                circuits[n_circuits] = alles
                n_circuits += 1

        print('Circuits:')
        for circ in circuits.items():
            k, v = circ
            print(f'{k}: {[coords[x] for x in v]}')
        print(f'Amount of circuits: {len(circuits)}')
        if n_circuits > 2 and len(circuits) == 1:
            print(f'Only one circuit left! {coords[coord1]}')
            break
        print('---------')

    lengths = sorted([len(v) for k, v in circuits.items()])[::-1]
    print(lengths)

    print(math.prod(lengths[0:3]))  # part1: 79056
