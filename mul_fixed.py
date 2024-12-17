from ortools.sat.python import cp_model

# Input data
data = {}
data["weights"] = [48, 30, 42, 36, 36, 48, 42, 42, 36, 24, 30, 30, 42, 36, 36]
data["values"] = [10, 30, 25, 50, 35, 30, 15, 40, 30, 35, 45, 10, 20, 30, 25]
assert len(data["weights"]) == len(data["values"])
num_items = len(data["weights"])
all_items = range(num_items)

data["bin_capacities"] = [100, 100, 100, 100, 100]

# Create the model
model = cp_model.CpModel()
num_bins = len(data["bin_capacities"])
all_bins = range(num_bins)

# Decision variables: x[bin][item] = 1 if item is placed in bin, else 0
x = [[model.NewIntVar(0, 1, f'x{bin}{item}') for item in all_items] for bin in all_bins]

# Constraints:
# 1. Each item must be assigned to exactly one bin
for item in all_items:
    model.Add(sum(x[bin][item] for bin in all_bins) == 1)

# 2. Weight constraint: the total weight in each bin must not exceed the bin's capacity
for bin in all_bins:
    weight_expr = sum(x[bin][item] * data['weights'][item] for item in all_items)
    model.Add(weight_expr <= data['bin_capacities'][bin])

# Objective: Maximize the total value
objective = sum(x[bin][item] * data['values'][item] for bin in all_bins for item in all_items)
model.Maximize(objective)

# Solve the model
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Output the result
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f"Total packed value: {int(solver.ObjectiveValue())}")
    total_weight = 0
    for bin in all_bins:
        print(f"Bin {bin}")
        bin_weight = 0
        bin_value = 0
        for item in all_items:
            if solver.Value(x[bin][item]) == 1:
                print(f"Item:{item} weight:{data['weights'][item]} value:{data['values'][item]}")
                bin_weight += data['weights'][item]
                bin_value += data['values'][item]
        print(f"Packed bin weight: {bin_weight}")
        print(f"Packed bin value: {bin_value}")
        total_weight += bin_weight
    print(f"Total packed weight: {total_weight}")
else:
    print("No Solution")
