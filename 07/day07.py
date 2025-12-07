from pathlib import Path
import logging
import coloredlogs
from collections import defaultdict
import pprint


coloredlogs.install(level='INFO')
logger = logging.getLogger(__name__)


def read_input(filename: Path) -> tuple[list, list]:
    """Reads from input file, strips newline characters,
    and returns list of fresh ID ranges and available IDs

    :param filename: filename to read
    :type filename: Path
    :return: two lists: fresh ID ranges and available IDs
    :rtype: list
    """
    with open(filename, "r") as f:
        data = f.readlines()

    diagram = []

    for line in data:
        line = line.strip()

        diagram.append([i for i in line])

    logger.debug("Puzzle input:")
    logger.debug('\n' + pprint.pformat(diagram))

    return diagram


def main(filename):
    # Part 1: keep track of how often the beam is split
    # Part 2: keep track of how often a beam can be split

    diagram = read_input(Path(filename))

    # Get size of diagram
    rows, cols = len(diagram), len(diagram[0])
    logger.debug(f'Diagram size: {rows} x {cols}')

    # Loop over diagram
    start_position = diagram[0].index('S')
    logger.debug(f'Start position: {start_position}')

    # Keep a set of found beams, starting with "S"
    beams = set()
    beams.add(start_position)

    # Keep track of how many times we've split the beam
    split_count = 0

    # Keep track of how many times we've hit a position
    heatmap = defaultdict(int)
    heatmap[start_position] = 1

    # Loop over all rows in the diagram
    for r in range(rows):
        # Loop over all items in the row
        for c in range(len(diagram[r])):
            # If we find a split where the beam is
            if diagram[r][c] == "^" and c in beams:
                # Increase split count
                split_count += 1
                logger.debug(f'Split found at: {c}, splitcount = {split_count}, {beams=}')

                # Original beam is removed
                beams.remove(c)

                # And added to the sides
                beams.add(c-1)
                beams.add(c+1)

                # Update the diagram with beam patterns
                diagram[r][c-1] = '|'
                diagram[r][c+1] = '|'

                # For part2, keep track how often we've hit a position
                # Keep on counting as before splitter
                heatmap[c-1] = heatmap[c-1] + heatmap[c]
                heatmap[c+1] = heatmap[c+1] + heatmap[c]

                # Beam ends in the splitter, reset this to 0
                heatmap[c] = 0

            # Did not encounter a splitter, continue the beam
            if c in beams:
                diagram[r][c] = '|'

    logger.info(f'Splitcount (part1) = {split_count}')
    logger.info(f'Heatmap count (part2): {sum(heatmap.values())}')

    return split_count, sum(heatmap.values())


if __name__ == "__main__":  # pragma: no cover
    main("07/sample01.txt")
    main("07/input.txt")
