n, k, q = map(int, input().split())
d = list(map(int, input().split()))
c = []
for _ in range(n+1):
    c.append(list(map(int, input().split())))
y=[0 for x in range(k)]
x=[0 for x in range(n)]    
visited = [False for x in range(n)]

def checkY(v,k):
    if v==0:
        return True
    if load[k] + d[v] > q:
        return False
    if visited[v] = True:
        return False
    return True
def solve():
    f = 0
    fs = float('inf') 
    y[0] = 0
    for v in range(1,n+1):
        visited[v] = False
    Try_Y(1)
    return fs

def Try_Y(k):
    s=0
    if y[k-1] > 0:
        s=y[k-1]+1
    for v in range(s,n+1):
        if checkY(v,k):
            y[k]=v
            if v>0:
                segments = segments +1
            visited[v] = True
            f = f + c[0][v]
            load[k]+=load[k]+d[v]
            if k<K:
                Try_Y(y[1],1)
            else:
                nbr = segments
                Try_X(y[1],1)
            load[k] = load[k] - d[v]
            visited[v] = False
            f = f - c[0][v]
            if v>0:
                segments = segments -1  



