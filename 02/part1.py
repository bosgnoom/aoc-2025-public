from pathlib import Path
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logger = logging.getLogger(__name__)


def read_input(filename: Path) -> list:
    """Reads from input file, strips newline characters

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


def valid_id(id: str) -> bool:
    mid = len(id) // 2
    left = id[:mid]
    right = id[mid:]

    logger.debug(f'{left} - {right} --> {left != right}')

    return left != right


def main(puzzle):
    valid_id('55')
    pass


if __name__ == "__main__":
    puzzle = read_input(Path("02/sample01.txt"))
    main(puzzle)
