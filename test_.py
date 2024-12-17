from ortools.linear_solver import pywraplp

def solve_tsp(distance_matrix):
    solver = pywraplp.Solver.CreateSolver('SCIP')

    num_cities = len(distance_matrix)
    x = {}
    #decision var
    for i in range(num_cities):
        for j in range(num_cities):
            x[i, j] = solver.IntVar(0, 1, f'x_{i}_{j}')

    for i in range(num_cities):
        solver.Add(solver.Sum([x[j, i] for j in range(num_cities) if j != i]) == 1)

    for i in range(num_cities):
        solver.Add(solver.Sum([x[i, j] for j in range(num_cities) if j != i]) == 1)

    u = {}
    for i in range(num_cities):
        u[i] = solver.IntVar(0, num_cities - 1, f'u_{i}')
    for i in range(1, num_cities):
        for j in range(1, num_cities):
            if i != j:
                solver.Add(u[i] - u[j] + num_cities * x[i, j] <= num_cities - 1)           

    # Define the objective function
    objective = solver.Objective()
    for i in range(num_cities):
        for j in range(num_cities):
            objective.SetCoefficient(x[i, j], distance_matrix[i][j])
    objective.SetMinimization()

    # Solve the problem
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        tour = []
        start_city = 0
        current_city = start_city
        while True:
            tour.append(current_city + 1)  
            for j in range(num_cities):
                if x[current_city, j].solution_value() == 1:
                    current_city = j
                    break
            if current_city == start_city:
                break
        return tour
    else:
        return None

if __name__ == "__main__":
    distance_matrix = []
    n = int(input())
    for i in range(n):
        distance_matrix.append(list(map(int, input().split())))

    tour = solve_tsp(distance_matrix)

    if tour:
        print(len(tour))
        print(" ".join(map(str, tour)))
    else:
        print("No solution found.")