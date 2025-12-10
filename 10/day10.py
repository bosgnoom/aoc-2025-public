from part1 import minimal_flips
from part2 import solve_joltage
from pathlib import Path
import logging
import coloredlogs
import pprint

coloredlogs.install(level='DEBUG')
logger = logging.getLogger(__name__)


def read_input(filename: Path) -> list:
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

    logger.debug(pprint.pformat(puzzle))

    return puzzle


def part1(data: list) -> int:
    data = read_input(Path('10/input.txt'))

    total = []
    for machine in data:

        joltage = machine.pop()
        wiring = [
            [int(b) for b in group.replace('(', '').replace(')', '').split(',')]
            for group in machine[1:]
        ]

        light_diagram = [0 if x == '.' else 1 for x in list(machine[0].replace('[', '').replace(']', ''))]

        print(light_diagram, wiring, joltage)

        ans = minimal_flips(light_diagram, wiring)
        print(ans)
        total.append(ans)

    print(f'Total: {sum(total)}')

    return sum(total)


def part2(data):

    total = []
    for machine in data:

        joltage = [int(x) for x in machine.pop().replace('{', '').replace('}', '').split(',')]
        wiring = [
            [int(b) for b in group.replace('(', '').replace(')', '').split(',')]
            for group in machine[1:]
        ]

        light_diagram = [0 if x == '.' else 1 for x in list(machine[0].replace('[', '').replace(']', ''))]

        print(joltage, wiring, )

        solution = solve_joltage(joltage, wiring)
        print(solution)
        print("Total presses:", sum(solution))
        total.append(sum(solution))

    print(f'Total: {total}\nSum: {sum(total)}')


if __name__ == "__main__":
    data = read_input(Path('10/sample01.txt'))
    part1(data)
    part2(data)
