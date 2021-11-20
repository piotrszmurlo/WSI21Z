import numpy as np

a =np.full((3, 3), 0)
evaluation_board = np.array([[3, 2, 3],[2, 4, 2], [3, 2, 3]])
# evaluation_board  = np.array([[4, 9, 2], [3, 5, 7], [8, 1, 6]])
board = np.array([[1,1,0],[0,-1,0], [0,0,0]])
win_board = np.array([[4, 9, 2], [3, 5, 7], [8, 1, 6]])
result = np.where(board == 0)
possible_moves = np.column_stack((result[0], result[1]))
next_boards =[]
print(board)
for possible_move in possible_moves:
    next_board = board.copy()
    next_board[possible_move[0]][possible_move[1]] = -1
    next_boards.append(next_board)
    values = []
# for next_board in next_boards:
    # print(next_board)

def get_possible_moves(board):
    result = np.where(board == 0)
    return np.column_stack((result[0], result[1]))


def is_over(board):
    scoreboard = board * win_board
    for row in scoreboard:
        if abs(sum(row)) == 15:
            return True
    for col in scoreboard.T:
        if abs(sum(col)) == 15:
            return True
    if abs(np.trace(np.flipud(scoreboard))) == 15:
        return True
    if abs(scoreboard.trace()) == 15:
        return True
    if get_possible_moves(board).size == 0:
        return True
    return False
# print(is_over(board))
# print(board)

def evaluate_board( board):
    if is_over(board):
        scoreboard = board * win_board
        for row in scoreboard:
            if sum(row) == 15:
                return 1000
        for col in scoreboard.T:
            if sum(col) == 15:
                return 1000
        if np.trace(np.flipud(scoreboard)) == 15:
            return 1000
        if scoreboard.trace() == 15:
            return 1000
        for row in scoreboard:
            if sum(row) == -15:
                return -1000
        for col in scoreboard.T:
            if sum(col) == -15:
                return -1000
        if np.trace(np.flipud(scoreboard)) == -15:
            return -1000
        if scoreboard.trace() == -15:
            return -1000
        return 0
    else:
        return sum(sum(board * evaluation_board))

# print(evaluate_board(evaluation_board))

# result = evaluation_board 
# print(result)
choice_board = evaluation_board*(1 - abs(board))
max_val = max(choice_board.flatten())
best_move = np.where(choice_board == max_val)
print(np.column_stack((best_move[0], best_move[1])))