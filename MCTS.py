import numpy as np
from Board import Board

class MCTS:
    def __init__(self, player_symbol, init_board):
        self.root = init_board
        self.player_symbol = player_symbol
        
    def find_next_move(self, max_iter, param):
        root = MCTSNode(self.root, self.player_symbol)

        for _ in range(max_iter):
            node = root

            # traverse down until an unexplored child node is reached
            while node.children:
                # Gets new child
                node = node._select(param) 
                
            # An unvisited node that is not expanded is expanded
            node = node._expand()
            
            # Simulate the game starting from the unvisited child node
            # From a simulation policy, continue playing until termination
            result = node._simulate()

            # Backpropagate it through the tree, when termination is reached
            node._backpropagate(result, self.player_symbol)
            
        # Choose the best move based on the number of visits
        best_child = max(root.children, key=lambda child: child.visits)
        return best_child.move


class MCTSNode:
    def __init__(self, board_state, symbol, move = None, parent=None):
        self.state = board_state
        self.symbol = symbol
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.move = move
        
    """Function returns a random child node from
    the nodes with the largest ucb score"""
    def _select(self, param):
        # Find and and return an unvisited child if that exists
        unvisited_children = [child for child in self.children if child.visits == 0]
        if unvisited_children:
            return np.random.choice(unvisited_children)
        
        # Calculate ucb score of a node
        ucb_score = lambda node, param: (node.wins/node.visits) + param * np.sqrt(np.log(self.visits)/node.visits)
        
        # Calculate the UCB1, or upper confidence bound for a every child
        UCB = [ucb_score(child, param) for child in self.children]

        # Get the indecies for the child nodes with the largest UBC values
        max_UCB_idx = np.argwhere(UCB == np.max(UCB)).flatten()
        max_children = [self.children[idx] for idx in max_UCB_idx]

        # Return the child nodes with the largest UBC values and least visits
        return min(max_children, key=lambda child: child.visits)
    

    """Function explores the child nodes for a given parent"""
    def _expand(self):
        # find all possible states fom leaf node
        zero_indices = np.where(self.state == 0)
        
        # If visits are 0 we want to simulate on this node
        if self.visits == 0:
            return self
        
        # If node is end of game we want to simulate on this node
        if len(zero_indices[0]) == 0:
            return self
        
        for row, col in zip(zero_indices[0], zero_indices[1]):
            # Copy current state and make move
            new_state = self.state.copy()
            new_state[row][col] = self.symbol

            # Create new child node
            child = MCTSNode(board_state=new_state, symbol=self.symbol*-1, parent=self, move=(row,col))
            self.children.append(child)
        
        return np.random.choice(self.children)


    """Function simulates the game, based on a policy,
    until the terminal node"""
    def _simulate(self):
        board = Board(self.state.copy())
        turn = self.symbol

        while board.check_winner() is False:
            # Find possible moves
            zero_indices = np.where(board.state == 0)
            possible_moves = list(zip(zero_indices[0], zero_indices[1]))
            
            # Select and make a random move
            rnd_move = possible_moves[np.random.randint(len(possible_moves))]
            board.make_move(rnd_move[0], rnd_move[1], turn)
            
            # Flip turn to other player
            turn *= -1
        return board.check_winner()
    
    # Another rollout policy using smarter moves
    def _simulate_rule(self):
        board = Board(self.state.copy())
        turn = self.symbol
        
        while board.check_winner() is False:
            # Find possible moves
            zero_indices = np.where(board.state == 0)
            possible_moves = list(zip(zero_indices[0], zero_indices[1]))
            
            # Check if the opponent has two markers in a row on a row, column, or diagonal and block it
            for i in range(3):
                # Rows
                if np.sum(board.state[i] == -turn) == 2 and np.sum(board.state[i] == 0) == 1:
                    j = np.where(board.state[i] == 0)[0][0]
                    board.make_move(i, j, turn)
                    break
                # Columns
                elif np.sum(board.state[:, i] == -turn) == 2 and np.sum(board.state[:, i] == 0) == 1:
                    j = np.where(board.state[:, i] == 0)[0][0]
                    board.make_move(j, i, turn)
                    break
                # Diagonal 1
                elif i == 0 and np.sum(np.diag(board.state) == -turn) == 2 and np.sum(np.diag(board.state) == 0) == 1:
                    j = np.where(np.diag(board.state) == 0)[0][0]
                    board.make_move(j, j, turn)
                    break
                # Diagonal 2
                elif i == 2 and np.sum(np.diag(np.fliplr(board.state)) == -turn) == 2 and np.sum(np.diag(np.fliplr(board.state)) == 0) == 1:
                    j = np.where(np.diag(np.fliplr(board.state)) == 0)[0][0]
                    board.make_move(2 - j, j, turn)
                    break
            else:
                # Select and make a random move
                rnd_move = possible_moves[np.random.randint(len(possible_moves))]
                board.make_move(rnd_move[0], rnd_move[1], turn)

            # Flip turn to other player
            turn *= -1
            
        return board.check_winner()



    """Function backpropagates through the tree and update wins
    and mark as visited"""
    def _backpropagate(self, result, player_symbol):

        # The expanded node is marked as visited
        self.visits += 1

        # If there's a win add +2 or tie +1 to the win
        if result == player_symbol:
            self.wins += 2
        elif result == 0:
            self.wins += 1
        
        # Backpropagate until parent is reached
        if self.parent:
            self.parent._backpropagate(result, player_symbol)

    
        