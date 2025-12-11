from itertools import islice
from collections import deque
import time
from itertools import permutations
from day11 import read_input
from pathlib import Path
import pprint
import networkx as nx


def all_simple_paths_limited(G, src, dst, limit_nodes):
    """Yield simple paths from src→dst that stay inside limit_nodes."""
    for path in nx.all_simple_paths(G, src, dst, cutoff=10):
        if all(n in limit_nodes for n in path):
            yield path


def find_paths_with_required(G, start, end, required):
    # Required nodes
    r1, r2 = list(required)

    # Precompute subgraphs limited to reachability cones
    reach_end = nx.descendants(G, start) | {start}
    reach_r1 = nx.descendants(G, start) | {start}
    reach_r2 = nx.descendants(G, start) | {start}

    # Paths for both orders: start→r1→r2→end  and start→r2→r1→end
    results = []

    def combine(a, b):
        # Combine two paths where a ends at X and b starts at X
        return a[:-1] + b

    # ----- Order: r1 → r2 -----
    for p1 in nx.all_simple_paths(G, start, r1):
        for p2 in nx.all_simple_paths(G, r1, r2):
            for p3 in nx.all_simple_paths(G, r2, end):
                results.append(combine(combine(p1, p2), p3))

    # ----- Order: r2 → r1 -----
    for p1 in nx.all_simple_paths(G, start, r2):
        for p2 in nx.all_simple_paths(G, r2, r1):
            for p3 in nx.all_simple_paths(G, r1, end):
                results.append(combine(combine(p1, p2), p3))

    return results


def debug(msg):
    print(f"[DBG] {msg}")


def timed(msg):
    print(f"[TIME] {msg}")


def all_simple_paths_debug(G, src, dst, heartbeat=1000):
    """Yield simple paths with progress/debug output."""
    count = 0
    t0 = time.time()
    for path in nx.all_simple_paths(G, src, dst, cutoff=15):
        count += 1
        if count % heartbeat == 0:
            debug(f"{src} → {dst}: generated {count} paths so far... "
                  f"(elapsed {time.time() - t0:.2f}s)")
        yield path
    debug(f"{src} → {dst}: DONE, total {count} paths (elapsed {time.time() - t0:.2f}s)")


def combine(p1, p2):
    return p1[:-1] + p2


def find_paths_with_required_debug(G, start, end, required):
    r1, r2 = list(required)

    total_start = time.time()

    # ---------------------------------------------
    # SEGMENT 1: PATHS start → r1
    # ---------------------------------------------
    timed(f"Computing paths {start} → {r1}")
    t0 = time.time()
    P_start_r1 = list(all_simple_paths_debug(G, start, r1))
    debug(f"Collected {len(P_start_r1)} paths for segment {start} → {r1} "
          f"(elapsed {time.time() - t0:.2f}s)\n")

    # SEGMENT 2: PATHS r1 → r2
    timed(f"Computing paths {r1} → {r2}")
    t0 = time.time()
    P_r1_r2 = list(all_simple_paths_debug(G, r1, r2))
    debug(f"Collected {len(P_r1_r2)} paths for segment {r1} → {r2} "
          f"(elapsed {time.time() - t0:.2f}s)\n")

    # SEGMENT 3: PATHS r2 → end
    timed(f"Computing paths {r2} → {end}")
    t0 = time.time()
    P_r2_end = list(all_simple_paths_debug(G, r2, end))
    debug(f"Collected {len(P_r2_end)} paths for segment {r2} → {end} "
          f"(elapsed {time.time() - t0:.2f}s)\n")

    # ORDER 1: start → r1 → r2 → end
    timed("Combining paths for order: start → r1 → r2 → end")
    t0 = time.time()
    order1 = []
    for p1 in P_start_r1:
        for p2 in P_r1_r2:
            for p3 in P_r2_end:
                order1.append(combine(combine(p1, p2), p3))
    debug(f"Order1 combinations = {len(order1)} (elapsed {time.time() - t0:.2f}s)\n")

    # ---------------------------------------------
    # NOW ORDER 2: start → r2 → r1 → end
    # ---------------------------------------------

    # SEGMENT 4: start → r2
    timed(f"Computing paths {start} → {r2}")
    t0 = time.time()
    P_start_r2 = list(all_simple_paths_debug(G, start, r2))
    debug(f"Collected {len(P_start_r2)} paths for segment {start} → {r2} "
          f"(elapsed {time.time() - t0:.2f}s)\n")

    # SEGMENT 5: r2 → r1
    timed(f"Computing paths {r2} → {r1}")
    t0 = time.time()
    P_r2_r1 = list(all_simple_paths_debug(G, r2, r1))
    debug(f"Collected {len(P_r2_r1)} paths for segment {r2} → {r1} "
          f"(elapsed {time.time() - t0:.2f}s)\n")

    # SEGMENT 6: r1 → end
    timed(f"Computing paths {r1} → {end}")
    t0 = time.time()
    P_r1_end = list(all_simple_paths_debug(G, r1, end))
    debug(f"Collected {len(P_r1_end)} paths for segment {r1} → {end} "
          f"(elapsed {time.time() - t0:.2f}s)\n")

    # ORDER 2: start → r2 → r1 → end
    timed("Combining paths for order: start → r2 → r1 → end")
    t0 = time.time()
    order2 = []
    for p1 in P_start_r2:
        for p2 in P_r2_r1:
            for p3 in P_r1_end:
                order2.append(combine(combine(p1, p2), p3))
    debug(f"Order2 combinations = {len(order2)} (elapsed {time.time() - t0:.2f}s)\n")

    # ---------------------------------------------
    # DONE
    # ---------------------------------------------
    results = order1 + order2

    timed(f"TOTAL time: {time.time() - total_start:.2f}s")
    debug(f"TOTAL valid paths = {len(results)}")

    return results


data = read_input(Path('11/input.txt'))
G = nx.DiGraph(data)
paths = find_paths_with_required_debug(G, "svr", "out", {"fft", "dac"})

print("==== FINAL PATHS ====")
for p in paths:
    print(p)
