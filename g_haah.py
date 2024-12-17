from ortools.linear_solver import pywraplp

def solve_edge_disjoint_paths(n, edges):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return "NOT_FEASIBLE"
    x = {}
    y = {}
    for u, v, c in edges:
        x[(u, v)] = solver.BoolVar(f"x[{u},{v}]")
        y[(u, v)] = solver.BoolVar(f"x[{u},{v}]")

    solver.Add(sum(x[(1, v)] for u, v, c in edges if u == 1) ==1)
    solver.Add(sum(y[(1, v)] for u, v, c in edges if u == 1) ==1)

    solver.Add(sum(x[(u, n)] for u, v, c in edges if v == n) ==1)
    solver.Add(sum(y[(u, n)] for u, v, c in edges if v == n) ==1)

    for node in range(2, n):
        solver.Add(sum(x[(u, node)] for u, v, c in edges if v == node) - 
                    sum(x[(node, v)] for u, v, c in edges if u == node) == 0)
        solver.Add(sum(y[(u, node)] for u, v, c in edges if v == node) - 
            sum(y[(node, v)] for u, v, c in edges if u == node) == 0)

    for u, v, c in edges:
        solver.Add(x[(u, v)] + y[(u, v)] <= 1)
    arrx = []
    arry = []    
    for u,v,c in edges:
        arrx.append(x[(u,v)]*c)
        arry.append(y[(u,v)]*c)
    Lx = solver.Sum(arrx)
    Ly = solver.Sum(arry)


    # Lx = solver.Sum([x[(u,v)]*c for u,v,c in edges])
    # Ly = solver.Sum([y[(u,v)]*c for u,v,c in edges])    
        

    solver.Minimize(Lx + Ly)

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        return int(solver.Objective().Value())
    else:
        return "NOT_FEASIBLE"

# Input
n, m = map(int, input().split())
edges = []
for _ in range(m):
    u, v, c = map(int, input().split())
    edges.append((u, v, c))

result = solve_edge_disjoint_paths(n, edges)
print(result)




# 25 48
# 1 2 2
# 1 3 3
# 2 4 8
# 2 5 5
# 3 4 1
# 3 6 7
# 3 20 5
# 3 25 9
# 4 5 9
# 4 6 3
# 4 21 6
# 4 25 7
# 5 8 9
# 5 9 1
# 5 25 3
# 6 7 4
# 6 8 4
# 7 8 8
# 7 10 4
# 8 9 5
# 8 10 5
# 9 10 3
# 10 11 1
# 10 12 3
# 11 12 6
# 11 15 2
# 12 14 2
# 12 15 9
# 13 15 1
# 14 15 7
# 15 18 2
# 15 19 1
# 16 20 4
# 17 20 3
# 17 18 1
# 17 19 5
# 19 20 9
# 19 22 3
# 19 25 5
# 20 21 1
# 20 22 3
# 20 24 8
# 21 23 4
# 21 24 8
# 21 25 9
# 23 24 8
# 23 25 1
# 24 25 6