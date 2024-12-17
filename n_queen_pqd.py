n = 40
import random as rd

x = [0 for i in range(n)]

def vio():
    v = 0 
    for i in range(n):
        for j in range(i+1, n):
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
                v+=1
            if x[i] + i == x[q] + q:
                v += 1
            if x[i] - i == x[q] - q:
                v += 1
    return v
def SelectMostVio():
    maxV = 0
    q = -1
    L=[]
    for i in range(n):
        v = imm_vio(i)
        if maxV < v:
            maxV = v
            L=[]
            L.append(i)
        elif maxV==v:
            L.append(i) 
        idx=rd.randint(0,len(L)-1) 
        q=L[idx]   
    return q
def GetDelta(q, r):
    current_violations = x[q]
    x[q] = r 
    new_violations = imm_vio(q)
    delta = new_violations - current_violations
    x[q] = current_violations
    return delta
def SelectMostPromissingRow(q):
    minV = float('inf')
    sel_r = -1
    for r in range(n):
        delta = GetDelta(q, r)
        if delta < minV:
            minV = delta
            L=[]
            L.append(r)
        elif delta == minV:
            L.append(r)
        idx=rd.randint(0,len(L)-1) 
        sel_r=L[idx]         

        # sel_r = r
    return sel_r
def GenInitSol():
    for q in range(n):
        x[q] = 0
def local_search(maxiter = 1000):
    global violations
    GenInitSol()
    violation = vio()
    for iter in range(maxiter):
        if violation == 0: 
            break
        q = SelectMostVio()
        r = SelectMostPromissingRow(q)
        x[q] = r
        violations = vio()
        print('Step', iter,' violations', violations)

local_search(5000)