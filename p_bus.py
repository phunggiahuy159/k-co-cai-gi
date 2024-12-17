n, k = map(int,input().split())
distance = []
for i in range(2*n+1):
    values = list(map(int, input().strip().split()))
    distance.append(values)
visited = [False for x in range(2*n+1)]
load = 0
f = 0
fs = float('inf')
cmin = min(distance[i][j] for i in range(2 * n + 1) for j in range(2 * n + 1) if i != j and distance[i][j] > 0)

x = [0 for x in range(2*n+1)]
def check(v):
    if visited[v]:
        return False
    if v > n and not visited[v - n]:  
        return False
    if v <= n and load + 1 > k:  
        return False
    return True  

def updateBest():
    global fs
    global f
    if f + distance[x[2 * n]][0] < fs:  
        fs = f + distance[x[2 * n]][0]



def Try(k):
    global f, load, fs
    for v in range(1, 2 * n + 1):
        if check(v):
            x[k] = v
            visited[v] = True
            f += distance[x[k - 1]][v]  
            
            if v <= n:
                load += 1  
            else:
                load -= 1  
            if k == 2 * n:  
                updateBest()
            else:

                if f + cmin * (2 * n + 1 - k) < fs:
                    Try(k + 1)

            if v <= n:
                load -= 1
            else:
                load += 1
            f -= distance[x[k - 1]][v]
            visited[v] = False

x[0] = 0
Try(1)


print(fs)