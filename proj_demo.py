from ortools.linear_solver import pywraplp
def ILP():
    n, q = map(int, input().split())
    worker_list =[[] for _ in range(n)]
    d = []
    pres = []
    starts = []
    for i in range(q):
        pres.append(tuple(map(int, input().split())))
    d = list(map(int, input().split()))
    m = int(input())
    starts = list(map(int, input().split()))
    K = int(input())
    cost_list = [[999 for _ in range(m)] for _ in range(n)]
    for i in range(K):
        line = input()
        parts = line.split()
        if len(parts) == 3:
            i, j, value = map(int, parts)
            worker_list[i - 1].append(j-1)
            cost_list[(i-1)][(j-1)] = value
    dct = {}
    for i in pres:
        if i[0]-1 not in dct:
            dct[i[0]-1] = [i[1]-1]
        else:
            dct[i[0]-1].append(i[1]-1)

    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()
    max_time = max(sum(d) + max(d)+max(starts), n + 1)
    x = [[None]*n for i in range(m)]
    
    for i in range(m):
        for j in range(n):
            x[i][j] = solver.IntVar(0, 1, 'x[{}, {}]'.format(i, j))

    for i in range(n):
        solver.Add(sum([x[j][i] for j in range(m)]) <= 1)

    for i in range(n):
        not_in = set(list(range(m))) - set(worker_list[i])
        for j in not_in:
            solver.Add(x[j][i] == 0)
    assign = [solver.IntVar(0, m-1, 'A[{}]'.format(i)) for i in range(n)]

    for i in range(m):
        for j in range(n):
            solver.Add(max_time * (-x[i][j]+1) + i >= assign[j])
            solver.Add(-max_time * (-x[i][j]+1) + i <= assign[j])

    times = [solver.IntVar(0, max_time, 'times[{}]'.format(i)) for i in range(n)]

    for first in dct:
        for second in dct[first]:
            solver.Add(times[first] + d[first] <= times[second])

    for i in range(m):
        for j in range(n):
            for k in range(j+1, n):
                if j != k:
                    t = solver.IntVar(0, 1, 'T[{}{}{}]'.format(i, j, k))
                    solver.Add((1 - x[i][j])*max_time + (1 - x[i][k])*max_time + times[j] + t*max_time >= times[k] + d[k])
                    solver.Add((1 - x[i][j])*max_time + (1 - x[i][k])*max_time + times[k] + (1-t)*max_time >= times[j] + d[j])
            solver.Add((1-x[i][j])*max_time + times[j] >= starts[i])

    costs = solver.IntVar(0, INF, 'cost')
    sum_ = 0
    for i in range(m):
        for j in range(n):
            sum_ += x[i][j] * cost_list[j][i]
    solver.Add(costs == sum_)
    number_task = solver.IntVar(1, n, 'n_t')
    task = 0
    for i in range(m):
        for  j in range(n):
            task += x[i][j]
    solver.Add(number_task == task)
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
            if status == 0:
                print(int(number_task.solution_value()))
                for i in range(n):
                    if x[int(assign[i].solution_value())][i].solution_value() ==1:
                        print(i+1, int(assign[i].solution_value()+1), int(times[i].solution_value()))
            else:
                if status == 2:
                    print('INFEASIBLE')
                elif status == 3:
                    print('Unbound')
                else:
                    print('ERROR')
        else:
            if status == 2:
                print('INFEASIBLE')
            elif status == 3:
                print('Unbound')
            else:
                print('ERROR')  
if __name__ == '__main__':
    ILP()