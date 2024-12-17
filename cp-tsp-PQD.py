import sys 
from ortools.sat.python import cp_model
class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    #print intermediate solution
    def __init__(self,variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
    def on_solution_callback(self):
        self.__solution_count += 1
        for v in self.__variables:
            print(v,' = ',self.Value(v), end = ' ')
        print()
    def solution_count(self):
        return self.__solution_count



def input():
 [n] = [int(x) for x in sys.stdin.readline().split()]
 c = []
 for i in range(n):
  row = [int(x) for x in sys.stdin.readline().split()]
  row.append(row[0])
  c.append(row)
 c.append(c[0])
 return n,c 
 
n,c = input()
#print(c)
D = 0
for i in range(n+1):
 for j in range(n+1):
  D += c[i][j]
#print('D = ',D)


In = [set() for i in range(n+1)]
Out = [set() for i in range(n+1)]

for i in range(n+1):
 for j in range(n+1):
  #if i != j:
  Out[i].add(j)

for i in range(n+1):
 for j in range(n+1):
  #if i != j:
  In[i].add(j) 
   
#for i in range(n+1):
# print('In[' + str(i) + '] = ',In[i],' Out[' + str(i) + '] = ',Out[i])
  
model = cp_model.CpModel()
#x = [[model.NewIntVar(0,1,'x(' + str(i) +# ',' + str(j) + ')') for j in Out[i]] for i in range(n)]
x = {}
for i in range(n+1):
 for j in Out[i]:
  x[i,j] = model.NewIntVar(0,1,'x(' + str(i) + ',' + str(j) + ')')
  #print('create varaible ',x[i,j])
y = [model.NewIntVar(0,D,'y(' + str(i) + ')') for i in range(n+1)]


for i in range(n):
 #print('Out-Flow of ',i,' Out = ',Out[i])
 model.Add(sum(x[i,j] for j in Out[i]) == 1)

for i in range(1,n+1):
 model.Add(sum(x[j,i] for j in In[i]) == 1)

for i in range(n+1):
 model.Add(x[i,i] == 0)
 
model.Add(y[0] == 0)

for i in range(n+1):
 for j in range(n+1):
  b = model.NewBoolVar('')
  model.Add(x[i,j] == 1).OnlyEnforceIf(b)
  model.Add(x[i,j] != 1).OnlyEnforceIf(b.Not())
  model.Add(y[i] + c[i][j] == y[j]).OnlyEnforceIf(b)
  
model.Minimize(y[n])

  
solver = cp_model.CpSolver()

solver.parameters.max_time_in_seconds = 5.0

status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
 print(solver.Value(y[n]))
 '''
 print('obj = ',solver.Value(y[n]))
 for i in range(n+1):
  for j in range(n+1):
   if solver.Value(x[i,j]) > 0:
    print('x[' + str(i) + ',' + str(j) + '] = ',solver.Value(x[i,j]))
 
 for i in range(n+1):
  print('y[' + str(i) + '] = ',solver.Value(y[i])) 
 ''' 
  
 '''
 for i in range(n):
  print('x[' + str(i) + '] = ',solver.Value(x[i]))
 for i in range(n+1):
  print(y[i],solver.Value(y[i]))
 ''' 
else:
 print('no solution')
