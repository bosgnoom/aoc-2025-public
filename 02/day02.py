from pathlib import Path
from collections import Counter

import logging
import coloredlogs

coloredlogs.install(level='INFO')
logger = logging.getLogger(__name__)


def read_input(filename: Path) -> list:
    """Reads from input file, strips newline characters and separates into low-high ID ranges

    :param filename: filename to read
    :type filename: Path
    :return: list of instructions
    :rtype: list
    """
    with open(filename, "r") as f:
        data = f.readlines()

    puzzle = [
        item.strip()
        for line in data
        for item in line.replace('\n', '').split(',')
        if item.strip() != '']

    logger.debug(puzzle)

    return puzzle


def valid_id(id: str) -> int:
    """Takes an id (as string), splits it in half.

    If the parts are equal, the ID is invalid and its value (as int) is returned.
    If unequal, the ID is valid and 0 is returned.

    :param id: Single ID
    :type id: str
    :return: ID score
    :rtype: int
    """
    mid = len(id) // 2
    left = id[:mid]
    right = id[mid:]

    logger.debug(f'{left} - {right} --> {left != right}')

    if left == right:
        logger.debug(id)
        return int(id)
    else:
        return 0


def valid_id2(id: str) -> int:
    """Takes an id (as string), splits it multiple times, to determine whether a sequence is repeated at least twice.

    If a part is repeated multiple times, the ID is invalid and its value (as int) is returned.
    If no repetitions, the ID is valid and 0 is returned.

    :param id: Single ID
    :type id: str
    :return: ID score
    :rtype: int
    """

    # ID cannot start with 0
    if id.startswith('0'):
        return 0

    # Let's loop this, starting from 1 to half length ID
    for n in range(1, 1 + len(id) // 2):
        # Only where ID can be split in equal parts
        if len(id) % n == 0:
            logger.debug(f'Splitting length: {n}')

            chunks = [id[i:i + n] for i in range(0, len(id), n)]

            logger.debug(f'{chunks=}')

            # We have a result if there are more than 2 repetitions and
            # there is only one thing which is repeated, so by converting
            # the chunks into a set, it should be only of length 1. The minimum
            # of 2 repetitions is ensured by looping over the ID length // 2 above.
            if len(set(chunks)) == 1:
                return int(id)
    return 0


def main(puzzle: list, part: int) -> int:
    """Main loop. Loops over each range in _puzzle_. As valid_id returns the value of the invalid ones,
    the returned values are summarized into the final score.

    :param puzzle: ID ranges
    :type puzzle: list
    :param part: which part of the puzzle
    :type part: int
    :return: total score
    :rtype: int
    """
    total = 0
    for item in puzzle:
        logger.info(f'Processing {item=}')
        low, high = item.split('-')

        for i in range(int(low), int(high) + 1):
            if part == 1:
                total += valid_id(str(i))
            else:
                total += valid_id2(str(i))

    return total


if __name__ == "__main__":
    puzzle = read_input(Path("02/input.txt"))
    logger.info(f'Total score part 1: {main(puzzle, 1)}')
    logger.info(f'Total score part 2: {main(puzzle, 2)}')
