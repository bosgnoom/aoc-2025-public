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
            # logger.debug(block)
            block_number = int(block[0].strip().replace(':', ''))
            # logger.debug(block_number)
            block_data = [x.strip() for x in block[1:] if len(x) > 1]
            # logger.debug(block_data)
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


def get_those_as_blocks(possibilities):

    print(possibilities[0:5])

    exit()


if __name__ == "__main__":
    filename = Path("12/input.txt")
    blocks, blocks_sizes, presents = read_input(filename)
    possibilities = get_those_who_fit(blocks_sizes, presents)

    solutions = []
    sol2 = []
    for i, line in enumerate(presents):
        line = line.split(': ')
        width, length = [int(x) for x in line[0].split('x')]
        packing_list = [int(x) for x in line[1].split(' ')]

        packs = sum(packing_list)
        room = width*length

        if room >= (packs*9):
            print(line, width, length,  packs, packs*9, width*length)

            solutions.append(line)

        if ((width // 3)*(length//3)) >= packs:
            sol2.append(line)

    logger.info(f'Amount of real possibilities: {len(solutions)}')
    n_poss = set(tuple(pos) for pos in possibilities)
    n_sol = set(tuple(sol) for sol in solutions)
    n_sol2 = set(tuple(sol) for sol in sol2)

    print(n_poss == n_sol)
    print(n_sol2 == n_sol)

    # solutions = []
    # for i, line in enumerate(possibilities[0:3]):
    #     print(i, line)
    #     width, length = [int(x) for x in line[0].split('x')]
    #     packing_list = [int(x) for x in line[1].split(' ')]

    #     solutions.append(solver(i, width, length, packing_list))

    # logger.info(f'Amount of real possibilities: {sum(solutions)}')

    # get_those_as_blocks(presents)

    #################################
    # Process those not yet generated
    #################################

    # files = sorted([int(i.stem.replace('packing_result_', '')) for i in Path('12/images/').glob('*.png')])

    # needed = []
    # for i, file in enumerate(files):
    #     if (i+len(needed)) != file:
    #         print(f'{i=} {file=}')
    #         needed.append(i)

    # if not needed:
    #     print("all done")
    # # Difficult ones:
    # # 40 ['45x45', '41 31 37 44 40 32'] sum: 225 225*9=2025 45*45=2025
    # for i in needed:
    #     line = possibilities[i]
    #     print(i, line)
    #     width, length = [int(x) for x in line[0].split('x')]
    #     packing_list = [int(x) for x in line[1].split(' ')]

    #     solver(i, width, length, packing_list)
