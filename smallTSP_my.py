from ortools.sat.python import cp_model
#input
n = int(input(''))
d = []
for x in range(n):
    val = list(map(int,input('').split()))
    d.append(val)
# print(d)    
# solver 
model = cp_model.CpModel()
x = [[0 for i in range(n)] for j in range(n)]
for i in range(n):
    for j in range(n):
        x[i][j] = model.NewIntVar(0,1,f'x{i}{j}')
#constraint
# in = out = 1 for every city
for i in range(n):
    lis1 = []
    lis2 = []
    for j in range(n):
        lis1.append(x[i][j])
        lis2.append(x[j][i])
    model.Add(sum(lis1) == 1)
    model.Add(sum(lis2) == 1)
#circuit    
for i in range(n):
    if i != 0:
        for j in range(i,n):
            b = model.NewBoolVar('')
            model.Add(x[i][j] == 1).OnlyEnforceIf(b)
            model.Add(x[i][j] != 1).OnlyEnforceIf(b.Not())
            model.Add(x[j][i] !=1).OnlyEnforceIf(b)



#objective
obj = []
for i in range(n):
    val = []
    for j in range(n):
        val.append(x[i][j]*d[i][j])
    obj.append(sum(val))  
final_obj = sum(obj)      


model.Minimize(final_obj)
solver = cp_model.CpSolver()
status = solver.Solve(model)
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(int(solver.ObjectiveValue()))
else:
    print("No Solution")







