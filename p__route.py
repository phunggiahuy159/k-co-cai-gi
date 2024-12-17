from ortools.linear_solver import pywraplp

def solve_network_broadcast(n, m, s, L, link_data):
  """Solves the network broadcast problem using SCIP.

  Args:
    n: Number of nodes.
    m: Number of links.
    s: Source node.
    L: Maximum transmission time.
    link_data: A list of tuples (u, v, t, c), where (u, v) is a link, t is
      the transmission time, and c is the cost.

  Returns:
    The total cost of the optimal solution or None if no solution exists.
  """

  # Create the MIP model
  solver = pywraplp.Solver.CreateSolver('SCIP')

  # Create variables
  x = {}
  t = {}
  for e in range(m):
    x[e] = solver.IntVar(0, 1, f'x[{e}]')
  for v in range(n):
    t[v] = solver.NumVar(0, solver.infinity(), f't[{v}]')

  # Set the objective function: Minimize total cost
  solver.Minimize(sum(link_data[e][3] * x[e] for e in range(m)))

  # Constraints
  # 1. Ensure all nodes are reachable from the source
  for v in range(n):
    if v != s:
      solver.Add(sum(x[e] for e in range(m) if link_data[e][0] == v or link_data[e][1] == v) >= 1)

  # 2. Maximum transmission time constraint
  for v in range(n):
    solver.Add(t[v] <= L)

  # 3. Flow conservation constraints
  for v in range(n):
    if v != s:
      solver.Add(sum(link_data[e][2] * x[e] for e in range(m) if link_data[e][0] == v) -
                   sum(link_data[e][2] * x[e] for e in range(m) if link_data[e][1] == v) == t[v])

  # 4. Initialize transmission time from the source
  t[s].SetBounds(0, 0)

  # Solve the model
  status = solver.Solve()

  if status == pywraplp.Solver.OPTIMAL:
    return solver.Objective().Value()
  else:
    return None
n, m, s, L = map(int, input().split())
time = {}
cost = {}
link_data = []

for _ in range(m):
    val = tuple(map(int, input().split()))
    link_data.append(val)

# Example usage
# n = 5  # Number of nodes
# m = 7  # Number of links
# s = 0  # Source node
# L = 10  # Maximum transmission time
# link_data = [(0, 1, 2, 3), (0, 2, 1, 2), (1, 2, 1, 1), (1, 3, 2, 2), (2, 3, 1, 3), (2, 4, 2, 4), (3, 4, 1, 2)]

total_cost = solve_network_broadcast(n, m, s, L, link_data)
if total_cost is not None:
  print("Total cost:", total_cost)
else:
  print("No solution found.")