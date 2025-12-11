from pathlib import Path
import logging
import coloredlogs
import pprint
import networkx as nx
import matplotlib.pyplot as plt

coloredlogs.install(level='INFO')
logger = logging.getLogger(__name__)


def read_input(filename: Path) -> dict:
    """Reads from input file, strips newline characters
    Sets up a dict where the first item is the key and the remaining items are a list of str

    :param filename: filename to read
    :type filename: Path
    :return: list of lists (each line as separate characters)
    :rtype: list
    """
    with open(filename, "r") as f:
        data = f.readlines()

    puzzle = [
        [x.replace(':', '') for x in line.strip().split(' ')]
        for line in data
    ]

    # Turn the puzzle into a dict, with the first one as key
    data = {x[0]: list(x[1:]) for x in puzzle}
    # logger.debug(pprint.pformat(puzzle))
    logger.debug(pprint.pformat(data))

    return data


if __name__ == "__main__":
    data = read_input(Path('11/input.txt'))
    G = nx.DiGraph(data)

    print(G)

    # Layout for positioning nodes
    # pos = nx.spring_layout(G, seed=42, k=0.8)  # or try nx.kamada_kawai_layout(G)

    # Draw nodes and edges
    # plt.figure(figsize=(8, 6))
    # nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=1200, edgecolors="black")
    # nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle="-|>", arrowsize=25)

    # Draw node labels (keys of the dict)
    # nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

    # plt.title("Directed Graph from Dictionary", fontsize=14)
    # plt.axis("off")
    # plt.tight_layout()

    # paths = list(nx.all_simple_paths(G, source="you", target="out"))
    # # pprint.pprint(paths)
    # print(len(paths))

    # plt.show()

    # part 2

    p1 = nx.shortest_path(G, "svr", "fft")
    p2 = nx.shortest_path(G, "fft", "dac")
    p3 = nx.shortest_path(G, "dac", "out")

    print(p1)
    print(p2)
    print(p3)

    p1 = list(nx.all_simple_paths(G, "svr", "fft"))
    print(p1, len(p1))
