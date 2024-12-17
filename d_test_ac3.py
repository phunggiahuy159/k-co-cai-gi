n = int(input(''))  # Read the number of variables
domain = {}

# Read domain values for each variable
for i in range(1, n + 1):
    values = list(map(int, input().strip().split()))
    k = values[0]  # Number of values for the variable
    domain_values = values[1:k + 1]  # List of domain values
    domain[i] = domain_values

m = int(input(''))  # Read number of constraints
constraints = []

# Read constraints
for _ in range(m):
    i, j, D = map(int, input().strip().split())
    constraints.append((i, j, D))  # Add the constraint

# Queue initialization with constraints
def revise_ac3(x, c):
    change = False
    i, j, d = c
    
    # If the variable is the first one in the constraint (Xi)
    if x == i:
        for value_x in domain[x][:]:  # Make a copy to iterate over
            count = 0
            for value_other in domain[j]:
                if value_x <= value_other + d:  # Check the constraint condition
                    break
                else:
                    count += 1
            if count == len(domain[j]):
                domain[x].remove(value_x)  # Remove the inconsistent value
                change = True
    
    # If the variable is the second one in the constraint (Xj)
    elif x == j:
        for value_x in domain[x][:]:  # Make a copy to iterate over
            count = 0
            for value_other in domain[i]:
                if value_other <= value_x + d:  # Check the constraint condition
                    break
                else:
                    count += 1
            if count == len(domain[i]):
                domain[x].remove(value_x)  # Remove the inconsistent value
                change = True
    
    return change

def ac3():
    queue = [(x, c) for x in domain.keys() for c in constraints if x == c[0]]
    
    # Perform AC3 algorithm
    while queue:
        x, c = queue.pop(0)
        
        if revise_ac3(x, c):  # If domain of x is revised
            if len(domain[x]) == 0:  # If the domain becomes empty, print FAIL
                print('FAIL')
                return
            
            # Add constraints for neighbors of x to the queue
            for y in domain.keys():
                if (y != x):
                    queue.extend([(y, c1) for c1 in constraints if (y == c1[0] and x == c1[1]) or (y == c1[1] and x == c1[0])])
    
    # After the AC3 process, print the domains
    for i in range(1, n + 1):
        if len(domain[i]) == 0:
            print('FAIL')  # If any domain is empty, print FAIL
            return
        else:
            # Print the size of the domain and its values
            print(len(domain[i]), *domain[i])

# Run AC3 algorithm
ac3()
