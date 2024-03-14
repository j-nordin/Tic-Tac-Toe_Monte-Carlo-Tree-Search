from Player import Player, MCTSPlayer, RandomPlayer
from Game import Game

# Create two players
player1 = RandomPlayer("Random", 1)
#player1 = Player("Alice", 1)
#player1 = MCTSPlayer("MCTS", 1, max_iter=50, param = 2)
player2 = MCTSPlayer("MCTS", -1, max_iter=50, param = 2)

wins = [0,0,0]

for _ in range(100):
    game = Game(player1, player2)
    winner = game.play(verbose=1)

    if winner == 1:
        wins[0] += 1
    elif winner == -1:
        wins[1] += 1
    else:
        wins[2] += 1

print(wins)