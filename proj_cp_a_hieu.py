from ortools.sat.python import cp_model
# from checker import Checker
# Input
N, Q = map(int, input().split())
pred = []
for _ in range(Q):
    pred.append(map(int, input().split()))
d = [0] + list(map(int, input().split()))
M = int(input())
s = [0] + list(map(int, input().split()))
K = int(input())
c = [[0 for i in range(M+1)] for j in range(N+1)]
for _ in range(K):
    task, team, cost = map(int, input().split())
    c[task][team] = cost

# def InputFromFile(filepath):
#     f = open(filepath, 'r')
#     N, Q = map(int, f.readline().strip("\n").split())
#     pred = []
#     for _ in range(Q):
#         pred.append(tuple(map(int, f.readline().strip("\n").split())))
#     d = [0] + list(map(int, f.readline().strip("\n").split()))
#     M = int(f.readline().strip("\n"))
#     s = [0] + list(map(int, f.readline().strip("\n").split()))
#     K = int(f.readline().strip("\n"))
#     c = [[0 for i in range(M+1)] for j in range(N+1)]
#     for _ in range(K):
#         task, team, cost = map(int, f.readline().strip("\n").split())
#         c[task][team] = cost
#     f.close()
#     return N, Q, pred, d, M, s, K, c

# N, Q, pred, d, M, s, K, c = InputFromFile('test.txt')


max_completion_time = sum(d) + sum(s)
max_cost = sum([sum(c[i]) for i in range(N+1)])

# Declare the solver
model = cp_model.CpModel()

# Declare variables
a = [[0 for i in range(M+1)] for j in range(N+1)]
for i in range(1, N+1):
    for j in range(1, M+1):
        a[i][j] = model.NewIntVar(0, 1, 'a' + str(i) + str(j))

t = [0 for _ in range(N+1)]
for i in range(1, N+1):
    t[i] = model.NewIntVar(0, max_completion_time, 'time' + str(i))

u = [0 for _ in range(N+1)]
for i in range(1, N+1):
    u[i] = model.NewIntVar(0, 1, 'u' + str(i))

num_tasks = model.NewIntVar(0, N, 'num_tasks')
completion_time = model.NewIntVar(0, max_completion_time, 'completion_time')
total_cost = model.NewIntVar(0, max_cost, 'total_cost')

# Declare the constraints
for i in range(1, N+1):
    model.Add(sum([a[i][j] for j in range(1, M+1)]) >= u[i])
    model.Add(sum([a[i][j] for j in range(1, M+1)]) <= u[i])

for i, j in pred:
    model.Add(t[j] >= t[i] + d[i])
    model.Add(u[i] >= u[j])

for i in range(1, N+1):
    model.Add(t[i] >= sum([s[j]*a[i][j] for j in range(1, M+1)]))
    tmp = model.NewBoolVar('tmp')
    model.Add(u[i] == 1).OnlyEnforceIf(tmp)
    model.Add(u[i] == 0).OnlyEnforceIf(tmp.Not())
    model.Add(t[i] + d[i] <= completion_time).OnlyEnforceIf(tmp)

for i in range(1, N+1):
    for j in range(1, M+1):
        model.Add(a[i][j] <= min(c[i][j], 1))

for i1 in range(1, N+1):
    for i2 in range(1, N+1):
        if i1 != i2:
            for j in range(1, M+1):
                b = model.NewBoolVar('b')
                model.Add(a[i1][j] + a[i2][j] == 2).OnlyEnforceIf(b)
                model.Add(a[i1][j] + a[i2][j] != 2).OnlyEnforceIf(b.Not())
                b1 = model.NewBoolVar('b1')
                b2 = model.NewBoolVar('b2')
                model.Add(t[i1] >= t[i2] + d[i2]).OnlyEnforceIf(b1)
                model.Add(t[i1] < t[i2] + d[i2]).OnlyEnforceIf(b1.Not())
                model.Add(t[i2] >= t[i1] + d[i1]).OnlyEnforceIf(b2)
                model.Add(t[i2] < t[i1] + d[i1]).OnlyEnforceIf(b2.Not())
                model.AddBoolOr(b1, b2).OnlyEnforceIf(b)

model.Add(num_tasks >= sum([u[i] for i in range(1, N+1)]))
model.Add(num_tasks <= sum([u[i] for i in range(1, N+1)]))
model.Add(total_cost >= sum(sum([c[i][j]*a[i][j] for j in range(1, M+1)]) for i in range(1, N+1)))
model.Add(total_cost <= sum(sum([c[i][j]*a[i][j] for j in range(1, M+1)]) for i in range(1, N+1)))

# Declare the objective function
c1 = (max_cost + 1)*(max_completion_time + 1)
c2 = max_cost + 1
c3 = 1
model.Maximize(c1*num_tasks - c2*completion_time -c3*total_cost)

# Solve the problem
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 300.0
status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    team = [0 for _ in range(N+1)]
    for i in range(1, N+1):
        for j in range(1, M+1):
            if solver.Value(a[i][j]) != 0:
                team[i] = j
                break
    # schedule = []
    # for i in range(1, N+1):
    #     if team[i] != 0:
    #         schedule.append(i)
    # print(len(schedule))
    # for i in schedule:
    #     print(i, team[i], solver.Value(t[i]))
    ans = ""
    schedule = []
    for i in range(1, N+1):
        if team[i] != 0:
            schedule.append(i)
    ans = ans + str(len(schedule)) + "\n"
    # print(len(schedule))
    for i in schedule:
        # print(i, team[i], int(t[i].solution_value()))
        ans = ans + str(i) + " " + str(team[i]) + " " + str(int(solver.Value(t[i]))) + "\n"
    f = open('output.txt', 'w')
    f.write(ans)
    f.close()

# print(solver.ObjectiveValue())
print('--------------------------------------------------------------------')
print(solver.Value(num_tasks), solver.Value(completion_time), solver.Value(total_cost))
print(solver.WallTime())
# print(solver.ExportModelAsLpFormat(False).replace('\\', '').replace(',_', ','), sep='\n')

for i in range(1, N+1):
    for j in range(1, M+1):
        print(solver.Value(a[i][j]), end = " ")
    print()
# Checker()