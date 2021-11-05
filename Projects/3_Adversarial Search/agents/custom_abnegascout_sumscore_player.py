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

    def scout(self, state: Isolation, depth: int,
              alpha: float, beta: float) -> float:

        if state.terminal_test():
            result = state.utility(state.player())
        elif depth == 0:
            result = liberty_difference(state)
        else:
            best_score = float('-inf')
            adaptive_beta = beta
            for action in state.actions():
                new_state = state.result(action)
                current_score = self.search(new_state, depth - 1,
                                            -adaptive_beta,
                                            -max(alpha, best_score))
                if current_score > best_score:
                    if adaptive_beta == beta or depth <= 2:
                        best_score = current_score
                    else:
                        best_score = self.scout(new_state, depth - 1, -beta,
                                                -current_score)
                if best_score >= beta:
                    break

                adaptive_beta = max(alpha, best_score) + 1

            result = best_score + liberty_difference(state)/depth

        return -result

    def search(self, state: Isolation, depth: int,
               alpha: float, beta: float) -> float:

        if state.terminal_test():
            result = state.utility(state.player())
        elif depth == 0:
            result = liberty_difference(state)
        else:
            best_score = float('-inf')
            for action in state.actions():
                best_score = max(best_score,
                                 self.search(state.result(action), depth - 1,
                                             -beta, -max(alpha, best_score)))
                if best_score >= beta:
                    break

            result = best_score + liberty_difference(state)/depth

        return -result
