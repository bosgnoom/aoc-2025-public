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
        puzzle = f.readlines()

    puzzle = [p.replace('\n', '') for p in puzzle]

    return puzzle


def calc_pos(old_pos: int, instruction: str) -> tuple[int, int]:
    """Calculate new position of dial and amount of clicks

    :param old_pos: current dial position
    :type old_pos: int
    :param instruction: instruction, like R17
    :type instruction: str
    :raises NotImplementedError: when unknown instruction is called
    :return: new position and amount of clicks
    :rtype: tuple
    """
    dir, distance = instruction[0], int(instruction[1:])
    if dir == "R":
        new = old_pos + distance
    elif dir == "L":
        new = old_pos - distance
    else:
        raise NotImplementedError

    new = new % 100
    clicks = 0
    if new == 0:
        clicks = 1

    logger.debug(f"I'm at {old_pos}, rotating {instruction} ({dir}, {distance}) to {new}")

    return new, clicks


def main(puzzle: list) -> int:
    """Calculates final dial position and amount of clicks (ending on zero)

    :param puzzle: list of instructions
    :type puzzle: list
    :return: amount of clicks
    :rtype: int
    """
    pos = 50
    total_clicks = 0

    for instr in puzzle:
        new_pos, clicks = calc_pos(pos, instr)
        pos = new_pos
        total_clicks += clicks

    logger.info(f'Finished at: {pos}, with {total_clicks=}')

    return total_clicks


if __name__ == "__main__":
    puzzle = read_input(Path("01/input.txt"))
    main(puzzle)
