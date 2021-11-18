import numpy as np

a =np.full((3, 3), 0)
evaluation_board = np.array([[3, 2, 3],[2, 4, 2], [3, 2, 3]])
evaluation_board  = np.array([[4, 9, 2], [3, 5, 7], [8, 1, 6]])
board = np.array([[1,1,1],[0,0,0], [0,0,0]])
bb = board.copy()
bb[1][1] = 5
# for i, val in enumerate(board):
print(board)
print(bb)
#     print(i, val)