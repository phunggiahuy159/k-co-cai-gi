n = int(input(''))
domain = {}
for i in range(1, n + 1):
    values = list(map(int, input().strip().split()))
    k = values[0]  
    domain_values = values[1:k + 1]  
    domain[i] = domain_values
m = int(input(''))
constraints = []
for _ in range(m):
    i, j, D = map(int, input().strip().split())
    constraints.append((i, j, D))


queue = [(x, c) for x in domain.keys() for c in constraints if x == c[0]]

print(queue)
# LEQ constraint Xi <= Xj + D
def revise_ac3(x,c):
    change = False
    i, j, d = c
    if x==i:
        for value_x in domain[x]:
            count = 0
            for value_other in domain[j]:
                if value_x <= value_other + d:
                    break
                else:
                    count += 1
            if count == len(domain[j]):
                domain[x].remove(value_x)   
                change = True  
    if x==j:
        for value_x in domain[x]:
            count = 0
            for value_other in domain[i]:
                if value_other <= value_x + d:
                    break
                else:
                    count += 1
            if count == len(domain[j]):
                domain[x].remove(value_x) 
                change = True
    return change

# print(revise_ac3(1,(1,2,4)))


def ac3():
    queue = [(x, c) for x in domain.keys() for c in constraints if x == c[0]]
    while len(queue[0]) != 0  :
        x, c =  queue[0]
        queue.pop(0)
        if revise_ac3(x,c):
            if len(domain[x]) != 0:
                # return 'FAIL'
                print('FAIL')
            else:
                queue.extend([(y, c1) for y in domain.keys() 
                    for c1 in constraints 
                    if (y == c1[0] and x == c1[1]) or (y == c1[1] and x == c1[0]) and y != x and c1 != c])
    for i in range(1, n + 1):
        tmp = sorted(domain[i])  # Sort values in increasing order
        print(len(tmp), end=' ')  # Print number of values first
        print(*tmp)           
            
ac3()            

