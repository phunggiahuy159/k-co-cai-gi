from ortools.linear_solver import pywraplp

# Input
n, m, s, l = map(int, input().split())
time = {}
cost = {}
edges = {}

for _ in range(m):
    u, v, t, c = map(int, input().split())
    time[(u, v)] = t
    cost[(u, v)] = c

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables: whether an edge (u, v) is selected
for edge in time.keys():
    u, v = edge
    edges[edge] = solver.IntVar(0, 1, f'x{u}{v}')

# Constraints



# 1. Ensure that each node (except the source) is reachable
for node in range(1, n + 1):
    if node != s:
        incoming_edges = [edges[(u, v)] for (u, v) in edges if v == node]
        solver.Add(sum(incoming_edges) >= 1)

# 2. Transmission time constraint
for node in range(1, n + 1):
    if node != s:
        incoming_edges = [(time[(u, v)], edges[(u, v)]) for (u, v) in edges if v == node]
        solver.Add(sum(t * x for t, x in incoming_edges) <= l)

# Objective: Minimize the total cost
solver.Minimize(solver.Sum(cost[edge] * edges[edge] for edge in edges))

# Solve
status = solver.Solve()

# Output
if status == pywraplp.Solver.OPTIMAL:
    total_cost = sum(cost[edge] * edges[edge].solution_value() for edge in edges)
    print(int(total_cost))
else:
    print("NO_SOLUTION")
