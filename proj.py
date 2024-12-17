from ortools.linear_solver import pywraplp

def solve_ilp(N, Q, pred, d, M, s, K, c):
    max_completion_time = sum(d) + sum(s)
    max_cost = sum([sum(c[i]) for i in range(N+1)])

    # Declare the solver
    solver = pywraplp.Solver.CreateSolver('SAT')

    # Declare variables
    a = [[0 for _ in range(M+1)] for _ in range(N+1)]
    for i in range(1, N+1):
        for j in range(1, M+1):
            a[i][j] = solver.IntVar(0, 1, 'a' + str(i) + str(j))

    t = [0 for _ in range(N+1)]
    for i in range(1, N+1):
        t[i] = solver.IntVar(0, max_completion_time, 'time' + str(i))

    u = [0 for _ in range(N+1)]
    for i in range(1, N+1):
        u[i] = solver.IntVar(0, 1, 'u' + str(i))

    m = [[0 for _ in range(N+1)] for _ in range(N+1)]
    b = [[0 for _ in range(N+1)] for _ in range(N+1)]

    for i in range(1, N+1):
        for j in range(1, N+1):
            m[i][j] = solver.IntVar(-max_completion_time, max_completion_time, 'm' + str(i) + str(j))
            b[i][j] = solver.IntVar(0, 1, 'b' + str(i) + str(j))

    num_tasks = solver.IntVar(0, N, 'num_tasks')
    completion_time = solver.IntVar(0, max_completion_time, 'completion_time')
    total_cost = solver.IntVar(0, max_cost, 'total_cost')

    # Declare the constraints
    for i in range(1, N+1):
        solver.Add(sum([a[i][j] for j in range(1, M+1)]) == u[i])

    for i, j in pred:
        solver.Add(t[j] >= t[i] + d[i])
        solver.Add(u[i] >= u[j])

    for i in range(1, N+1):
        solver.Add(t[i] >= sum([s[j]*a[i][j] for j in range(1, M+1)]))
        solver.Add(t[i] - (1 - u[i])*2*max_completion_time + d[i] <= completion_time)

    for i in range(1, N+1):
        for j in range(1, M+1):
            solver.Add(a[i][j] <= min(c[i][j], 1))

    for i1 in range(1, N+1):
        for i2 in range(i1+1, N+1):
            solver.Add(t[i1] - t[i2] - d[i2] <= m[i1][i2])
            solver.Add(t[i2] - t[i1] - d[i1] <= m[i1][i2])
            solver.Add(t[i1] - t[i2] - d[i2] + 2*max_completion_time*b[i1][i2] >= m[i1][i2])
            solver.Add(t[i2] - t[i1] - d[i1] + 2*max_completion_time*(1-b[i1][i2]) >= m[i1][i2])
            
            for j in range(1, M+1):
                solver.Add(m[i1][i2] + max_completion_time*(2 - a[i1][j] - a[i2][j]) >= 0)

    solver.Add(num_tasks == sum([u[i] for i in range(1, N+1)]))
    solver.Add(total_cost == sum(sum([c[i][j]*a[i][j] for j in range(1, M+1)]) for i in range(1, N+1)))

    c1 = (max_cost + 1)*(max_completion_time + 1)
    c2 = max_cost + 1
    c3 = 1
    solver.Maximize(c1*num_tasks - c2*completion_time - c3*total_cost)

    # Solve the problem
    status = solver.Solve()

    # Prepare the results
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        team = [0 for _ in range(N+1)]
        for i in range(1, N+1):
            for j in range(1, M+1):
                if a[i][j].solution_value() != 0:
                    team[i] = j
                    break
        schedule = []
        for i in range(1, N+1):
            if team[i] != 0:
                schedule.append(i)
        
        result = {
            'total_tasks_completed': int(num_tasks.solution_value()),
            'total_completion_time': int(completion_time.solution_value()),
            'total_cost': int(total_cost.solution_value()),
            'schedule': [(i, team[i], int(t[i].solution_value())) for i in schedule]
        }
    else:
        result = None

    return result


# Function to take input from terminal
def input_from_terminal():
    N, Q = map(int, input("Enter N and Q: ").split())
    
    pred = []
    print("Enter the precedence relations (i j) for Q tasks:")
    for _ in range(Q):
        i, j = map(int, input().split())
        pred.append((i, j))
    
    d = [0] + list(map(int, input("Enter task durations: ").split()))  # Add a 0 for 1-based index
    
    M = int(input("Enter the number of teams: "))
    
    s = [0] + list(map(int, input("Enter the start times for each team: ").split()))  # 1-based index
    
    K = int(input("Enter the number of valid task-team-cost relationships: "))
    c = [[0 for _ in range(M+1)] for _ in range(N+1)]  # Create the cost matrix (1-based indexing)
    
    print("Enter the valid task-team-cost relationships:")
    for _ in range(K):
        task, team, cost = map(int, input().split())
        c[task][team] = cost

    return N, Q, pred, d, M, s, K, c


def main():
    # Get input data from terminal
    N, Q, pred, d, M, s, K, c = input_from_terminal()
    
    # Solve the ILP problem
    result = solve_ilp(N, Q, pred, d, M, s, K, c)

    # Output the results
    if result:
        print(f"Total tasks completed: {result['total_tasks_completed']}")
        print(f"Total completion time: {result['total_completion_time']}")
        print(f"Total cost: {result['total_cost']}")
        for task, team, time in result['schedule']:
            print(f"Task {task} assigned to team {team} at time {time}")
    else:
        print("No solution found")


if __name__ == "__main__":
    main()
