def input_data():
    n, m, s, L = [int(x) for x in input().split()]
    edges = []
    for _ in range(m):
        u, v, t, c = [int(x) for x in input().split()]
        edges.append([u - 1, v - 1, t, c])
        edges.append([v - 1, u - 1, t, c])
    return n, m, s - 1, L, edges

n, m, s, L, edges = input_data()

from ortools.sat.python import cp_model
model = cp_model.CpModel()

x = {}
for i, j, t, c in edges:
    x[i, j] = model.NewIntVar(0, 1, f'x[{i},{j}]')
#y represent time
y = [model.NewIntVar(0, 1000, f'y[{i}]') for i in range(n)]

#constraint
model.Add(y[s] == 0)
for i, j, t, c in edges:
    model.Add(x[i, j] + x[j, i] <= 1)

for i, j, t, c in edges:
    b = model.NewBoolVar('')
    model.Add(x[i, j] == 1).OnlyEnforceIf(b)
    model.Add(x[i, j] != 1).OnlyEnforceIf(b.Not())
    model.Add(y[i] + t == y[j]).OnlyEnforceIf(b)

model.Add(sum(x[i, j] for i, j, t, c in edges) == n - 1)


for i in range(n):
    model.Add(y[i] <= L)


for i, j, t, c in edges:
    if j == 0:
        model.Add(x[i, j] == 0)

for j in range(1, n):
    model.Add(sum(x[u, v] for u, v, t, c in edges if v == j) == 1)
model.Minimize(sum(x[i, j] * c for i, j, t, c in edges))
solver = cp_model.CpSolver()
status = solver.Solve(model)
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(int(solver.ObjectiveValue()))

else:
    print("NO_SOLUTION")