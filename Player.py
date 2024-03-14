from MCTS import MCTS, MCTSNode
import numpy as np

# Implementing the player

# Player has a name and symbol
class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def next_move(self, board_state):
        return [int(x) for x in input("Enter move as 'row,col': ").split(',')]


class MCTSPlayer:
    def __init__(self, name, symbol, max_iter = 1000, param = 2):
        self.name = name
        self.symbol = symbol
        self.max_iter = max_iter
        self.param = param

    def next_move(self, board_state):
        # Use MCTS to find next move
        mcts = MCTS(self.symbol, board_state)
        return mcts.find_next_move(max_iter = self.max_iter, param=self.param)
    
class RandomPlayer:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def next_move(self, board_state):
        # Find possible moves
        zero_indices = np.where(board_state == 0)
        possible_moves = list(zip(zero_indices[0], zero_indices[1]))
        
        # Make a random move
        return possible_moves[np.random.randint(len(possible_moves))]