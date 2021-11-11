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
             best_score: int, action_count: int, action: Action) -> Dict:

    return {'round': state.ply_count,
            'depth': search_depth,
            'max depth': max_search_depth,
            'score': best_score,
            'options': action_count,
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
                current_options = None

                for action in state.actions():
                    score = self.search(state.result(action), search_depth,
                                        -beta, -max(alpha, best_score))

                    if best_score < score or current_options is None:
                        best_score = score
                        current_options = [action]
                    elif best_score == score:
                        current_options.append(action)

                action_chosen = random.choice(current_options)
                self.queue.put(action_chosen)
                self.context = log_stat(state, search_depth, max_search_depth,
                                        best_score, len(current_options),
                                        action_chosen)

    def search(self, state: Isolation, search_depth: int,
               alpha: float, beta: float) -> float:

        if state.terminal_test():
            result = state.utility(state.player())

        elif search_depth == 0:
            result = liberty_difference(state) * 100

        else:
            score = float('-inf')
            for action in state.actions():
                score = max(score,
                            self.search(state.result(action), search_depth - 1,
                                        -beta, -max(alpha, score)))
                if score >= beta:
                    break

            result = score + int(liberty_difference(state) * 100
                                 / search_depth)

        return -result
