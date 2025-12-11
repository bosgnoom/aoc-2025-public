import pprint
from pathlib import Path
from day11 import read_input
import networkx as nx
from itertools import permutations


def all_simple_paths_ordered_debug(G, start, via1, via2, end):
    """Return all simple paths start -> via1 -> via2 -> end, with debug prints."""
    paths = []

    print(f"\n=== Searching: {start} → {via1} → {via2} → {end} ===")

    # ---- 1) start -> via1 ----
    print(f"Finding paths {start} -> {via1} ...")
    p1_list = list(nx.all_simple_paths(G, start, via1, cutoff=10))
    print(f"  Found {len(p1_list)} paths for first segment.")

    for n1, p1 in enumerate(p1_list, start=1):
        if n1 % 1000 == 0:
            print(f"  Processed {n1}/{len(p1_list)} first-segment paths...")

        visited1 = set(p1[:-1])  # avoid reusing these nodes

        # ---- 2) via1 -> via2 ----
        def dfs_v1_to_v2():
            stack = [(via1, [via1])]
            count = 0
            while stack:
                node, path = stack.pop()
                if node == via2:
                    yield path
                    continue
                for nbr in G[node]:
                    if nbr not in visited1 and nbr not in path:
                        stack.append((nbr, path + [nbr]))
                count += 1
                if count % 100000 == 0:
                    print(f"    [dbg] {via1}->{via2} DFS expanded {count} states so far...")

        p2_count = 0
        for p2 in dfs_v1_to_v2():
            p2_count += 1
            visited2 = visited1.union(p2[:-1])

            # ---- 3) via2 -> end ----
            def dfs_v2_to_end():
                stack = [(via2, [via2])]
                count_inner = 0
                while stack:
                    node, path = stack.pop()
                    if node == end:
                        yield path
                        continue
                    for nbr in G[node]:
                        if nbr not in visited2 and nbr not in path:
                            stack.append((nbr, path + [nbr]))
                    count_inner += 1
                    if count_inner % 10000 == 0:
                        print(f"      [dbg] {via2}->{end} DFS expanded {count_inner} states so far...")

            for p3 in dfs_v2_to_end():

                full = p1 + p2[1:] + p3[1:]
                paths.append(full)

                if len(paths) % 50 == 0:
                    print(f"      [STATS] Accumulated total paths: {len(paths)}")

        print(f"  Second segment produced {p2_count} partial paths from {via1} → {via2}")

    print(f"=== Completed ordered search ({start} → {via1} → {via2} → {end}).")
    print(f"Final count for this ordering: {len(paths)} paths.\n")

    return paths


def all_paths_via_unordered_debug(G, start, vias, end):
    """vias = list/set of required intermediate nodes, any order."""
    all_paths = []

    for order in permutations(vias):
        v1, v2 = order
        print(f"\n### ORDERING: {start} → {v1} → {v2} → {end} ###")

        subpaths = all_simple_paths_ordered_debug(G, start, v1, v2, end)
        all_paths.extend(subpaths)

        print(f"Collected {len(subpaths)} paths for this ordering.")
        print(f"Total accumulated: {len(all_paths)} paths\n")

    # Deduplicate final list
    print("Removing duplicates...")
    unique = [list(x) for x in {tuple(p) for p in all_paths}]
    print(f"Deduplicated total: {len(unique)} paths.\n")

    return unique


data = read_input(Path('11/input.txt'))
G = nx.DiGraph(data)

paths = all_paths_via_unordered_debug(G, "svr", ["fft", "dac"], "out")

for p in paths:
    print(p)
