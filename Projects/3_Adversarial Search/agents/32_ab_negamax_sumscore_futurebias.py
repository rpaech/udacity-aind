import random
from sample_players import DataPlayer
from isolation.isolation import Action, Isolation
from typing import Optional, Tuple, Dict


def liberty_difference(state: Isolation) -> int:

    def liberty_count(player_id: int) -> int:
        return len(state.liberties(state.locs[player_id]))

    this_player = state.player()
    next_player = 1 - this_player

    return liberty_count(this_player) - liberty_count(next_player)


def log_stat(state: Isolation, search_depth: int, max_search_depth: int,
             best_score: int, action: Action) -> Dict:

    return {'round': state.ply_count,
            'depth': search_depth,
            'max depth': max_search_depth,
            'score': best_score,
            'action': action}


class CustomPlayer(DataPlayer):

    def get_action(self, state: Isolation) -> None:

        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))

        else:
            max_search_depth = len(state.liberties(None)) // 2

            for search_depth in range(max_search_depth):

                alpha = float("-inf")
                beta = float("inf")
                best_score = float("-inf")
                best_action = None

                for action in state.actions():
                    score = self.search(state.result(action), search_depth,
                                        -beta, -max(alpha, best_score))

                    if best_score < score or best_action is None:
                        best_score = score
                        best_action = action

                self.queue.put(best_action)
                self.context = log_stat(state, search_depth, max_search_depth,
                                        best_score, best_action)

    def search(self, state: Isolation, search_depth: int,
               alpha: float, beta: float) -> float:

        if state.terminal_test():
            result = state.utility(state.player())

        elif search_depth == 0:
            result = liberty_difference(state)

        else:
            score = float('-inf')
            for action in state.actions():
                score = max(score,
                            self.search(state.result(action), search_depth - 1,
                                        -beta, -max(alpha, score)))
                if score >= beta:
                    break

            result = score + liberty_difference(state) / search_depth

        return -result
