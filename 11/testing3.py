import networkx as nx
import pprint
from pathlib import Path
from day11 import read_input
import networkx as nx
from itertools import permutations

import time
import networkx as nx
from collections import deque


def compute_reachability_to_target(G: nx.DiGraph, target):
    """
    Return a set of nodes that can reach `target` (including target itself).
    We compute descendants on the reversed graph: nodes reachable from `target`
    in G.reverse() are exactly nodes that can reach `target` in G.
    """
    # Using nx.descendants on reverse graph
    rev = G.reverse(copy=False)
    reach = nx.descendants(rev, target)
    reach.add(target)
    return reach


def all_paths_with_nodes_pruned_debug(
    G: nx.DiGraph,
    start: str,
    end: str,
    required_nodes,
    *,
    heartbeat_states=1000000,
    max_states=None,
    max_paths=None,
):
    """
    One-pass DFS (stack) enumerator for all simple paths start->end that include ALL required_nodes.
    Strong pruning using precomputed reachability:
      - prune nodes that cannot reach `end`
      - prune nodes that cannot reach any REQUIRED node not yet seen
    Debug info printed periodically.

    Parameters:
      - heartbeat_states: print a heartbeat every this many expanded states
      - max_states: stop after this many expanded states (if not None)
      - max_paths: stop after this many found paths (if not None)

    Returns:
      - list of paths (each path is a list of nodes)
    """
    required = set(required_nodes)
    t0 = time.time()
    print(f"[INFO] Precomputing reachability... (end={end}, required={required})")
    can_reach_end = compute_reachability_to_target(G, end)
    reach_required = {r: compute_reachability_to_target(G, r) for r in required}

    print(f"[INFO] Nodes that can reach end: {len(can_reach_end)}")
    for r in required:
        print(f"[INFO] Nodes that can reach {r}: {len(reach_required[r])}")

    # Quick reject: if start cannot reach end or cannot reach any required node -> nothing to do
    if start not in can_reach_end:
        print(f"[WARN] start '{start}' cannot reach end '{end}' -> no paths.")
        return []
    for r in required:
        if start not in reach_required[r] and start != r:
            print(f"[WARN] start '{start}' cannot reach required node '{r}' -> no paths.")
            return []

    # Stack: (current_node, path_list, seen_required_set)
    stack = [(start, [start], {start} & required)]
    results = []
    states = 0
    pushes = 0
    pruned_cant_reach_end = 0
    pruned_cant_reach_required = 0

    last_hb = t0

    while stack:
        node, path, seen_required = stack.pop()
        states += 1

        # Heartbeat
        if states % heartbeat_states == 0:
            elapsed = time.time() - t0
            print(f"[HB] states={states:,}, pushes={pushes:,}, found_paths={len(results):,}, "
                  f"stack_size={len(stack):,}, pruned_end={pruned_cant_reach_end:,}, "
                  f"pruned_req={pruned_cant_reach_required:,}, elapsed={elapsed:.1f}s")

        if max_states is not None and states >= max_states:
            print(f"[STOP] Reached max_states={max_states:,}. Aborting search.")
            break
        if max_paths is not None and len(results) >= max_paths:
            print(f"[STOP] Reached max_paths={max_paths:,}. Aborting search.")
            break

        # PRUNE: current node must be able to reach end
        if node not in can_reach_end:
            pruned_cant_reach_end += 1
            continue

        # PRUNE: for every required node not yet seen, ensure it's reachable from current node
        cant_reach_some_required = False
        for r in (required - seen_required):
            if node not in reach_required[r]:
                pruned_cant_reach_required += 1
                cant_reach_some_required = True
                break
        if cant_reach_some_required:
            continue

        # If we've arrived at end, check requirement satisfaction
        if node == end:
            if required <= seen_required:
                results.append(path)
            continue

        # Expand neighbors
        for nbr in G[node]:
            # avoid cycles (simple paths only)
            if nbr in path:
                continue
            # minor cheap pruning: neighbor must be able to reach end
            if nbr not in can_reach_end:
                pruned_cant_reach_end += 1
                continue
            # neighbor must be able to reach any remaining required nodes
            ok = True
            for r in (required - (seen_required | ({nbr} & required))):
                if nbr not in reach_required[r]:
                    ok = False
                    pruned_cant_reach_required += 1
                    break
            if not ok:
                continue

            new_seen = seen_required | ({nbr} & required)
            stack.append((nbr, path + [nbr], new_seen))
            pushes += 1

    elapsed = time.time() - t0
    print("\n[RESULT] Search finished.")
    print(f"  elapsed: {elapsed:.2f}s")
    print(f"  states expanded: {states:,}")
    print(f"  nodes pushed: {pushes:,}")
    print(f"  pruned (can't reach end): {pruned_cant_reach_end:,}")
    print(f"  pruned (can't reach req): {pruned_cant_reach_required:,}")
    print(f"  valid paths found: {len(results):,}")
    return results


# ---------------------------
# Example usage:
# ---------------------------
if __name__ == '__main__':
    data = read_input(Path('11/input.txt'))
    G = nx.DiGraph(data)
    # G = nx.DiGraph(...)  # build or load your graph
    # Example small graph: (uncomment to test)
    # G = nx.DiGraph({
    #     "svr": ["a", "b"],
    #     "a": ["fft", "x"],
    #     "b": ["dac"],
    #     "fft": ["dac", "out"],
    #     "dac": ["out"],
    #     "x": ["out"],
    #     "out": []
    # })

    paths = all_paths_with_nodes_pruned_debug(G, "svr", "out", {"fft", "dac"},
                                              heartbeat_states=1000000,
                                              max_states=None, max_paths=None)
    for p in paths:
        print(p)
    pass
