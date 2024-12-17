from ortools.sat.python import cp_model
data = {}
data["weights"] = [48, 30, 42, 36, 36, 48, 42, 42, 36, 24, 30, 30, 42, 36, 36]
data["values"] = [10, 30, 25, 50, 35, 30, 15, 40, 30, 35, 45, 10, 20, 30, 25]
assert len(data["weights"]) == len(data["values"])
num_items = len(data["weights"])
all_items = range(num_items)

data["bin_capacities"] = [100, 100, 100, 100, 100]
model = cp_model.CpModel()
num_bins = len(data["bin_capacities"])
all_bins = range(num_bins)
#decision var
x = [[None for x in all_items] for y in all_bins]  #shape:
for bin in all_bins:
    for item in all_items:
        x[bin][item] = model.new_int_var(0, 1 ,f'x{bin}{item}')
#constraint
# each item belong to exactly 1 bin
for item in all_items:
    item_list = []
    for tmp_bin in all_bins:
        item_list.append(x[tmp_bin][item])
    model.add(sum(item_list) <=1)
# in each bin the weight cannot excess cap

# In each bin, the weight cannot exceed the bin's capacity
for bin in all_bins:
    weight_expr = sum(x[bin][tmp_item] * data['weights'][tmp_item] for tmp_item in all_items)
    model.add(weight_expr <= data['bin_capacities'][bin])

# for bin in all_bins:
#     cap = sum([x[bin][tmp_item]*data['weights'][tmp_item] for tmp_item in all_items])
#     model.add(cap<data['bin_capacities'][bin])
#objective 

obj = 0
for bin in all_bins:
    val_per_bin = sum([x[bin][tmp_item]*data['values'][tmp_item] for tmp_item in all_items])
    obj+=val_per_bin
model.maximize(obj)
solver = cp_model.CpSolver()
status = solver.Solve(model)
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(int(solver.ObjectiveValue()))
else:
    print("No Solution")








'''' 
answer:
Total packed value: 395.0
Bin 0
Item:2 weight:42 value:25
Item:7 weight:42 value:40
Packed bin weight: 84
Packed bin value: 65

Bin 1
Item:1 weight:30 value:30
Item:4 weight:36 value:35
Item:10 weight:30 value:45
Packed bin weight: 96
Packed bin value: 110

Bin 2
Item:12 weight:42 value:20
Item:14 weight:36 value:25
Packed bin weight: 78
Packed bin value: 45

Bin 3
Item:3 weight:36 value:50
Item:8 weight:36 value:30
Item:9 weight:24 value:35
Packed bin weight: 96
Packed bin value: 115

Bin 4
Item:5 weight:48 value:30
Item:13 weight:36 value:30
Packed bin weight: 84
Packed bin value: 60

Total packed weight: 438
'''