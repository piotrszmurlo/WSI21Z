import numpy as np

class TicTacToe:
    def __init__(self, depth_max, depth_min):
        self.board = np.full((3, 3), 0)
        # self.board =  np.array([[1,1,1],[0,0,0], [0,0,0]])
        self.depth_max = depth_max
        self.depth_min = depth_min
        self.max_turn = True
        self.evaluation_board = np.array([[3, 2, 3],[2, 4, 2], [3, 2, 3]])
        self.win_board = np.array([[4, 9, 2], [3, 5, 7], [8, 1, 6]])

    def minimax(self, board, depth, maximize):
        if depth == 0 or self.is_over(board):
            return self.evaluate(board)
        possible_moves = self.get_possible_moves(board)
        values = []
        for move in possible_moves:
            new_board = board.copy()
            if maximize:
                new_board[move[0]][move[1]] = 1
            else:
                new_board[move[0]][move[1]] = -1
            value = self.minimax(new_board, depth - 1, maximize)
            values.append(value)
        if maximize:
            return max(values)
        else:
            return min(values)

    def max_move(self, depth_max):
        possible_moves = self.get_possible_moves(self.board)
        new_boards = []
        for possible_move in possible_moves:
            new_board = self.board.copy()
            new_board[possible_move[0]][possible_move[1]] = 1
            new_boards.append(new_board)
        values = []
        for new_board in new_boards:
            values.append(self.minimax(new_board, depth_max, True))
        final_choice = values.index(max(values))
        self.board[possible_moves[final_choice][0]][[possible_moves[final_choice][1]]] = 1
        self.max_turn = False

    def min_move(self, depth_min):
        possible_moves = self.get_possible_moves(self.board)
        new_boards = []
        for possible_move in possible_moves:
            new_board = self.board.copy()
            new_board[possible_move[0]][possible_move[1]] = -1
            new_boards.append(new_board)
        values = []
        for new_board in new_boards:
            values.append(self.minimax(new_board, depth_min, False))
        final_choice = values.index(min(values))
        self.board[possible_moves[final_choice][0]][[possible_moves[final_choice][1]]] = -1
        self.max_turn = True
        

    def evaluate(self, board):
        return sum(sum(board * self.evaluation_board))

    def is_over(self, board):
        scoreboard = board * self.win_board
        for row in scoreboard:
            if abs(sum(row)) == 15:
                # print('True')
                return True
        for col in scoreboard.T:
            if abs(sum(col)) == 15:
                # print('True')
                return True
        if abs(np.trace(np.flipud(scoreboard))) == 15:
            # print('True')
            return True
        if abs(scoreboard.trace()) == 15:
            # print('True')
            return True
        if self.get_possible_moves(board).size == 0:
            # print('True')
            return True
        # print('False')
        return False

    def get_possible_moves(self, board):
        result = np.where(board == 0)
        return np.column_stack((result[0], result[1]))

    def play(self):
        while not self.is_over(self.board):
            self.max_move(self.depth_max)
            self.print_board() 
            if not self.is_over(self.board):
                self.min_move(self.depth_min)
                self.print_board() 
        # self.print_board()  
    def print_board(self):
        li = [[' ',' ',' '], [' ',' ',' '], [' ',' ',' ']]
        for i, row in enumerate(self.board):
            for j, element in enumerate(row):
                if element == 1:
                    li[i][j] = 'X'
                elif element == -1:
                    li[i][j] = 'O'
                elif element == 0:
                    li[i][j] = ' '
        for i in range(3):
            print(li[i])
        print('')
def main():
    game = TicTacToe(3,3)
    game.play()

if __name__ == '__main__':
    main()