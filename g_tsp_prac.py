from ortools.sat.python import cp_model

def solve_tsp(n, c):
    # Create the CP-SAT model
    model = cp_model.CpModel()
    
    # Decision variables
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                x[(i, j)] = model.NewIntVar(0, 1, f'x({i},{j})')
    
    # Additional variable for subtour elimination
    y = [model.NewIntVar(0, sum(sum(row) for row in c), f'y({i})') for i in range(n)]
    
    # Flow constraints
    for i in range(n):
        model.Add(sum(x[(i, j)] for j in range(n) if i != j) == 1)  # Outflow from each node
    for j in range(n):
        model.Add(sum(x[(i, j)] for i in range(n) if i != j) == 1)  # Inflow to each node
    
    # Subtour elimination constraints
    model.Add(y[0] == 0)  # Starting node
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                b = model.NewBoolVar('')
                model.Add(x[(i, j)] == 1).OnlyEnforceIf(b)
                model.Add(x[(i, j)] == 0).OnlyEnforceIf(b.Not())
                model.Add(y[i] + c[i][j] == y[j]).OnlyEnforceIf(b)
    
    # Objective function: minimize the cost
    model.Minimize(sum(x[(i, j)] * c[i][j] for i in range(n) for j in range(n) if i != j))
    
    # Solve the model
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30.0
    status = solver.Solve(model)
    
    # Output the result
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"Minimum cost: {solver.ObjectiveValue()}")
        path = []
        current = 0
        while True:
            for j in range(n):
                if current != j and solver.Value(x[(current, j)]) == 1:
                    path.append(current)
                    current = j
                    break
            if current == 0:
                break
        path.append(0)
        print("Path:", path)
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
solve_tsp(n, c)
