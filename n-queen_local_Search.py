#input
import random
n=int(input())
# position=list(map(int, input().split()))
board=[x for x in range(0,n)]
random.shuffle(board)
def comb2(n): return n*(n-1)//2

def conflicts(board):
    n = len(board)
    
    horizontal_cnt = [0] * n
    diagonal1_cnt = [0] * 2 * n
    diagonal2_cnt = [0] * 2 * n
    for i in range(n):
        horizontal_cnt[board[i]] += 1
        diagonal1_cnt[i + board[i]] += 1
        diagonal2_cnt[i - board[i] + n] += 1
    
    return sum(map(comb2, horizontal_cnt + diagonal1_cnt + diagonal2_cnt))
    
def generate_neighbors(board):
    neighbors = []
    for col in range(len(board)):
        for row in range(len(board)):   
            if board[col] != row:  
                new_board = board[:]
                new_board[col] = row
                neighbors.append(new_board)
    return neighbors

def quality_function(board):
    return conflicts(board)

def local_search(n):
    current = board
    current_quality = quality_function(board)
    while True:
        neighbors = generate_neighbors(board)
        best = None
        best_quality = current_quality
        for neighbor in neighbors:
            quality = quality_function(neighbor)
            if quality < best_quality:
                best_quality = quality
                best = neighbor
        if best is None:
            break
        else:
            current = best
            current_quality = best_quality
    
    return current
print(board)
# ans=[(x+1) for x in board]
# print(local_search(ans))
ans=[x+1 for x in local_search(board)]
print(ans)