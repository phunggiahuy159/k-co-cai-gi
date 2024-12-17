# N task, Q pair of pres, M teams, duration of task, avai contain time team i available

from ortools.linear_solver import pywraplp
N, Q = map(int,input().split())
worker_list =[[] for _ in range(N)] #worker_list[i]: task i+1 can be complete by team j+1

pre = []
duration = []
for _ in range(Q):
    task_i, task_j = map(int,input().split())
    pre.append(tuple((task_i,task_j)))
duration = list(map(int,input().split()))
M = int(input())
avai = list(map(int,input().split()))

K = int(input())
cost = [[999 for _ in range(M)] for _ in range(N)]
for i in range(K):
    line = input()
    parts = line.split()
    if len(parts) == 3:
        i, j, value = map(int, parts)
        worker_list[i - 1].append(j-1)
        cost[(i-1)][(j-1)] = value

#dct[i]: task i must be done before tasks in [i]
dct = {}
for i in pre:
    if i[0]-1 not in dct:
        dct[i[0]-1] = [i[1]-1]
    else:
        dct[i[0]-1].append(i[1]-1)


x = [[None]*M for i in range(N)]


solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

for i in range(N):
    for j in range(M):
        x[i][j] = solver.IntVar(0, 1, 'x{}{}'.format(i, j))
# 1 task must be completed up to  1 team
for i in range(N):
    solver.Add(sum([x[i][j] for j in range(M)]) <= 1)

#1 task can be performed by some teams that in worker list
for i in range(N):
    not_in = set(list(range(M))) - set(worker_list[i])
    for j in not_in:
        solver.Add(x[i][j] == 0)
large = 9999


assign = [solver.IntVar(0, M-1, 'A[{}]'.format(i)) for i in range(N)]

for i in range(M):
    for j in range(N):
        solver.Add(large * (-x[i][j]+1) + i >= assign[j])
        solver.Add(-large * (-x[i][j]+1) + i <= assign[j])

times = [solver.IntVar(0, large, 'times[{}]'.format(i)) for i in range(N)]

for first in dct:
    for second in dct[first]:
        solver.Add(times[first] + duration[first] <= times[second])

for i in range(N):
    for j in range(M):
        for k in range(j+1, N):
            if j != k:
                t = solver.IntVar(0, 1, 'T[{}, {}, {}]'.format(i, j, k))
                solver.Add((1 - x[i][j])*large + (1 - x[i][k])*large + times[j] + t*large >= times[k] + duration[k])
                solver.Add((1 - x[i][j])*large + (1 - x[i][k])*large + times[k] + (1-t)*large >= times[j] + duration[j])
        solver.Add((1-x[i][j])*large + times[j] >= avai[i])

costs = solver.IntVar(0, INF, 'cost')
sum_ = 0
for i in range(N):
    for j in range(M):
        sum_ += x[i][j] * cost[j][i]
solver.Add(costs == sum_)
number_task = solver.IntVar(1, N, 'n_t')
task = 0
for i in range(N):
    for  j in range(M):
        task += x[i][j]
solver.Add(number_task == task)
Z = solver.IntVar(0, INF, 'z')
for i in range(N):
    solver.Add(Z >= times[i] + duration[i])
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
            for i in range(N):
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



