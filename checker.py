def InputFromFile(filepath):
    f = open(filepath, 'r')
    N, Q = map(int, f.readline().strip("\n").split())
    pred = []
    for _ in range(Q):
        pred.append(map(int, f.readline().strip("\n").split()))
    d = [0] + list(map(int, f.readline().strip("\n").split()))
    M = int(f.readline().strip("\n"))
    s = [0] + list(map(int, f.readline().strip("\n").split()))
    K = int(f.readline().strip("\n"))
    c = [[0 for i in range(M+1)] for j in range(N+1)]
    for _ in range(K):
        task, team, cost = map(int, f.readline().strip("\n").split())
        c[task][team] = cost
    f.close()
    return N, Q, pred, d, M, s, K, c

def ReadOutput(filepath, N, Q, pred, d, M, s, K, c):
    f = open(filepath, 'r')
    completed = [0 for i in range(N+1)]
    time = [0 for i in range(N+1)]
    num = int(f.readline().strip("\n"))
    ans = []
    for i in range(num):
        task, team, t = map(int, f.readline().strip("\n").split())
        ans.append((task, team, t))
        completed[task] = team
        time[task] = t
    f.close()
    return num, completed, time, ans

def Checker():
    N, Q, pred, d, M, s, K, c = InputFromFile('test.txt')

    num, completed, time, ans = ReadOutput('output.txt', N, Q, pred, d, M, s, K, c)

    pre = [0 for i in range(M+1)]
    ans = sorted(ans, key = lambda tup: tup[-1])

    # Check if there is a team doing multiple tasks simultaneously or a team is not ready to work
    total_time = 0
    total_cost = 0

    for task, team, t in ans:
        if t < s[team]:
            if pre[team] == 0:
                print(f"Team {team} is not ready to do task {task} yet!")
                exit(0)
            else:
                print(f"Team {team} is doing task {pre[team]} and task {task} simultaneously!")
                exit(0)
        else:
            s[team] = max(s[team], t + d[task])
            pre[team] = task
            total_time = max(total_time, t + d[task])
            total_cost += c[task][team]

    # Check if a task is completed but its preceding tasks are not completed 
    for u, v in pred:
        if completed[u] == 0 and completed[v] != 0:
            print(f"Task {v} is completed before task {u}!")
            exit(0)
        elif completed[u] != 0 and completed[v] != 0:
            if time[v] < time[u] + d[u]:
                print(f"Task {v} is assigned before completion of task {u}!")
                exit(0)

    print("Total tasks completed:", num)
    print("Total completion time:", total_time)
    print("Total cost:", total_cost)

if __name__ == '__main__':
    Checker()