from os import stat
import random
from sample_players import DataPlayer
from isolation.isolation import Action, Isolation
from typing import Tuple


MAX_SEARCH_DEPTH = 3


class CustomPlayer(DataPlayer):
    
    def __new__(cls, player_id):
        return CustomMinimaxPlayer(player_id)


class CustomABNegamaxPlayer(DataPlayer):

    def get_action(self, state: Isolation) -> None:

        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            _, action = self.search(state, 0, float('-inf'), float('inf'))
            self.queue.put(action)

    def search(self, state: Isolation, depth: int, 
               alpha: float, beta: float) -> Tuple[float, Action]:

        if state.terminal_test():
            actions = state.actions()
            if len(actions) > 0:
                return state.utility(state.player()), actions[0]
            else:
                return state.utility(state.player()), None
        
        if depth == MAX_SEARCH_DEPTH:
            return self.score(state), None

        best_action = None
        best_score = float('-inf')

        for action in state.actions():

            new_state = state.result(action)

            score, _ = self.search(new_state, depth + 1, 
                                   -beta, -max(alpha, best_score))
            score = -score

            if score > best_score:
                best_score = score
                best_action = action

            if best_score >= beta:
                break

        return best_score, best_action

    def score(self, state: Isolation) -> int:

        own_loc = state.locs[state.player()]
        opp_loc = state.locs[1 - state.player()]

        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)

        result = len(own_liberties) - len(opp_liberties) 
        return result


class CustomNegamaxPlayer(DataPlayer):

    def get_action(self, state: Isolation) -> None:

        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            _, action = self.search(state)
            self.queue.put(action)

    def search(self, state: Isolation, depth: int = 0) -> Tuple[float, Action]:

        if state.terminal_test():
            actions = state.actions()
            if len(actions) > 0:
                return state.utility(state.player()), actions[0]
            else:
                return state.utility(state.player()), None
        
        if depth == MAX_SEARCH_DEPTH:
            return self.score(state), None

        best_action = None
        best_score = float('-inf')

        for action in state.actions():

            new_state = state.result(action)

            score, _ = self.search(new_state, depth + 1)
            score = -score

            if score > best_score:
                best_score = score
                best_action = action

        return best_score, best_action

    def score(self, state: Isolation) -> int:

        own_loc = state.locs[state.player()]
        opp_loc = state.locs[1 - state.player()]

        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)

        result = len(own_liberties) - len(opp_liberties) 
        return result


class CustomMinimaxPlayer(DataPlayer):

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
