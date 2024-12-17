
#n domain for n var
#m constraint
def read_input():
    # Read the number of variables
    n = int(input().strip())
    
    # Dictionary to store the domains of each variable
    domains = {}

    # Reading the domains for each variable Xi
    for i in range(1, n + 1):
        values = list(map(int, input().strip().split()))
        k = values[0]  # First value is the number of domain elements
        domain_values = values[1:k + 1]  # The subsequent k values are the domain values
        domains[i] = domain_values
    
    # Read the number of LEQ constraints
    m = int(input().strip())
    
    # List to store the LEQ constraints
    constraints = []

    # Reading the constraints
    for _ in range(m):
        i, j, D = map(int, input().strip().split())
        constraints.append((i, j, D))

    # Output the parsed data
    return n, domains, m, constraints

# Test the function
n, domains, m, constraints = read_input()

# Display the result


def domain(x):
    return domains[x]
#[(1, 2, 4), (2, 3, -3), (4, 2, -1), (3, 4, 2)]  constraint
def get_neightboor(x):
    res = []
    for i in constraints:
        if i[0]==x:
            res.append(i[1])
        if i[1]==x:
            res.append(i[0])    
    return res

def revise(x, c):

    D = c[2]  
    revise = False
    if c[1] == x:
        y = c[0]
        pos_x = 1  
    elif c[0] == x:
        y = c[1]
        pos_x = 0  
    else:
        return False  

    domain_x = domain(x)
    domain_y = domain(y)
    
    new_domain_x = set()
    
    for val_x in domain_x:
        satisfy_constraint = False
        
        for val_y in domain_y:
            if pos_x == 1:  
                if val_y <= val_x + D:
                    satisfy_constraint = True
                    break
            elif pos_x == 0:  
                if val_x <= val_y + D:
                    satisfy_constraint = True
                    break
        if satisfy_constraint:
            new_domain_x.add(val_x)
    if len(new_domain_x) != len(domain_x):
        domains[x] = list(new_domain_x)  
        revise = True
    return revise


print(revise(1,(1,2,4)))    

            






# print(get_neightboor(1))

         
    

# print(f"Number of LEQ constraints (m): {m}")
# print("Constraints:")
# for i, j, D in constraints:
#     print(f"  X{i} <= X{j} + {D}")

# def domain(x):
#     return 