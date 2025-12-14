import math
from pathlib import Path
import logging
import coloredlogs
import pprint
import networkx as nx
import matplotlib.pyplot as plt

coloredlogs.install(level='INFO')
logger = logging.getLogger(__name__)

PLOTTING = True


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

    logger.debug(pprint.pformat(data))

    return data


def prune_graph(G: nx.DiGraph, source: str, dest: str) -> nx.DiGraph:
    """
    Cuts away all nodes before source and all nodes after target,
    hereby reducing the network. This makes part 2 solvable, because the
    network is soo large

    :param G: Original network
    :type G: nx.DiGraph
    :param source: source
    :type source: str
    :param dest: destiny node
    :type dest: str
    :return: Description
    :rtype: DiGraph
    """

    descendants = nx.descendants(G, source) | {source}  # add source back to descendants
    ancestors = nx.ancestors(G, dest) | {dest}  # add destiny back to ancestors
    subgraph = descendants & ancestors  # intersection (both in A and B)

    return G.subgraph(subgraph).copy()


def count_pathways(data: dict, source: str, dest: str) -> int:
    """
    Docstring for count_pathways

    :param data: Dict like network information {"a": ['b', 'c']}
    :type data: dict
    :param source: source node
    :type source: str
    :param dest: destiny node
    :type dest: str
    :return: amount of different paths from source to destiny
    :rtype: int
    """

    # Set up network
    logger.info('Setting up network')
    G = nx.DiGraph(data)
    logger.info(f'Original network: {G}')

    G = prune_graph(G, source, dest)
    logger.info(f'Reduced network: {G}')

    if PLOTTING:
        # Prepare figure
        plt.figure(figsize=(16, 9))

        # Let's highlight "you" and "out"
        highlight_nodes = [source, dest,  'you', 'out']

        node_colors = [
            'red' if node in highlight_nodes else 'lightblue'
            for node in G.nodes()
        ]

        # Layout for positioning nodes
        logger.info('Drawing network')
        pos = nx.kamada_kawai_layout(G)

        nx.draw_networkx_nodes(G, pos, node_size=100, alpha=0.8, node_color=node_colors)
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(G, pos, font_size=8)

    # Count how many paths lead from you to out, hurray for networkx
    logger.info('Setting up all_simple_paths')
    paths = nx.all_simple_paths(G, source=source, target=dest)  # this is a generator

    # Count amount of paths, show progress
    logger.info('Counting all simple paths')
    total = 0
    for path in paths:
        logger.debug(path)

        total += 1

        if total % 10_000 == 0:
            logger.info(f'\033[1m{source}\033[0m to \033[1m{dest}\033[0m: \033[1;91m{total}\033[0m')

    logger.info(f'Amount of paths from \033[1m{source}\033[0m to \033[1m{dest}\033[0m: \033[1;91m{total}\033[0m')

    return total


def run_all(filename_part1: str, filename_part2: str) -> tuple[int, int]:
    """
    Runs both part 1 and part 2 of day 11,
    Calculating amount of paths between sources and targets

    :param filename_part1: Input part 1
    :type filename_part1: str
    :param filename_part2: Input part 2
    :type filename_part2: str
    :return: Amount of paths for part 1 and part 2
    :rtype: tuple[int, int]
    """
    # Part 1
    result_1 = count_pathways(read_input(Path(filename_part1)), "you", "out")

    # Part 2
    # Has different sample data
    data = read_input(Path(filename_part2))

    # It's going to be either svr->dac->fft->out or
    #                         svr->fft->dac->out
    # Let's find these routes
    answer_part2 = []
    try:
        answer_part2.extend([count_pathways(data, "fft", "dac"),
                            count_pathways(data, "svr", "fft"),
                            count_pathways(data, "dac", "out"),
                             ])

    except nx.NodeNotFound:
        logger.critical('fft->dac does not exist!')
        answer_part2.extend([count_pathways(data, "dac", "fft"),
                            count_pathways(data, "svr", "dac"),
                            count_pathways(data, "fft", "out"),
                             ])

    except Exception as e:
        logger.critical('Something went wrong:')
        logger.critical(e)

    # answer_part 2 has now thee items of possibilities,
    # to get to total possibilities, multiply
    result_2 = math.prod(answer_part2)
    logger.info(f'Amount of routes from \033[1msvr\033[0m to \033[1mout\033[0m: \033[1;91m{result_2}\033[0m')

    # Show figures
    plt.show()

    return result_1, result_2


if __name__ == "__main__":  # pragma: no cover
    # day11('11/sample01.txt', '11/sample02.txt')
    run_all('11/input.txt', '11/input.txt')
