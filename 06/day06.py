from pathlib import Path
import logging
import coloredlogs
import math


coloredlogs.install(level='INFO')
logger = logging.getLogger(__name__)


def read_input(filename: Path) -> list:
    """Reads from input file, strips newline characters, 
    and returns homework.

    Each line is split into separate numbers, accounting for multiple spaces to seperate them.

    :param filename: filename to read
    :type filename: Path
    :return: homework data
    :rtype: list
    """
    with open(filename, "r") as f:
        data = f.readlines()

    homework = []
    for i, line in enumerate(data):
        line = line.strip()
        if i < len(data) - 1:
            numbers = [int(num) for num in line.split()]
        else:
            numbers = [op for op in line.split()]
        homework.append(numbers)

    logger.debug("Puzzle input:")
    logger.debug(homework)

    return homework


def part1(homework: list) -> int:
    """Process the homework data.

    :param homework: homework data
    :type homework: list
    :return: None
    :rtype: None
    """

    # Transpose the homework, easier for processing
    transposed = list(zip(*homework))

    # Track total score
    total = 0

    # Loop over homework
    for i in transposed:
        nums = i[:-1]
        operator = i[-1]

        if operator == "*":
            answer = math.prod(nums)
        elif operator == "+":
            answer = sum(nums)
        else:
            raise ValueError(f"Unknown operator: {operator[i]}")

        total += answer

        logger.debug(f"{operator.join([str(x) for x in nums])} = {answer}")

    logger.info(f"Total part 1: {total}")

    return total


def part2(filename) -> int:
    """Process the homework data for part 2.

    :param homework: homework data
    :type homework: list
    :return: None
    """

    # Remember writing a nice input parsing function?
    # Well... For part 2 we needed the weirdly formatted input...
    with open(filename, "r") as f:
        homework = f.readlines()

    # make sure all lines are the same length by padding with spaces
    max_width = max(len(line) for line in homework)
    homework = [line.ljust(max_width) for line in homework]

    # Transpose the assignment
    transposed = list(zip(*homework))

    # Keep track of total score
    total = 0

    # Collect column data
    current = []

    # Loop over all columns, starting from the right (last)
    for col in reversed(transposed):
        # Collect the raw number (all but operator)
        raw = ''.join(col[:-1]).strip()

        # Catch empty columns (between assignments)
        if not raw:
            continue

        # Convert number to integer and add to current list
        current.append(int(raw))

        # Get the operator for this column
        op = col[-1]

        # If we hit an operator, process the current list of numbers
        if op in ['+', '*']:
            if op == '+':
                score = sum(current)
            else:
                score = math.prod(current)

            total += score
            logger.debug(f'{op.join([str(x) for x in current])} = {score}')

            # Reset for next assignment
            current = []

    logger.info(f'Total part 2: {total}')

    return total


if __name__ == "__main__":  # pragma: no cover
    # filename = Path("06/sample01.txt")
    filename = Path("06/input.txt")
    part1(read_input(filename))
    part2(filename)
