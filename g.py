import random
import math

def initialize_board(n):
    return [random.randint(0, n - 1) for _ in range(n)]

def count_conflicts(board, col, row):
    return sum((board[c] == row) or (board[c] - c == row - col) or (board[c] + c == row + col) for c in range(len(board)) if c != col)

def total_conflicts(board):
    return sum(count_conflicts(board, col, board[col]) for col in range(len(board)))

def simulated_annealing(n, max_iterations=10000, initial_temp=100, cooling_rate=0.99):
    board = initialize_board(n)
    temperature = initial_temp

    for _ in range(max_iterations):
        current_conflicts = total_conflicts(board)
        if current_conflicts == 0:
            return board

        col = random.randint(0, n - 1)
        current_row = board[col]

        new_row = random.randint(0, n - 1)
        while new_row == current_row:
            new_row = random.randint(0, n - 1)

        new_conflicts = current_conflicts - count_conflicts(board, col, current_row) + count_conflicts(board, col, new_row)

        if new_conflicts < current_conflicts or random.random() < math.exp((current_conflicts - new_conflicts) / temperature):
            board[col] = new_row

        temperature *= cooling_rate

    return ["Could not find the solution"]

n = int(input(""))
solution = simulated_annealing(n)
ans = ' '.join(map(str, solution))
print(n)
print(ans)
