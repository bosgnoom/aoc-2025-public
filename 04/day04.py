from pathlib import Path
import pygame
import logging
import coloredlogs

coloredlogs.install(level='INFO')
logger = logging.getLogger(__name__)

# Screen settings
SCALE = 8
FPS = 10


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
        list(item.strip())
        for line in data
        for item in line.replace('\n', '').split(',')
        if item.strip() != '']

    logger.debug(puzzle)

    return puzzle


def draw_map(screen: pygame.Surface, font: pygame.font.Font, grid: list) -> None:
    """Draws puzzle on screen

    :param screen: Game window
    :type screen: pygame.Surface
    :param font: Font to be displayed
    :type font: _type_
    :param grid: Puzzle data
    :type grid: list
    """

    # Clear screen
    screen.fill((0, 0, 0))

    # Fill screen again, iterating over grid
    for i, line in enumerate(grid):
        for ii, c in enumerate(line):

            # "Fancy" coloring here
            if c == '@':
                color = (127, 255, 127)
            else:
                color = (64, 127, 64)

            text = font.render(c, True, color)
            screen.blit(text, (SCALE * ii, SCALE * i))


def count_neighbours(puzzle: list) -> set:
    """Counts neighbours of a roll on the puzzle map

    - Checks whether a cell is filled with a roll (@)
    - Counts neighbours
    - If neighbours is < 4 the roll can be removed

    - The set of rolls to be removed is calculated

    :param puzzle: Puzzle map
    :type puzzle: list
    :return: Rolls to be removed
    :rtype: set
    """
    directions = [
        (0, 1),    # Right
        (1, 0),    # Down
        (1, 1),    # Down-right diagonal
        (1, -1),   # Down-left diagonal
        (0, -1),   # Left
        (-1, 0),   # Up
        (-1, -1),  # Up-left diagonal
        (-1, 1)    # Up-right diagonal
    ]

    # Get size of puzzle
    rows, cols = len(puzzle), len(puzzle[0])

    # Check boundaries (are coords within map?)
    def is_valid(x: int, y: int) -> bool:
        return 0 <= x < rows and 0 <= y < cols

    # Loop over puzzle
    accessable = []
    for i in range(rows):
        for j in range(cols):
            if puzzle[i][j] == "@":
                count = 0
                for dx, dy in directions:
                    nx = j + dy
                    ny = i + dx

                    if is_valid(nx, ny) and puzzle[ny][nx] == "@":
                        logger.debug(f'Checking for ({i} {j}) -> ({ny} {nx}) = {puzzle[ny][nx]}')
                        count += 1

                logger.debug(f'Searching neighbours for {i} {j} --> {count} found')

                if count < 4:
                    accessable.append((j, i))

    accessable = set(accessable)

    logger.debug(f'{accessable=}')

    return accessable


def main(puzzle: list) -> int:
    """Main loop for puzzle

    Uses pygame for funsies

    Loops over the puzzle grid, untill no more rolls can be removed

    :param puzzle: Puzzle map
    :type puzzle: list
    :return: Amount of rolls removed in total
    :rtype: int
    """
    # Set up pygame
    pygame.init()
    pygame.font.init()
    timert = pygame.time.Clock()
    font = pygame.font.SysFont('freemono', size=SCALE)
    size_x = SCALE * len(puzzle[0])
    size_y = SCALE * len(puzzle)
    screen = pygame.display.set_mode([size_x, size_y])

    # Draw map on screen
    draw_map(screen, font, puzzle)

    # Update display
    pygame.display.flip()

    # Count how many rolls are removed
    total_removed = 0

    # Loop untill nothing can be removed
    while len(to_be_removed := count_neighbours(puzzle)) > 0:

        # Clear out rolls which can be removed
        for x, y in to_be_removed:
            puzzle[y][x] = "."

        # Update total counter
        total_removed += len(to_be_removed)
        logger.info(f'Amount rolls removed: {len(to_be_removed)}, {total_removed=}')

        # Draw map on screen
        draw_map(screen, font, puzzle)

        # Update display
        pygame.display.flip()
        timert.tick(FPS)

        # Check if pygame wants to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    # Close pygame window
    pygame.quit()

    return total_removed


if __name__ == "__main__":
    # puzzle = read_input(Path("04/sample01.txt"))
    puzzle = read_input(Path("04/input.txt"))

    # Note to self: answer from part 1 is 1st iteration
    logger.critical(f'Total rolls removed: {main(puzzle)}')
