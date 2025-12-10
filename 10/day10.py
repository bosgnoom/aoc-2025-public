from part1 import minimal_flips
from part2 import solve_joltage
from pathlib import Path
import logging
import coloredlogs
import pprint

coloredlogs.install(level='DEBUG', fmt='%(asctime)s %(levelname)s %(name)s [%(module)s:%(funcName)s] %(message)s')
logger = logging.getLogger(__name__)


def read_input(filename: Path) -> list[str]:
    """Reads from input file, strips newline characters

    :param filename: filename to read
    :type filename: Path
    :return: list of lists (each line as separate characters)
    :rtype: list
    """
    with open(filename, "r") as f:
        data = f.readlines()

    puzzle = [
        [x for x in line.strip().split(' ')]
        for line in data
    ]

    logger.debug('Puzzle input')
    logger.debug(pprint.pformat(puzzle))

    return puzzle


def part1(data: list) -> int:
    """
    Runs part 1 of day 10

    Extracts the needed light diagram and the button wiring schematics of each machine.
    Joltage is not yet needed, so ignored here.


    :param data: Machine data
    :type data: list
    :return: Total amount of button presses for all machines
    :rtype: int
    """

    total = 0
    for machine in data:

        # Machine data is [light diagram] (buttons) {joltage}
        light_diagram = [0 if x == '.' else 1
                         for x in list(machine[0].replace('[', '').replace(']', ''))]

        button_wiring = [
            [int(x) for x in group.replace('(', '').replace(')', '').split(',')]
            for group in machine[1:-1]
        ]

        ans = minimal_flips(light_diagram, button_wiring)

        logger.debug(f'Machine: {light_diagram} {button_wiring} --> {ans} flips needed')

        total += ans

    logger.info(f'Total button flips needed for part 1: {total}')

    return int(total)


def part2(data: list[str]) -> int:
    """
    Part 2 is completely (?) different. Instead of using XOR logic, now we want to calculate
    the joltage for each light. This will be done using PuLP, linear (integer) programming.

    Let's sove for each machine!

    :param data: Description
    :type data: list[str]
    :return: Description
    :rtype: int
    """

    total = []
    for machine in data:
        # Extract only button wiring diagram and needed joltage
        joltage = [int(x) for x in machine.pop().replace('{', '').replace('}', '').split(',')]
        wiring = [
            [int(b) for b in group.replace('(', '').replace(')', '').split(',')]
            for group in machine[1:]
        ]

        logger.debug(f'{joltage=}, {wiring=}')

        solution = solve_joltage(joltage, wiring)
        logger.debug(f"Total presses: {sum(solution)}")
        total.append(sum(solution))

    logger.info(f'Total for part 2: {sum(total)}')

    return sum(total)


if __name__ == "__main__":  # pragma: no cover
    data = read_input(Path('10/input.txt'))
    answers = [part1(data), part2(data)]

    logger.info(f'Answers part 1 and 2: {answers}')
