from ortools.linear_solver import pywraplp

def input_data():
    m,n = [int(x) for x in input().split()]
    preference_matrix = []
    for i in range(m):
        r = [int(x)-1 for x in input().split()[1:]]
        preference_matrix.append(r)

    k = int(input())
    B = []
    for _ in range(k):
        [i,j] = [int(x)-1 for x in input().split()]
        B.append([i,j])
    
    return m,n,preference_matrix,B

m,n,preference_matrix, B = input_data()

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()
x = [[solver.IntVar(0,1,'x(' + str(t) + ',' + str(i) + ')' ) for i in range(n)] for t in range(m)]
y = [solver.IntVar(0, n, 'y(' + str(t) +')') for t in range (m)]
z = solver.IntVar(0, n, 'z')

for t in range(m):
    for i in range(n):
        if not(i in preference_matrix[t]):
            c = solver.Constraint(0,0)
            c.SetCoefficient(x[t][i],1)
for [i,j] in B:
    for t in range(m):
        c = solver.Constraint(0,1)
        c.SetCoefficient(x[t][i],1)
        c.SetCoefficient(x[t][j],1)

for t in range(m):
    c = solver.Constraint(0,0)
    for i in range(n):
        c.SetCoefficient(x[t][i],1)
    c.SetCoefficient(y[t],-1)

for t in range(m):
    c = solver.Constraint(0,INF)
    c.SetCoefficient(z,1)
    c.SetCoefficient(y[t],-1)


for i in range(n):
    c = solver.Constraint(1,1)
    for t in range(m):
        c.SetCoefficient(x[t][i],1)

obj = solver.Objective()
obj.SetCoefficient(z,1)


status = solver.Solve()

print(int(solver.Objective().Value()))