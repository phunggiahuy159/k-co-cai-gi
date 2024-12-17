import random

def initialize_board(n):
    return [random.randint(0, n - 1) for _ in range(n)]

def count_conflicts(board, col, row):
    return sum((board[c] == row) or (board[c] - c == row - col) or (board[c] + c == row + col) for c in range(len(board)) if c != col)

def total_conflicts(board):
    return sum(count_conflicts(board, col, board[col]) for col in range(len(board)))

def tabu_search(n, max_iterations=1000, tabu_tenure=10):
    board = initialize_board(n)
    best_board = board[:]
    best_conflicts = total_conflicts(board)

    tabu_list = []

    for _ in range(max_iterations):
        if best_conflicts == 0:
            return best_board

        neighbors = []
        for col in range(n):
            current_row = board[col]
            for new_row in range(n):
                if new_row != current_row:
                    neighbor = board[:]
                    neighbor[col] = new_row
                    neighbors.append((neighbor, col, current_row, new_row))

        neighbors.sort(key=lambda x: total_conflicts(x[0]))

        for neighbor, col, old_row, new_row in neighbors:
            if (col, new_row) not in tabu_list:
                board = neighbor
                current_conflicts = total_conflicts(board)
                if current_conflicts < best_conflicts:
                    best_board = board[:]
                    best_conflicts = current_conflicts
                tabu_list.append((col, old_row))
                if len(tabu_list) > tabu_tenure:
                    tabu_list.pop(0)
                break

    return best_board if best_conflicts == 0 else ["Could not find the solution"]

n = int(input(""))
solution = tabu_search(n)
ans = ' '.join(map(str, solution))
print(n)
print(ans)
