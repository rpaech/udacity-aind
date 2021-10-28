
import gamestate as game

from minimax import min_value


depth_limit = 1
expected_values = 0
rootNode = game.GameState()
tests = [((0, 0), 2), ((1, 0), 3), ((2, 0), 1), ((0, 1), 2), ((1, 1), 3)]

if all(min_value(rootNode.result(a), depth_limit) == v for a, v in tests):
    print("Good job!")
else:
    print("Uh oh!\n Looks like one or more of the values didn't match.")

