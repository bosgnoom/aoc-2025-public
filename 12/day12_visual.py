import pprint
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from pulp import LpProblem, LpVariable, LpBinary, lpSum, LpStatus, LpMinimize
from pulp import HiGHS_CMD, PULP_CBC_CMD
import logging
import coloredlogs
from collections import defaultdict
from day12 import read_input

coloredlogs.install(level='INFO', fmt='%(asctime)s %(levelname)s %(name)s [%(module)s:%(funcName)s] %(message)s')
logger = logging.getLogger(__name__)

# =========================================================
# 1. Utilities for rotations, reflections, orientation gen
# =========================================================


def rotate_pattern(pat):
    """Rotate 3x3 pattern 90 degrees clockwise."""
    return [''.join(pat[2 - c][r] for c in range(3)) for r in range(3)]


def reflect_pattern(pat):
    """Reflect 3x3 pattern horizontally."""
    return [row[::-1] for row in pat]


def generate_orientations(pattern):
    """Generate unique rotations + reflections."""
    seen = set()
    out = []

    cur = pattern
    for _ in range(4):
        for refl in [False, True]:
            p = reflect_pattern(cur) if refl else cur
            key = tuple(p)
            if key not in seen:
                seen.add(key)
                out.append(p)
        cur = rotate_pattern(cur)
    return out


# =========================================================
# 2. Placement generator
# =========================================================

def enumerate_placements(grid_h, grid_w, piece_types):
    """Return a list of (piece_type_id, orientation, top_row, left_col, covered_cells)."""
    placements = []
    for pid, (pattern, count) in enumerate(piece_types):
        orientations = generate_orientations(pattern)
        for ori in orientations:
            filled = [(r, c) for r in range(3) for c in range(3) if ori[r][c] == '#']
            if not filled:
                continue

            # bounding box inside board
            for r in range(grid_h - 3 + 1):
                for c in range(grid_w - 3 + 1):
                    cells = [(r + dr, c + dc) for (dr, dc) in filled]
                    placements.append((pid, ori, r, c, tuple(cells)))
    return placements


# =========================================================
# 3. MILP model with PuLP
# =========================================================

def solve_pulp(grid_h, grid_w, piece_types):
    logger.info('Setting up PuLP')
    placements = enumerate_placements(grid_h, grid_w, piece_types)

    prob = LpProblem("PiecePacking", LpMinimize)

    # binary variable for each placement
    x = [LpVariable(f"x_{i}", 0, 1, LpBinary) for i in range(len(placements))]

    # objective doesn't matter; minimize sum of chosen placements
    prob += lpSum(x)

    # each piece type must use exactly its given count
    for pid, (_, needed) in enumerate(piece_types):
        prob += lpSum(x[i] for i, (ppid, _, _, _, _) in enumerate(placements) if ppid == pid) == needed

    # each cell covered at most once
    for r in range(grid_h):
        for c in range(grid_w):
            prob += lpSum(
                x[i] for i, (_, _, _, _, cells) in enumerate(placements) if (r, c) in cells
            ) <= 1

    logger.info("Solving with CBC...")
    prob.solve(PULP_CBC_CMD(msg=1))  # , timeLimit=300))
    # logger.info("Solving with HIGHS...")
    # prob.solve(HiGHS_CMD(msg=True, timeLimit=300))

    if LpStatus[prob.status] != "Optimal":
        logger.critical(f"No optimal solution found: {LpStatus[prob.status]}")
        return None, placements

    logger.info("Optimal solution found.")
    selected = [i for i in range(len(x)) if x[i].value() > 0.5]
    return selected, placements


# =========================================================
# 4. Board reconstruction & visualization
# =========================================================

def render_solution(grid_h, grid_w, piece_types, placements, selected):
    board = -1 * np.ones((grid_h, grid_w), dtype=int)

    # for sel in selected:
    #     pid, _, _, _, cells = placements[sel]
    #     for (r, c) in cells:
    #         board[r, c] = pid

    for col, sel in enumerate(selected):
        pid, _, _, _, cells = placements[sel]
        for (r, c) in cells:
            board[r, c] = col

    return board


def visualize(board, filename):
    cmap = plt.get_cmap("tab20").copy()
    cmap.set_under("#0b3d0b")  # background color for -1

    plt.figure(figsize=(10, 10))
    plt.imshow(board, interpolation='nearest', cmap=cmap, vmin=0)
    plt.title(f"Packing result {filename}")
    plt.savefig(filename, dpi=120)
    plt.close()
    logger.debug(f"Saved visualization to {filename}")


# =========================================================
# 5. Example usage
# =========================================================


def solver(n: int,
           H: int, W: int,
           blocks: defaultdict,
           packing_list: list[int]) -> bool:

    piece_types = []
    for i in range(len(packing_list)):
        piece_types.append((blocks[i], packing_list[i]))

    selected, placements = solve_pulp(H, W, piece_types)

    if selected is None:
        logger.critical("None from selected, infeasible")
        return False

    board = render_solution(H, W, piece_types, placements, selected)

    visualize(board, Path(f"12/images/packing_result_{n}.png"))

    return True


def day12_visual_sample(filename):
    # Process sample file here
    blocks, _, presents = read_input(Path(filename))

    # Loop over all items in sample file
    solutions = []
    for i, line in enumerate(presents):
        line = line.split(': ')
        width, length = [int(x) for x in line[0].split('x')]
        packing_list = [int(x) for x in line[1].split(' ')]

        solutions.append(
            solver(1000+i, length, width, blocks, packing_list))

    # Show result
    logger.info(f'Amount of possibilities: {sum(solutions)}')

    return sum(solutions)


if __name__ == "__main__":
    day12_visual_sample('12/sample01.txt')
