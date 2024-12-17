import random

def initialize_board(n):
    board = []
    for i in range(n):
        board.append(-1)
    for col in range(n):  
        board[col] = random.randint(0, n-1)
    return board

def count_conflicts_helper(board, col, row): 
    conflicts = 0
    for c in range(len(board)):
        if c == col: 
            continue
        if (board[c] == row) or (board[c] - c) == (row - col) or (board[c] + c) == (row + col): 
            conflicts += 1 
    return conflicts

def find_most_conflicted_helper(board):
    max_conflicts = -1
    most_conflicted_cols = []
    for col in range(len(board)):
        row = board[col] 
        conflicts = count_conflicts_helper(board, col, row) 
        if conflicts == max_conflicts:  
            most_conflicted_cols.append(col)
        elif conflicts > max_conflicts: 
            max_conflicts = conflicts 
            most_conflicted_cols = [col] 
    decision = random.choice(most_conflicted_cols) 
    return decision #pick at random between ties

def solve_n_queens(n, max_iterations=1000, random_restarts=50): #random restarts are bounded to make sure it won't run forever
    board = initialize_board(n)
    for i in range(max_iterations):
        column = find_most_conflicted_helper(board)
        if count_conflicts_helper(board, column, board[column]) == 0:
            return board
        min_conflicts = len(board)
        second_min_conflict = 1+len(board)
        best_rows = []
        for row in range(len(board)): 
            conflicts = count_conflicts_helper(board, column, row)
            if conflicts == min_conflicts:
                best_rows.append(row)
            elif conflicts < min_conflicts:
                second_min_conflict = min_conflicts
                min_conflicts = conflicts
                best_rows = [row]
        if second_min_conflict == 1 + len(board): 
            board[column] = random.choice(best_rows)
        else:
            if random.random() < 0.95: 
                board[column] = random.choice(best_rows)
            else:  
                board[column] = second_min_conflict
    else:
        if random_restarts==0:
            return ["Could not find the solution"] 
        return solve_n_queens(n, max_iterations, random_restarts=random_restarts-1) 

n = int(input(""))
solution = solve_n_queens(n)
ans = ''
for x in solution:
    ans += str(x) + ' '
print(n)    
print(ans)