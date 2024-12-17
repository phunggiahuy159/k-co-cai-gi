from ortools.linear_solver import pywraplp

def solve_edge_disjoint_paths(n, edges):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return "NOT_FEASIBLE"

    x = {}
    for u, v, c in edges:
        x[(u, v)] = solver.BoolVar(f"x[{u},{v}]")
        x[(v, u)] = solver.BoolVar(f"x[{v},{u}]")

    for node in range(1, n + 1):
        if node == 1:  
            solver.Add(sum(x[(1, v)] for u, v, c in edges if u == 1) - 
                       sum(x[(v, 1)] for u, v, c in edges if v == 1) == 2)
        elif node == n:  
            solver.Add(sum(x[(u, n)] for u, v, c in edges if v == n) - 
                       sum(x[(n, v)] for u, v, c in edges if u == n) == 2)
        else:  
            solver.Add(sum(x[(u, node)] for u, v, c in edges if v == node) - 
                       sum(x[(node, v)] for u, v, c in edges if u == node) == 0)

    for u, v, c in edges:
        solver.Add(x[(u, v)] + x[(v, u)] <= 1)

    # Objective function (minimize the total cost)
    solver.Minimize(solver.Sum(x[(u, v)] * c for u, v, c in edges))

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        return int(solver.Objective().Value())
    else:
        return "NOT_FEASIBLE"

# Input
n, m = map(int, input().split())
edges = []
for _ in range(m):
    u, v, c = map(int, input().split())
    edges.append((u, v, c))

result = solve_edge_disjoint_paths(n, edges)
print(result)
