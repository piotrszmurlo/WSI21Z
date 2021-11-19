import numpy as np

class TicTacToe:
    def __init__(self, depth_max, depth_min):
        self.current_board = np.full((3, 3), 0)
        # self.current_board =  np.array([[1,1,0],[0,0,0], [0,0,0]])
        self.depth_max = depth_max
        self.depth_min = depth_min
        self.max_turn = True
        self.evaluation_board = np.array([[3, 2, 3],[2, 4, 2], [3, 2, 3]])
        self.win_board = np.array([[4, 9, 2], [3, 5, 7], [8, 1, 6]])

    def minimax(self, board, depth, is_maximizing):
        if self.is_over(board) or depth == 0:
            return self.evaluate_board(board)
        possible_moves = self.get_possible_moves(board)
        next_boards = []
        for possible_move in possible_moves:
            next_board = board.copy()
            if is_maximizing:
                next_board[possible_move[0]][possible_move[1]] = 1
            else:
                next_board[possible_move[0]][possible_move[1]] = -1
            next_boards.append(next_board)
        values = []
        if is_maximizing:
            for next_board in next_boards:
                value = self.minimax(next_board, depth - 1, False)
                values.append(value)
            # print(f'max: {max(values)}')
            return max(values)
        else:
            for next_board in next_boards:
                value = self.minimax(next_board, depth - 1, True)
                values.append(value)
            # print(f'min: {min(values)}')
            return min(values)
    
    def max_move(self, depth_max):
        possible_moves = self.get_possible_moves(self.current_board)
        next_boards = []
        for possible_move in possible_moves:
            next_board = self.current_board.copy()
            next_board[possible_move[0]][possible_move[1]] = 1
            next_boards.append(next_board)
            values = []
        for next_board in next_boards:
            val = self.minimax(next_board, depth_max, False)
            print(val)
            values.append(val)
        final_choice = values.index(max(values)) 
        self.current_board[possible_moves[final_choice][0]][[possible_moves[final_choice][1]]] = 1
        self.max_turn = False

    def min_move(self, depth_min):
        possible_moves = self.get_possible_moves(self.current_board)
        next_boards = []
        for possible_move in possible_moves:
            next_board = self.current_board.copy()
            next_board[possible_move[0]][possible_move[1]] = -1
            next_boards.append(next_board)
            values = []
        for next_board in next_boards:
            values.append(self.minimax(next_board, depth_min, True))
        final_choice = values.index(max(values)) 
        self.current_board[possible_moves[final_choice][0]][[possible_moves[final_choice][1]]] = -1
        self.max_turn = False
        

    def evaluate_board(self, board):
        if self.is_over(board):
            scoreboard = board * self.win_board
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
        else:
            return sum(sum(board * self.evaluation_board))

    def is_over(self, board):
        scoreboard = board * self.win_board
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
        if self.get_possible_moves(board).size == 0:
            return True
        return False

    def get_possible_moves(self, board):
        result = np.where(board == 0)
        return np.column_stack((result[0], result[1]))

    def play(self):
        while not self.is_over(self.current_board):
            self.max_move(self.depth_max)
            # print(self.evaluate_board(self.current_board))
            self.print_board() 
            if not self.is_over(self.current_board):
                self.min_move(self.depth_min)
                # print(self.evaluate_board(self.current_board))
                self.print_board() 

    def print_board(self):
        li = [[' ',' ',' '], [' ',' ',' '], [' ',' ',' ']]
        for i, row in enumerate(self.current_board):
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
    game = TicTacToe(3, 2)
    game.play()
    # game.max_move(9)

if __name__ == '__main__':
    main()