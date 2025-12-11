import networkx as nx
G = nx.DiGraph()

with open('11/input.txt') as f:
    for line in f:
        start, end = line.rstrip("\n").split(":")
        end = end.split()
        if isinstance(end, str):
            end = [end]
        for e in end:
            G.add_edges_from([(start, e)])


paths = list(nx.all_simple_paths(G, source="you", target="out"))
print(len(paths))

# Prune the graph to nodes relevant for source → target


def prune_to_relevant(G, source, target):
    reachable = nx.descendants(G, source) | {source}
    ancestors = nx.ancestors(G, target) | {target}
    keep = reachable & ancestors
    return G.subgraph(keep).copy()


G = nx.DiGraph()

with open('11/input.txt') as f:
    for line in f:
        start, end = line.rstrip("\n").split(":")
        end = end.split()
        if isinstance(end, str):
            end = [end]
        for e in end:
            G.add_edges_from([(start, e)])

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print(f"G is a directed acyclic graph: {nx.is_directed_acyclic_graph(G)}")
# it's acyclic, and there are paths from fft -> dac. This implies that there are no paths from dac to fft
# so we care only about the paths svr -> fft -> dac -> out

G_svr_fft = prune_to_relevant(G, 'svr', 'fft')
print("\nPruned graph from svr to fft:")
print("Nodes:", G_svr_fft.number_of_nodes())
print("Edges:", G_svr_fft.number_of_edges())

G_fft_dac = prune_to_relevant(G, 'fft', 'dac')
print("\nPruned graph from fft to dac:")
print("Nodes:", G_fft_dac.number_of_nodes())
print("Edges:", G_fft_dac.number_of_edges())

G_dac_out = prune_to_relevant(G, 'dac', 'out')
print("\nPruned graph from dac to out:")
print("Nodes:", G_dac_out.number_of_nodes())
print("Edges:", G_dac_out.number_of_edges())

paths_svr_fft = list(nx.all_simple_paths(G_svr_fft, "svr", "fft"))
print(f"N paths between svr and fft: {len(paths_svr_fft)}")

paths_fft_dac = list(nx.all_simple_paths(G_fft_dac, "fft", "dac"))
print(f"N paths between fft and dac: {len(paths_fft_dac)}")

paths_dac_out = list(nx.all_simple_paths(G_dac_out, "dac", "out"))
print(f"N paths between dac and out: {len(paths_dac_out)}")

print(f"{len(paths_svr_fft) * len(paths_fft_dac) * len(paths_dac_out)}")
