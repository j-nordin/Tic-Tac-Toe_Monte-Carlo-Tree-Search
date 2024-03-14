from Player import Player, MCTSPlayer, RandomPlayer
from Game import Game


# Grid search (letting the random player start each game)
def grid_search(max_iters, cs, n_games):
    scores = {}
    for iter in max_iters:
        for c in cs:
            print(f"Using max_iter: {iter} and c: {c}", end="")
            wins = [0,0,0]
            for _ in range(n_games):
                    player1 = RandomPlayer("Random", 1)
                    player2 = MCTSPlayer("MCTS", -1, max_iter=iter, param = c)
                    game = Game(player1, player2)
                    winner = game.play(verbose=0)
                    if winner == 1:
                        wins[0] += 1
                    elif winner == -1:
                        wins[1] += 1
                    else:
                        wins[2] += 1
            loss_ratio = wins[0]/sum(wins)
            print(" ==> Loss ratio: ", loss_ratio)
            scores.setdefault(iter, {})[c] = loss_ratio
    return scores