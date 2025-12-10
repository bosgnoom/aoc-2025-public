from pulp import LpStatus
from pulp import PULP_CBC_CMD
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpInteger, value
import logging
import coloredlogs

coloredlogs.install(level='DEBUG', fmt='%(asctime)s %(levelname)s %(name)s [%(module)s:%(funcName)s] %(message)s')
logger = logging.getLogger(__name__)


def solve_joltage(target: list[int], flip_ops: list[list[int]]) -> int:
    """
    Solve a minimum-press button-flip problem using integer linear programming.

    Each flip operation is a column vector that flips a fixed set of bit
    positions. The function attempts to find the minimum number of times each
    operation should be applied so that the resulting bit pattern matches the
    desired `target` vector.

    The system is formulated as the ILP:

        minimize    sum_j x_j
        subject to  Σ_j A[i,j] * x_j == target[i]    for all bit i
                    x_j ∈ ℤ,  x_j ≥ 0

    where A[i,j] = 1 if flip operation j toggles bit i.

    Parameters
    ----------
    target : list[int]
        Desired bit pattern. Each entry is typically 0 or 1, indicating the
        required number of toggles modulo 2 for each bit.
    flip_ops : list[list[int]]
        List of flip operations. Each operation is a list of bit indices that
        this operation toggles.

    Returns
    -------
    list[int]
        List of integer press counts `x_j` for each flip operation. The list
        length equals the number of operations. Values may be greater than 1
        depending on the ILP solution.

    Notes
    -----
    - This formulation uses ordinary integer equality, not modulo-2 arithmetic.
      For problems over GF(2), consider reducing constraints modulo 2 or using
      a dedicated GF(2) solver.
    - Feasibility and optimality depend on the ILP solver backend available to
      PuLP on the system.
    """

    n_bits = len(target)
    n_ops = len(flip_ops)
    logger.debug("Number of bits: %d, number of operations: %d", n_bits, n_ops)
    logger.debug("Target bit vector: %s", target)

    # Build matrix
    A = [[0] * n_ops for _ in range(n_bits)]
    for j, op in enumerate(flip_ops):
        for b in op:
            A[b][j] = 1

    # Define ILP
    prob = LpProblem("MinButtonPresses", LpMinimize)
    x = [LpVariable(f"x{j}", lowBound=0, cat=LpInteger) for j in range(n_ops)]

    # Objective: minimize total presses
    prob += lpSum(x)

    # Constraints: each bit must reach target
    for i in range(n_bits):
        prob += lpSum(A[i][j] * x[j] for j in range(n_ops)) == target[i]

    # Solve
    prob.solve(PULP_CBC_CMD(msg=False))

    logger.debug("Solver status: %s", LpStatus[prob.status])

    return [int(value(var)) for var in x]


def sample() -> int:
    target = [3, 5, 4, 7]
    flip_ops = [
        [3],
        [1, 3],
        [2],
        [2, 3],
        [0, 2],
        [0, 1]
    ]
    solution = solve_joltage(target, flip_ops)

    logger.debug(f"Total presses: {sum(solution)}")
    return sum(solution)


if __name__ == "__main__":  # pragma: no cover
    sample()
