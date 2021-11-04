import random
from sample_players import DataPlayer
from isolation.isolation import Isolation


MAX_SEARCH_DEPTH = 6


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
            value = self.score(state)
        else:
            value = float('-inf')
            for action in state.actions():
                value = max(value,
                            self.search(state.result(action), depth - 1,
                                        -beta, -max(alpha, value)))
                if value >= beta:
                    break

        return -value

    def score(self, state: Isolation) -> int:

        playerA_options = len(state.liberties(state.locs[state.player()]))
        playerB_options = len(state.liberties(state.locs[1 - state.player()]))

        return playerA_options - playerB_options
