import random
from sample_players import DataPlayer
from isolation.isolation import Action, Isolation
from typing import Tuple


MAX_SEARCH_DEPTH = 3


class CustomPlayer(DataPlayer):

    def get_action(self, state):
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            self.queue.put(self.search(state, depth=MAX_SEARCH_DEPTH))

    def search(self, state, depth):

        def min_value(state, depth):

            if state.terminal_test():
                return state.utility(self.player_id)

            if depth <= 0:
                return self.score(state)

            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), depth - 1))

            return value

        def max_value(state, depth):

            if state.terminal_test():
                return state.utility(self.player_id)

            if depth <= 0:
                return self.score(state)

            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), depth - 1))

            return value

        return max(state.actions(),
                   key=lambda x: min_value(state.result(x), depth - 1))

    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        result = len(own_liberties) - len(opp_liberties)
        return result
