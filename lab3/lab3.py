import numpy as np
from random import randint


def main():
    game = TicTacToe(3, -1)  # depth = -1 -> random moves
    game.play(ab_max = False, ab_min = False)  #True -> ab pruning on


class TicTacToe:
    def __init__(self, depth_max, depth_min):
        self.states_checked_max = 0
        self.states_checked_min = 0
        self.current_board = np.full((3, 3), 0)
        self.depth_max = depth_max
        self.depth_min = depth_min
        self.evaluation_board = np.array([[3, 2, 3],[2, 4, 2], [3, 2, 3]])
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
                value, _ = self.minimax(next_board, depth - 1, False)
                values.append(value)
            max_val = max(values)
            final_choice = values.index(max_val)
            return (max_val, possible_moves[final_choice])
        else:
            for next_board in next_boards:
                value, _ = self.minimax(next_board, depth - 1, True)
                values.append(value)
            min_val = min(values)
            final_choice = values.index(min_val)
            return (min_val, possible_moves[final_choice])


    def alfa_beta(self, board, depth, is_maximizing, alfa = -np.inf, beta = np.inf):
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
            alfa = -np.inf
            for next_board in next_boards:
                value = self.alfa_beta(next_board, depth - 1, False, alfa, beta)[0]
                values.append(value)
                alfa = max(alfa, value)
                if alfa >= beta:
                    final_choice = values.index(alfa)
                    return (beta, possible_moves[final_choice])
            final_choice = values.index(alfa)
            return (alfa, possible_moves[final_choice])
        else:
            beta = np.inf
            for next_board in next_boards:
                value = self.alfa_beta(next_board, depth - 1, True, alfa, beta)[0]
                beta = min(beta, value)
                values.append(value)
                if alfa >= beta:
                    final_choice = values.index(beta)
                    return (alfa, possible_moves[final_choice])    #chyba niepoczebne
            final_choice = values.index(beta)
            return (beta, possible_moves[final_choice])


    def zero_depth_move(self, is_max):
            choice_board = self.evaluation_board*(1 - abs(self.current_board))
            max_val = max(choice_board.flatten())
            best_moves = np.where(choice_board == max_val)
            move = np.column_stack((best_moves[0], best_moves[1]))[0]
            if is_max:
                self.states_checked_max += len(self.get_possible_moves(self.current_board))
            else:
                self.states_checked_min += len(self.get_possible_moves(self.current_board))
            self.current_board[move[0]][move[1]] = 1 if is_max else -1


    def max_move(self, depth_max, ab):
        if depth_max > 0:
            if ab:
                _, move = self.alfa_beta(self.current_board, depth_max, True)
            else:
                _, move = self.minimax(self.current_board, depth_max, True)
            self.states_checked_max += len(self.get_possible_moves(self.current_board))
            self.current_board[move[0]][move[1]] = 1
        elif depth_max == 0:
            self.zero_depth_move(True)
        else:
            possible_moves = self.get_possible_moves(self.current_board)
            i = randint(0, len(possible_moves) - 1)
            self.current_board[possible_moves[i][0]][possible_moves[i][1]] = 1
        self.max_turn = False


    def min_move(self, depth_min, ab):
        if depth_min > 0:
            if ab:
                _, move = self.alfa_beta(self.current_board, depth_min, False)
            else:
                _, move = self.minimax(self.current_board, depth_min, False)
            self.states_checked_min += len(self.get_possible_moves(self.current_board))
            self.current_board[move[0]][move[1]] = -1
        elif depth_min == 0:
            self.zero_depth_move(False)
        else:
            possible_moves = self.get_possible_moves(self.current_board)
            i = randint(0, len(possible_moves) - 1)
            self.current_board[possible_moves[i][0]][possible_moves[i][1]] = -1
        self.max_turn = True
        

    def evaluate_board(self, board):
        if self.is_over(board):
            for row in board:
                if sum(row) == 3:
                    return 1000
            for col in board.T:
                if sum(col) == 3:
                    return 1000
            if np.trace(np.flipud(board)) == 3:
                return 1000
            if board.trace() == 3:
                return 1000
            for row in board:
                if sum(row) == -3:
                    return -1000
            for col in board.T:
                if sum(col) == -3:
                    return -1000
            if np.trace(np.flipud(board)) == -3:
                return -1000
            if board.trace() == -3:
                return -1000
            return 0
        else:
            return sum(sum(board * self.evaluation_board))


    def is_over(self, board):
        for row in board:
            if abs(sum(row)) == 3:
                return True
        for col in board.T:
            if abs(sum(col)) == 3:
                return True
        if abs(np.trace(np.flipud(board))) == 3:
            return True
        if abs(board.trace()) == 3:
            return True
        if self.get_possible_moves(board).size == 0:
            return True
        return False


    def get_possible_moves(self, board):
        result = np.where(board == 0)
        return np.column_stack((result[0], result[1]))


    def play(self, ab_max, ab_min):
        while not self.is_over(self.current_board):
            self.max_move(self.depth_max, ab_max)
            self.print_board() 
            if not self.is_over(self.current_board):
                self.min_move(self.depth_min, ab_min)
                self.print_board() 
        result = self.evaluate_board(self.current_board)
        print(f'max states: {self.states_checked_max}')
        print(f'min states: {self.states_checked_min}')
        if result == 1000:
            print(f'Max (X) (D = {self.depth_max}, ab_max = {ab_max}) won vs D = {self.depth_min}, ab_min = {ab_min}')
            return (1, self.states_checked_max, self.states_checked_min)
        elif result == -1000:
            self.print_board() 
            print(f'Min (O) (D = {self.depth_min}, ab_min = {ab_min}) won vs D = {self.depth_max}, ab_max = {ab_max}')
            return (-1, self.states_checked_max, self.states_checked_min)
        else:
            print(f'Draw (Dmax = {self.depth_max} ab_max = {ab_max}, Dmin = {self.depth_min} ab_min = {ab_min})')
            return (0, self.states_checked_max, self.states_checked_min)


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


if __name__ == '__main__':
    main()