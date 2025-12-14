import os
import multiprocessing
from pathlib import Path
import logging
import coloredlogs
from day12_visual import solver
from day12 import read_input, get_those_who_fit

coloredlogs.install(level='INFO', fmt='%(asctime)s %(levelname)s %(name)s [%(module)s:%(funcName)s] %(message)s')
logger = logging.getLogger(__name__)


def solve_one(args):
    # Unpack args, return as pointer? to function
    i, line, blocks = args

    width, length = [int(x) for x in line[0].split('x')]
    packing_list = [int(x) for x in line[1].split(' ')]

    return solver(i, length, width, blocks, packing_list)


if __name__ == "__main__":
    # Read input
    filename = Path("12/input.txt")
    blocks, blocks_sizes, presents = read_input(filename)
    possibilities = get_those_who_fit(blocks_sizes, presents)

    # Get already generated ones (this is computational heavy!)
    # This is a list of integers, 0->xxx, follows the items in possibilities
    files = sorted([int(i.stem.replace('packing_result_', '')) for i in Path('12/images/').glob('*.png')])

    needed = [i for i in range(len(possibilities)) if i not in files]

    if not needed:
        logger.info("All done!")
        logger.info(f'Amount of possibilities: {len(possibilities)}')
    else:
        logger.info(f'Amount of possibilities to generate: {len(needed)}')
        # Fire up multiprocessing
        cpu_count = os.cpu_count()  # number of processes

        # Prepare arguments for Pool.map
        args_list = [(i, possibilities[i], blocks) for i in needed]

        with multiprocessing.Pool(processes=cpu_count-1) as pool:
            solutions = pool.map(solve_one, args_list)

        print(solutions)

        logger.info(f'Amount of real possibilities processed: {sum(solutions)}')
