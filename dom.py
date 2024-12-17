def read_input():

    n = int(input().strip())
    
    domains = {}

    for i in range(1, n + 1):
        values = list(map(int, input().strip().split()))
        k = values[0]  
        domain_values = values[1:k + 1] 
        domains[i] = domain_values
    
    m = int(input().strip())
    
    constraints = []

    for _ in range(m):
        i, j, D = map(int, input().strip().split())
        constraints.append((i, j, D))

    return n, domains, m, constraints

'''
Perform the domain consistency for the CSP with n variables X1, X2, . . ., Xn with a set of LEQ constraints under the form: Xi <= Xj + D

Input
Line 1: contains a positive integer n (1 <= n <= 50)
Line i+1 (i = 1, 2, ..., n): contains a positive integer k and k subsequent integers v(i,1), v(i,2), . . ., v(i,k) which are the values of the domain of Xi 
Line n+2: contains a positive integer m (1 <=  m <= 50) which is the number of LEQ constraints
Line n+2+i (i = 1, 2, ..., m): contains i, j and D which represent the LEQ constraint Xi <= Xj + D
 
Output
Line i (i = 1, 2, ..., n): contains q (number of values of the domain of Xi) and a sequence (increasing order) of values of the domain of Xi the DC propagation (after each value, there is a SPACE character) or print FAIL if the domain of some variable becomes empty.

Example
Input
4
3 1 2 7
7 1 2 3 4 5 6 7
4 2 4 6 8
5 1 3 5 7 9
4
1 2 4
2 3 -3
4 2 -1
3 4 2


Output
FAIL

Input
5 
3 1 2 7 
7 1 2 3 4 5 6 7 
4 2 4 6 8 
5 1 3 5 7 9 
6 1 2 3 4 5 6  
3 
1 2 4 
4 2 -1 
5 3 -1
Output
3 1 2 7  
6 2 3 4 5 6 7  
4 2 4 6 8  
3 1 3 5  
6 1 2 3 4 5 6
'''

n, domains, m, constraints = read_input()
queue = [(x, c) for x in domains.keys() for c in constraints if x == c[0]]

# print(n, domains, m, constraints)
# 4 {1: [1, 2, 7], 2: [1, 2, 3, 4, 5, 6, 7], 3: [2, 4, 6, 8], 4: [1, 3, 5, 7, 9]} 4 [(1, 2, 4), (2, 3, -3), (4, 2, -1), (3, 4, 2)]
# print(queue)

# print("----------------")
# print(domains[1][:])
def ac3(n, domains, m, constraints):
    for c in constraints:
        i, j, _ = c
        queue.append((i, c))
        queue.append((j, c))
    while queue:
        (x, c) = queue.pop(0)
        if revise(x, c, domains):
            if not domains[x]:
                print("FAIL")
                return "FAIL"
            queue.extend([(y, c1) for y in domains.keys() 
                for c1 in constraints 
                if (y == c1[0] and x == c1[1]) or (y == c1[1] and x == c1[0]) and y != x and c1 != c])
    for i in range(1, n + 1):
        domain = sorted(domains[i])  # Sort values in increasing order
        print(len(domain), end=' ')  # Print number of values first
        print(*domain)


def revise(x, c, domains):
    change = False
    i, j, D = c
    if x == i:
        domain_copy = domains[x].copy()
        for value in domain_copy:
            if not any(value <= valj + D for valj in domains[j]):
                domains[x].remove(value)
                change = True
        return change
    elif x == j:
        domain_copy = domains[x].copy()
        for value in domain_copy:
            if not any(vali <= value + D for vali in domains[i]):
                domains[x].remove(value)
                change = True
        return change

ac3(n, domains, m, constraints)