from ortools.sat.python import cp_model

model = cp_model.CpModel()
n = int(input())
distance_matrix = [] 
D = sum(sum(row) for row in distance_matrix)  
for i in range(n):
    distance_matrix.append(list(map(int, input().split())))
x = [[model.NewIntVar(0, 1, f'x({i},{j})') for j in range(n)] for i in range(n)]

y = [model.NewIntVar(0, n-1,  f'y({i})') for i in range(n)]
model.Minimize(sum(distance_matrix[i][j] * x[i][j] for i in range(n) for j in range(n)))


for i in range(n):
    model.Add(sum(x[i][j] for j in range(n) if j != i) == 1)  
    model.Add(sum(x[j][i] for j in range(n) if j != i) == 1)  

for i in range(1, n):
    for j in range(1, n):
        if i != j:
            model.Add(y[i] - y[j] + n * x[i][j] <= n - 1)
print(x)
print(y)



solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(solver.ObjectiveValue())
    for i in range(n):
        for j in range(n):
            if solver.Value(x[i][j]) == 1:
                print(f"Travel from city {i} to city {j}")
else:
    print("No solution found.")