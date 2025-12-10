import numpy as np
from itertools import product


def _gaussian_elimination_mod2(A: np.ndarray, b: np.ndarray):
    """
    Perform Gaussian elimination over GF(2) on Ax = b.

    Returns
    -------
    A2 : np.ndarray
        Row-reduced version of A.
    b2 : np.ndarray
        Corresponding transformed right-hand side.
    pivots : list[int]
        pivots[c] = row index for pivot in column c, or -1 if column is free.
    """
    n_rows, n_cols = A.shape
    A2 = A.copy()
    b2 = b.copy()
    pivots = [-1] * n_cols

    r = 0
    for c in range(n_cols):
        # Find pivot
        for rr in range(r, n_rows):
            if A2[rr, c] == 1:
                A2[[r, rr]] = A2[[rr, r]]
                b2[[r, rr]] = b2[[rr, r]]
                pivots[c] = r
                break

        if pivots[c] == -1:
            continue  # free column

        # Eliminate
        for rr in range(n_rows):
            if rr != r and A2[rr, c] == 1:
                A2[rr] ^= A2[r]
                b2[rr] ^= b2[r]

        r += 1

    return A2, b2, pivots


def _check_consistency(A: np.ndarray, b: np.ndarray) -> bool:
    """
    Check whether Ax = b is consistent in GF(2).
    """
    for r in range(A.shape[0]):
        if not A[r].any() and b[r] == 1:
            return False
    return True


def minimal_flips(target_bits: list[int], flip_ops: list[list[int]]) -> int:
    """
    Compute the minimum number of flip operations needed to obtain a desired
    bit pattern from an all-zero initial state, where each flip operation
    toggles a specific set of bit positions.

    The method translates each flip operation into a column of a binary
    matrix A, with the target bit vector as b. The linear system A·x = b
    is solved over GF(2) using Gaussian elimination. Because GF(2) systems
    may have many solutions, the function enumerates all combinations of
    null-space basis vectors to find the solution vector x with the smallest
    Hamming weight—representing the minimum number of operations.

    Parameters
    ----------
    target_bits : list[int]
        Desired bit configuration (each entry must be 0 or 1).
    flip_ops : list[list[int]]
        List of allowed flip operations. Each operation is a list of bit
        indices that this operation toggles.

    Returns
    -------
    int or None
        The minimal number of flip operations required to create
        ``target_bits`` using XOR combinations of the allowed operations,
        or ``None`` if no solution exists.
    """
    n_bits = len(target_bits)
    n_ops = len(flip_ops)

    # Build matrix A (bits × operations)
    A = np.zeros((n_bits, n_ops), dtype=np.uint8)
    for col, op in enumerate(flip_ops):
        for bit in op:
            A[bit, col] = 1

    b = np.array(target_bits, dtype=np.uint8)

    # Gaussian elimination over GF(2)
    A2, b2, pivots = _gaussian_elimination_mod2(A, b)

    # Consistency check
    if not _check_consistency(A2, b2):
        return None

    # Separate pivot and free columns
    pivot_cols = [c for c, p in enumerate(pivots) if p != -1]
    free_cols = [c for c, p in enumerate(pivots) if p == -1]

    # Particular solution with free variables = 0
    x0 = np.zeros(n_ops, dtype=np.uint8)
    for c in pivot_cols:
        r = pivots[c]
        rhs = b2[r]
        for fc in free_cols:
            if A2[r, fc]:
                rhs ^= x0[fc]
        x0[c] = rhs

    # Build nullspace basis vectors
    null_basis = []
    for fc in free_cols:
        v = np.zeros(n_ops, dtype=np.uint8)
        v[fc] = 1
        for c in pivot_cols:
            r = pivots[c]
            if A2[r, fc]:
                v[c] = 1
        null_basis.append(v)

    # Enumerate all combinations of nullspace contributions
    best = None
    for coeffs in product([0, 1], repeat=len(null_basis)):
        x = x0.copy()
        for coef, v in zip(coeffs, null_basis):
            if coef:
                x ^= v

        w = x.sum()  # Hamming weight

        if best is None or w < best:
            best = w

    return best
