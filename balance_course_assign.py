import sys 
from ortools.linear_solver import pywraplp
def input():
    [m,n]=[int(x) for x in sys.stdin.readline().split()]
    P = []

    for i in range(m):
        r = [int(x)-1 for x in sys.stdin.readline().split()]
        P.append(r)
    [K] = [int(x) for x in sys.stdin.readline().split() ]
    B=[]
    for k in range(K):
        [i,j]=[int(x) for x in sys.stdin.readline().split()]
        B.append([i-1,j-1])
    return m,n,P,B 
m,n,P,B=input()

solver= pywraplp.Solver.CreateSolver("SCIP")
INF = solver.infinity()


x = [[solver.IntVar(0, 1,'x'+str(t)+'('+str(i)+')')for i in range(n)]for t in range(m)]
y=[solver.IntVar(0, n, '(' + str(t) + ")") for t in range(m)]
z= solver.IntVar(0,n,'z')

for t in range(m):
    for i in range(n):
        if not (i in P[t]):
            c=solver.Constraint(0,0)
            c.SetCoefficient(x[t][i],1)

for [i,j] in B:
    for t in range(m):
        c=solver.Constraint(0,1) 
        c.SetCoefficient(x[t][i],1)
        c.SetCoefficient(x[t][j],1)

for t in range(m):
    c = solver.Constraint(0, 0)
    for i in range(n):
        c.SetCoefficient(x[t][i], 1)
    c.SetCoefficient(y[t], -1)



for t in range(m):
    c=solver.Constraint(0,INF)
    c.SetCoefficient(z,1)
    c.SetCoefficient(y[t],-1)
for i in range(n):
    c = solver.Constraint(1,1)
    for t in range(m):
        c.SetCoefficient(x[t][i],1)

obj=solver.Objective()
obj.SetCoefficient(z,1)
obj.SetMinimization()
status=solver.Solve()

print(solver.Objective().Value())
'''
if status != pywraplp.Solver.OPTIMAL:
    print('no optimal')
else:
    print('obj=',solver.Objective().Value())
for t in range(m):
    for i in range(n):
        print(x[t][i],'=',x[t][i].solution_value())    
        '''




