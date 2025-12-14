from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from pulp import LpProblem, LpVariable, LpBinary, lpSum, LpStatus, LpMinimize
from pulp import HiGHS_CMD, PULP_CBC_CMD

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

    print("Solving with CBC...")
    prob.solve(PULP_CBC_CMD(msg=1))  # , timeLimit=300))
    # print("Solving with HIGHS...")
    # prob.solve(HiGHS_CMD(msg=True, timeLimit=300))

    if LpStatus[prob.status] != "Optimal":
        print("No optimal solution found:", LpStatus[prob.status])
        return None, placements, None

    print("Optimal solution found.")
    selected = [i for i in range(len(x)) if x[i].value() > 0.5]
    return selected, placements, prob


# =========================================================
# 4. Board reconstruction & visualization
# =========================================================

def render_solution(grid_h, grid_w, piece_types, placements, selected):
    board = -1 * np.ones((grid_h, grid_w), dtype=int)

    for sel in selected:
        pid, _, _, _, cells = placements[sel]
        for (r, c) in cells:
            board[r, c] = pid

    return board


def visualize(board, filename="result.png"):
    plt.figure(figsize=(10, 10))
    plt.imshow(board, interpolation='nearest', cmap="tab10")
    plt.title("Packing result (digits = piece id, -1 empty)")
    # plt.colorbar()
    plt.savefig(filename, dpi=120)
    plt.close()
    print("Saved visualization to", filename)


# =========================================================
# 5. Example usage
# =========================================================

def solver(n: int = 0, H: int = 25, W: int = 25, needeth: list[int] = [1, 2, 3, 4, 5, 6]) -> bool:
    # Example grid
    # H, W = 49, 65

    # Example pieces: (pattern, count_required)

    piece_types = [
        (["###", ".#.", "###"], needeth[0]),
        (["###", ".##", "##."], needeth[1]),
        (["###", "##.", "#.."], needeth[2]),
        (["###", "#.#", "#.#"], needeth[3]),
        (["###", "###", "..#"], needeth[4]),
        (["##.", ".##", ".##"], needeth[5]),
    ]

    selected, placements, prob = solve_pulp(H, W, piece_types)

    if selected is None:
        print("None from selected, infeasible")
        return False

    board = render_solution(H, W, piece_types, placements, selected)

    # print("\nBoard:")
    # for r in range(H):
    #     print("".join('.' if board[r, c] == -1 else str(board[r, c]) for c in range(W)))

    visualize(board, Path(f"12/images/packing_result_{n}.png"))

    return True


if __name__ == "__main__":
    solver(0, 25, 25, [1, 2, 10, 11, 4, 6])
