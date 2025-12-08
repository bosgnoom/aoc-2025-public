import math
from pathlib import Path
import pprint
from scipy.spatial import KDTree
import numpy as np


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


# --- DSU (Union-Find) implementation ---
coords = read_input(Path("08/sample01.txt"))
# Buidl KD tree (yay, there's a function to calculate all distances in one go)
tree = KDTree(coords)

# Calculate distances from tree
dm = tree.sparse_distance_matrix(tree, max_distance=np.inf)

# scipy thinggy into something I understand (list), skipping inverted pairs
distances = [(int(n1), int(n2), dist) for (n1, n2), dist in dm.items() if dist > 0 and n1 < n2]

parent = list(range(len(coords)))
size = [1] * len(coords)


def find(x):
    while x != parent[x]:
        x = parent[x]
    return x


def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb:
        print(f"    Nodes {coords[a]} and {coords[b]} already in same component {ra}")
        return ra

    # Union by size (optional but strongly recommended)
    if size[ra] < size[rb]:
        ra, rb = rb, ra

    parent[rb] = ra
    size[ra] += size[rb]
    print(f"    Merged component of {coords[b]} (root {rb}) into {coords[a]} (root {ra})")
    print(f"    New size of component {ra}: {size[ra]}")
    return ra


# --- Build components using DSU based on your distances list ---

# Sort distances by the weight (just like your original code)
distances = sorted(distances, key=lambda x: x[2])

for coord1, coord2, _ in distances[:10]:
    union(coord1, coord2)


# --- Convert DSU structure into your circuits format ---

components = {}  # dict of sets, like your circuits variable

for node in range(len(coords)):
    root = find(node)
    if root not in components:
        components[root] = set()
    components[root].add(node)

# Now 'components' is the DSU-based version of your circuits dict
pprint.pprint(components)
lengths = sorted([len(v) for k, v in components.items()], reverse=True)
print(lengths)
print(math.prod(lengths[0:3]))  # part1: 79056


# --- Part 2: Keep adding edges until all nodes are in a single chain ---
print("\nPart 2: Connecting until a single component")
k = 0
while True:
    _, a, b = distances[k]  # distances contains edges with (coord1, coord2, dist)
    new_size = union(a, b)

    # check if all nodes are connected
    if new_size == len(coords):

        print(f"\nAll nodes connected by last edge: {coords[a]} - {coords[b]}")
        # print(f"Part 2 {x1} x {x2} = {x1 * x2}")
        break

    k += 1
