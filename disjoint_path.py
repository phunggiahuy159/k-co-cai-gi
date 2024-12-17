n, m = map(int, input().split())
edges = []
for _ in range(m):
    u, v, c = map(int, input().split())
    edges.append((u, v, c))
from ortools.linear_solver import pywraplp

def solve_edge_disjoint_paths(n, edges, s=1, t=10):
    # Initialize the solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    # Create variables x(i, j) and y(i, j)
    x = {}
    y = {}
    for (i, j, c) in edges:
        x[(i, j)] = solver.BoolVar(f'x[{i},{j}]')
        y[(i, j)] = solver.BoolVar(f'y[{i},{j}]')
    # Create Lx(i) and Ly(i) variables for each node
    Lx = {i: solver.NumVar(0, solver.infinity(), f'Lx[{i}]') for i in range(1, n + 1)}
    Ly = {i: solver.NumVar(0, solver.infinity(), f'Ly[{i}]') for i in range(1, n + 1)}

    # Flow balance constraints for each node except source and target
    for i in range(1, n + 1):
        if i != s and i != t:
            solver.Add(sum(x[(i, j)] for (i_, j, c) in edges if i_ == i) ==
                       sum(x[(j, i_)] for (j, i_, c) in edges if i_ == i))
            solver.Add(sum(y[(i, j)] for (i_, j, c) in edges if i_ == i) ==
                       sum(y[(j, i_)] for (j, i_, c) in edges if i_ == i))

    solver.Add(sum(x[(s, j)] for (s_, j, c) in edges if s_ == s) == 1)
    solver.Add(sum(y[(s, j)] for (s_, j, c) in edges if s_ == s) == 1)
    solver.Add(sum(x[(i, t)] for (i, t_, c) in edges if t_ == t) == 1)
    solver.Add(sum(y[(i, t)] for (i, t_, c) in edges if t_ == t) == 1)

    for (i, j, c) in edges:
        solver.Add(x[(i, j)] + y[(i, j)] <= 1)

    # Distance accumulation constraints
    for (i, j, c) in edges:
        solver.Add(Lx[j] >= Lx[i] + c * x[(i, j)])
        solver.Add(Ly[j] >= Ly[i] + c * y[(i, j)])

    # Initial distance constraints
    solver.Add(Lx[s] == 0)
    solver.Add(Ly[s] == 0)

    # Objective function: minimize Lx(t) + Ly(t)
    solver.Minimize(Lx[t] + Ly[t])

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Minimum cost:', solver.Objective().Value())
        return solver.Objective().Value()
    else:
        print('No solution found.')
        return None

# n = 10
# solve_edge_disjoint_paths(n, edges)
