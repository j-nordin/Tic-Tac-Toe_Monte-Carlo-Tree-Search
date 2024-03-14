import numpy as np

from Board import Board

class Game:
    def __init__(self, player1, player2):
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1

    def play(self, verbose=0):
        winner = False
        while winner is False:
            # Print info
            if verbose > 2:
                self.board.print_board()
                print(f"{self.current_player.name}'s turn ({self.current_player.symbol}).")

            # Ask player for next move
            row, col = self.current_player.next_move(self.board.state)

            # Make the move
            if not self.board.make_move(row, col, self.current_player.symbol):
                print("Invalid move. Try again.")
                continue

            # Check if there is a winner
            winner = self.board.check_winner()

            # Switch player
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1

        # Print the final board and winner
        if verbose > 1:
            self.board.print_board()
        if verbose > 0:
            if winner == 0:
                print("The game ended in a tie.")
            else:
                print(f"{winner} has won the game!")
        return winner
