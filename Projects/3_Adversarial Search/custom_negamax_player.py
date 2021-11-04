import random
from sample_players import DataPlayer
from isolation.isolation import Action, Isolation
from typing import Optional, Tuple


MAX_SEARCH_DEPTH = 3


class CustomPlayer(DataPlayer):

    def get_action(self, state: Isolation) -> None:

        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            _, action = self.search(state)
            self.queue.put(action)

    def search(self, state: Isolation, depth: int = 0
               ) -> Tuple[float, Optional[Action]]:

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
