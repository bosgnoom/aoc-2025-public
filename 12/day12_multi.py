import os
import multiprocessing as mp
from pathlib import Path
import logging
import coloredlogs
import pprint
from collections import defaultdict
from day12_visual import solver

coloredlogs.install(level='DEBUG', fmt='%(asctime)s %(levelname)s %(name)s [%(module)s:%(funcName)s] %(message)s')
logger = logging.getLogger(__name__)


def read_input(filename: Path) -> dict:
    """Reads from input file

    :param filename: filename to read
    :type filename: Path
    :return: list of lists (each line as separate characters)
    :rtype: list
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

            # Save block info
            blocks[block_number] = block_data

            # As first test: check block size first, reduce possibilities if the
            # blocks do not fit in the region
            blocks_sizes[block_number] = ''.join(block_data).count('#')
            i += 5
        else:
            # There's an x, so this is region and a packing list
            presents.append(data[i].strip())

            i += 1

    logger.debug(pprint.pformat(blocks))
    logger.debug(pprint.pformat(blocks_sizes))
    logger.debug(pprint.pformat(presents[0: 3]))

    return blocks, blocks_sizes, presents


def get_those_who_fit(blocks_sizes, presents):

    # Let's loop over each line, check first if sum(block size) matches the region size
    these_will_fit = []
    for present in presents:
        line = present.split(': ')
        width, length = [int(x) for x in line[0].split('x')]
        shapes = [int(x) for x in line[1].split(' ')]

        # logger.debug(f'{width}, {length}, {shapes}')
        area = width * length
        blocks_area = 0
        for i, j in enumerate(shapes):
            # logger.debug(j*blocks_sizes[i])
            blocks_area += j*blocks_sizes[i]
            # logger.debug(f'{i=}, {j=}, {blocks_area=}')
        if blocks_area > area:
            pass
            # logger.info('Too large!')
        else:
            # logger.info('Could fit')
            these_will_fit.append(line)

    # oeps, this is already the answer!
    logger.info(f'Amount of package lists which fit in region: {len(these_will_fit)}')

    return these_will_fit


# Example top-level solver function

def solve_one(args):
    i, line = args
    width, length = [int(x) for x in line[0].split('x')]
    packing_list = [int(x) for x in line[1].split(' ')]
    return solver(i, width, length, packing_list)  # your existing solver function


if __name__ == "__main__":
    filename = Path("12/input.txt")
    blocks, blocks_sizes, presents = read_input(filename)
    possibilities = get_those_who_fit(blocks_sizes, presents)

    cpu_count = os.cpu_count()  # number of processes

    # Prepare arguments for Pool.map
    args_list = [(i, line) for i, line in enumerate(possibilities)]

    with mp.Pool(processes=cpu_count-1) as pool:
        solutions = pool.map(solve_one, args_list)

    # print(solutions)

    logger.info(f'Amount of real possibilities: {sum(solutions)}')
