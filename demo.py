
from ortools.linear_solver import pywraplp


def main():
    # [START solver]
    # Create the mip solver with the CP-SAT backend.
    solver = pywraplp.Solver.CreateSolver("SAT")
    if not solver:
        return
    # [END solver]

    # [START variables]
    infinity = solver.infinity()
    # x and y are integer non-negative variables.
    x = solver.IntVar(0.0, infinity, "x")
    y = solver.IntVar(0.0, infinity, "y")

    print("Number of variables =", solver.NumVariables())

    solver.Add(x + 7 * y <= 17.5)

    solver.Add(x <= 3.5)

    print("Number of constraints =", solver.NumConstraints())

    solver.Maximize(x + 10 * y)
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print("Objective value =", solver.Objective().Value())
        print("x =", x.solution_value())
        print("y =", y.solution_value())
    else:
        print("The problem does not have an optimal solution.")

    print("\nAdvanced usage:")
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")
    print(f"Problem solved in {solver.nodes():d} branch-and-bound nodes")


if __name__ == "__main__":
    main()
