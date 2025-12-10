from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpInteger, value


def solve_joltage(target, flip_ops):
    n_bits = len(target)
    n_ops = len(flip_ops)

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
    prob.solve()
    return [int(value(var)) for var in x]


if __name__ == "__main__":
    target = [3, 5, 4, 7]
    flip_ops = [
        [3],
        [1, 3],
        [2],
        [2, 3],
        [0, 2],
        [0, 1]
    ]

    print(target, flip_ops)
    solution = solve_joltage(target, flip_ops)
    print(solution)
    print("Total presses:", sum(solution))
