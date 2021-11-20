import numpy as np
from random import randint

class TicTacToe:
    def __init__(self, depth_max, depth_min):
        self.states_checked_max = 0
        self.states_checked_min = 0
        self.current_board = np.full((3, 3), 0)
        # self.current_board =  np.array([[0,0,0],[0,1,0], [0,0,0]])
        self.depth_max = depth_max
        self.depth_min = depth_min
        self.evaluation_board = np.array([[3, 2, 3],[2, 4, 2], [3, 2, 3]])
        self.win_board = np.array([[4, 9, 2], [3, 5, 7], [8, 1, 6]])
        self.max_turn = True

    def minimax(self, board, depth, is_maximizing):
        if self.is_over(board) or depth == 0:
            return (self.evaluate_board(board), None)
        possible_moves = self.get_possible_moves(board)
        next_boards = []
        for possible_move in possible_moves:
            next_board = board.copy()
            if is_maximizing:
                next_board[possible_move[0]][possible_move[1]] = 1
            else:
                next_board[possible_move[0]][possible_move[1]] = -1
            next_boards.append(next_board)
            if self.max_turn:
                self.states_checked_max = self.states_checked_max + 1
            else:
                self.states_checked_min = self.states_checked_min + 1
        values = []
        if is_maximizing:
            for next_board in next_boards:
                value, _a = self.minimax(next_board, depth - 1, False)
                values.append(value)
            max_val = max(values)
            final_choice = values.index(max_val)
            if depth == self.depth_max: 
                print(f'max: {values}')
            return (max_val, possible_moves[final_choice])
        else:
            for next_board in next_boards:
                value, _a = self.minimax(next_board, depth - 1, True)
                values.append(value)
            min_val = min(values)
            final_choice = values.index(min_val)
            if depth == self.depth_min: 
                print(f'min: {values}')            
            # print(f'min: {min(values)}')
            return (min_val, possible_moves[final_choice])
    
    def zero_depth_move(self, is_max):
            choice_board = self.evaluation_board*(1 - abs(self.current_board))
            max_val = max(choice_board.flatten())
            best_moves = np.where(choice_board == max_val)
            move = np.column_stack((best_moves[0], best_moves[1]))[0]
            self.current_board[move[0]][move[1]] = 1 if is_max else -1

    def max_move(self, depth_max):
        if depth_max > 0:
            val, move = self.minimax(self.current_board, depth_max, True)
            # print(val)
            self.current_board[move[0]][move[1]] = 1
        elif depth_max == 0:
            self.zero_depth_move(True)
        else:
            possible_moves = self.get_possible_moves(self.current_board)
            i = randint(0, len(possible_moves))
            self.current_board[possible_moves[i][0]][possible_moves[i][1]] = -1
        self.max_turn = False

    def min_move(self, depth_min):
        if depth_min > 0:
            val, move = self.minimax(self.current_board, depth_min, False)
            # print(val)
            self.current_board[move[0]][move[1]] = -1
        elif depth_min == 0:
            self.zero_depth_move(False)
        else:
            possible_moves = self.get_possible_moves(self.current_board)
            i = randint(0, len(possible_moves))
            self.current_board[possible_moves[i][0]][possible_moves[i][1]] = -1
        self.max_turn = True
        
        

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
            return 0
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
            self.min_move(self.depth_min)
            # print(self.evaluate_board(self.current_board))
            self.print_board() 
            if not self.is_over(self.current_board):
                self.max_move(self.depth_max)
                # print(self.evaluate_board(self.current_board))
                self.print_board() 
        print(f'max states: {self.states_checked_max}')
        print(f'min states: {self.states_checked_min}')

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
    game = TicTacToe(5, 3)
    game.play()

if __name__ == '__main__':
    main()