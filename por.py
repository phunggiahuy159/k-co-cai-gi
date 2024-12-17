from ortools.linear_solver import pywraplp

def ILP():
    n, q = map(int, input().split())
    worker_list = [[] for _ in range(n)]
    d = []
    pres = []
    starts = []

    for _ in range(q):
        pres.append(tuple(map(int, input().split())))

    d = list(map(int, input().split()))
    
    m = int(input())
    starts = list(map(int, input().split()))
    
    K = int(input())
    
    cost_list = [[999 for _ in range(m)] for _ in range(n)]
    
    for _ in range(K):
        line = input().split()
        i, j, value = map(int, line)
        worker_list[i - 1].append(j - 1)
        cost_list[i - 1][j - 1] = value

    dct = {}
    for i in pres:
        if i[0] - 1 not in dct:
            dct[i[0] - 1] = [i[1] - 1]
        else:
            dct[i[0] - 1].append(i[1] - 1)

    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()
    large = max(sum(d) + max(d) + max(starts), n + 1)

    X = [[solver.IntVar(0, 1, f'X[{i},{j}]') for j in range(n)] for i in range(m)]
    
    times = [solver.IntVar(0, large, f'times[{i}]') for i in range(n)]
    
    for i in range(n):
        solver.Add(sum(X[j][i] for j in range(m)) <= 1)

    for i in range(n):
        not_in = set(range(m)) - set(worker_list[i])
        for j in not_in:
            solver.Add(X[j][i] == 0)

    for first in dct:
        for second in dct[first]:
            solver.Add(times[first] + d[first] <= times[second])

    for i in range(m):
        for j in range(n):
            solver.Add((1 - X[i][j]) * large + times[j] >= starts[i])

    for i in range(m):
        for j in range(n):
            for k in range(j + 1, n):
                solver.Add((1 - X[i][j]) * large + (1 - X[i][k]) * large + times[j] >= times[k] + d[k])
                solver.Add((1 - X[i][j]) * large + (1 - X[i][k]) * large + times[k] >= times[j] + d[j])

    costs = solver.Sum(X[i][j] * cost_list[j][i] for i in range(m) for j in range(n))
    number_task = solver.Sum(X[i][j] for i in range(m) for j in range(n))
    Z = solver.IntVar(0, INF, 'z')
    for i in range(n):
        solver.Add(Z >= times[i] + d[i])

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
                for i in range(n):
                    for j in range(m):
                        if X[j][i].solution_value() == 1:
                            print(i + 1, j + 1, int(times[i].solution_value()))
                            break
            else:
                print('INFEASIBLE' if status == pywraplp.Solver.INFEASIBLE else 'ERROR')
        else:
            print('INFEASIBLE' if status == pywraplp.Solver.INFEASIBLE else 'ERROR')

if __name__ == '__main__':
    ILP()
