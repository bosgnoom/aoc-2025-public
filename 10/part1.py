import numpy as np
from itertools import product


def minimal_flips(target_bits, flip_ops):
    n_bits = len(target_bits)
    n_ops = len(flip_ops)

    # Build A matrix
    A = np.zeros((n_bits, n_ops), dtype=np.uint8)
    for j, op in enumerate(flip_ops):
        for b in op:
            A[b, j] = 1
    b = np.array(target_bits, dtype=np.uint8)

    # --- Gaussian elimination mod 2 ---
    A2 = A.copy()
    b2 = b.copy()
    piv = [-1] * n_ops
    r = 0

    for c in range(n_ops):
        # find pivot
        for rr in range(r, n_bits):
            if A2[rr, c] == 1:
                A2[[r, rr]] = A2[[rr, r]]
                b2[[r, rr]] = b2[[rr, r]]
                piv[c] = r
                break
        if piv[c] == -1:
            continue

        # eliminate
        for rr in range(n_bits):
            if rr != r and A2[rr, c] == 1:
                A2[rr] ^= A2[r]
                b2[rr] ^= b2[r]

        r += 1

    # check consistency
    for rr in range(n_bits):
        if not A2[rr].any() and b2[rr] == 1:
            return None  # no solution

    # pivot/free split
    pivot_cols = [c for c in range(n_ops) if piv[c] != -1]
    free_cols = [c for c in range(n_ops) if piv[c] == -1]

    # find particular solution (free vars = 0)
    x0 = np.zeros(n_ops, dtype=np.uint8)
    for c in pivot_cols:
        row = piv[c]
        rhs = b2[row]
        for fc in free_cols:
            if A2[row, fc]:
                rhs ^= x0[fc]
        x0[c] = rhs

    # compute nullspace basis vectors
    # each free variable introduces one null basis vector
    null_basis = []
    for fc in free_cols:
        v = np.zeros(n_ops, dtype=np.uint8)
        v[fc] = 1
        for c in pivot_cols:
            r = piv[c]
            if A2[r, fc]:
                v[c] = 1
        null_basis.append(v)

    # enumerate nullspace combinations only
    best = None
    for coeffs in product([0, 1], repeat=len(null_basis)):
        x = x0.copy()
        for coef, v in zip(coeffs, null_basis):
            if coef:
                x ^= v
        w = x.sum()
        if best is None or w < best:
            best = w

    return best
