from ortools.linear_solver import pywraplp

def ILP():
    n, q = map(int, input().split())
    worker_list = [[] for _ in range(n)]
    pres = []
    
    for _ in range(q):
        pres.append(tuple(map(int, input().split())))
    
    d = list(map(int, input().split()))
    m = int(input())
    starts = list(map(int, input().split()))
    K = int(input())
    
    cost_list = [[999 for _ in range(m)] for _ in range(n)]
    for _ in range(K):
        line = input()
        parts = line.split()
        if len(parts) == 3:
            task, team, value = map(int, parts)
            worker_list[task - 1].append(team - 1)
            cost_list[task - 1][team - 1] = value

    dct = {}
    for i in pres:
        if i[0] - 1 not in dct:
            dct[i[0] - 1] = [i[1] - 1]
        else:
            dct[i[0] - 1].append(i[1] - 1)

    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()
    large = max(sum(d) + max(d) + max(starts), n + 1)

    X = [[solver.IntVar(0, 1, f'X[{i}, {j}]') for j in range(n)] for i in range(m)]

    # Each task is assigned to at most one team
    for j in range(n):
        solver.Add(sum(X[i][j] for i in range(m)) <= 1)

    # Tasks can only be assigned to eligible teams
    for j in range(n):
        not_in = set(range(m)) - set(worker_list[j])
        for i in not_in:
            solver.Add(X[i][j] == 0)

    assign = [solver.IntVar(0, m - 1, f'A[{j}]') for j in range(n)]

    for i in range(m):
        for j in range(n):
            solver.Add(large * (1 - X[i][j]) + i >= assign[j])
            solver.Add(-large * (1 - X[i][j]) + i <= assign[j])

    times = [solver.IntVar(0, large, f'times[{j}]') for j in range(n)]

    # Precedence constraints
    for first in dct:
        for second in dct[first]:
            solver.Add(times[first] + d[first] <= times[second])

    # Ensure team availability and task durations do not overlap
    for i in range(m):
        for j in range(n):
            for k in range(j + 1, n):
                if j != k:
                    t = solver.IntVar(0, 1, f'T[{i}, {j}, {k}]')
                    solver.Add((1 - X[i][j]) * large + (1 - X[i][k]) * large + times[j] + t * large >= times[k] + d[k])
                    solver.Add((1 - X[i][j]) * large + (1 - X[i][k]) * large + times[k] + (1 - t) * large >= times[j] + d[j])
            solver.Add((1 - X[i][j]) * large + times[j] >= starts[i])

    costs = solver.IntVar(0, INF, 'cost')
    total_cost = sum(X[i][j] * cost_list[j][i] for i in range(m) for j in range(n))
    solver.Add(costs == total_cost)

    number_task = solver.IntVar(1, n, 'n_t')
    total_tasks = sum(X[i][j] for i in range(m) for j in range(n))
    solver.Add(number_task == total_tasks)

    Z = solver.IntVar(0, INF, 'z')
    for j in range(n):
        solver.Add(Z >= times[j] + d[j])

    # Objective: Maximize the number of tasks completed
    solver.Maximize(number_task)
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solver.Add(number_task == number_task.solution_value())
        solver.Minimize(Z)
        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            solver.Add(Z == Z.solution_value())
            solver.Minimize(costs)
            status = solver.Solve()

            if status == pywraplp.Solver.OPTIMAL:
                print(int(number_task.solution_value()))
                for j in range(n):
                    for i in range(m):
                        if X[i][j].solution_value() == 1:
                            print(j + 1, i + 1, int(times[j].solution_value()))
            else:
                print('INFEASIBLE' if status == 2 else 'UNBOUNDED' if status == 3 else 'ERROR')
        else:
            print('INFEASIBLE' if status == 2 else 'UNBOUNDED' if status == 3 else 'ERROR')
    else:
        print('INFEASIBLE' if status == 2 else 'UNBOUNDED' if status == 3 else 'ERROR')

if __name__ == '__main__':
    ILP()
