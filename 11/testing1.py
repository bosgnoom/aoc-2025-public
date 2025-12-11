from day11 import read_input
from pathlib import Path
import networkx as nx
import pprint


def all_simple_paths_ordered(G, start, via1, via2, end):
    """Return all simple paths start -> via1 -> via2 -> end."""
    paths = []

    # Paths start -> via1
    p1_list = list(nx.all_simple_paths(G, start, via1))
    pprint.pprint(p1_list)
    print(len(p1_list))

    for p1 in p1_list:
        # Note: path p1 ends at via1; its visited nodes should be excluded afterward
        visited1 = set(p1[:-1])  # everything except via1

        # Next: via1 -> via2, avoid visited nodes
        def dfs_v1_to_v2():
            stack = [(via1, [via1])]
            while stack:
                node, path = stack.pop()
                if node == via2:
                    yield path
                    continue
                for nbr in G[node]:
                    if nbr not in visited1 and nbr not in path:
                        stack.append((nbr, path + [nbr]))

        for p2 in dfs_v1_to_v2():
            visited2 = visited1.union(p2[:-1])

            # Final: via2 -> end, avoid all previously visited nodes
            def dfs_v2_to_end():
                stack = [(via2, [via2])]
                while stack:
                    node, path = stack.pop()
                    if node == end:
                        yield path
                        continue
                    for nbr in G[node]:
                        if nbr not in visited2 and nbr not in path:
                            stack.append((nbr, path + [nbr]))

            for p3 in dfs_v2_to_end():
                # Combine with overlap removed
                full = p1 + p2[1:] + p3[1:]
                paths.append(full)

    return paths


def all_paths_via_unordered(G, start, vias, end):
    """vias = set/list of nodes required but order does not matter."""
    from itertools import permutations

    all_paths = []
    for order in permutations(vias):
        v1, v2 = order
        subpaths = all_simple_paths_ordered(G, start, v1, v2, end)
        all_paths.extend(subpaths)

    # Deduplicate (paths are lists, so use tuple)
    unique = [list(x) for x in {tuple(p) for p in all_paths}]
    return unique


data = read_input(Path('11/input.txt'))
G = nx.DiGraph(data)

paths = all_paths_via_unordered(G, "svr", ["fft", "dac"], "out")

for p in paths:
    print(p)
