import math
from pathlib import Path
import pprint
from scipy.spatial import KDTree
import numpy as np


def read_input(filename: Path) -> list:
    """Reads from input file, strips newline characters"""
    with open(filename, "r") as f:
        data = f.readlines()

    puzzle = [
        [int(x) for x in line.strip().split(',')]
        for line in data
    ]

    return puzzle


# --- DSU (Union-Find) implementation ---
coords = read_input(Path("08/sample01.txt"))

# Build KD tree
tree = KDTree(coords)

# Calculate distances from tree
dm = tree.sparse_distance_matrix(tree, max_distance=np.inf)

# Convert to list of (index1, index2, distance), skipping duplicates
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
        # Already in the same component
        return size[ra]

    # Union by size
    if size[ra] < size[rb]:
        ra, rb = rb, ra

    parent[rb] = ra
    size[ra] += size[rb]
    return size[ra]


# --- Part 1: initial DSU processing (first 10 edges) ---
distances = sorted(distances, key=lambda x: x[2])

for coord1, coord2, _ in distances[:10]:
    coord1, coord2 = int(coord1), int(coord2)
    union(coord1, coord2)

# Convert DSU structure into dict of sets
components = {}
for node in range(len(coords)):
    root = find(node)
    if root not in components:
        components[root] = set()
    components[root].add(node)

pprint.pprint(components)
lengths = sorted([len(v) for k, v in components.items()], reverse=True)
print(lengths)
print(math.prod(lengths[0:3]))  # part1


# --- Part 2: Keep adding edges until all nodes are connected ---
print("\nPart 2: connecting until a single component")
k = 0
while True:
    coord1, coord2, dist = distances[k]
    coord1, coord2 = int(coord1), int(coord2)

    print(coords[coord1], coords[coord2])

    new_size = union(coord1, coord2)

    print(new_size)

    # Check if all nodes are connected
    if new_size == len(coords):
        x1 = coords[coord1][0]  # first coordinate of the last edge
        x2 = coords[coord2][0]  # first coordinate of the last edge
        print(f"All nodes connected by last edge: {coord1} - {coord2}")
        print(f"Part 2 {x1} x {x2} = {x1 * x2}")
        break

    k += 1
