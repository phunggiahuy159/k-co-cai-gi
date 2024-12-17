
from ortools.linear_solver import pywraplp

def solve_tsp(distance_matrix):
    num_locations = len(distance_matrix)
    
    # Create the solver
    solver = pywraplp.Solver.CreateSolver('GLOP')

    # Variables: x[i][j] = 1 if we travel from i to j
    x = {}
    for i in range(num_locations):
        for j in range(num_locations):
            if i != j:
                x[i, j] = solver.BoolVar(f'x[{i},{j}]')

    # Objective function: minimize total travel cost
    objective_terms = []
    for i in range(num_locations):
        for j in range(num_locations):
            if i != j:
                objective_terms.append(distance_matrix[i][j] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))

    # Constraints
    # Each location must be entered and exited exactly once
    for k in range(num_locations):
        solver.Add(solver.Sum(x[i, k] for i in range(num_locations) if i != k) == 1)
        solver.Add(solver.Sum(x[k, j] for j in range(num_locations) if j != k) == 1)

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Objective value =', solver.Objective().Value())
        route = []
        for i in range(num_locations):
            for j in range(num_locations):
                if i != j and x[i, j].solution_value() > 0:
                    route.append((i, j))
        print('Route:', route)
    else:
        print('The problem does not have an optimal solution.')

# Example distance matrix
distance_matrix = [
    [0, 1, 1, 9],
    [1, 0, 9, 3],
    [1, 9, 0, 2],
    [9, 3, 2, 0]
]

solve_tsp(distance_matrix)