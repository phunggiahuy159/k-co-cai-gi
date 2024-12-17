n, k, q = map(int, input().split())
d = list(map(int, input().split()))
c = []
for _ in range(n + 1):
    c.append(list(map(int, input().split())))

# State variables
y = [0] * k  
x = [0] * n  
visited = [False] * (n + 1)
load = [0] * k
segments = 0
f = 0
fs = float('inf')  
def checkY(v, k):
    if v == 0:  # Returning to depot is always valid
        return True
    if load[k] + d[v-1] > q:  # Check load capacity
        return False
    if visited[v]:  # Check if node is already visited
        return False
    return True


# Solve the problem
def solve():
    global fs, visited
    for v in range(1, n + 1):  # Initialize visited array
        visited[v] = False
    Try_Y(1)
    return fs


# Assign nodes to trucks
def Try_Y(k):
    global f, fs, segments, load
    start = 0
    if y[k - 1] > 0:
        start = y[k - 1] + 1  # Start after the last assigned node

    for v in range(start, n + 1):
        if checkY(v, k):
            y[k] = v
            if v > 0:
                segments += 1  # New segment
            visited[v] = True
            f += c[y[k - 1]][v]  # Update cost
            load[k] += d[v-1]

            if k < k:  # Assign next truck
                Try_Y(k + 1)
            else:  # All trucks assigned, solve paths
                nbr = segments
                Try_X(1, nbr)

            # Backtrack
            load[k] -= d[v-1]
            f -= c[y[k - 1]][v]
            visited[v] = False
            if v > 0:
                segments -= 1  # Remove segment

def Try_X(k, nbr):
    global f, fs
    if k > nbr:
        # Update best solution
        if f < fs:
            fs = f
        return

    for v in range(1, n + 1):
        if not visited[v]:
            x[k] = v
            visited[v] = True
            f += c[x[k - 1]][v]  # Add path cost

            Try_X(k + 1, nbr)

            # Backtrack
            f -= c[x[k - 1]][v]
            visited[v] = False


# Solve the problem and print the result
result = solve()
print(result)
