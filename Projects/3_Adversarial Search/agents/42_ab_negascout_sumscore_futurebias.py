"""Implementation of the CustomPlayer class using the ABNegascout algorithm
with iterative deepening and a cumulative scoring mechanism that applies a bias
towards future liberty strength against the opposing agent.

Author: Robert Paech
Date: 6 Nov 2021
"""

import random
from sample_players import DataPlayer
from isolation.isolation import Action, Isolation
from typing import Optional, Tuple, Dict


def liberty_difference(state: Isolation) -> int:
    """Returns the difference between the number of liberties of the current
    player compared to the opposing player.

    Args:
        state: Isolation - The current state of the board.
    Returns:
        int - The liberty difference between the two players, from the
            perspective of the current player.
    """

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
    """Implementation of the CustomPlayer class using the ABNegascout algorithm
    with iterative deepening and a cumulative scoring mechanism that applies a
    bias towards future liberty strength against the opposing agent.

    The ABNegascout is an application of the Negamax algorithm (a close variant
    of Minimax) with alpha-beta pruning and a scout test that attempts to
    minimise the alpha-beta search window more quickly.  By reducing the search
    window more quickly it is intended that more favourable branches of the
    tree can be more deeply explored to identify greater advantages over the
    opposing agent.

    Scoring is based on the difference in liberties between the two players
    (ie, the #my_moves - #opponent_moves heuristic); however, it expands on
    this by cumulatively suming the liberty differences for a branch.  In
    addition, a bias toward having greater liberty strength in the longer term
    is applied by dividing the liberty difference for the current node by the
    search depth minus the current_depth. The intent of the bias is to
    encourage the algorithm to choose paths with limited liberties in the short
    term, if they provide access to greater liberties in the medium to long
    term.
    """

    def get_action(self, state: Isolation) -> None:
        """Identify the best course of action for the active player.

        If the first move for the player, get_action simply chooses a square
        at random.

        Args:
            state: Isolation - The current state of the board.
        Returns:
            None.
        """

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
                    score = self.scout(state.result(action), search_depth,
                                       -beta, -max(alpha, best_score))

                    if best_score < score or best_action is None:
                        best_score = score
                        best_action = action

                self.queue.put(best_action)
                self.context = log_stat(state, search_depth, max_search_depth,
                                        best_score, best_action)

    def scout(self, state: Isolation, search_depth: int,
              alpha: float, beta: float) -> float:

        if state.terminal_test():
            result = state.utility(state.player())

        elif search_depth == 0:
            result = liberty_difference(state)

        else:
            best_score = float('-inf')
            adaptive_beta = beta

            for action in state.actions():
                new_state = state.result(action)
                current_score = self.search(new_state, search_depth - 1,
                                            -adaptive_beta,
                                            -max(alpha, best_score))

                if current_score > best_score:
                    if adaptive_beta == beta or search_depth <= 2:
                        best_score = current_score
                    else:
                        best_score = self.scout(new_state, search_depth,
                                                -beta, -current_score)

                if best_score >= beta:
                    break

                adaptive_beta = max(alpha, best_score) + 1

            result = best_score + liberty_difference(state) / search_depth

        return -result

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
