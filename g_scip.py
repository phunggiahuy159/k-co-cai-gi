from ortools.linear_solver import pywraplp

def solve_tsp_scip(n, c):
    # Create the SCIP solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("SCIP solver not available.")
        return

    # Decision variables: x[i, j] is 1 if the path goes from i to j, 0 otherwise
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:  # No self-loops
                x[(i, j)] = solver.BoolVar(f'x[{i},{j}]')

    # Additional variables for subtour elimination
    u = [solver.NumVar(0, n - 1, f'u[{i}]') for i in range(n)]

    # Objective function: minimize total cost
    solver.Minimize(solver.Sum(c[i][j] * x[(i, j)] for i in range(n) for j in range(n) if i != j))

    # Constraints: exactly one outgoing edge from each node
    for i in range(n):
        solver.Add(solver.Sum(x[(i, j)] for j in range(n) if i != j) == 1)

    # Constraints: exactly one incoming edge to each node
    for j in range(n):
        solver.Add(solver.Sum(x[(i, j)] for i in range(n) if i != j) == 1)

    # Subtour elimination constraints
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                solver.Add(u[i] - u[j] + n * x[(i, j)] <= n - 1)

    # Solve the problem
    status = solver.Solve()

    # Output the solution
    if status == pywraplp.Solver.OPTIMAL:
        print(f"Minimum cost: {solver.Objective().Value()}")
        print("Path:")
        current_node = 0
        visited = [False] * n
        path = [0]
        while len(path) < n:
            for j in range(n):
                if current_node != j and x[(current_node, j)].solution_value() > 0.5:
                    path.append(j)
                    visited[j] = True
                    current_node = j
                    break
        path.append(0)  # Return to the start
        print(path)
    else:
        print("No solution found.")

# Input
def read_input():
    import sys
    [n] = [int(x) for x in sys.stdin.readline().split()]
    c = []
    for i in range(n):
        row = [int(x) for x in sys.stdin.readline().split()]
        c.append(row)
    return n, c

n, c = read_input()
solve_tsp_scip(n, c)
