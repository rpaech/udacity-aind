# AB negamax search with iterative deepening and modified heuristic

import random
from sample_players import DataPlayer
from isolation.isolation import Isolation


MAX_SEARCH_DEPTH = 100


def liberty_difference(state: Isolation) -> int:

    def liberty_count(player_id: int) -> int:
        return len(state.liberties(state.locs[player_id]))

    this_player = state.player()
    next_player = 1 - this_player

    return liberty_count(this_player) - liberty_count(next_player)


class CustomPlayer(DataPlayer):

    def get_action(self, state: Isolation) -> None:

        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            for depth in range(MAX_SEARCH_DEPTH):
                action = max(state.actions(), key=lambda x:
                             self.search(state.result(x), depth,
                                         float('-inf'), float('inf')))
                self.queue.put(action)

    def search(self, state: Isolation, depth: int,
               alpha: float, beta: float) -> float:

        if state.terminal_test():
            value = state.utility(state.player())
        elif depth == 0:
            value = liberty_difference(state)
        else:
            value = float('-inf')
            for action in state.actions():
                value = max(value,
                            self.search(state.result(action), depth - 1,
                                        -beta, -max(alpha, value)))
                if value >= beta:
                    break

            value += liberty_difference(state)

        return -value
