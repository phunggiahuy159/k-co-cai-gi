from ortools.linear_solver import pywraplp
#input

n=int(input())
distance_matrix=[]
for i in range(n):
    distance_matrix.append(list(map(int, input().split())))

solver = pywraplp.Solver.CreateSolver('SCIP')

#decision var
x={}
for i in range(n):
    for j in range(n):
        x[i, j]=solver.IntVar(0, 1, f'x{i}{j}')

for i in range(n):
    solver.Add(solver.Sum([x[j, i] for j in range(n) if j!=i]) == 1)  
    solver.Add(solver.Sum([x[i, j] for j in range(n) if j!=i]) == 1)  

u={}
for i in range(n):
    u[i]=solver.IntVar(0, n-1, f'u{i}')
for i in range(1, n):
    for j in range(1, n):
        if i!= j:
            solver.Add(u[i] - u[j] + n * x[i, j] <= n - 1)
objective=solver.Objective()
for i in range(n):
    for j in range(n):
        objective.SetCoefficient(x[i, j], distance_matrix[i][j])
objective.SetMinimization()
status=solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    tour = []
    start_city = 0
    current_city = start_city
    while True:
        tour.append(current_city + 1)  
        for j in range(n):
            if x[current_city, j].solution_value() == 1:
                current_city = j
                break
        if current_city == start_city:
            break
    print(len(tour))
    print(" ".join(map(str, tour)))