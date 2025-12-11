from itertools import product
import numpy as np
import pytest
from part1 import minimal_flips
from part2 import sample


# Learning by example, this is what a LLM came up with...


def test_single_bit_single_op():
    # Flip bit 0 → target [1]
    assert minimal_flips([1], [[0]]) == 1


def test_single_bit_unreachable():
    # Operation flips nothing → cannot reach [1]
    assert minimal_flips([1], [[]]) is None


def test_two_bits_independent_ops():
    # Two independent operations
    # op0 flips bit0   → [1,0]
    # op1 flips bit1   → [0,1]
    # target is [1,1] so we need both
    assert minimal_flips([1, 1], [[0], [1]]) == 2


def test_two_bits_one_op():
    # One operation flips both bits at once
    assert minimal_flips([1, 1], [[0, 1]]) == 1


def test_redundant_ops():
    # target = [1,0,1]
    # op0 = flip 0,2
    # op1 = flip 0 only
    # op2 = flip 2 only
    # Best is op0 (1 op), not op1+op2 (2 ops)
    assert minimal_flips([1, 0, 1], [[0, 2], [0], [2]]) == 1


def test_multiple_solutions_choose_minimal():
    # op0 flips [0]
    # op1 flips [0]
    # target = [1]
    #
    # Solutions:
    #   x0=1,x1=0 → weight 1
    #   x0=0,x1=1 → weight 1
    #   x0=1,x1=1 → weight 2  (redundant)
    #
    # Result must be 1.
    assert minimal_flips([1], [[0], [0]]) == 1


def test_three_bits_chain_ops():
    # op0: flip 0,1
    # op1: flip 1,2
    # target: [1,0,1]
    #
    # Solve: pick op0 and op1 → XOR:
    #    op0 ^ op1 flips 0,2 → gives [1,0,1]
    # Minimum weight = 2
    assert minimal_flips([1, 0, 1], [[0, 1], [1, 2]]) == 2


def test_inconsistent_system():
    # Flip ops never touch bit 2 → impossible to reach target[2]=1
    assert minimal_flips([0, 0, 1], [[0], [1]]) is None


def brute_force_min_flips(target_bits, flip_ops):
    n = len(flip_ops)
    best = None

    for mask in product([0, 1], repeat=n):
        result = [0] * len(target_bits)

        # apply selected ops
        for op_index, use in enumerate(mask):
            if use:
                for bit in flip_ops[op_index]:
                    result[bit] ^= 1

        if result == target_bits:
            w = sum(mask)
            best = w if best is None or w < best else best

    return best


@pytest.mark.parametrize("n_bits,n_ops", [(4, 4), (5, 3)])
def test_random_small(n_bits, n_ops):
    rng = np.random.default_rng(0)

    for _ in range(50):
        target = rng.integers(0, 2, size=n_bits).tolist()

        flip_ops = [
            sorted(rng.choice(
                n_bits,
                size=rng.integers(0, n_bits),
                replace=False
            ).tolist())
            for _ in range(n_ops)
        ]

        expected = brute_force_min_flips(target, flip_ops)
        actual = minimal_flips(target, flip_ops)

        assert actual == expected
