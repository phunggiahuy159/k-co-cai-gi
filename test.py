from ortools.sat.python import cp_model
model = cp_model.CpModel()

x = model.new_int_var(0,3,'x')
y = model.new_int_var(0,2,'y')
z = model.new_int_var(0,2,'z')
model.Add(x!=y)
model.Add(y!=z)
model.Add(z!=x)
model.maximize(x+y+z)
solver = cp_model.CpSolver()
status = solver.Solve(model)
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(int(solver.ObjectiveValue()))
