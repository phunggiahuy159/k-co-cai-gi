n, k, q = map(int, input().split())  # Number of clients, number of trucks, truck capacity
d = list(map(int, input().split()))  # Packages requested by clients
d.insert(0, 0)  # Insert depot demand as 0
c = []  # Distance matrix
for _ in range(n + 1):
    c.append(list(map(int, input().split())))

# Global variables
y = [0] * (k + 1)  # Trucks' first client
visited = [False] * (n + 1)  # Track visited clients
load = [0] * (k + 1)  # Current load of each truck
f = 0  # Current total cost
fs = float('inf')  # Minimum total cost
segments = 0  # Number of visited clients (to check completeness)


def checkY(v, truck):
    """Check if client v can be the first client of truck."""
    if v == 0:  # Depot is always valid
        return True
    if visited[v] or load[truck] + d[v] > q:  # Client already visited or exceeds capacity
        return False
    return True


def checkX(v, prev, truck):
    """Check if client v can follow the current client in truck's route."""
    if v == 0:  # Returning to the depot is always valid
        return True
    if visited[v]:  # Already visited
        return False
    return True


def Try_Y(truck):
    """Assign first client to each truck (or no client)."""
    global f, fs, segments
    if truck > k:  # All trucks have been assigned
        if segments == n:  # If all clients are assigned, optimize the routes
            Try_X(1, 0)  # Start route optimization
        return

    for v in range(n + 1):  # Try all clients (or no client for an empty truck)
        if checkY(v, truck):
            y[truck] = v
            if v > 0:  # If not the depot
                visited[v] = True
                load[truck] += d[v]
                f += c[0][v]  # Cost from depot to the first client
                segments += 1

            Try_Y(truck + 1)  # Recur for the next truck

            # Backtrack
            if v > 0:
                visited[v] = False
                load[truck] -= d[v]
                f -= c[0][v]
                segments -= 1


def Try_X(truck, prev):
    """Find the optimal route for the current truck."""
    global f, fs
    if truck > k:  # All trucks' routes have been assigned
        fs = min(fs, f)  # Update the minimum cost
        return

    if y[truck] == 0:  # Empty truck
        Try_X(truck + 1, 0)
        return

    for v in range(n + 1):  # Try all clients and returning to the depot
        if v == 0:  # Returning to depot
            if prev != 0:  # End route for the current truck
                f += c[prev][0]
                Try_X(truck + 1, 0)  # Move to the next truck
                f -= c[prev][0]
        elif checkX(v, prev, truck):  # Assign client v to the current truck
            visited[v] = True
            f += c[prev][v]
            Try_X(truck, v)  # Continue route for the same truck
            f -= c[prev][v]
            visited[v] = False


# Solve the problem
def solve():
    global fs
    Try_Y(1)  # Start assigning clients to trucks
    return fs


# Output the result
result = solve()
print(result if result != float('inf') else -1)  # Print -1 if no valid solution exists
