from collections import deque

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

    return n, domains, m, constraints

def domain(x):
    return domains[x]

def get_neighbors(x):
    """
    Get all neighboring variables of x based on the constraints.
    """
    neighbors = []
    for i, j, D in constraints:
        if i == x:
            neighbors.append(j)
        elif j == x:
            neighbors.append(i)
    return set(neighbors)

def revise(x, c):
    D = c[2]
    revised = False

    # Determine which variable in the constraint is `x` and which is the neighbor `y`
    if c[1] == x:
        y = c[0]
        pos_x = 1  # Indicates `x` is Xj
    elif c[0] == x:
        y = c[1]
        pos_x = 0  # Indicates `x` is Xi
    else:
        return False  # x is not in the given constraint, no need to revise

    # Get domains of `x` and `y`
    domain_x = domain(x)
    domain_y = domain(y)
    
    # Initialize a new domain for `x`
    new_domain_x = []

    # AC-3 Revise: Iterate over domain of `x`
    for val_x in domain_x:
        satisfy_constraint = False

        # Check if there's any value in `domain_y` that satisfies the constraint
        for val_y in domain_y:
            if pos_x == 1:  # x is Xj, so the constraint is Xi <= Xj + D
                if val_y <= val_x + D:
                    satisfy_constraint = True
                    break
            elif pos_x == 0:  # x is Xi, so the constraint is Xi <= Xj + D
                if val_x <= val_y + D:
                    satisfy_constraint = True
                    break

        # If the value satisfies the constraint, add it to the new domain
        if satisfy_constraint:
            new_domain_x.append(val_x)

    # Check if domain of `x` is revised
    if set(new_domain_x) != set(domain_x):
        domains[x] = new_domain_x  # Update the domain of `x`
        revised = True

    return revised

def ac3():
    queue = deque()
    for (i, j, D) in constraints:
        queue.append((i, j))
    while queue:
        (xi, xj) = queue.popleft()
        if revise(xi, (xi, xj, next((D for (a, b, D) in constraints if (a == xi and b == xj) or (a == xj and b == xi)), 0))):
            if len(domain(xi)) == 0:
                return False
            for xk in get_neighbors(xi):
                if xk != xj:
                    queue.append((xk, xi))    
    return True

n, domains, m, constraints = read_input()

is_consistent = ac3()
if is_consistent == False:
    print('FAIl')
else:
    for x in domains.keys():
        res = ''
        ans = domains[x]
        length = len(ans)
        res = res + str(length)
        for x in ans:
            res += ' ' + str(x)
        print(res)     