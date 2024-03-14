# Implementing the board
import numpy as np

class Board:
    def __init__(self, state=None):
        self.state = np.zeros((3, 3), dtype=int) if state is None else state

    def print_board(self):
        print('-------------')
        for i in range(3):
            print('|', self.state[i][0], '|', self.state[i][1], '|', self.state[i][2], '|')
            print('-------------')

    def make_move(self, row, col, symbol):
        if self.state[row][col] != 0:
            return False
        self.state[row][col] = symbol
        return True

    def check_winner(self):

        # Sum all different ways to win
        sum_cols = np.sum(self.state, axis=0)
        sum_rows = np.sum(self.state, axis=1)
        sum_diag = np.trace(self.state)
        sum_diag_T = np.sum(np.diag(np.fliplr(self.state)))

        # Make it into a table
        sums = np.concatenate((sum_cols, sum_rows, [sum_diag, sum_diag_T]))

        # Find if theres a win, 'tie' or no win
        if 3 in sums:
            return 1
        elif -3 in sums:
            return -1
        elif np.count_nonzero(self.state) == 9:
            return 0
        else:
            return False
