n = int(input())

x = [0 for i in range(n)]

def vio():
    v = 0
    for i in range(n):
        for j in range(i + 1, n):
            if x[i] == x[j]:
                v += 1
            if x[i] + i == x[j] + j:
                v += 1
            if x[i] - i == x[j] - j:
                v += 1
    return v

def imm_vio(q):
    v = 0
    for i in range(n):
        if i != q:
            if x[i] == x[q]:
                v += 1
            if x[i] + i == x[q] + q:
                v += 1
            if x[i] - i == x[q] - q:
                v += 1
    return v

def SelectMostVio():
    maxV = -1  # Initialize with a value less than any possible violation count
    q = -1     # Initialize q
    for i in range(n):
        v = imm_vio(i)
        if maxV < v:
            maxV = v
            q = i  # Return the index, not the violation count
    return q

def GetDelta(q, r):
    original_value = x[q]  # Store the original value
    x[q] = r
    new_violations = imm_vio(q)
    x[q] = original_value  # Restore the original value
    return new_violations - imm_vio(q)  # Recalculate original violations


def SelectMostPromissingRow(q):
    minV = float('inf')
    sel_r = -1 # Initialize sel_r
    for r in range(n):
        delta = GetDelta(q, r)
        if delta < minV:
            minV = delta
            sel_r = r
    return sel_r

def GenInitSol():
    pivot = n // 2

    for q in range(pivot):
        x[q] = 2*q +2
        x[pivot + q] = 2*q + 1

def local_search(maxiter=1000):
    GenInitSol()
    violations = vio()  # Initialize violations here
    for iter in range(maxiter):
        if violations == 0:
            break
        q = SelectMostVio()
        if q == -1: # Handle case where no violations are found
            break
        r = SelectMostPromissingRow(q)
        x[q] = r
        violations = vio()  # Update violations after the move
        # print('Step', iter, ' violations', violations)

local_search(10)
print(n)

print(*x)