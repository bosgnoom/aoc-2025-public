from pathlib import Path
import logging
import coloredlogs
import pprint
from collections import defaultdict


coloredlogs.install(level='INFO', fmt='%(asctime)s %(levelname)s %(name)s [%(module)s:%(funcName)s] %(message)s')
logger = logging.getLogger(__name__)


def read_input(filename: Path) -> tuple[defaultdict, defaultdict, list]:
    """
    Reads from input file:
    - block definitions
    - calculates used space in blocks (i.e. counting #)
    - determines the packing list for each block

    :param filename: Puzzle input
    :type filename: Path
    :return: blocks, sizes and present lists
    :rtype: tuple[defaultdict, defaultdict, list]
    """

    # Read input file
    with open(filename, "r") as f:
        data = f.readlines()

    # Store blocks (and their "used" size)
    blocks = defaultdict()
    blocks_sizes = defaultdict()
    presents = []

    # Counter for the while loop
    i = 0
    while i < len(data):
        # Read 5 lines, look for a block/piece definition or a list of region and needed presents
        block = data[i:i+5]

        # Inverted logic, so mentally in the same order as input file
        if "x" not in block[0]:
            # No x, so the 5 lines describe a block
            block_number = int(block[0].strip().replace(':', ''))
            block_data = [x.strip() for x in block[1:] if len(x) > 1]

            blocks[block_number] = block_data
            blocks_sizes[block_number] = ''.join(block_data).count('#')
            i += 5
        else:
            # There's an x, so this is region and number of presents line
            presents.append(data[i].strip())

            i += 1

    logger.debug(pprint.pformat(blocks))
    logger.debug(pprint.pformat(blocks_sizes))
    logger.debug(pprint.pformat(presents[0: 10]))

    return blocks, blocks_sizes, presents


def get_those_who_fit(blocks_sizes: defaultdict, presents: list) -> list:
    """
    As a first cut-away, let's remove all possibilities where even if we'd squeeze all the packages,
    they will not fit into the region.

    e.g. block 0 will not fit into a 2x2 region
         block 1 will fit into 3x3 region

    :param blocks_sizes: Block sizes
    :type blocks_sizes: defaultdict
    :param presents: Packing list
    :type presents: list
    :return: Packages which will fit
    :rtype: list
    """

    # Let's loop over each line, check first if sum(block size) matches the region size
    these_will_fit = []
    for present in presents:
        line = present.split(': ')
        width, length = [int(x) for x in line[0].split('x')]
        shapes = [int(x) for x in line[1].split(' ')]
        area = width * length

        blocks_area = 0
        for i, j in enumerate(shapes):
            blocks_area += j * blocks_sizes[i]

        if blocks_area > area:
            logger.debug(f'{line} is too large!')
        else:
            logger.debug(f'{line} could fit')
            these_will_fit.append(line)

    logger.info(f'Amount of package lists which fit in region: {len(these_will_fit)}')

    return these_will_fit


def get_those_as_blocks(presents: list) -> list:
    """
    As a second cut-away, let's consider all blocks to be as solid 3x3 blocks. So,
    if these will fit inside the regio, we don't need to bother with turning and flipping
    in order to make all fit. 

    :param presents: Packing list
    :type presents: list
    :return: Description
    :rtype: list
    """

    possible = []
    for line in presents:
        line = line.split(': ')
        width, length = [int(x) for x in line[0].split('x')]
        packing_list = [int(x) for x in line[1].split(' ')]

        packs = sum(packing_list)

        # Integer divide the width and length into pack sizes (3x3 blocks)
        if ((width // 3)*(length//3)) >= packs:
            possible.append(line)

    logger.info(f'Amount of real possibilities: {len(possible)}')

    exit()


if __name__ == "__main__":
    filename = Path("12/input.txt")
    blocks, blocks_sizes, presents = read_input(filename)

    possibilities = get_those_who_fit(blocks_sizes, presents)
    logger.info(f'Amount of possibilities as block size: {len(possibilities)}')

    possibilities = get_those_as_blocks(presents)
    logger.info(f'Amount of possibilities as solid blocks: {len(possibilities)}')

    # Note to self: if we squish the blocks, 575 fit
    #               if we consider them as 3x3 blocks, 575 will fit
    # As these numbers are the same, concluding that I needed to do this the other way
    # around, seeing them as solid 3x3 blocks --> 575 fit, squising them --> 575 will fit
    # this means we're done here!
